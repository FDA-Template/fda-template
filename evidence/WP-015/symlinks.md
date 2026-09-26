# WP-015 — Symlinks por objetos Git

## Regla implementada

Un symlink se identifica **solo** por modo Git `120000` (`_ls_tree_entry` /
`_check_symlink` en `scripts/check_scope.py`). Su destino es el contenido del
blob de la revisión correspondiente, leído con `git cat-file blob <sha>` y
decodificado UTF-8 estricto — nunca `open`, `readlink`, `realpath` ni `stat`
(acreditado por `tests/scope/test_security_static.py`).

Revisión inspeccionada según el estado del diff, exactamente como exige el
contrato:

| Estado | Revisión(es) inspeccionada(s) | Implementado en |
|---|---|---|
| `A`, `M` | `head` | `_judge`, rama `letter in ("A", "M")` |
| `D` | `merge-base` | `_judge`, rama `letter == "D"` |
| `T` | `merge-base` **y** `head` (misma ruta) | `_judge`, rama `else` (T) |
| `R`, `C` | `merge-base` para el origen, `head` para el destino | `_judge`, rama `else` (R/C) |

El destino se resuelve **textualmente** contra el directorio del enlace
(`scope_rules.resolve_symlink_target`): separa por `/`, resuelve `..` sin
tocar disco, y declara violación si el destino es absoluto o si el
plegado agota la pila (sale de la raíz). El resultado final se evalúa
contra permitidos/prohibidos con el mismo `match_any` que cualquier otra
ruta (`scope_rules.evaluate_symlink`), sin segunda implementación.

## Cobertura por estado, con revisión, modo, blob y veredicto

Todas las pruebas siguientes están en verde (comando 6 de
`evidence/WP-015/verification.md`).

### Unitarias puras (`tests/scope/test_scope_rules.py`, clase `TestSymlinkResolution`)

| Caso | Prueba | Veredicto |
|---|---|---|
| Destino absoluto (`/etc/passwd`) | `test_absolute_target_is_violation` | `symlink_absoluto` |
| Sale de la raíz (`../outside` desde un enlace en la raíz) | `test_escape_root_is_violation` | `symlink_fuera_de_raiz` |
| Sale de la raíz en profundidad (`../../../outside` desde `a/b/link`) | `test_deep_escape_root_is_violation` | `symlink_fuera_de_raiz` |
| Resolución textual relativa normal (`../other.md` desde `docs/sub/link`) | `test_relative_target_resolves_textually` | resuelve a `docs/other.md` |
| Resolución dentro del mismo directorio | `test_relative_target_within_same_dir` | resuelve a `docs/other.md` |
| Destino dentro de permitidos | `test_evaluate_symlink_target_inside_allowed` | `ok=True` |
| Destino fuera de permitidos | `test_evaluate_symlink_target_outside_allowed` | `symlink_fuera_de_permitidos` |
| Destino dentro de prohibidos (gana sobre permitidos) | `test_evaluate_symlink_target_inside_forbidden` | `symlink_prohibido` |
| Destino absoluto vía `evaluate_symlink` | `test_evaluate_symlink_absolute_target` | `symlink_absoluto` |
| Un enlace permitido no amplía el alcance de su destino | `test_symlink_never_amplifies_scope` | `ok=False` |

### Integración vía Git real (`tests/scope/test_check_scope_cli.py`)

| Estado | Modo Git | Escenario | Prueba | Veredicto |
|---|---|---|---|---|
| `T` (regular → symlink) | `120000` en `head`; `100644` en `merge-base` | `docs/note.txt` deja de ser archivo regular y pasa a symlink apuntando a `../secrets/token` | `test_typechange_to_symlink_outside_allowed` | `symlink_fuera_de_permitidos` |
| `A` | `120000` en `head` | symlink añadido apuntando dentro de lo permitido | `test_symlink_pointing_inside_allowed_is_ok` | `ok` (exit 0) |
| `A` | `120000` en `head` | symlink añadido con destino absoluto | `test_symlink_absolute_target_is_violation` | `symlink_absoluto` |
| `A` | `120000` en `head` | symlink añadido que sale de la raíz | `test_symlink_escaping_root_is_violation` | `symlink_fuera_de_raiz` |
| `D` | `120000` en `merge-base` | symlink absoluto existente en `base`, eliminado en `head`; se juzga desde `merge-base` | `test_deleted_symlink_target_judged_from_merge_base` | `symlink_absoluto` |

La fila `D` demuestra explícitamente que, aunque el symlink ya no existe en
`head`, `check_scope.py` sigue detectando la violación porque inspecciona el
modo y el blob de la revisión `merge-base` (nunca el working tree, que ni
siquiera contiene el enlace en ese punto de la ejecución del test, dado que
`git rm` ya lo retiró antes de invocar la CLI).

## Ausencia de segunda implementación

`_check_symlink` en `scripts/check_scope.py` no reimplementa ninguna regla de
resolución o matching: llama a `scope_rules.evaluate_symlink`, que a su vez
reutiliza `scope_rules.match_any` (el mismo matcher que usa `scope_rules.evaluate`
para rutas ordinarias). No hay parser ni matcher duplicado.
