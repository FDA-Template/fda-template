# WP-015 — Verificación

## C3 excepcional — candidato para revalidación enfocada

`DEC-013`, fusionada en `7d1b26afcb3285e29ee17dee7548b34351948330`,
habilitó un único C3 para el residual cerrado `WP015-F2`. La rama incorporó
esa decisión sin reescribir historia mediante el merge
`9b66c8e75b1aa37574b151bb5821ef9dc648d9a7`. La apertura de C3 quedó
versionada antes de corregir en
`eb085a115ab6ac24078d8b4b551305f5ac99f2d8`.

Claude Code realizó una sola pasada y modificó únicamente
`tests/scope/test_check_scope_cli.py`. El coordinador comprometió ese cambio
como `TESTED_HEAD` antes de ejecutar la batería completa.

| Campo | Valor |
|---|---|
| Base vigente y `merge-base` | `7d1b26afcb3285e29ee17dee7548b34351948330` |
| Candidata C2 preservada | `4ad9eb354e3ff13c0a936be6c8a0eee691e44246` |
| Apertura C3 previa | `eb085a115ab6ac24078d8b4b551305f5ac99f2d8` |
| `TESTED_HEAD` C3 | `333eb072e62f3298f465c32c9d47a69b043cb8c1` |
| Árbol de `TESTED_HEAD` C3 | `4efabe75db5bfb1eb845e5e0a8db0d906e0d1eeb` |
| Autor/corrector | Claude Code (implementer), una invocación, sin subagentes |
| Coste C3 | `0.784279 USD` = `0.68 EUR` |
| Estado antes de Astra | **Batería APTO; revalidación enfocada de F2 pendiente** |

### Corrección y falsabilidad de WP015-F2

La variante local crea una `.gitmodules` no versionada que contiene solo la
asociación `[submodule "vendor"]` / `path = vendor`; `ignore=all` permanece
exclusivamente en `.git/config` del repositorio temporal. Sobre el mismo
`base` y `head` se acreditan tres observaciones:

1. el diff con los flags de producción salvo `--ignore-submodules=none` queda
   vacío: la manipulación local es efectiva;
2. la CLI real conserva exit `1`, ruta `vendor` y motivo
   `fuera_de_permitidos`;
3. una mutación únicamente en memoria de `_diff_records`, idéntica salvo por
   retirar el override, hace que la entrada real `check_scope.main` cambie a
   exit `0` y cero violaciones. `scripts/check_scope.py` no se edita.

Así, la regresión falla si desaparece el override y deja de ser el falso verde
identificado tras C2.

### Doce comandos literales

Se ejecutaron literalmente, en orden, sobre
`HEAD=333eb072e62f3298f465c32c9d47a69b043cb8c1`. La salida íntegra y cada
código de retorno están en `evidence/WP-015/verificacion-c3-literal.log`.

| # | Resultado C3 |
|---|---|
| 1–3 | rutas probadas limpias, sin staged ni archivos sin seguimiento |
| 4 | 152/152 pruebas en verde |
| 5 | 14/14 pruebas de seguridad estática en verde |
| 6 | `run-suite.sh`: 152/152, mismo HEAD y estado Git antes/después |
| 7 | `check_scope.py WP-015 origin/main...HEAD`: `OK`, cero violaciones; `merge_base=7d1b26a...` |
| 8 | shellcheck limpio |
| 9 | gobierno: 10 correctas, 0 fallidas |
| 10 | guard: 68 correctas, 0 fallidas, 10 huecos conocidos |
| 11 | manual: 0 fallos, 67 enlaces |
| 12 | `git diff --check`: limpio |

### Criterios de aceptación tras C3

