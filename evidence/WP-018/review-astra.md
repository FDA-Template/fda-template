# WP-018 — Revisión Astra de origen de `WP018-DOR7-PSHA-R2`

## Identidad y procedencia

- Fecha del dictamen: 2026-10-15.
- Instrumento: GPT-6 Astra, razonamiento Alto, rol `code-reviewer`, contexto
  nuevo y revisión estrictamente de solo lectura.
- Instancia revisora: `/root/review_r2_candidate`.
- Base revisada: `origin/main`
  `9cdfaefddfdb50fa1fba385e265243022b67061f`.
- Workflow SHA-256:
  `7ea50ded863cf57f2cac6916dada3dece9305bb6af60266601ca79ffa76b1594`.
- Candidata: `/private/tmp/wp018-dor7-provider-sha-r2-candidate.lxugrv`.
- SHA-256 del `SHA256SUMS` raíz, con 54 entradas verificadas:
  `bfa60e607b707a62f19e16bfce7035749608f7ff336bf3cc45d7027a8f5db891`.
- Preimagen autorizada:
  `/private/tmp/wp018-dor7-psha-r2-preimage-20261015.Hig7rf`.
- SHA-256 del `SHA256SUMS` de la preimagen, con 40 entradas verificadas:
  `5a03258545e2bb0b4761d343a1d3b3cbd444b61adc1dbce4e1d1da4afac4230c`.
- SHA-256 de la salida final externa normalizada con LF terminal:
  `9743d1e16cced76e0c2b0711b5ff7e890ac7c0ec9162953b57e2ea183c00177c`.

Identidad de los archivos técnicos directos de la candidata revisada:

| Ruta | SHA-256 |
|---|---|
| `00-common.sh` | `08cec9261f69b8ccb51faf2bcf26adcfb309e75ba71ae0bf7183e18051c29784` |
| `00-constants.sh` | `dc8a201d8465016d54d9a486068d50fbc07ec7601245b84f8e3b39006b466bc4` |
| `01-capture-live.sh` | `54c6c922bb24b35afc9c8dc9f8683400dac2eb27dca895a688e743aadaa1af01` |
| `02-update-provider.sh` | `d747033aac084f0f3f011c2202df456a274f0d68f84cbc6c7c5cdb47a5396cbf` |
| `03-rollback-provider.sh` | `c865075807b42fa76ffce0d93b058195786baa7b3ec2d0c687aef57c7115858c` |
| `lib/r2.py` | `8e9c53e6bfc52fcc223a58adb818cd12f3c5ea36ae833a568ea34ce2320cff8f` |
| `lib/sanitize_policy.py` | `e015a29be1d20f0d0816ffeba1140851f19ee5b3668185775b7941394a489eb9` |
| `tests/fake-capture.sh` | `670b0ad23fcea330ee8d74ff72955cf542d38e5cbcfdfc6bc92fee10e94017a5` |
| `tests/fake-gcloud.py` | `218f77ddbba4d496864fcaa184eef3beb9b7e6f1ba2892d11a1a2e3556042f2b` |
| `tests/fake-gh.sh` | `bf60dbd00554eae2d7f2b5d207b2c1c572a2a2c744eff6ad3454e2eb36a31339` |
| `tests/run-local-tests.sh` | `f56632bc2fce7b0306f4352123dd7903614e850840ccc85b892433fcb088b666` |
| `README.md` | `64521eca0f731004471ffa7eeb59e46789feb0a5eb67e0e45a6f5b30eaff9a51` |
| `LOCAL-VERIFICATION.md` | `966c06d6b9fb0e39078a59d56a4265bdd8007a0ec6c511783baed61d20bd8144` |
| `authorized-preimage/SHA256SUMS` | `5a03258545e2bb0b4761d343a1d3b3cbd444b61adc1dbce4e1d1da4afac4230c` |

El `SHA256SUMS` raíz autentica además cada archivo saneado de la preimagen. La
revisora comprobó su cobertura exacta y no encontró dependencia ejecutable de
la candidata C2.

## Dictamen completo original

