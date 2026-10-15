# WP-018 — Revisión Astra de origen de la actualización del provider

## Identidad y procedencia

- Fecha del dictamen: 2026-10-12.
- Instrumento: GPT-6 Astra, razonamiento Alto, rol `code-reviewer`, contexto
  nuevo y revisión estrictamente de solo lectura.
- Base revisada: `origin/main`
  `6821c0a83efd547b7617a1fed9c168e33224889c`.
- Candidata: `/private/tmp/wp018-dor7-provider-sha-candidate`.
- Digest agregado de la candidata:
  `ad5e237ed687bab12b442d7cb1505b1209f262c6aa8281d6e9f072e471b59591`.
- Preimagen autorizada:
  `/private/tmp/wp018-dor7-provider-sha-preflight-20261012-v4`.
- SHA-256 del `SHA256SUMS` de la preimagen:
  `65f51dd297d6f5e625792856a0529b3b803117db0be50fd0c39e6c2b9a274136`.
- Sesión de revisión recuperada:
  `01a131e0-ed58-7d13-873e-76233f3b6fb0`.
- SHA-256 de la salida final original extraída con LF terminal:
  `14dea04c4d31aef918331322a7ba9d1f9879058566d69860f961a98b212f332b`.

Identidad byte a byte de la candidata revisada:

| Ruta | SHA-256 |
|---|---|
| `00-common.sh` | `b0c5fe4e79934f2059d0c3df231af0bd898094acc69d7d933e4f2fe4d66ec0f1` |
| `00-run-bounded.sh` | `c386ee34473a3c22d84e7a9fe72e7cf45a5d629f17c84d3d3c7f471631cf014b` |
| `01-read-only-preflight.sh` | `4b3baa71c3d3db6bd21e83bc723c1ee9c713c9de4535aab7bd5fc21b5b396fc6` |
| `02-update-provider-sha.sh` | `77d6355c3cc137552945ca7cee2358c5d6a45e6867d1054498a824bc8d4f55d3` |
| `03-rollback-provider-sha.sh` | `3c54975aee02cdb9b18e84d29525cca2c2a86e754fc7651404bb538600ea6622` |
| `MANIFEST.md` | `cf0cc90abd8586576fcf48de67d0e4af4b4065557a767979dd45ffaff4bb92e2` |
| `tests/fixtures/gcloud` | `09a7ed78aba3b9df2a479c5f23f7ddda84f767108b61ec3fbb1acc0c07ba09bc` |
| `tests/run-local-tests.sh` | `7802e592601d889a8b03581a11bffddcc2f1612d102a4d6b67b52d4d934b6262` |

La transcripción siguiente conserva completo el contenido de la salida final
original. Sus identificadores `WP018-DOR7-SHA-F1` a `F5` corresponden a los
alias normativos `WP018-PSHA-F1` a `F5` de DEC-010 §17. Los enlaces absolutos
documentan las ubicaciones históricas revisadas; no conceden autoridad a esos
bytes ni sustituyen sus hashes.

## Dictamen completo original

VEREDICTO: CAMBIOS SOLICITADOS
Dictamen de la candidata: **NO APTO**.

Revisión inicial independiente y de solo lectura contra `origin/main=6821c0a83efd547b7617a1fed9c168e33224889c`. No he corregido archivos ni ejecutado mutaciones externas.

[BLOQUEANTE] WP018-DOR7-SHA-F1 — El rollback manual no puede recuperar una actualización fallida
Archivo: [03-rollback-provider-sha.sh:20](/private/tmp/wp018-dor7-provider-sha-candidate/03-rollback-provider-sha.sh:20)
Problema: exige `SHA256SUMS` y `result.json` con `APTO` de una ejecución exitosa. Sin embargo, [02-update-provider-sha.sh:58](/private/tmp/wp018-dor7-provider-sha-candidate/02-update-provider-sha.sh:58) remite precisamente a este rollback cuando falla la recuperación automática. Los archivos exigidos solo se generan al final del camino exitoso, en las líneas 100–101.
Escenario: la actualización se aplica, falla la lectura posterior y el rollback automático falla por una indisponibilidad temporal. El directorio conserva la preimagen y el journal, pero no `result.json` ni `SHA256SUMS` raíz. Al recuperarse el servicio, el rollback manual termina con código 66 antes de actuar.
Arreglo sugerido: custodiar la preimagen y el inicio antes de mutar; permitir recuperación de una ejecución fallida identificada y autorizada, verificando su custodia y el estado vivo, sin exigir un resultado exitoso inexistente.