| # | Criterio | Evaluación C3 |
|---|---|---|
| 1 | Tablas DEC-002/DEC-012, corpus, precedencia y globs | **CUMPLE** — suite completa en verde; sin cambios semánticos fuera de F2 |
| 2 | A/M/D/T/R/C, nombres inusuales, inventario y códigos | **CUMPLE** — 152/152 pruebas |
| 3 | Symlinks por modos y blobs | **CUMPLE** — suite y evidencia histórica inmutables |
| 4 | Fallo cerrado de contrato/rango/UTF-8/marcadores | **CUMPLE** — negativas en verde |
| 5 | Working tree no altera el contrato | **CUMPLE** — `TestContractManipulationIgnored` en verde |
| 6 | Suite deja idénticos HEAD y estado Git | **CUMPLE** — comando 6, aislamiento intacto |
| 7 | Inventario completo y límite local documentado | **CUMPLE** — comando 7 y evidencia existente |
| 8 | Biblioteca única importada por CLI | **CUMPLE** — AST y suite en verde; producción sin cambios en C3 |
| 9 | Identidad de bytes y suelo T3 | **PENDIENTE DE GATE** — manifiesto C3 generado; falta dictamen enfocado de la misma Astra |

El manifiesto ordenado de los diez archivos probados está en
`evidence/WP-015/manifiesto-tested-head-c3.json`. Los nueve archivos sin
cambios conservan los blobs de C2; `tests/scope/test_check_scope_cli.py` pasa a
blob `c98ab0af21679d4fd541a3883b4fd6e594751195` y SHA-256
`62df84cd2d815feab810ecd1a43f741679ac77ea6ce2b058b7fc6508c53d6734`.

**VEREDICTO DE BATERÍA: APTO.** Comandos: `12 / 12` en verde. Criterios:
`8` cumplidos, `0` incumplidos, `1` pendiente del gate T3. El candidato no se
declara todavía APTO de entrega: requiere la revalidación enfocada de Astra.

## C2 — candidato para revalidación enfocada final

Claude Code abrió C2 previamente en `d59c9c6` y comprometió las correcciones
de `WP015-F2`, `WP015-F3`, `WP015-F4` y `WP015-F6` antes de que el servicio
interrumpiera la invocación por límite temporal. No se sustituyó al autor ni
se modificó su código: el coordinador ejecutó después las verificaciones y
generó las evidencias deterministas previstas por ese commit.

| Campo | Valor |
|---|---|
| Base autorizada | `30939377590a3c3b49ba705ef0f20c4832df61bd` |
| Candidato C1 revalidado | `ce17110a71c39eb6533ae54ca438ededf765fceb` |
| Apertura C2 previa | `d59c9c64d0401032768530cea8010dff2f314ccf` |
| `TESTED_HEAD` C2 | `a855c2f2505a0a1a92310d71218444d6a0987bff` |
| Árbol de `TESTED_HEAD` C2 | `8f04016927bed6b21a284ad25ab198536e8675f4` |
| Autor/corrector | Claude Code (implementer) |
| Estado | **NO APTO tras revalidación enfocada final; 2/2 ciclos agotados** |

El commit C2 modifica únicamente `scripts/check_scope.py` y `tests/scope/**`:
añade la regresión con gitlink real, validación cerrada de puntuaciones y
pares modo/tipo, la regresión completa de separadores Unicode y un regenerador
determinista de evidencias de symlinks. `scripts/scope_rules.py` y el manual no
cambian en C2.

Los doce comandos del contrato se ejecutaron literalmente, en orden, con
`HEAD=a855c2f2505a0a1a92310d71218444d6a0987bff`. Todos terminaron con exit `0`;
la salida íntegra está en `evidence/WP-015/verificacion-c2-literal.log`:

| # | Resultado C2 |
|---|---|
| 1–3 | rutas probadas limpias, sin staged ni archivos sin seguimiento |
| 4 | 152/152 pruebas en verde |
| 5 | 14/14 pruebas de seguridad estática en verde |
| 6 | `run-suite.sh`: 152/152, mismo HEAD antes/después |
| 7 | `check_scope.py WP-015 origin/main...HEAD`: `OK`, cero violaciones |
| 8 | shellcheck limpio |
| 9 | gobierno: 10 correctas, 0 fallidas |
| 10 | guard: 68 correctas, 0 fallidas, 10 huecos conocidos |
| 11 | manual: 0 fallos, 66 enlaces |
| 12 | `git diff --check`: limpio |