VEREDICTO: CAMBIOS SOLICITADOS

DICTAMEN: **NO APTO — NO EJECUTAR**

Candidata revisada:
`/private/tmp/wp018-dor7-provider-sha-r2-candidate.lxugrv`.

`SHA256SUMS` fue verificado íntegramente y con cobertura exacta de archivos. El
digest del manifiesto revisado es
`bfa60e607b707a62f19e16bfce7035749608f7ff336bf3cc45d7027a8f5db891`.
También se verificó el manifiesto de preimagen
`5a03258545e2bb0b4761d343a1d3b3cbd444b61adc1dbce4e1d1da4afac4230c`.

### WP018-PSHA-R2-F1 — Bloqueante

**El rollback no puede reanudarse después de un corte durante su recaptura.**

Archivo: `03-rollback-provider.sh:60`; relacionado:
`01-capture-live.sh:18`.

Todos los intentos de recuperación utilizan el mismo directorio
`RUN/rollback-preimage`, pero el capturador rechaza cualquier salida existente.
No existe recuperación de una captura incompleta ni reutilización verificada de
una completa.

Tras restaurar el provider, el rollback puede iniciar su recaptura y recibir
`SIGKILL` después de crear `rollback-preimage`, o después de terminar la
captura pero antes de registrar `rolled-back`. La custodia conserva
`rollback-intent`. Cada nuevo `--manual` llega a la misma captura, encuentra el
directorio existente y termina con código 65. La recuperación queda
permanentemente sin finalizar mediante el procedimiento entregado.

Arreglo sugerido: registrar intentos de recuperación separados y recuperables;
reutilizar únicamente capturas completas y verificadas, o crear una nueva
captura sin sobrescribir la anterior. Probar cortes dentro de la captura de
recuperación y antes de su evento terminal.

### WP018-PSHA-R2-F2 — Importante

**La comparación omite el resultado de captura y acepta diferencias no
autorizadas.**

Archivo: `lib/r2.py:25`; relacionados: `lib/r2.py:150`,
`01-capture-live.sh:138`.

`result.json` está fuera de las 38 superficies comparadas. `validate_capture`
verifica algunos campos, pero no compara su contenido completo. `DEC-010`
§18.4 exige cubrir el resultado de captura y limitar las exclusiones volátiles.

La preimagen autorizada contiene `gcp.core_project: "UNSET"` y
`comparison.stable_surfaces: 34`. La recaptura elimina el primer campo y escribe
`38` en el segundo; puede producir `APTO` sin detectar estas diferencias, que
no son `observed_at`, `etag` ni `updateTime`. Otros campos del resultado tampoco
quedan contrastados.

Arreglo sugerido: incluir el resultado en la comparación contractual,
conservando sus campos y separando explícitamente los informes derivados. Si
debe cambiar su esquema o semántica, resolverlo en el contrato antes de aceptar
nuevas exclusiones.

### WP018-PSHA-R2-F3 — Importante

**La batería no verifica el capturador de producción ni la inhibición real de
`errexit`.**

Archivo: `tests/run-local-tests.sh:23`; relacionados:
`tests/run-local-tests.sh:75`, `tests/run-local-tests.sh:112`.

Las pruebas reemplazan íntegramente `01-capture-live.sh` por un doble que copia
la preimagen. No ejercitan sus llamadas, proyecciones, guardas ni
`sanitize_policy.py`. Tampoco cortan el rollback. El `if "$UPDATE" …` ejecuta
otro proceso Bash; no demuestra el comportamiento de funciones ejecutadas en
un contexto que inhiba su propio `errexit`.

Introducir una omisión en la proyección IAM o romper una guarda del capturador
real deja intactos todos los caminos ejecutados por esta batería. Asimismo, el
corte descrito en F1 no está entre sus siete puntos.

Arreglo sugerido: ejecutar el capturador original con dobles de sus dependencias
externas; cubrir sanitización, errores de autenticación, resultados incompletos
y recuperación interrumpida. Añadir pruebas directas de las funciones
pertinentes bajo `if`, `!` y listas condicionales. Ajustar las afirmaciones de
`LOCAL-VERIFICATION.md` a la evidencia obtenida.

