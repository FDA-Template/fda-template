"""scope_rules.py — Biblioteca única de parseo, matching y evaluación de
alcance para WP-015 (sucesor limpio de WP-002).

Implementa exclusivamente:
  - la gramática de DEC-012 (parseo léxico de "## Archivos permitidos" y
    "## Archivos prohibidos");
  - la semántica de traversal por componente de DEC-002;
  - el matching de globs (*, **, ?, sufijo "/") y la precedencia
    "prohibidos gana; fuera de permitidos se deniega" de _TEMPLATE.md;
  - la resolución textual de destinos de symlink (DEC-002 §6).

No lee el sistema de archivos, no invoca shell, no evalúa código dinámico.
Toda entrada es texto ya obtenido por el llamador (normalmente scripts/check_scope.py,
mediante objetos Git). Esta es la ÚNICA implementación de estas reglas: ningún
otro módulo debe reproducir el parser ni el matcher (contrato WP-015 §3).
"""

from __future__ import annotations

import re
from typing import List, NamedTuple, Optional, Sequence, Tuple

__all__ = [
    "ContractError",
    "Verdict",
    "SENTINELS",
    "parse_contract",
    "compile_glob",
    "match_any",
    "has_traversal",
    "evaluate",
    "resolve_symlink_target",
    "evaluate_symlink",
]


class ContractError(Exception):
    """Contrato malformado: el llamador debe traducirlo a exit 2."""


class Verdict(NamedTuple):
    ok: bool
    motivo: Optional[str]
    patron: Optional[str]


# --- 1. Gramática DEC-012 ---------------------------------------------------

SENTINELS = frozenset({"ninguno", "none", "n/a", "-"})

_H = " \t"  # DEC-012 §1: H es solo espacio ASCII o tabulador horizontal.

_HEADER_RE = re.compile(r"^##[ \t]")
_ENTRY_RE = re.compile(r"^[ \t]*-[ \t]+(.*)$")

_PERMITIDOS_HEADER = "## Archivos permitidos"
_PROHIBIDOS_HEADER = "## Archivos prohibidos"


def _strip_cr(line: str) -> str:
    # Tolerancia a CRLF sin tratar '\r' como parte de la gramática H.
    if line.endswith("\r"):
        return line[:-1]
    return line


def _section_end(lines: Sequence[str], start_idx: int, boundaries: Sequence[int]) -> int:
    for b in boundaries:
        if b > start_idx:
            return b
    return len(lines)


def _leading_h_len(line: str) -> int:
    i = 0
    n = len(line)
    while i < n and line[i] in _H:
        i += 1
    return i


def _parse_entries(section_lines: Sequence[str]) -> List[str]:
    """Extrae las entradas ejecutables de una sección, aplicando DEC-012 §1-3."""
    entries: List[str] = []
    for raw in section_lines:
        line = _strip_cr(raw)
        idx = _leading_h_len(line)
        if idx == len(line):
            continue  # línea en blanco: se ignora
        first = line[idx]
        if first == "-":
            m = _ENTRY_RE.match(line)
            if not m:
                # "-" presente pero sin el separador H+ obligatorio, o vacío.
                raise ContractError("marcador de lista malformado")
            candidate = m.group(1).rstrip(_H)
            if candidate == "":
                raise ContractError("entrada vacía")
            entries.append(candidate)
        elif first in ("*", "+"):
            raise ContractError("marcador de lista alternativo (* o +) no admitido")
        else:
            continue  # explicación sin marcador: se ignora (DEC-012 §3)
    return entries


def _resolve_list(entries: Sequence[str], *, allow_empty: bool, label: str) -> List[str]:
    sentinel_hits = [e for e in entries if e in SENTINELS]
    if sentinel_hits and len(entries) > 1:
        raise ContractError(f"sentinela mezclado con patrones en {label}")
    if not entries:
        if not allow_empty:
            raise ContractError(f"sección {label} vacía")
        return []
    if len(entries) == 1 and entries[0] in SENTINELS:
        if not allow_empty:
            raise ContractError(f"sección {label} vacía")
        return []
    return list(entries)


