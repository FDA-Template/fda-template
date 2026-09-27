#!/usr/bin/env bash
#
# tests/scope/generate-evidence-hashes.sh — Manifiesto JSON de identidad de
# evidencia para WP-015.
#
# No es un test (no coincide con test_*.py): es una utilidad de evidencia,
# permitida por estar dentro de tests/scope/**. Para cada ruta recibida,
# imprime a stdout un ÚNICO array JSON, ordenado de forma determinista por
# "ruta", con el modo y el blob Git (git ls-tree) y el SHA-256 de su
# contenido de working tree (shasum) — el manifiesto que WP-015 §6 exige,
# ligado al commit de HEAD en el momento de la invocación.
#
# WP015-F8 (revisión Astra, C1): antes solo existía una tabla Markdown y una
# salida de texto libre (RUTA=/LS_TREE=/SHA256=), no un manifiesto JSON
# ordenado. Este script ahora produce exactamente ese JSON, de forma
# determinista (mismo orden, mismas claves) para poder versionarlo bajo
# evidence/WP-015/** y compararlo byte a byte entre invocaciones.
#
# Solo lectura: no muta nada, ni en este repositorio ni en ninguno temporal.
# El único archivo temporal que crea (para pasar los registros a Python de
# forma segura ante rutas con espacios o bytes especiales) se borra siempre
# al terminar.
#
# Uso: bash tests/scope/generate-evidence-hashes.sh <ruta> [<ruta> ...]
# Salida: un array JSON en stdout, ordenado por "ruta", con indentación de
#         2 espacios y claves ordenadas.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

tmp_records="$(mktemp)"
trap 'rm -f "$tmp_records"' EXIT

for ruta in "$@"; do
  entry_line="$(git ls-tree HEAD -- "$ruta")"
  meta="${entry_line%%$'\t'*}"
  modo="${meta%% *}"
  rest="${meta#* }"
  blob="${rest#* }"
  hash_sha256="$(shasum -a 256 -- "$ruta" | awk '{print $1}')"
  printf '%s\0%s\0%s\0%s\0' "$ruta" "$modo" "$blob" "$hash_sha256" >> "$tmp_records"
done

python3 - "$tmp_records" <<'PYEOF'
import json
import sys

with open(sys.argv[1], "rb") as fh:
    data = fh.read()

fields = data.split(b"\x00")
if fields and fields[-1] == b"":
    fields = fields[:-1]

records = []
for i in range(0, len(fields), 4):
    ruta, modo, blob, sha256 = (f.decode("utf-8") for f in fields[i : i + 4])
    records.append({"ruta": ruta, "modo": modo, "blob": blob, "sha256": sha256})

records.sort(key=lambda r: r["ruta"])
print(json.dumps(records, indent=2, sort_keys=True, ensure_ascii=False))
PYEOF