### WP018-PSHA-R2-F4 — Importante

**Las respuestas administrativas crudas persisten identidades y sobreviven a
`SIGKILL`.**

Archivo: `01-capture-live.sh:25`; relacionados: `01-capture-live.sh:35`,
`01-capture-live.sh:66`, `01-capture-live.sh:94`.

El saneamiento ocurre después de escribir respuestas completas en `OUT/.raw`.
La eliminación depende de un trap `EXIT`, que no se ejecuta ante `SIGKILL`.

Un corte después de capturar `project-iam-policy.json` y antes de `cleanup`
conserva los miembros IAM originales en disco. Las respuestas crudas de commits
y del entorno también pueden conservar identidades personales que sus
proyecciones finales eliminan. Los permisos restrictivos del directorio no
equivalen a ausencia de esas identidades en la evidencia local.

Arreglo sugerido: sanear por streaming antes de cualquier persistencia y
conservar exclusivamente las representaciones permitidas. Probar que los cortes
no dejan respuestas crudas en los directorios del expediente.

### WP018-PSHA-R2-F5 — Importante

**Un error al comprobar impersonación se interpreta como ausencia de
impersonación.**

Archivo: `00-common.sh:26`.

`config get-value auth/impersonate_service_account … || true` convierte
cualquier fallo de la consulta en un resultado aceptable si `stdout` queda
vacío.

Si existe impersonación configurada y el subproceso que consulta esa propiedad
termina por señal antes de producir `stdout`, la guarda acepta la cadena vacía.
Las comprobaciones posteriores pueden encontrar la cuenta activa esperada y
continuar. No se ha acreditado entonces la ausencia de impersonación antes de
la mutación.

Arreglo sugerido: distinguir una consulta exitosa con valor vacío o `(unset)`
de una consulta fallida; ante esta última devolver error. Añadir un doble que
falle únicamente esa consulta y comprobar que no se alcanza ninguna mutación.

## Comprobaciones satisfactorias y límites

La batería autorizada terminó con código 0; también pasaron sintaxis Bash,
ShellCheck y análisis sintáctico Python. Por inspección, los anclajes coinciden
con la base y workflow indicados, las operaciones de recursos incluyen
`--project`, el cambio del provider se limita a la condición y los eventos
posteriores no alteran el árbol sellado. No se observaron dependencias
ejecutables de C2 ni un bypass activable mediante variables de entorno en
producción. La procedencia histórica de la autoría no puede demostrarse solo
con estos bytes.

La revisora no modificó la candidata o el repositorio, no consultó servicios
externos y no abrió ramas o ciclos. Los cinco hallazgos permanecen abiertos.

## Estado de custodia del dictamen de origen

El bloque anterior preserva el dictamen completo de origen de R2. La sección
siguiente registra la primera revalidación enfocada después de consumir R2-C1.
Ni el dictamen de origen ni su revalidación autorizan materialización técnica o
ejecución del provider.

## Revalidación enfocada de R2-C1 — 1/2

### Identidad y ejecución

- Fecha: 2026-10-15.
- Revisora: la misma instancia independiente GPT-6 Astra, razonamiento Alto,
  rol `code-reviewer`, `/root/review_r2_candidate`.
- Modo: solo lectura; no modificó archivos ni consultó servicios externos.
- Postimagen: `/private/tmp/wp018-dor7-provider-sha-r2-c1-author`.
- Manifiesto externo completo: 55 entradas; SHA-256
  `133aa34695c7329552c2a7427540eed8dfbf2d1f0cf63cf0163dba9fd1c47fa3`.
- `authorized-preimage/**`: idéntica a la candidata de origen.
- Salida final de la revisora, normalizada con LF terminal: SHA-256
  `51d0cd2ac776ab88c53eee4df6086ada6ce366ddea82dc32d8b99f6464c846ef`.
- Invocación del autor: código `0`, `is_error:false`, 64 turnos, nueve
  denegaciones Bash, cero subagentes y cero solicitudes web.
