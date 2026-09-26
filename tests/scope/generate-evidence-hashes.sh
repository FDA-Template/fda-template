#!/usr/bin/env bash
#
# tests/scope/generate-evidence-hashes.sh — Manifiesto de identidad de
# evidencia para WP-015.
#
# No es un test (no coincide con test_*.py): es una utilidad de evidencia,
# permitida por estar dentro de tests/scope/**. Imprime, para cada ruta
# recibida, su modo y blob Git (git ls-tree) y el SHA-256 de su contenido de
# working tree (shasum), en el mismo formato que evidence/WP-015/verification.md
# exige para el manifiesto de TESTED_HEAD.
#
# Solo lectura: no muta nada, ni en este repositorio ni en ninguno temporal.
#
# Uso: bash tests/scope/generate-evidence-hashes.sh <ruta> [<ruta> ...]

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

for ruta in "$@"; do
  entrada="$(git ls-tree HEAD -- "$ruta")"
  hash_sha256="$(shasum -a 256 "$ruta" | awk '{print $1}')"
  echo "RUTA=$ruta"
  echo "LS_TREE=$entrada"
  echo "SHA256=$hash_sha256"
  echo "---"
done
