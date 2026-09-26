#!/usr/bin/env bash
#
# tests/scope/run-suite.sh — Entrypoint headless de la suite de WP-015.
#
# Ejecuta la batería completa de tests/scope (unittest discover) y, además,
# acredita el criterio de aislamiento del contrato: el repositorio FDA queda
# exactamente igual antes y después, porque toda la suite trabaja sobre
# repositorios Git temporales y desechables (mktemp -d) y nunca sobre este
# repositorio.
#
# Uso:  bash tests/scope/run-suite.sh
# Salida: exit 0 = pruebas en verde Y aislamiento intacto
#         exit 1 = alguna prueba falló, o el aislamiento se rompió
#
# Headless, sin red, sin TTY.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

echo "============================================================"
echo " WP-015 — suite de scripts/check_scope.py y scripts/scope_rules.py"
echo "============================================================"

# --- 1. Huella de aislamiento, ANTES -----------------------------------------
head_antes="$(git rev-parse HEAD)"
estado_antes="$(git status --porcelain=v1 -z -uall | shasum -a 256)"

echo
echo "--- HEAD antes: $head_antes ---"

# --- 2. Batería completa -----------------------------------------------------
resultado_tests=0
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scope -p 'test_*.py' -v
resultado_tests=$?

# --- 3. Huella de aislamiento, DESPUÉS ---------------------------------------
head_despues="$(git rev-parse HEAD)"
estado_despues="$(git status --porcelain=v1 -z -uall | shasum -a 256)"

echo
echo "--- HEAD después: $head_despues ---"

aislamiento_roto=0
if [ "$head_antes" != "$head_despues" ]; then
  echo "FALLO AISLAMIENTO: HEAD cambió durante la suite ($head_antes -> $head_despues)"
  aislamiento_roto=1
fi
if [ "$estado_antes" != "$estado_despues" ]; then
  echo "FALLO AISLAMIENTO: git status difiere antes/después de la suite"
  aislamiento_roto=1
fi

echo
echo "============================================================"
if [ "$resultado_tests" -eq 0 ] && [ "$aislamiento_roto" -eq 0 ]; then
  echo " RESULTADO: OK (pruebas en verde, aislamiento intacto)"
  echo "============================================================"
  exit 0
fi

echo " RESULTADO: FALLO (tests=$resultado_tests aislamiento_roto=$aislamiento_roto)"
echo "============================================================"
exit 1