- Crudo externo del autor:
  `/private/tmp/wp018-author-r2-c1-raw.json`; SHA-256
  `d7e389d6f6373bb4e6fc68a1ceec59b8d79515efaaf163cae0a4677a51a2426e`.
- Coste: `4.1209296 USD / 3.6474859267... EUR`, redondeado a `3.65 EUR`.

El diff modifica exactamente estos 11 archivos permitidos:

- `00-common.sh`, `01-capture-live.sh`, `03-rollback-provider.sh`;
- `lib/r2.py`, `lib/sanitize_policy.py`;
- `tests/fake-capture.sh`, `tests/fake-gcloud.py`, `tests/fake-gh.sh`,
  `tests/run-local-tests.sh`;
- `README.md`, `LOCAL-VERIFICATION.md`.

El `SHA256SUMS` interno no fue regenerado: fallan las 11 entradas modificadas.
La verificación independiente obtuvo `bash -n=0` y AST Python `0`, pero
ShellCheck `1`. La batería abortó antes del bootstrap con `from: unbound
variable`; en otro runtime Bash el trap de limpieza llegó a ocultar el fallo y
devolver `0`. Ninguno de esos resultados acredita la batería.

### Dictamen enfocado completo

VEREDICTO: CAMBIOS SOLICITADOS

DICTAMEN: **NO APTO — NO EJECUTAR**

Revalidación enfocada R2-C1: 1/2.

Verificado el manifiesto externo completo, 55 entradas, SHA-256
`133aa34695c7329552c2a7427540eed8dfbf2d1f0cf63cf0163dba9fd1c47fa3`.
El diff modifica exactamente los 11 archivos permitidos indicados;
`authorized-preimage/**` permanece intacta. El manifiesto interno sigue
obsoleto: fallan sus 11 entradas modificadas.

| Hallazgo original | Estado tras R2-C1 |
|---|---|
| F1 — Recuperación interrumpida | ABIERTO: mejorado el procedimiento; falta demostrar los cortes y completar la validación de capturas reutilizadas |
| F2 — Comparación de `result.json` | CERRADO |
| F3 — Batería real y `errexit` | ABIERTO |
| F4 — Persistencia de respuestas crudas | CERRADO |
| F5 — Consulta fallida de impersonación | CERRADO |

#### WP018-PSHA-R2-F1 — Importante

**La reutilización no comprueba que el intento sea una captura completa.**

Archivo: `03-rollback-provider.sh:77`; relacionado: `lib/r2.py:247`.

Se reutiliza el directorio si pasa `compare`, que valida la preimagen de
referencia y compara las 39 superficies observadas, pero no valida el
manifiesto, el conjunto completo de archivos ni el cierre de la captura
observada.

Tras un `SIGKILL` después de escribir `result.json` y antes de producir
`drift-comparison.json` o `SHA256SUMS`, el siguiente rollback puede reutilizar
ese directorio y registrar `rolled-back` aunque el expediente de recaptura siga
incompleto.

Arreglo sugerido: validar explícitamente la captura candidata antes de
reutilizarla; si no está completa, preservarla y realizar otro intento.
Demostrar ambos caminos mediante cortes reales. El bloqueo original por
directorio existente está corregido, pero F1 no reúne todavía evidencia
suficiente para cerrarse.

#### WP018-PSHA-R2-F3.a — Importante

**La batería aborta antes de ejecutar sus pruebas.**

Archivo: `tests/run-local-tests.sh:55`.

Las comillas simples del CEL cierran la cadena que contiene el programa jq;
`$from` acaba siendo expandido por Bash. Con `from` sin definir, la ejecución
emite `from: unbound variable` antes del bootstrap. ShellCheck también detecta
SC1078, SC1079 y SC2154.

Arreglo sugerido: proporcionar la condición mediante argumentos jq
correctamente delimitados, conservar las comillas del CEL como datos y ejecutar
toda la batería.

