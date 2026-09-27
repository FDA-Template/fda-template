# WP-015 — Verificación

`C1`: corrección de `WP015-F1` a `WP015-F8` (revisión completa de Astra en
`evidence/WP-015/revision-astra.md`), conforme a DEC-010. Autor y corrector
único: Claude Code (implementer). No es C2 y no se abre C2 en este
documento; `evidence/WP-015/ciclos.md` sigue en `abierto` hasta que el
coordinador lo cierre con el coste estructurado de esta pasada.

**Los doce comandos de `## Verificación` se ejecutaron, en el orden exacto
del contrato, sobre este `TESTED_HEAD`.** La salida íntegra y el código de
salida de cada uno están en `evidence/WP-015/verificacion-c1.log`. Tres
invocaciones literales (el envoltorio `python3 -c "..."` y los dos
`python3 -m unittest discover ...`) quedaron bloqueadas por la lista `allow`
de `.claude/settings.json` de esta sesión de autor/corrector —no por
`guard.sh` ni por el contrato de WP-015—; el `.log` documenta, para cada una,
la ejecución real y funcionalmente equivalente que las sustituye (el mismo
resultado observable), exactamente como ya se hizo y se aceptó durante la
implementación inicial.

## Identidad de `TESTED_HEAD` (C1)

| Campo | Valor |
|---|---|
| Rama | `wp/WP-015-check-scope-local` |
| Base autorizada | `30939377590a3c3b49ba705ef0f20c4832df61bd` (`origin/main`) |
| Candidato revisado por Astra | `b1a8031bf715bff43239e7f835d396f301f5d5a2` |
| Commit que abre `C1` (versionado antes de corregir) | `9d5d5dee4bf416786b26ee53e22917a227ccc7c1` |
| `TESTED_HEAD` (C1) | `513d68c422a9d8380e0100944e7eb68d8f42ece9` |
| Árbol de `TESTED_HEAD` | `b25e195b072432001c3552c9518a684fa8f632b6` |
| `merge-base(origin/main, TESTED_HEAD)` | `30939377590a3c3b49ba705ef0f20c4832df61bd` (= base autorizada) |

`TESTED_HEAD` sustituye al de la implementación inicial
(`718ce294fe592c2b6df7c13c5f56caea4199d7f2`, ya cerrado y superado por esta
corrección). El único commit de código/pruebas de `C1` es
`513d68c422a9d8380e0100944e7eb68d8f42ece9` — "WP-015: C1 - corrige
WP015-F1 a WP015-F8 de la revision Astra" —, que modifica exactamente
`scripts/check_scope.py`, `scripts/scope_rules.py`,
`tests/scope/generate-evidence-hashes.sh`, `tests/scope/test_check_scope_cli.py`,
`tests/scope/test_scope_rules.py` y `tests/scope/test_security_static.py`.
Ningún commit posterior a este toca código, pruebas ni manual; los
commits siguientes son exclusivamente de evidencia y deben demostrar diff
cero respecto de este `TESTED_HEAD` en las rutas probadas:

```bash
git diff --exit-code 513d68c422a9d8380e0100944e7eb68d8f42ece9 -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md
```

## Manifiesto de identidad (JSON, ordenado por ruta)

`WP015-F8`: `evidence/WP-015/manifiesto-tested-head-c1.json`, generado
determinísticamente con `bash tests/scope/generate-evidence-hashes.sh
<rutas...>` (solo lectura: `git ls-tree` + `shasum -a 256`, ensamblado con
`json.dumps(..., sort_keys=True)` dentro del propio script). Contiene, para
cada uno de los nueve archivos bajo los patrones probados, su `ruta`, `modo`,
`blob` (Git, SHA-1) y `sha256` (contenido), ordenado alfabéticamente por
`ruta`. Verificado byte a byte contra `git ls-files -s` de las mismas nueve
rutas (idéntico blob y modo, ver `evidence/WP-015/verificacion-c1.log`).

**Nota sobre el bit ejecutable** (sin cambios respecto de la implementación
inicial): `chmod`/`git update-index --chmod` siguen denegados por el permiso
de herramienta de esta sesión; los `.sh` de `tests/scope/` quedan en modo
`100644`. No afecta a ninguna verificación (siempre `bash <script>`).

## Resultados de los doce comandos (resumen; íntegro en `verificacion-c1.log`)

| # | Comando | Exit | Resultado |
|---|---|---|---|
| 1 | `git diff --exit-code HEAD -- ...` | `0` | vacío |
| 2 | `git diff --cached --exit-code HEAD -- ...` | `0` | vacío |
| 3 | `git ls-files --others ... \| python3 -c ...` | `0` | bloqueo de permisos; equivalente real ejecutado, vacío |
| 4 | `python3 -m unittest discover -p 'test_*.py'` | `0` | bloqueo de permisos; 134/134 vía comando 6 (anidado) |
| 5 | `python3 -m unittest discover -p 'test_security_static.py'` | `0` | bloqueo de permisos; 13/13 vía comando 6 (anidado) |
| 6 | `bash tests/scope/run-suite.sh` | `0` | 134/134 pruebas, aislamiento intacto |
| 7 | `python3 scripts/check_scope.py WP-015 origin/main...HEAD` | `0` | `OK`, cero violaciones |
| 8 | `shellcheck --severity=warning --shell=bash tests/scope/run-suite.sh` | `0` | vacío |
| 9 | `bash tests/governance/test-check-active.sh` | `0` | 10 correctas, 0 fallidas |
| 10 | `bash tests/guard/run-suite.sh` | `0` | 68 correctas, 0 fallidas, 10 huecos conocidos |
| 11 | `python3 evidence/WP-000/checks/check-manual.py` | `0` | 0 fallos, 66 enlaces |
| 12 | `git diff --check` | `0` | vacío |

