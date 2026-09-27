"""_repo.py — Repositorios Git temporales y desechables para la suite de WP-015.

No es un módulo de pruebas (no coincide con ``test_*.py``): es la utilidad
compartida que crean los tests para construir escenarios A/M/D/T/R/C y
symlinks sin tocar el repositorio FDA.

Cumple el límite del contrato de WP-015 §6: cada repositorio se crea con
``mktemp`` (aquí, ``tempfile.mkdtemp``), fija identidad Git local y solo
ejecuta, como comandos Git que mutan estado, ``init``, ``config``, ``add``,
``commit``, ``mv`` y ``rm`` — siempre dentro de su propio directorio temporal,
nunca contra el repositorio FDA. Las consultas de solo lectura (``rev-parse``)
son las mismas que usa cualquier operador para inspeccionar un repositorio y
no mutan nada.

Sin red, sin remotos. La limpieza (``cleanup``) borra únicamente el propio
directorio temporal.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple

# WP015-F6 (revalidación enfocada de C1, C2): fecha de autor/committer FIJA
# para que dos ejecuciones de la misma secuencia de operaciones produzcan,
# byte a byte, el mismo commit SHA. Sin esto, cada `commit()` usa la hora
# real del reloj y el SHA cambia en cada ejecución, de modo que ninguna
# evidencia puede citar un identificador "real" reproducible. La fecha en sí
# es arbitraria; lo único que importa es que sea constante.
_FIXED_DATE = "2026-01-01T00:00:00+0000"


class TempRepo:
    """Un repositorio Git desechable en un directorio `mktemp -d`."""

    def __init__(self) -> None:
        self.path = tempfile.mkdtemp(prefix="wp015-scope-")
        self._init()

    # --- construcción -------------------------------------------------

    def _git(
        self,
        *args: str,
        input_bytes: Optional[bytes] = None,
        extra_env: Optional[Dict[str, str]] = None,
    ) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        if extra_env:
            env.update(extra_env)
        proc = subprocess.run(
            ["git", *args],
            cwd=self.path,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"git {' '.join(args)} falló en {self.path}: "
                f"{proc.stderr.decode('utf-8', 'replace')}"
            )
        return proc

    def _init(self) -> None:
        self._git("init", "-q")
        self._git("config", "user.email", "wp015-tests@example.invalid")
        self._git("config", "user.name", "WP-015 tests")
        self._git("config", "commit.gpgsign", "false")

    # --- escritura de fixtures (no son comandos Git) -------------------

    def write(self, relpath: str, content: bytes) -> None:
        full = os.path.join(self.path, relpath)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(content)

    def write_text(self, relpath: str, text: str) -> None:
        self.write(relpath, text.encode("utf-8"))

    def symlink(self, relpath: str, target: bytes) -> None:
        """Crea un symlink cuyo destino es `target` (bytes arbitrarios)."""
        full = os.path.join(self.path, relpath)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        full_bytes = full.encode("utf-8")
        os.symlink(target, full_bytes)

    def remove_from_worktree(self, relpath: str) -> None:
        """Borra el archivo del working tree SIN pasar por `git rm`."""
        full = os.path.join(self.path, relpath)
        if os.path.islink(full) or os.path.isfile(full):
            os.remove(full)

    # --- las seis mutaciones Git admitidas ------------------------------

    def add(self, *relpaths: str) -> None:
        if relpaths:
            self._git("add", "-A", "--", *relpaths)
        else:
            self._git("add", "-A")

    def commit(self, message: str) -> str:
        # Fecha fija (ver _FIXED_DATE): mismo mensaje + mismo árbol + mismo
        # padre + misma identidad + misma fecha => mismo SHA, siempre.
        self._git(
            "commit",
            "-q",
            "-m",
            message,
            extra_env={
                "GIT_AUTHOR_DATE": _FIXED_DATE,
                "GIT_COMMITTER_DATE": _FIXED_DATE,
            },
        )
        return self.rev_parse("HEAD")

    def mv(self, src: str, dst: str) -> None:
        # `git mv` no crea el directorio destino: se asegura aquí, sin ser
        # una mutación Git (no cuenta contra el límite de subcomandos).
        full_dst = os.path.join(self.path, dst)
        parent = os.path.dirname(full_dst)
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._git("mv", src, dst)

    def rm(self, *relpaths: str) -> None:
        self._git("rm", "-q", "--", *relpaths)

    # --- lectura (no muta nada) ------------------------------------------

    def rev_parse(self, ref: str) -> str:
        proc = self._git("rev-parse", ref)
        return proc.stdout.decode("utf-8").strip()

    # --- ciclo de vida ----------------------------------------------------

    def cleanup(self) -> None:
        shutil.rmtree(self.path, ignore_errors=True)

    def __enter__(self) -> "TempRepo":
        return self

    def __exit__(self, *exc) -> None:
        self.cleanup()


def run_check_scope(repo: TempRepo, script_path: str, wp_id: str, range_str: str) -> Tuple[int, List[str]]:
    """Invoca check_scope.py como subprocess con cwd en el repo temporal.

    Devuelve (exit_code, líneas_de_stdout). No usa shell.
    """
    proc = subprocess.run(
        ["python3", script_path, wp_id, range_str],
        cwd=repo.path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    stdout_text = proc.stdout.decode("utf-8", "replace")
    lines = stdout_text.splitlines()
    return proc.returncode, lines


# --- WP015-F3 (revalidación enfocada de C1, C2): shim de "git" ------------
#
# Astra exige que las tres reproducciones exactas (puntuación R/C > 100,
# modo desconocido, pareja modo/tipo incoherente) "lleguen a main", es
# decir, que se ejerzan mediante una invocación real de scripts/check_scope.py
# como subprocess -- no solo llamando a parse_name_status_z/parse_ls_tree_z
# directamente. Git real nunca emite esas formas (son adversariales por
# construcción), así que no pueden reproducirse con un repositorio Git
# genuino sin manipular el propio Git. La técnica de prueba estándar para
# esto es un ejecutable "git" de sustitución, antepuesto al PATH SOLO del
# proceso hijo de check_scope.py: intercepta EXCLUSIVAMENTE la invocación
# exacta señalada (por subcomando y, opcionalmente, por la ausencia de un
# flag que distingue la llamada) y delega cualquier otra invocación, byte a
# byte, al git real (resuelto una única vez por ruta absoluta). No muta
# ningún repositorio real, no usa red y no toca `settings.json` ni el PATH
# de esta sesión: el cambio de PATH vive únicamente en el `env` que se pasa
# al subprocess de prueba.


def make_git_shim(
    shim_dir: str, match_argv0: str, forbid_flag: Optional[str], crafted_stdout: bytes
) -> str:
    """Crea en `shim_dir` un ejecutable `git` que devuelve `crafted_stdout`
    (exit 0) para las invocaciones cuyo primer argumento sea `match_argv0` y
    que NO contengan `forbid_flag` entre sus argumentos (si se indica);
    cualquier otra invocación se delega al git real. Devuelve la ruta del
    shim.
    """
    real_git = shutil.which("git")
    if not real_git:
        raise RuntimeError("git no encontrado en PATH: no se puede construir el shim")

    payload_path = os.path.join(shim_dir, "_payload.bin")
    with open(payload_path, "wb") as fh:
        fh.write(crafted_stdout)

    forbid_check = ""
    if forbid_flag:
        forbid_check = (
            f'  for a in "$@"; do\n'
            f'    if [ "$a" = "{forbid_flag}" ]; then exec "{real_git}" "$@"; fi\n'
            f"  done\n"
        )

    script = (
        "#!/bin/sh\n"
        f'if [ "$1" = "{match_argv0}" ]; then\n'
        f"{forbid_check}"
        f'  cat "{payload_path}"\n'
        "  exit 0\n"
        "fi\n"
        f'exec "{real_git}" "$@"\n'
    )
    shim_path = os.path.join(shim_dir, "git")
    with open(shim_path, "w", encoding="utf-8") as fh:
        fh.write(script)
    os.chmod(shim_path, 0o755)
    return shim_path


def run_check_scope_with_shim(
    repo: TempRepo, script_path: str, wp_id: str, range_str: str, shim_dir: str
) -> Tuple[int, List[str]]:
    """Como `run_check_scope`, pero antepone `shim_dir` al PATH del
    subprocess de check_scope.py, sin afectar al PATH del proceso de prueba.
    """
    env = dict(os.environ)
    env["PATH"] = shim_dir + os.pathsep + env.get("PATH", "")
    proc = subprocess.run(
        ["python3", script_path, wp_id, range_str],
        cwd=repo.path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        shell=False,
    )
    stdout_text = proc.stdout.decode("utf-8", "replace")
    lines = stdout_text.splitlines()
    return proc.returncode, lines
