#!/usr/bin/env python3
"""check_scope.py — Verificador local determinista de alcance (WP-015).

Sucesor limpio y mínimo de WP-002 (DEC-011). Dados un WP-ID y un rango Git
canónico ``<base>...<head>``, lee el contrato EXCLUSIVAMENTE del
``merge-base`` mediante objetos Git, evalúa todo el diff con la gramática de
DEC-012 y la semántica de DEC-002 (biblioteca única en scripts/scope_rules.py)
y enumera todas las violaciones encontradas.

Códigos de salida:
  0  OK          — cero violaciones.
  1  VIOLACION*  — una línea por incumplimiento, cada una con su JSON.
  2  ERROR       — uso, contrato, Git, codificación o forma no resoluble.

Uso:
  python3 scripts/check_scope.py WP-NNN BASE...HEAD

Este ejecutable es LOCAL: no es un check de GitHub, no se ejecuta en CI y no
bloquea ninguna fusión por sí mismo (DEC-007, tres estados de check_scope;
DEC-011 §1). No se invoca shell y no se lee ninguna ruta del working tree
para decidir el veredicto: ni el contrato, ni un destino de symlink, ni
ninguna ruta juzgada. Ver docs/manual/02-ciclo-de-un-wp.md.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Sequence, Tuple

import scope_rules

# WP015-F7 (revisión Astra, C1): [0-9] es siempre ASCII estricto en Python,
# a diferencia de \d, que en modo Unicode (el predeterminado) también casa
# dígitos decimales no ASCII (p. ej. ٩٠١, U+0669 U+0660 U+0661). El contrato
# exige exactamente WP-[0-9]{3}; con \d, "WP-٩٠١" pasaba el validador.
_WP_ID_RE = re.compile(r"^WP-[0-9]{3}$")

# DiffRecord: (letra_de_estado, ruta_o_origen, destino_o_None)
DiffRecord = Tuple[str, str, Optional[str]]

# LsTreeEntry: (modo, tipo, sha, ruta)
LsTreeEntry = Tuple[str, str, str, str]


class CheckScopeError(Exception):
    """Cualquier condición que exige exit 2 (fail-closed)."""

    def __init__(self, motivo: str, **detalle):
        super().__init__(motivo)
        self.motivo = motivo
        self.detalle = detalle


# --- Invocación de Git, sin shell -------------------------------------------


def _git_env() -> Dict[str, str]:
    env = dict(os.environ)
    # Los nombres de ruta se tratan siempre como literales, nunca como globs
    # de pathspec: un nombre inusual (con '*', '?', '[') no debe reinterpretarse.
    env["GIT_LITERAL_PATHSPECS"] = "1"
    return env


def _run_git(args: Sequence[str], cwd: Optional[str]) -> Tuple[int, bytes, bytes]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_git_env(),
            shell=False,
        )
    except OSError as exc:
        raise CheckScopeError("fallo de subprocess al invocar git", comando=list(args), error=str(exc))
    return proc.returncode, proc.stdout, proc.stderr


def _decode(raw: bytes, motivo: str, **detalle) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise CheckScopeError(motivo, **detalle)


# --- Argumentos --------------------------------------------------------------


def _parse_args(argv: Sequence[str]) -> Tuple[str, str, str]:
    if len(argv) != 2:
        raise CheckScopeError(
            "uso: check_scope.py WP-NNN BASE...HEAD", argumentos=list(argv)
        )
    wp_id, range_str = argv
    if not _WP_ID_RE.fullmatch(wp_id):
        raise CheckScopeError("WP-ID mal formado, se exige WP-NNN", wp_id=wp_id)
    if range_str.count("...") != 1:
        raise CheckScopeError(
            "el rango debe tener exactamente la forma BASE...HEAD", rango=range_str
        )
    base, _, head = range_str.partition("...")
    if base == "" or head == "":
        raise CheckScopeError("el rango tiene un extremo vacío", rango=range_str)
    return wp_id, base, head


# --- Parsers puros de salida Git (testables sin subprocess) ----------------
#
# WP015-F3 (revisión Astra, C1): estos parsers deben rechazar CUALQUIER forma
# que no sea exactamente la que Git emite para un registro bien formado.
# Antes aceptaban salidas truncadas (sin NUL final), rutas vacías, estados
# con letra válida pero cola arbitraria ("AWRONG", "Rxxx" sin dígitos) y
# metadata de ls-tree con modo/tipo/object id de forma libre. "Registro Git
# desconocido" (WP-015 §2) se aplica ahora a los cuatro.

# Modo Git: siempre exactamente 6 dígitos OCTALES (0-7), nunca 8 o 9.
_MODE_RE = re.compile(r"^[0-7]{6}$")
# Object id: SHA-1 hexadecimal en minúsculas, exactamente 40 caracteres.
_OID_RE = re.compile(r"^[0-9a-f]{40}$")
_VALID_LS_TREE_TYPES = frozenset({"blob", "tree", "commit"})
# Puntuación de similitud de R/C: dígitos ASCII estrictos, nunca \d Unicode.
_SCORE_RE = re.compile(r"^[0-9]+$")


def _split_ls_tree_line(entry_text: str) -> LsTreeEntry:
    meta, sep, path = entry_text.partition("\t")
    if not sep or path == "":
        raise CheckScopeError("registro Git desconocido en ls-tree", entrada=entry_text)
    parts = meta.split(" ")
    if len(parts) != 3:
        raise CheckScopeError("registro Git desconocido en ls-tree", entrada=entry_text)
    mode, obj_type, sha = parts
    if not _MODE_RE.fullmatch(mode):
        raise CheckScopeError("modo de ls-tree inválido", entrada=entry_text)
    if obj_type not in _VALID_LS_TREE_TYPES:
        raise CheckScopeError("tipo de objeto de ls-tree desconocido", entrada=entry_text)
    if not _OID_RE.fullmatch(sha):
        raise CheckScopeError("object id de ls-tree inválido", entrada=entry_text)
    return mode, obj_type, sha, path


def parse_ls_tree_z(raw: bytes) -> List[LsTreeEntry]:
    """Parsea la salida de ``git ls-tree -z``. Función pura sobre bytes.

    Una salida no vacía debe terminar en NUL: si no, es una salida truncada
    y se trata como registro Git desconocido, nunca como entrada válida.
    """
    if raw == b"":
        return []
    if not raw.endswith(b"\x00"):
        raise CheckScopeError("salida de ls-tree truncada (falta el NUL final)")
    entries = raw[:-1].split(b"\x00")
    result: List[LsTreeEntry] = []
    for raw_entry in entries:
        entry_text = _decode(raw_entry, "entrada de ls-tree con codificación inválida")
        result.append(_split_ls_tree_line(entry_text))
    return result


def select_contract(entries: Sequence[LsTreeEntry], wp_id: str) -> Tuple[str, str]:
    """Elige el único contrato canónico ``work-packages/WP-NNN-*.md``."""
    pattern = re.compile(r"^work-packages/" + re.escape(wp_id) + r"-[^/]+\.md$")
    matches = [
        (path, sha) for (_mode, obj_type, sha, path) in entries
        if obj_type == "blob" and pattern.fullmatch(path)
    ]
    if len(matches) == 0:
        raise CheckScopeError("contrato ausente en el merge-base", wp=wp_id)
    if len(matches) > 1:
        raise CheckScopeError(
            "más de un contrato coincide en el merge-base",
            wp=wp_id,
            candidatos=[p for p, _ in matches],
        )
    return matches[0]


def parse_name_status_z(raw: bytes) -> List[DiffRecord]:
    """Parsea ``git diff -z --name-status``. Función pura sobre bytes.

    Consume una o dos rutas para A/M/D/T y R/C respectivamente. Cualquier
    estado desconocido, no fusionado o ambiguo, cualquier registro truncado,
    o una salida sin el NUL final obligatorio, produce CheckScopeError
    (fail-closed). WP015-F3 (revisión Astra, C1): un estado A/M/D/T debe ser
    EXACTAMENTE esa letra (nunca "AWRONG") y la puntuación de R/C debe ser
    dígitos ASCII no vacíos (nunca "Rxxx"); ninguna ruta puede ser vacía.
    """
    if raw == b"":
        return []
    if not raw.endswith(b"\x00"):
        raise CheckScopeError("salida de diff truncada (falta el NUL final)")
    raw_tokens = raw[:-1].split(b"\x00")
    tokens = [_decode(t, "ruta del diff con codificación inválida") for t in raw_tokens]

    records: List[DiffRecord] = []
    i, n = 0, len(tokens)
    while i < n:
        status = tokens[i]
        i += 1
        if not status:
            raise CheckScopeError("registro de diff vacío")
        letter = status[0]
        if letter in ("A", "M", "D", "T"):
            if status != letter:
                raise CheckScopeError(
                    "estado de diff desconocido, no fusionado o ambiguo", status=status
                )
            if i >= n:
                raise CheckScopeError("registro de diff truncado", status=status)
            path = tokens[i]
            i += 1
            if path == "":
                raise CheckScopeError("ruta vacía en el registro de diff", status=status)
            records.append((letter, path, None))
        elif letter in ("R", "C"):
            score = status[1:]
            if not _SCORE_RE.fullmatch(score):
                raise CheckScopeError(
                    "puntuación de renombrado/copia inválida", status=status
                )
            if i + 1 >= n:
                raise CheckScopeError("registro de diff truncado", status=status)
            src, dst = tokens[i], tokens[i + 1]
            i += 2
            if src == "" or dst == "":
                raise CheckScopeError("ruta vacía en el registro de diff", status=status)
            records.append((letter, src, dst))
        else:
            raise CheckScopeError(
                "estado de diff desconocido, no fusionado o ambiguo", status=status
            )
    return records


# --- Resolución de repositorio, merge-base y contrato -----------------------


def _repo_root() -> str:
    rc, out, err = _run_git(["rev-parse", "--show-toplevel"], cwd=None)
    if rc != 0:
        raise CheckScopeError(
            "no se pudo resolver la raíz del repositorio git",
            stderr=_decode(err, "raíz del repositorio con stderr no UTF-8"),
        )
    root = _decode(out, "raíz del repositorio con codificación inválida").strip()
    if not root:
        raise CheckScopeError("raíz del repositorio vacía")
    return root


def _merge_base(repo_root: str, base: str, head: str) -> str:
    rc, out, err = _run_git(["merge-base", base, head], cwd=repo_root)
    if rc != 0:
        raise CheckScopeError(
            "merge-base no resoluble para el rango dado",
            base=base,
            head=head,
            stderr=_decode(err, "merge-base con stderr no UTF-8"),
        )
    text = _decode(out, "merge-base con salida no UTF-8").strip()
    if not text or "\n" in text:
        raise CheckScopeError("merge-base con salida ambigua o truncada", salida=text)
    return text


def _find_contract(repo_root: str, merge_base: str, wp_id: str) -> Tuple[str, str]:
    rc, out, err = _run_git(
        ["ls-tree", "-r", "-z", merge_base, "--", "work-packages/"], cwd=repo_root
    )
    if rc != 0:
        raise CheckScopeError(
            "no se pudo listar work-packages/ en el merge-base",
            stderr=_decode(err, "ls-tree con stderr no UTF-8"),
        )
    entries = parse_ls_tree_z(out)
    return select_contract(entries, wp_id)


def _read_blob_text(repo_root: str, sha: str) -> str:
    rc, out, err = _run_git(["cat-file", "blob", sha], cwd=repo_root)
    if rc != 0:
        raise CheckScopeError(
            "blob ausente o ilegible",
            blob=sha,
            stderr=_decode(err, "cat-file con stderr no UTF-8"),
        )
    return _decode(out, "blob con codificación UTF-8 inválida", blob=sha)


# --- Diff ---------------------------------------------------------------


def _diff_records(repo_root: str, merge_base: str, head: str) -> List[DiffRecord]:
    # WP015-F2 (revisión Astra, C1): sin --ignore-submodules=none, un
    # .gitmodules NO VERSIONADO o una configuración LOCAL con
    # submodule.<nombre>.ignore=all pueden hacer que Git omita del diff un
    # gitlink modificado. Ninguno de los dos vive en un objeto Git alcanzable
    # desde merge-base o head, así que dependen del working tree/config local
    # del ejecutor: exactamente lo que WP-015 §2 prohíbe que altere el
    # veredicto. Forzar "none" ignora esa configuración y evalúa siempre el
    # diff completo de gitlinks.
    rc, out, err = _run_git(
        [
            "diff",
            "-z",
            "--name-status",
            "-M",
            "-C",
            "--find-copies-harder",
            "--ignore-submodules=none",
            merge_base,
            head,
        ],
        cwd=repo_root,
    )
    if rc != 0:
        raise CheckScopeError(
            "diff no resoluble entre merge-base y head",
            stderr=_decode(err, "diff con stderr no UTF-8"),
        )
    return parse_name_status_z(out)


# --- Symlinks por objetos Git ------------------------------------------------


def _ls_tree_entry(repo_root: str, rev: str, path: str) -> Optional[LsTreeEntry]:
    rc, out, err = _run_git(["ls-tree", "-z", rev, "--", path], cwd=repo_root)
    if rc != 0:
        raise CheckScopeError(
            "no se pudo consultar ls-tree para una ruta juzgada",
            rev=rev,
            ruta=path,
            stderr=_decode(err, "ls-tree con stderr no UTF-8"),
        )
    entries = parse_ls_tree_z(out)
    if not entries:
        return None
    if len(entries) > 1:
        raise CheckScopeError("ls-tree ambiguo para una ruta exacta", rev=rev, ruta=path)
    return entries[0]


def _check_symlink(
    repo_root: str,
    rev: str,
    path: str,
    rol: str,
    allowed: Sequence[str],
    forbidden: Sequence[str],
    violations: List[dict],
) -> None:
    entry = _ls_tree_entry(repo_root, rev, path)
    if entry is None:
        raise CheckScopeError(
            "registro Git desconocido: la ruta no existe en la revisión esperada",
            rev=rev,
            ruta=path,
        )
    mode, _obj_type, sha, _path = entry
    if mode != "120000":
        return
    rc, out, err = _run_git(["cat-file", "blob", sha], cwd=repo_root)
    if rc != 0:
        raise CheckScopeError(
            "blob de destino de symlink ausente",
            blob=sha,
            ruta=path,
            stderr=_decode(err, "cat-file de symlink con stderr no UTF-8"),
        )
    target = _decode(out, "destino de symlink con codificación inválida", ruta=path)
    verdict = scope_rules.evaluate_symlink(path, target, allowed, forbidden)
    if not verdict.ok:
        violations.append(
            {"ruta": path, "rol": rol, "motivo": verdict.motivo, "patron": verdict.patron}
        )


# --- Juicio del diff completo ------------------------------------------------


def _judge(
    repo_root: str,
    merge_base: str,
    head: str,
    allowed: Sequence[str],
    forbidden: Sequence[str],
    records: Sequence[DiffRecord],
) -> List[dict]:
    violations: List[dict] = []

    def add(path: str, rol: str, verdict: scope_rules.Verdict) -> None:
        violations.append(
            {"ruta": path, "rol": rol, "motivo": verdict.motivo, "patron": verdict.patron}
        )

    for letter, p1, p2 in records:
        if letter in ("A", "M", "D", "T"):
            path = p1
            verdict = scope_rules.evaluate(path, allowed, forbidden)
            if not verdict.ok:
                add(path, "ruta", verdict)
            if letter in ("A", "M"):
                _check_symlink(repo_root, head, path, "ruta", allowed, forbidden, violations)
            elif letter == "D":
                _check_symlink(repo_root, merge_base, path, "ruta", allowed, forbidden, violations)
            else:  # T: cambio de tipo, se juzgan ambos extremos de la misma ruta
                _check_symlink(repo_root, merge_base, path, "ruta", allowed, forbidden, violations)
                _check_symlink(repo_root, head, path, "ruta", allowed, forbidden, violations)
        else:  # R, C
            src, dst = p1, p2
            assert dst is not None
            v_src = scope_rules.evaluate(src, allowed, forbidden)
            if not v_src.ok:
                add(src, "origen", v_src)
            v_dst = scope_rules.evaluate(dst, allowed, forbidden)
            if not v_dst.ok:
                add(dst, "destino", v_dst)
            _check_symlink(repo_root, merge_base, src, "origen", allowed, forbidden, violations)
            _check_symlink(repo_root, head, dst, "destino", allowed, forbidden, violations)

    return violations


# --- Orquestación y salida ---------------------------------------------------


def _emit_json(obj: dict) -> None:
    # WP015-F4 (revisión Astra, C1): con ensure_ascii=False, una ruta con
    # U+0085/U+2028/U+2029 se emitía como el byte Unicode literal. Esos tres
    # son separadores de línea para str.splitlines() (y U+2028/U+2029 para
    # el estándar Unicode de límites de línea en general), de modo que un
    # lector que no reconstruya JSON de verdad podía leer una sola violación
    # como si fueran varias líneas de log, incluida una "VIOLACION" forjada.
    # ensure_ascii=True escapa todo carácter no ASCII como \uXXXX: la línea
    # física sigue siendo una sola, sin perder ninguna ruta ni WP-015 §1
    # (claves ordenadas, JSON de una línea).
    print(json.dumps(obj, sort_keys=True, ensure_ascii=True))


def _emit_error(err: CheckScopeError, context: dict) -> None:
    payload = dict(context)
    payload["motivo"] = err.motivo
    if err.detalle:
        payload["detalle"] = err.detalle
    print("ERROR")
    _emit_json(payload)


def main(argv: Sequence[str]) -> int:
    context: dict = {}
    try:
        wp_id, base, head = _parse_args(argv)
        context["wp"] = wp_id
        context["base"] = base
        context["head"] = head

        repo_root = _repo_root()
        merge_base = _merge_base(repo_root, base, head)
        context["merge_base"] = merge_base

        contract_path, contract_blob = _find_contract(repo_root, merge_base, wp_id)
        context["contrato"] = contract_path
        context["contrato_blob"] = contract_blob

        contract_text = _read_blob_text(repo_root, contract_blob)
        try:
            allowed, forbidden = scope_rules.parse_contract(contract_text)
        except scope_rules.ContractError as exc:
            raise CheckScopeError("contrato malformado", razon=str(exc))

        records = _diff_records(repo_root, merge_base, head)
        violations = _judge(repo_root, merge_base, head, allowed, forbidden, records)
    except CheckScopeError as err:
        _emit_error(err, context)
        return 2
    except Exception as exc:  # fail-closed: ningún fallo no previsto sale silencioso
        _emit_error(
            CheckScopeError("fallo interno no previsto", tipo=type(exc).__name__, error=str(exc)),
            context,
        )
        return 2

    if violations:
        violations.sort(key=lambda v: (v["ruta"], v["rol"], v["motivo"]))
        for violation in violations:
            print("VIOLACION")
            _emit_json(violation)
        return 1

    print("OK")
    summary = dict(context)
    summary["violaciones"] = []
    _emit_json(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
