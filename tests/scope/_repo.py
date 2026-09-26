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
from typing import List, Optional, Tuple


class TempRepo:
    """Un repositorio Git desechable en un directorio `mktemp -d`."""

    def __init__(self) -> None:
        self.path = tempfile.mkdtemp(prefix="wp015-scope-")
        self._init()

    # --- construcción -------------------------------------------------

    def _git(self, *args: str, input_bytes: Optional[bytes] = None) -> subprocess.CompletedProcess:
        proc = subprocess.run(
            ["git", *args],
            cwd=self.path,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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
        self._git("commit", "-q", "-m", message)
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
