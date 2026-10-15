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

## Estado de custodia

Este archivo preserva el dictamen de origen de R2. No constituye una
revalidación y no consume R2-C1. La candidata permanece **NO APTO — NO
EJECUTAR** hasta que una corrección autorizada y la revalidación enfocada de la
misma revisora cierren todos los hallazgos. Abrir R2-C1 no autoriza al autor,
la materialización técnica ni la ejecución del provider.