def parse_contract(text: str) -> Tuple[List[str], List[str]]:
    """Parsea el blob del contrato y devuelve (permitidos, prohibidos).

    Aplica exclusivamente la gramática de DEC-012 y el fail-closed de DEC-002.
    No consulta el sistema de archivos ni ninguna fuente distinta del texto
    recibido. Lanza ContractError ante cualquier forma malformada.
    """
    if not isinstance(text, str):
        raise ContractError("contrato no es texto decodificado")

    lines = text.split("\n")
    boundaries = [i for i, l in enumerate(lines) if _HEADER_RE.match(_strip_cr(l))]

    permitidos_idx = [i for i in boundaries if _strip_cr(lines[i]) == _PERMITIDOS_HEADER]
    prohibidos_idx = [i for i in boundaries if _strip_cr(lines[i]) == _PROHIBIDOS_HEADER]

    if len(permitidos_idx) == 0:
        raise ContractError("sección '## Archivos permitidos' ausente")
    if len(permitidos_idx) > 1:
        raise ContractError("sección '## Archivos permitidos' duplicada")
    if len(prohibidos_idx) == 0:
        raise ContractError("sección '## Archivos prohibidos' ausente")
    if len(prohibidos_idx) > 1:
        raise ContractError("sección '## Archivos prohibidos' duplicada")

    permitidos_lines = lines[
        permitidos_idx[0] + 1 : _section_end(lines, permitidos_idx[0], boundaries)
    ]
    prohibidos_lines = lines[
        prohibidos_idx[0] + 1 : _section_end(lines, prohibidos_idx[0], boundaries)
    ]

    allowed_entries = _parse_entries(permitidos_lines)
    forbidden_entries = _parse_entries(prohibidos_lines)

    allowed = _resolve_list(allowed_entries, allow_empty=False, label="permitidos")
    forbidden = _resolve_list(forbidden_entries, allow_empty=True, label="prohibidos")
    return allowed, forbidden


# --- 2. Matching, traversal y precedencia -----------------------------------


def compile_glob(pattern: str) -> re.Pattern:
    """Traduce un patrón literal (ya extraído por parse_contract) a regex.

    * no cruza '/'; ** sí; ? es un carácter distinto de '/'; un patrón acabado
    en '/' cubre todo su contenido; el resto es literal (_TEMPLATE.md,
    DEC-002). No se consulta el sistema de archivos.
    """
    out: List[str] = []
    i = 0
    n = len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    ere = "".join(out)
    if pattern.endswith("/"):
        ere = ere + ".*"
    return re.compile(ere)


_GLOB_CACHE: dict = {}


def _compiled(pattern: str) -> re.Pattern:
    rx = _GLOB_CACHE.get(pattern)
    if rx is None:
        rx = compile_glob(pattern)
        _GLOB_CACHE[pattern] = rx
    return rx


def match_any(path: str, patterns: Sequence[str]) -> Optional[str]:
    """Devuelve el primer patrón de `patterns` que caza `path`, o None."""
    for p in patterns:
        if _compiled(p).fullmatch(path):
            return p
    return None


def has_traversal(path: str) -> bool:
    """DEC-002: traversal es un componente exactamente '..', nunca subcadena."""
    return any(component == ".." for component in path.split("/"))


def evaluate(path: str, allowed: Sequence[str], forbidden: Sequence[str]) -> Verdict:
    """Evalúa una ruta versionada contra el contrato ya parseado.

    Orden: traversal (buena formación) → prohibidos (gana) → permitidos
    (lista blanca). Precedencia fijada por _TEMPLATE.md y DEC-002 §5.
    """
    if has_traversal(path):
        return Verdict(False, "traversal", None)
    hit_forbidden = match_any(path, forbidden)
    if hit_forbidden is not None:
        return Verdict(False, "prohibido", hit_forbidden)
    hit_allowed = match_any(path, allowed)
    if hit_allowed is not None:
        return Verdict(True, None, hit_allowed)
    return Verdict(False, "fuera_de_permitidos", None)


# --- 3. Destinos de symlink (DEC-002 §6) ------------------------------------


def resolve_symlink_target(link_path: str, target: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Resuelve textualmente el destino de un symlink contra su directorio.

    Devuelve (ok, motivo, resuelto). `ok=False` con motivo describe un
    destino absoluto o que sale de la raíz del repositorio; nunca toca disco
    (nada de open/readlink/realpath/stat, DEC-002 §6).
    """
    if target.startswith("/"):
        return False, "symlink_absoluto", None

    link_dir = link_path.rsplit("/", 1)[0] if "/" in link_path else ""
    stack: List[str] = [c for c in link_dir.split("/") if c] if link_dir else []

    for component in target.split("/"):
        if component in ("", "."):
            continue
        if component == "..":
            if stack:
                stack.pop()
            else:
                return False, "symlink_fuera_de_raiz", None
        else:
            stack.append(component)

    return True, None, "/".join(stack)


def evaluate_symlink(
    link_path: str, target: str, allowed: Sequence[str], forbidden: Sequence[str]
) -> Verdict:
    """Evalúa el destino de un symlink ya resuelto textualmente contra el
    contrato. No repite el matcher: reutiliza match_any."""
    ok, motivo, resolved = resolve_symlink_target(link_path, target)
    if not ok:
        return Verdict(False, motivo, None)
    assert resolved is not None
    hit_forbidden = match_any(resolved, forbidden)
    if hit_forbidden is not None:
        return Verdict(False, "symlink_prohibido", hit_forbidden)
    hit_allowed = match_any(resolved, allowed)
    if hit_allowed is not None:
        return Verdict(True, None, hit_allowed)
    return Verdict(False, "symlink_fuera_de_permitidos", None)