[BLOQUEANTE] WP018-DOR7-SHA-F2 — La preimagen autorizada no funciona como barrera contra deriva
Archivo: [02-update-provider-sha.sh:30](/private/tmp/wp018-dor7-provider-sha-candidate/02-update-provider-sha.sh:30)
Problema: se autentica la captura autorizada y se obtiene otra fresca, pero nunca se comparan. Los oráculos parciales permiten cambios materiales y después declaran `environment_drift:false`. Incumple DEC-010 §16.3.1–2.
Escenario: después de la captura autorizada aparece en la política del proyecto un binding `roles/editor` para `alcance-fda-wp018-push@fda-template.iam.gserviceaccount.com`. Reproduje en memoria esa modificación sobre la captura: el filtro de [00-common.sh:121](/private/tmp/wp018-dor7-provider-sha-candidate/00-common.sh:121) devuelve `true`. La ejecución continúa hasta la mutación aunque el entorno haya cambiado. También hay campos de las suscripciones que el filtro de preflight no compara.
Arreglo sugerido: comparar la captura fresca contra la autorizada antes de mutar, con una lista explícita y mínima de campos volátiles excluidos. Cualquier diferencia restante debe detener el acto. Mantener también los oráculos semánticos.

[IMPORTANTE] WP018-DOR7-SHA-F3 — La verificación del rollback no demuestra restauración exacta
Archivo: [02-update-provider-sha.sh:50](/private/tmp/wp018-dor7-provider-sha-candidate/02-update-provider-sha.sh:50)
Problema: tanto el rollback automático como el manual solo llaman a `assert_provider_json`; no comparan el provider completo restaurado con la preimagen. Ese oráculo omite campos admitidos por la API, entre ellos `oidc.jwksJson`.
Escenario: entre preimagen y postimagen aparece un `oidc.jwksJson`. La comparación completa de la actualización detecta el cambio y activa rollback; restaurar exclusivamente `attributeCondition` deja ese campo intacto, pero el oráculo acepta el resultado y se anuncia «restored the exact provider preimage». Comprobé en memoria que añadir `oidc.jwksJson` conserva código 0 en `assert_provider_json`. Es un campo real del [recurso OIDC oficial](https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.locations.workloadIdentityPools.providers#Oidc).
Arreglo sugerido: comparar también la postimagen de ambos rollbacks con la preimagen completa, excluyendo únicamente metadatos justificados. Si persiste cualquier diferencia, declarar recuperación incompleta y parar; no ampliar automáticamente la mutación autorizada.

[IMPORTANTE] WP018-DOR7-SHA-F4 — No hay pruebas de los caminos principales ni de recuperación
Archivo: [tests/run-local-tests.sh:58](/private/tmp/wp018-dor7-provider-sha-candidate/tests/run-local-tests.sh:58)
Problema: actualización y rollback solo se prueban con confirmaciones incorrectas y búsquedas de texto. No se ejecutan con dobles sus caminos exitosos, fallos posteriores a la mutación, rollback automático, recuperación manual o comparación de preimágenes. Tampoco hay pruebas directas de los oráculos nuevos de provider, IAM y custodia.
Escenario: sustituir el cuerpo de `rollback_on_failure` por una operación vacía conservaría las comprobaciones actuales; F1–F3 no son detectables por esta batería.
Arreglo sugerido: incorporar pruebas sin red mediante dobles cerrados de `gcloud` y `gh`, con fallos inyectados y comprobación de llamadas, estados y códigos. Cubrir las guardas de identidad y todos los bytes rechazados de `core.project`, incluidos espacios, varias líneas, ausencia de LF y salida no cero.

[MENOR] WP018-DOR7-SHA-F5 — Faltan flags de proyecto exigidos por el contrato
Archivo: [00-common.sh:137](/private/tmp/wp018-dor7-provider-sha-candidate/00-common.sh:137)
Problema: `service-accounts keys list`, `projects get-iam-policy` y las lecturas `projects describe` y `billing projects describe` no llevan `--project=fda-template`, exigido para todas las llamadas de recursos por DEC-010 §16.3.6.
Escenario: con `core.project` sin configurar, estas invocaciones salen sin el flag contractual, aunque sus argumentos identifican recursos del proyecto correcto. No he demostrado una selección errónea de recurso; por ello no lo considero bloqueante.
Arreglo sugerido: añadir el flag explícito y comprobarlo en los dobles de todas las llamadas de recursos.

Comprobaciones satisfactorias: los 37 archivos de la preimagen verifican contra `SHA256SUMS`, cuyo hash coincide con `65f51dd297d6f5e625792856a0529b3b803117db0be50fd0c39e6c2b9a274136`; el workflow canónico conserva el hash exigido; el commit normativo toca exactamente los cuatro archivos autorizados. Sintaxis y ShellCheck pasan; el supervisor devuelve 0 y 124 en éxito y timeout. La guarda de `core.project` compara bytes antes de normalizar. Las mutaciones previstas conservan `--disabled`; no encontré enable, dispatch, creación de bindings ni intercambio STS. La secuencia documental separa correctamente preparación, revisión, materialización y ejecución.

Limitación: no pude refrescar personalmente el estado externo. `gh` carece de conexión desde el sandbox y `gcloud`, localizado mediante su ruta absoluta, no puede abrir su almacenamiento de credenciales bajo estas restricciones. He verificado las capturas entregadas y sus hashes, no afirmo una observación viva independiente. Tampoco ejecuté la batería completa, porque crea archivos temporales; revisé su código y ejecuté únicamente comprobaciones que no modifican archivos.

**Parada antes de C1:** DEC-010 §16.3 exige apertura versionada y autorizada antes de corregir. No consta aquí esa ruta; `/private/tmp` no la sustituye. Este dictamen solo informa los hallazgos y no autoriza corrección, materialización ni ejecución.

## Estado de custodia

Este archivo preserva el dictamen de origen; no constituye una revisión nueva,
no cambia su `NO APTO` y no consume C1. La limitación de observación viva queda
cerrada únicamente para la apertura por la preimagen postfusión separada de
2026-10-15; no altera retrospectivamente el alcance del dictamen original.

## Revalidación enfocada de C1

- Fecha: 2026-10-15.
- Revisora: la misma instancia independiente GPT-6 Astra, razonamiento Alto,
  rol `code-reviewer`, `/root/wp018_provider_sha_review`.
- Alcance: únicamente el resultado de C1, la identidad de los ocho archivos y
  el estado de `WP018-PSHA-F1` a `WP018-PSHA-F5`.
- Modo: solo lectura; no modificó archivos ni ejecutó red o infraestructura.
- SHA-256 de la transcripción externa con LF terminal:
  `e2f82b2cf7869b2a5df07122ea23768e774a339186c3afac690cdb6061f4d052`.

### Dictamen enfocado completo

VEREDICTO: CAMBIOS SOLICITADOS

**Revalidación enfocada C1: NO APTO, sin cambios.**

La revisora comprobó que los ocho archivos de C1 conservan los hashes
históricos y que `diff -qr` no encuentra diferencias con la candidata
revisada. Permanecen abiertos, sin cambios de severidad:

| Hallazgo | Severidad | Estado |
|---|---|---|
| `WP018-PSHA-F1` — recuperación manual tras fallo | Bloqueante | Abierto |
| `WP018-PSHA-F2` — comparación con preimagen autorizada | Bloqueante | Abierto |
| `WP018-PSHA-F3` — restauración completa del provider | Importante | Abierto |
| `WP018-PSHA-F4` — pruebas de ejecución y recuperación | Importante | Abierto |
| `WP018-PSHA-F5` — proyecto explícito en llamadas | Menor | Abierto |

El JSON de la invocación verifica exactamente el SHA-256
`74f2c6cd8f1f79ba91980c3c311a56d49230729b815b877ec303c4516f51896e`.
Confirma `is_error: true`, fallo de renovación OAuth, `duration_api_ms: 0`,
todos los contadores de tokens a cero, `modelUsage: {}`,
`permission_denials: []` y `total_cost_usd: 0`. Las capturas registran inicio
`10:05:29Z`, fin `10:05:32Z` y salida `1`. El campo `subtype: "success"` no
convierte esta ejecución en exitosa frente al error explícito y su código de
salida.

El cero es una cifra F1 defendible para esta invocación: procede del resultado
estructurado y concuerda con el fallo anterior a la llamada de inferencia.
Corresponde a `0 USD / 0 EUR`, no a un cero de relleno ni a cero invocaciones.
Su registro como coste medido requiere el extracto saneado y la custodia
prescritos; la revisión no los escribió.

Según DEC-010 §17.3, C1 está consumido desde el lanzamiento, aunque no haya
producido cambios. El resultado correcto para actualizar su misma fila es: una
invocación, autor invocado, fallo de autenticación, sin cambios, dictamen `NO
APTO` y cinco hallazgos abiertos. La fila versionada leída por la revisora aún
conservaba `abierto / 0 / no`; corresponde actualizarla con este resultado,
sin crear otro C1.

Esta revalidación no abre C2 ni autoriza reintentar como C1. Una siguiente
invocación correctora correspondería a C2 y requiere su apertura versionada y
autorización separada. La revisora no modificó archivos ni ejecutó red o
infraestructura.

## Revalidación enfocada final de C2

- Fecha: 2026-10-15.
- Revisora: la misma instancia independiente GPT-6 Astra, razonamiento Alto,
  rol `code-reviewer`, `/root/wp018_provider_sha_review`.
- Alcance: resultado de C2 y estado final de `WP018-PSHA-F1` a
  `WP018-PSHA-F5`.
- Modo: solo lectura; no modificó archivos ni ejecutó red o infraestructura.
- Base exclusiva: `origin/main`
  `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e`.
- Candidata: `/private/tmp/wp018-dor7-provider-sha-c2-author`.
- Digest agregado de la candidata:
  `1625f0666d24c65732bd71d45d92120f4f6c95f2fc861c555f2a9a58aebe91da`.
- SHA-256 de la transcripción externa normalizada con LF terminal:
  `c200e2a4d61ab408ffe9aa25e7385f284c2d5ee94dbfe975097fc86d31278efa`.

Identidad byte a byte de la candidata C2 revisada:

| Ruta | SHA-256 |
|---|---|
| `00-common.sh` | `a7cd645e19abfb133c324064750e063a6da744913cb5b0e98a41945b2d7ae675` |
| `00-run-bounded.sh` | `c386ee34473a3c22d84e7a9fe72e7cf45a5d629f17c84d3d3c7f471631cf014b` |
| `01-read-only-preflight.sh` | `92aa04778972a3dff6aab61bf80f4f18d85c49a6733edb908f260021d985ac98` |
| `02-update-provider-sha.sh` | `f0550dcf4c912769732cf8264ba09e74977fbb48d1e6a60b4c6ba7d4971f8664` |
| `03-rollback-provider-sha.sh` | `c47c140230455c90aa2a6f79612f7db87d73f9a77b7894abf2b68371e0b2fe7d` |
| `MANIFEST.md` | `918f0aac199f033a01a913bb84cd7a156503e11c00c0374ae1e31480fa3fed46` |
| `tests/fixtures/gcloud` | `3b4af729434006816ea297e4fdc1582a5fdb39a9aa9ffdd0eb485c26b2d3007c` |
| `tests/run-local-tests.sh` | `15cab3c1c22f1ade3a843c6031b6f74bca5646792f887893efc94c0f979f55b8` |

### Dictamen enfocado completo

VEREDICTO: RECHAZA

**C2: NO APTO. Ciclos correctores agotados; no existe C3.**

| Hallazgo | Estado final | Evidencia |
|---|---|---|
| `WP018-PSHA-F1` | **Abierto — bloqueante** | La recuperación acepta ejecuciones fallidas, pero una interrupción después de ampliar el journal invalida su custodia. |
| `WP018-PSHA-F2` | **Abierto — bloqueante** | La comparación omite políticas y fixtures; además mantiene la base y preimagen históricas. |
| `WP018-PSHA-F3` | **Cerrado en el diff** | Ambos rollbacks comparan el provider completo, excluyendo únicamente `etag` y `updateTime`. La falta de ejecución integral permanece en F4. |
| `WP018-PSHA-F4` | **Abierto — importante** | La batería falla y no cubre los caminos completos de actualización y rollback automático. |
| `WP018-PSHA-F5` | **Cerrado** | Las cuatro llamadas señaladas incorporan `--project="$PROJECT_ID"`. |

**WP018-PSHA-F1.** `mutation/SHA256SUMS` se genera antes de mutar, pero
después se añade una entrada al `journal.jsonl` sin actualizar ese sello. La
recuperación manual exige verificarlo. Si la actualización y las
comprobaciones terminan, se añade `state:"verified"` y el proceso recibe
`SIGKILL` antes de crear la custodia raíz, el provider conserva la condición
nueva, no existe una ejecución completada y la recuperación manual rechaza el
journal por hash incorrecto. El problema original de recuperación tras
interrupción no queda resuelto.

**WP018-PSHA-F2.** Se comparan únicamente `result.json`,
`gcp/provider.json` y `gcp/pool.json`. Se omiten las políticas IAM,
suscripciones, topic y logging que sustentan la autorización. Añadir
`roles/editor` a la cuenta push en la política del proyecto sigue pasando el
oráculo original porque esa política no participa en la comparación.

Además, `NEW_MAIN_SHA` sigue siendo
`6821c0a83efd547b7617a1fed9c168e33224889c`; el objetivo exclusivo autorizado
es `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e`. También permanecen el hash de
la preimagen histórica y su descripción en el manifiesto. Con `main` en la
cabeza congelada correcta, el preflight rechaza su SHA; la condición nueva
preparada tampoco corresponde a esa cabeza.

**WP018-PSHA-F4.** El caso negativo invoca la comparación dentro de `if`,
donde Bash inhibe `errexit`. Un primer `cmp` fallido queda seguido por
comparaciones exitosas y la función devuelve `0`. El test termina entonces
con error; las pruebas posteriores de restauración y recuperación no llegan a
ejecutarse. El escenario observado cambia `result.main` de `"m"` a
`"DIFFERENT"` mientras provider y pool coinciden. Este defecto del retorno
bajo `if` no demuestra que la llamada directa de `02`, con `set -e`, acepte
ese mismo caso.

`MANIFEST.md` declara que faltan las pruebas completas de actualización
exitosa, fallo posterior a la mutación y rollback automático. El hash fijo no
constituye una imposibilidad: los bytes del workflow ya disponibles en el
commit local congelado producen exactamente el hash exigido.

Las comprobaciones independientes de sintaxis y ShellCheck pasan. La
comparación completa rechaza una diferencia en `oidc.jwksJson`. La batería
completa `tests/run-local-tests.sh` terminó con código `1`; la revisora no la
repitió porque crea archivos temporales y su revisión era estrictamente de
solo lectura.

El crudo C2 coincide con SHA-256
`655a53eaaeba62bd9cadc1399cb2279b87eb589227df9909ae75c7e76f3462dc`:
salida del autor `0`, coste `3.4601586 USD = 3.0626293149 EUR`. El éxito de la
invocación no acredita la corrección de la candidata.

**Disposición: parada segura.** C1 y C2 están consumidos. Se preservan la
candidata, hashes y evidencias, y se registra C2 como `NO APTO`, con F1, F2 y
F4 abiertos. No procede corregir ni reejecutar esta candidata. La causa de no
convergencia es la rederivación incompleta de base/preimagen y la ausencia de
validación integral del flujo de recuperación. Corresponde devolver la
transición a decisión humana y replanificación, manteniendo la contención
externa y sin habilitar WIF, despachar workflows ni ejecutar el provider.