Correspondencia de C2:

| Hallazgo | Cierre implementado y probado |
|---|---|
| `WP015-F2` | `TestGitlinkIgnoreOverrideRegression` crea un repositorio anidado registrado como gitlink y conserva exit `1`, ruta `vendor` e inventario idéntico sin manipulación, con `.gitmodules` no versionado `ignore=all` y con configuración local `ignore=all`. |
| `WP015-F3` | puntuaciones R/C limitadas a 0..100; conjunto cerrado y coherente de modos/tipos; reproducciones `R101`, `777777 blob` y `100644 commit` llegan a la CLI real y devuelven exit `2`. |
| `WP015-F4` | regresión con U+0085, U+2028, U+2029, LF y tab: cinco violaciones, diez líneas, ASCII y recuperación exacta; falla si se restaura `ensure_ascii=False`. |
| `WP015-F6` | `regenerate-symlink-evidence.sh` reproduce SHA concretos para A/M/D/T/R; `symlinks.md` registra revisión, ruta/rol, modo, blob y veredicto. |

El manifiesto ordenado de los diez archivos probados está en
`evidence/WP-015/manifiesto-tested-head-c2.json`, ligado a `TESTED_HEAD` C2.
Los commits posteriores de evidencia deben mantener diff cero respecto a
`a855c2f2505a0a1a92310d71218444d6a0987bff` en código, pruebas y manual.

La revalidación final de Astra cerró F3, F4 y F6. F2 queda abierto únicamente
porque la prueba de configuración local no asocia `vendor` mediante
`.gitmodules`, por lo que no activa realmente `submodule.vendor.ignore=all` y
no detectaría la retirada del override. El código corregido sí conservó la
violación en la reproducción efectiva de Astra. Con C2 consumido no procede
otra corrección sin una decisión humana nueva, previa, fechada y versionada.

## Evidencia histórica de C1

`C1`: corrección de `WP015-F1` a `WP015-F8` (revisión completa de Astra en
`evidence/WP-015/revision-astra.md`), conforme a DEC-010. Autor y corrector
único: Claude Code (implementer). No es C2 y no se abre C2 en este
documento; `evidence/WP-015/ciclos.md` sigue en `abierto` hasta que el
coordinador lo cierre con el coste estructurado de esta pasada.

**Los doce comandos de `## Verificación` se ejecutaron literalmente y en el
orden exacto del contrato.** La pasada del autor está en
`evidence/WP-015/verificacion-c1.log`; sus comandos 3, 4 y 5 quedaron
bloqueados por los permisos de esa sesión. El coordinador repitió después los
doce comandos en su forma literal exacta, sobre un head cuyas rutas probadas
son idénticas a este `TESTED_HEAD`, y todos devolvieron exit `0`. La salida
íntegra de esa segunda pasada está en
`evidence/WP-015/verificacion-c1-literal.log` y prevalece para acreditar la
literalidad contractual.

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

## Resultados de los doce comandos literales

Resumen de la pasada del coordinador; salida íntegra en
`verificacion-c1-literal.log`:

| # | Comando | Exit | Resultado |
|---|---|---|---|
| 1 | `git diff --exit-code HEAD -- ...` | `0` | vacío |
| 2 | `git diff --cached --exit-code HEAD -- ...` | `0` | vacío |
| 3 | `git ls-files --others ... \| python3 -c ...` | `0` | ejecución literal; vacío |
| 4 | `python3 -m unittest discover -p 'test_*.py'` | `0` | ejecución literal; 134/134 |
| 5 | `python3 -m unittest discover -p 'test_security_static.py'` | `0` | ejecución literal; 14/14 |
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
2. Los permisos del autor bloquearon inicialmente los comandos literales 3,
   4 y 5; el coordinador los ejecutó después sin sustituciones, todos exit `0`,
   y preservó la salida en `evidence/WP-015/verificacion-c1-literal.log`.
3. `WP015-F2` sin integración de gitlink real (ver tabla de arriba):
   corrección aplicada, prueba de integración específica pendiente.
