# WP-018 — Registro de ciclos de `WP018-DOR7-PSHA-R2`

Este registro aplica `DEC-010` §18 y pertenece exclusivamente a la transición
nueva que rederiva desde cero la actualización de `assertion.workflow_sha` del
provider de DOR-7. No reactiva la transición histórica, no abre C3, no activa
WP-018 y no modifica infraestructura. Este registro tampoco autoriza otra
invocación, la ejecución de la candidata, el provider, WIF, el workflow o C0.

## Anclajes congelados

- Rama durable R2: `ops/wp018-dor7-provider-sha-r2-custody`.
- Base exclusiva: `origin/main`
  `9cdfaefddfdb50fa1fba385e265243022b67061f`.
- Padre de la base: `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e`.
- Workflow: `.github/workflows/wp018-dor7-emergency-push.yml`.
- SHA-256 del workflow:
  `7ea50ded863cf57f2cac6916dada3dece9305bb6af60266601ca79ffa76b1594`.
- Preimagen administrativa fresca y saneada:
  `/private/tmp/wp018-dor7-psha-r2-preimage-20261015.Hig7rf`.
- Observación de la preimagen: `2026-10-15T14:27:48Z`, resultado `APTO`, cero
  deriva en 34 comparaciones históricas estables, pool y provider
  deshabilitados, cero roles personalizados, claves de usuario, secretos,
  variables o despachos.
- SHA-256 del `SHA256SUMS` de la preimagen, con 40 entradas verificadas:
  `5a03258545e2bb0b4761d343a1d3b3cbd444b61adc1dbce4e1d1da4afac4230c`.

Cualquier cambio posterior de `main`, workflow, candidata o estado externo
detiene la transición y exige decisión humana previa. Los anclajes no se
actualizan en cascada. Antes de invocar al autor se debe repetir la comprobación
de ausencia de deriva contra esta preimagen; esta apertura no sustituye ese
gate.

La rama histórica `ops/wp018-dor7-provider-sha-custody` permanece congelada,
sin fusionar y anclada en
`1da4697d33fc73d5318c2e91f1b15af7d4852d3a`. Sus C1 y C2 continúan consumidos,
su candidata C2 conserva `NO APTO — NO EJECUTAR` y no se copia, mezcla, importa
o usa como andamio de R2.

## Candidata R2 y revisión de origen

La candidata R2 está preservada fuera del repositorio en
`/private/tmp/wp018-dor7-provider-sha-r2-candidate.lxugrv`. Se rederivó desde
cero sobre la base y preimagen anteriores. Su `SHA256SUMS` contiene 54 entradas
verificadas y tiene SHA-256
`bfa60e607b707a62f19e16bfce7035749608f7ff336bf3cc45d7027a8f5db891`.

La única revisión completa independiente GPT-6 Astra, razonamiento Alto,
contexto nuevo y solo lectura emitió `NO APTO — NO EJECUTAR` el 2026-10-15. Su
identidad, transcripción y hashes están custodiados en `review-astra.md`.
Permanecen abiertos exclusivamente los cinco hallazgos concretos siguientes:

| Hallazgo R2 | Severidad | Alcance corrector |
|---|---|---|
| `WP018-PSHA-R2-F1` | Bloqueante | hacer reanudable el rollback tras un corte durante la recaptura |
| `WP018-PSHA-R2-F2` | Importante | incorporar `result.json` a la comparación contractual sin exclusiones nuevas |
| `WP018-PSHA-R2-F3` | Importante | probar el capturador real, sanitización, cortes de rollback e inhibición real de `errexit` |
| `WP018-PSHA-R2-F4` | Importante | impedir que respuestas crudas con identidades lleguen al disco o sobrevivan a `SIGKILL` |
| `WP018-PSHA-R2-F5` | Importante | fallar cerrado si no puede comprobarse la ausencia de impersonación |

Estos identificadores pertenecen a la revisión de R2: no reabren
`WP018-PSHA-F3` o `WP018-PSHA-F5` históricos. Los cierres históricos y los ocho
hallazgos anteriores continúan como regresiones obligatorias. R2-C1 solo puede
corregir los cinco hallazgos de la tabla y sus efectos directos. La preimagen
autorizada es inmutable. Los archivos técnicos que pueden recibir esas
correcciones son:

- `00-common.sh`, `00-constants.sh`, `01-capture-live.sh`,
  `02-update-provider.sh` y `03-rollback-provider.sh`;
- `lib/r2.py` y `lib/sanitize_policy.py`;
- `tests/fake-capture.sh`, `tests/fake-gcloud.py`, `tests/fake-gh.sh` y
  `tests/run-local-tests.sh`;
- `README.md`, `LOCAL-VERIFICATION.md` y el `SHA256SUMS` raíz regenerado.

