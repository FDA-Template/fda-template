#!/usr/bin/env bash
#
# tests/scope/regenerate-symlink-evidence.sh — WP015-F6 (revalidación
# enfocada de C1, C2): mecanismo de SOLO LECTURA para regenerar y verificar
# los identificadores REALES (commit, ruta/rol, modo, blob y veredicto) que
# evidence/WP-015/symlinks.md cita para cada estado A/M/D/T/R cubierto.
#
# Construye UN repositorio Git temporal y desechable (`mktemp -d`), con
# identidad y fecha de autor/committer FIJAS (ver tests/scope/_repo.py,
# _FIXED_DATE), de modo que los commits resultantes son reproducibles byte
# a byte: cualquiera puede ejecutar este mismo script en cualquier máquina y
# obtener exactamente los mismos SHA que cita la evidencia. No usa
# `git submodule add`, no usa red y no muta el repositorio FDA ni ningún
# repositorio ajeno a su propio temporal.
#
# La resolución del veredicto la hace scripts/check_scope.py, ya existente:
# este script no reimplementa ninguna regla de alcance ni de symlinks.
#
# Uso: bash tests/scope/regenerate-symlink-evidence.sh

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CHECK_SCOPE="$REPO_ROOT/scripts/check_scope.py"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

export GIT_AUTHOR_NAME="WP-015 fixture"
export GIT_AUTHOR_EMAIL="wp015-fixture@example.invalid"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000"
export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"

cd "$TMP" || exit 1
git init -q
git config commit.gpgsign false

mkdir -p work-packages docs
cat > work-packages/WP-901-sandbox.md <<'CONTRACT'
# WP-901 — contrato sintético de prueba

## Objetivo y contexto

Sintético, solo para regenerar evidencia de symlinks de WP-015.

## Archivos permitidos

- docs/**

## Archivos prohibidos

- ninguno
CONTRACT

printf 'contenido\n' > docs/note.txt
printf 'contenido\n' > docs/target_ok.md
ln -s /etc/passwd docs/absolute_link.md
git add -A
git commit -q -m "c0: base con note.txt regular y absolute_link.md symlink absoluto"
C0="$(git rev-parse HEAD)"

rm docs/note.txt
ln -s ../secrets/tok2 docs/note.txt
rm docs/absolute_link.md
ln -s ../secrets/tok docs/newlink.md
git add -A
git commit -q -m "c1: A newlink.md, D absolute_link.md, T note.txt a symlink"
C1="$(git rev-parse HEAD)"

rm docs/newlink.md
ln -s ../secrets/tok3 docs/newlink.md
git add -A
git commit -q -m "c2: M newlink.md cambia de destino"
C2="$(git rev-parse HEAD)"

mkdir -p docs/a/b
ln -s ../../target_ok.md docs/a/b/renlink.md
git add -A
git commit -q -m "c3: A a/b/renlink.md, destino permitido desde esa profundidad"
C3="$(git rev-parse HEAD)"

git mv docs/a/b/renlink.md docs/renlink.md
git commit -q -m "c4: R renlink.md a la raiz de docs, mismo destino relativo"
C4="$(git rev-parse HEAD)"

echo "=================================================================="
echo " Commits deterministas (fecha y autor fijos; reproducibles siempre)"
echo "=================================================================="
echo "c0=$C0"
echo "c1=$C1"
echo "c2=$C2"
echo "c3=$C3"
echo "c4=$C4"
echo

reportar_ls_tree() {
  rev="$1"; ruta="$2"
  echo "  git ls-tree $rev -- $ruta"
  echo "  -> $(git ls-tree "$rev" -- "$ruta")"
}

echo "--- Estado A: rango $C0...$C1, ruta docs/newlink.md, rol ruta ---"
reportar_ls_tree "$C1" docs/newlink.md
echo "  veredicto (check_scope.py real):"
python3 "$CHECK_SCOPE" WP-901 "$C0...$C1" | sed 's/^/    /'
echo

echo "--- Estado D: rango $C0...$C1, ruta docs/absolute_link.md, rol ruta ---"
reportar_ls_tree "$C0" docs/absolute_link.md
echo "  (mismo rango y veredicto que el bloque A; ver arriba)"
echo

echo "--- Estado T: rango $C0...$C1, ruta docs/note.txt, rol ruta ---"
reportar_ls_tree "$C0" docs/note.txt
reportar_ls_tree "$C1" docs/note.txt
echo "  (mismo rango y veredicto que el bloque A; ver arriba)"
echo

echo "--- Estado M: rango $C1...$C2, ruta docs/newlink.md, rol ruta ---"
reportar_ls_tree "$C2" docs/newlink.md
echo "  veredicto (check_scope.py real):"
python3 "$CHECK_SCOPE" WP-901 "$C1...$C2" | sed 's/^/    /'
echo

echo "--- Estado R: rango $C3...$C4, origen docs/a/b/renlink.md, destino docs/renlink.md ---"
reportar_ls_tree "$C3" docs/a/b/renlink.md
reportar_ls_tree "$C4" docs/renlink.md
echo "  veredicto (check_scope.py real):"
python3 "$CHECK_SCOPE" WP-901 "$C3...$C4" | sed 's/^/    /'
echo

echo "=================================================================="
echo " Fin. Repositorio temporal: $TMP (se borra al salir)"
echo "=================================================================="