Además, con `/bin/bash` 3.2.57 la ejecución abortada devuelve `0`, sin imprimir
el resultado terminal de la batería. Esto difiere del código `1` observado en
otro runtime; ninguno acredita pruebas superadas. Debe preservarse el estado de
fallo durante la limpieza y verificarse el comportamiento en el runtime
admitido.

#### WP018-PSHA-R2-F3.b — Importante

**El bootstrap tiene otro bloqueo independiente del error de comillas.**

Archivo: `tests/run-local-tests.sh:96`; relacionado: `lib/r2.py:208`.

Se llama a `compare` utilizando como preimagen un directorio que todavía no
contiene `drift-comparison.json`. `validate_capture` exige ese archivo antes de
permitir la comparación. Corregido únicamente F3.a, el bootstrap alcanza esta
llamada y falla por conjunto de archivos distinto; la comparación no puede
crear su salida porque primero valida la preimagen incompleta.

Arreglo sugerido: construir una fixture completa y coherente antes de utilizarla
como preimagen; generar y verificar su manifiesto cuando todos sus archivos
estén finalizados.

#### WP018-PSHA-R2-F3.c — Importante

**El nuevo caso F1 no interrumpe una recuperación.**

Archivo: `tests/run-local-tests.sh:254`.

`fail:after-update` provoca el rollback automático completo. Después, el test
sobrescribe parte de su captura y llama al rollback manual, cuyo estado ya es
`rolled-back`. Con los bloqueos anteriores corregidos y el flujo automático
funcionando, `03-rollback-provider.sh:21` retorna inmediatamente; no crea
`rollback-preimage.attempt-2` y la aserción posterior falla. No se ha ejecutado
ningún corte dentro del rollback.

Arreglo sugerido: cortar efectivamente la recuperación mientras mantiene
`rollback-intent`, comprobar la evidencia parcial conservada y reanudarla.
Añadir también el corte posterior a la captura y anterior al evento terminal.

#### WP018-PSHA-R2-F3.d — Importante

**Sigue sin ejercitarse la inhibición de `errexit` dentro de las funciones.**

Archivo: `tests/run-local-tests.sh:155`.

Las nuevas pruebas `if` y `!` siguen invocando scripts como procesos separados.
Eso no inhibe el `errexit` de las funciones ejecutadas dentro de esos procesos.
La batería puede aceptar estas pruebas sin haber llamado directamente a una
función relevante desde `if`, `!` o una lista condicional.

Arreglo sugerido: añadir pruebas directas y aisladas de las funciones
pertinentes bajo esos contextos, con dependencias simuladas y errores
verificables.

### Cierres acreditados y disposición

- F2 compara las 39 superficies, incluido `result.json`, conserva
  `core_project` y solo excluye las tres claves volátiles autorizadas. La
  preimagen real pasa su validación; su comparación consigo misma devuelve 39
  superficies y cero diferencias.
- F4 elimina `.raw` y procesa las respuestas sensibles por streaming antes de
  persistirlas. La prueba sintética del saneador emite hashes de miembros.
- F5 propaga el fallo de consulta. Una comprobación aislada bajo `if`, con
  `gcloud` simulado fallando, devuelve 77.

Sintaxis Bash y AST Python pasan; ShellCheck falla. No hay batería integral
válida. La limitación de ejecución está declarada por el autor; no es deuda
oculta.

R2-C1 queda **NO APTO**. R2-C2 puede plantearse exclusivamente para los
residuales F1/F3 y sus efectos directos, preservando los cierres F2/F4/F5,
regenerando el manifiesto y obteniendo evidencia ejecutada. Su apertura e
invocación requieren actos separados y presupuesto disponible acreditado.
Después de R2-C2 solo queda la segunda revalidación enfocada; si continúa `NO
APTO`, corresponde parada y replanificación, sin R2-C3.

## Estado de custodia tras R2-C1

Este archivo registra el dictamen completo de origen y la primera revalidación
enfocada. La postimagen R2-C1 permanece **NO APTO — NO EJECUTAR**. F2, F4 y F5
quedan cerrados; F1 y F3 permanecen abiertos. R2-C2 no está abierto y este
dictamen no autoriza al autor, otra corrección, materialización o ejecución.