No se permite modificar `authorized-preimage/**`, ampliar la mutación, aceptar
nuevas exclusiones volátiles, reutilizar C2 ni corregir algo ajeno a los cinco
hallazgos y sus efectos directos.

## Estado versionado de los ciclos R2

| Ciclo | Estado | Fecha de apertura | Invocaciones correctoras | Autor ejecutado | Base | Coste acumulado R2 |
|---|---|---|---:|---|---|---:|
| R2-C1 | `NO APTO — consumido` | 2026-10-15 | 1 | sí; terminó, sin verificación ejecutada válida | `9cdfaefddfdb50fa1fba385e265243022b67061f` | 3.65 de 5.00 EUR |

R2-C1 adquirió autoridad mediante el commit publicado
`1cce54865a8d3c9444f3b632fe35038f0b3c5431`. Se consumió al comenzar su única
invocación correctora; el éxito del instrumento no acredita la postimagen y no
se crea una segunda fila R2-C1.

### Apertura de R2-C2

| Ciclo | Estado | Fecha de apertura | HEAD y candidata de entrada | Revisión de origen | Hallazgos autorizables | Invocaciones correctoras | Autor ejecutado | Base | Coste acumulado R2 |
|---|---|---|---|---|---|---:|---|---|---:|
| R2-C2 | `abierto` | 2026-10-15 | custodia R2-C1 `b4ec67626e836877d96e83e700c4ce9755904922`; postimagen externa con manifiesto completo `133aa34695c7329552c2a7427540eed8dfbf2d1f0cf63cf0163dba9fd1c47fa3` | `review-astra.md`, revalidación enfocada 1/2; salida `51d0cd2ac776ab88c53eee4df6086ada6ce366ddea82dc32d8b99f6464c846ef` | `WP018-PSHA-R2-F1`, `WP018-PSHA-R2-F3` y efectos directos | 0 | no | `9cdfaefddfdb50fa1fba385e265243022b67061f` | 3.65 de 5.00 EUR |

La autorización humana del 2026-10-15 cubre exclusivamente esta apertura
documental. La fila solo adquiere autoridad cuando el commit que la contiene
queda publicado en la rama durable R2. No autoriza todavía una invocación del
autor, y R2-C2 no se consume hasta que esa eventual invocación comience.

La postimagen R2-C1 es la entrada inmutable de R2-C2. No se corrige in situ: un
acto posterior deberá copiar exactamente sus bytes a una ubicación nueva,
comprobar el manifiesto externo completo y detenerse ante cualquier diferencia.
El `SHA256SUMS` interno obsoleto es un defecto conocido de la candidata, no una
fuente válida para reconstruir o adaptar bytes.

El alcance corrector queda cerrado así:

1. **F1:** antes de reutilizar una recaptura de rollback, validar su conjunto
   completo de archivos, manifiesto y cierre; una captura incompleta se preserva
   y fuerza un intento nuevo. Ejecutar cortes reales después de `result.json`,
   antes de `drift-comparison.json` o `SHA256SUMS` y antes del evento terminal.
2. **F3.a:** corregir el quoting del CEL y preservar el código de fallo durante
   la limpieza, incluido Bash 3.2, sin falsos códigos `0`.
3. **F3.b:** construir una fixture bootstrap completa y coherente antes de
   invocar `compare`, incluido `drift-comparison.json`, y sellarla solo después
   de finalizar todos sus archivos.
4. **F3.c:** probar una recuperación realmente interrumpida; no vale provocar
   primero un rollback automático ya terminado y llamar después al modo manual.
5. **F3.d:** ejercitar directamente las funciones pertinentes bajo `if`, `!` y
   listas condicionales, de modo que la inhibición interna de `errexit` sea el
   comportamiento probado y no el de otro proceso Bash.

Solo pueden tocarse, cuando sea efecto directo de esos puntos, los archivos
técnicos ya enumerados en la sección anterior y el `SHA256SUMS` raíz. Este debe
regenerarse sobre los bytes finales con cobertura exacta. F2, F4 y F5 permanecen
cerrados y son regresiones obligatorias: `result.json` sigue entre las 39
superficies sin exclusiones nuevas; ninguna respuesta administrativa cruda
llega a disco; y cualquier fallo al consultar impersonación detiene el flujo.
`authorized-preimage/**` permanece inmutable.

La evidencia exigida comprende sintaxis Bash, ShellCheck, AST Python y la
batería local completa, todos ejecutados con código de salida significativo.
Después solo cabe la segunda y última revalidación enfocada de la misma Astra.
Si no emite `APTO`, se preserva la candidata y se para para replantear; no
existe R2-C3.

## Coste y gates anteriores al autor

- Subpresupuesto incremental de R2: `5.00 EUR`, dentro del techo invariable de
  `100.00 EUR` de WP-018.