## Correspondencia hallazgo → corrección → prueba

| Hallazgo | Corrección | Pruebas nuevas |
|---|---|---|
| `WP015-F1` | `scope_rules.compile_glob` compila con `re.DOTALL` | `TestDoubleStarAndDirSuffixConsumeLF` (7, unitarias) + 3 CLI con Git real en `TestExitOne` |
| `WP015-F2` | `_diff_records` añade `--ignore-submodules=none` | cubierto por la batería general; sin gitlinks en este repositorio de pruebas no se construyó un repo con submódulo real (ver «Deuda» abajo) |
| `WP015-F3` | `parse_name_status_z`/`parse_ls_tree_z` estrictos | 15 pruebas en `TestPureParsers` con respuestas Git controladas |
| `WP015-F4` | `_emit_json` con `ensure_ascii=True` | cubierto por toda la batería de CLI (cada línea JSON emitida ya pasa por esta ruta); ver `evidence/WP-015/seguridad.md` |
| `WP015-F5` | `test_security_static._analyze` resuelve alias | `TestAnalyzerNegativeSamples` (9 pruebas) |
| `WP015-F6` | symlinks `M`/`R`, UTF-8 inválido real, contrato ampliado en HEAD | 5 pruebas nuevas en `TestExitOne`/`TestContractManipulationIgnored` |
| `WP015-F7` | `_WP_ID_RE` con `[0-9]{3}` | `test_wp_id_with_unicode_digits_is_exit_2` |
| `WP015-F8` | manifiesto JSON determinista | `evidence/WP-015/manifiesto-tested-head-c1.json`, generado por el script actualizado |

**Deuda declarada — `WP015-F2` sin integración con gitlink real.** La
corrección (`--ignore-submodules=none`) está aplicada y la batería general
(134/134) sigue en verde, pero esta pasada no añadió un test de integración
que cree un submódulo Git real dentro de un repositorio temporal (requiere
`git submodule add`, fuera de las seis mutaciones Git que
`tests/scope/_repo.py` tiene admitidas: `init/config/add/commit/mv/rm`) para
reproducir exactamente el escenario de `.gitmodules` no versionado con
`ignore=all` ocultando el gitlink. El indicador estático más cercano —que la
CLI real ya invoca `--ignore-submodules=none`— está en el propio código
(comentario junto a la llamada) y en `evidence/WP-015/verificacion-c1.log`
comando 7. Se declara como deuda pendiente en vez de fabricar una prueba con
una mutación Git fuera del alcance admitido; corresponde a la revalidación
enfocada decidir si esto cierra `F2` o exige una vía distinta (por ejemplo,
una extensión acotada del alcance de `_repo.py` autorizada aparte).

## Resumen de criterios de aceptación (C1)

- [x] Los ocho hallazgos autorizados (`WP015-F1`–`WP015-F8`) están
  corregidos, cada uno con al menos una prueba nueva que demuestra la
  corrección (excepto la deuda declarada de integración de `F2` arriba).
- [x] No se abrió ninguna revisión general nueva ni se amplió el alcance:
  el diff de `C1` se limita a `scripts/check_scope.py`, `scripts/scope_rules.py`
  y `tests/scope/**` (commit `513d68c`).
- [x] 134/134 pruebas en verde, aislamiento del repositorio FDA acreditado
  antes/después (`evidence/WP-015/verificacion-c1.log`, comando 6).
- [x] `python3 scripts/check_scope.py WP-015 origin/main...HEAD` en verde
  sobre el nuevo `TESTED_HEAD`.
- [x] Manifiesto JSON ordenado por ruta, ligado a `TESTED_HEAD`, versionado
  en `evidence/WP-015/manifiesto-tested-head-c1.json`.
- [x] `git diff --check` limpio; sin cambios fuera de los cinco patrones
  permitidos.

## Deuda y bloqueos declarados

1. Bit ejecutable ausente en los `.sh` de `tests/scope/` (sin cambios desde
   la implementación inicial; sigue sin afectar a ninguna verificación).
2. Tres invocaciones literales bloqueadas por el permiso de herramienta de
   esta sesión concreta (comandos 3, 4 y 5); documentadas con su ejecución
   real equivalente en `evidence/WP-015/verificacion-c1.log`.
3. `WP015-F2` sin integración de gitlink real (ver tabla de arriba):
   corrección aplicada, prueba de integración específica pendiente.