- Coste histórico preservado: `3.0626293149... EUR`; ambos expedientes no
  podrán superar juntos `8.0626293149... EUR`.
- Tipo mensual vigente: `1.1298 USD/EUR`, referencia BCE del 2026-10-01.
- La única invocación R2-C1 dispone de F1 defendible en `cost-f1.json` y
  `cost.md`: `4.1209296 USD / 3.6474859267... EUR`, redondeado a `3.65 EUR`.
  Quedan `1.3525140733... EUR` del subpresupuesto R2.
- Toda invocación correctora requiere F1 desde el lanzamiento con
  `claude -p --output-format json`, `WP-018` explícito, versión exacta
  previamente comprobada y sin `--continue` o `--resume`.
- Antes del autor deben verificarse rama remota, commit de apertura, identidad
  de candidata y preimagen, ausencia de deriva, autenticación headless, tipo
  mensual y presupuesto restante. La falta de cualquiera obliga a parar.

La misma revisora independiente realizó la primera revalidación enfocada y
mantuvo la candidata `NO APTO`. Solo queda una eventual revalidación enfocada
después de R2-C2. No existe R2-C3.

## Resultado de R2-C1

El gate saneado previo al autor terminó `APTO` el 2026-10-15: 38 superficies,
cero deriva, ningún crudo persistido y SHA-256 de su `SHA256SUMS`
`b5a09113c1ecc25d23330bc5bfc04b6057f1201bd8147fad8c259be3f75ef747`.
Confirmó la base y workflow congelados, contención externa y rama R2 publicada.

La única invocación correctora comenzó el `2026-10-15T16:49:48Z` y terminó el
`2026-10-15T17:19:16Z` con código `0`. Claude Code `2.1.272` registró
`is_error:false`, 64 turnos, nueve denegaciones Bash, cero subagentes, cero
solicitudes web y coste `4.1209296 USD / 3.6474859267... EUR`. El crudo externo
es `/private/tmp/wp018-author-r2-c1-raw.json`, con SHA-256
`d7e389d6f6373bb4e6fc68a1ceec59b8d79515efaaf163cae0a4677a51a2426e`.

La postimagen está preservada en
`/private/tmp/wp018-dor7-provider-sha-r2-c1-author`. Modificó exactamente 11
archivos permitidos y mantuvo `authorized-preimage/**` byte a byte. Su
manifiesto externo completo contiene 55 entradas y tiene SHA-256
`133aa34695c7329552c2a7427540eed8dfbf2d1f0cf63cf0163dba9fd1c47fa3`.
El `SHA256SUMS` interno no se regeneró y sus 11 entradas modificadas fallan.

El autor no pudo ejecutar pruebas por las denegaciones de su entorno. La
verificación independiente posterior obtuvo sintaxis Bash y AST Python
correctos, pero ShellCheck falló y la batería abortó antes del bootstrap con
`from: unbound variable`. En Bash 3.2 la misma salida fallida llegó a devolver
`0` por una regresión de limpieza; ningún resultado acredita pruebas superadas.

La primera revalidación enfocada de la misma Astra emitió `NO APTO — NO
EJECUTAR`. El estado queda:

| Hallazgo | Estado tras R2-C1 |
|---|---|
| `WP018-PSHA-R2-F1` | Abierto: la captura reutilizada no se valida como completa y faltan cortes ejecutados |
| `WP018-PSHA-R2-F2` | Cerrado: `result.json` participa en las 39 superficies sin exclusiones nuevas |
| `WP018-PSHA-R2-F3` | Abierto: batería rota, bootstrap incoherente, caso F1 incorrecto e inhibición interna de `errexit` sin probar |
| `WP018-PSHA-R2-F4` | Cerrado: respuestas sensibles proyectadas y saneadas en streaming |
| `WP018-PSHA-R2-F5` | Cerrado: el fallo al consultar impersonación se propaga y detiene |

R2-C2 queda abierto pero no consumido: tiene cero invocaciones correctoras y no
ha modificado la candidata. Una eventual invocación del autor exige otro acto
humano, gates previos completos y un límite que no pueda superar los
`1.3525140733... EUR` restantes. Si no puede acreditarse cualquiera de esas
condiciones, corresponde parar sin consumir el ciclo.

## Autorizaciones separadas

Esta composición autoriza únicamente publicar la fila de apertura de R2-C2. No
autoriza invocar al autor, modificar o ejecutar la candidata, ejecutar pruebas
con servicios reales, materializarla, actualizar o recuperar el provider,
habilitar WIF, crear roles o bindings, despachar el workflow, abrir o ejecutar
C0, fusionar o descartar ninguna rama. Cada acto requiere su propia
autorización humana conforme a `DEC-010` §18.5.
