# WP-018 — Registro de ciclos de `WP018-DOR7-PSHA-R2`

Este registro aplica `DEC-010` §18 y pertenece exclusivamente a la transición
nueva que rederiva desde cero la actualización de `assertion.workflow_sha` del
provider de DOR-7. No reactiva la transición histórica, no abre C3, no activa
WP-018, no modifica infraestructura y no autoriza al autor, la ejecución de la
candidata, el provider, WIF, el workflow o C0.

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

## Apertura versionada de R2-C1

| Ciclo | Estado | Fecha de apertura | Invocaciones correctoras | Autor ejecutado | Base | Subpresupuesto R2 disponible |
|---|---|---|---:|---|---|---:|
| R2-C1 | `abierto` | 2026-10-15 | 0 | no | `9cdfaefddfdb50fa1fba385e265243022b67061f` | 5.00 EUR |

`abierto` describe la postimagen que adquiere autoridad únicamente cuando estos
bytes quedan versionados y publicados en la rama durable R2. Mientras solo
existan en `/private/tmp`, R2-C1 no está abierto. Crear, commitear y publicar la
rama no consume el ciclo. R2-C1 se consume cuando comienza la primera
invocación correctora del autor, aunque falle antes de inferencia, se interrumpa
o no produzca cambios. No se crea una segunda fila R2-C1.

## Coste y gates anteriores al autor

- Subpresupuesto incremental de R2: `5.00 EUR`, dentro del techo invariable de
  `100.00 EUR` de WP-018.
- Coste histórico preservado: `3.0626293149... EUR`; ambos expedientes no
  podrán superar juntos `8.0626293149... EUR`.
- Tipo mensual vigente: `1.1298 USD/EUR`, referencia BCE del 2026-10-01.
- No existe aún una invocación R2 ni un coste R2 medido. Cero invocaciones no es
  un importe; no se crea `cost-f1.json` o `cost.md` hasta disponer de F1.
- La primera invocación correctora requiere F1 desde el lanzamiento con
  `claude -p --output-format json`, `WP-018` explícito, versión exacta
  previamente comprobada y sin `--continue` o `--resume`.
- Antes del autor deben verificarse rama remota, commit de apertura, identidad
  de candidata y preimagen, ausencia de deriva, autenticación headless, tipo
  mensual y presupuesto restante. La falta de cualquiera obliga a parar.

Después de la eventual invocación se actualiza esta misma fila con resultado,
coste y estado. La misma revisora independiente puede realizar como máximo dos
revalidaciones enfocadas, una después de R2-C1 y otra después de R2-C2. No
existe R2-C3.

## Autorizaciones separadas

Esta apertura no autoriza a invocar al autor, modificar la candidata, ejecutar
sus pruebas con servicios reales, materializarla, actualizar o recuperar el
provider, habilitar WIF, crear roles o bindings, despachar el workflow, abrir o
ejecutar C0, abrir R2-C2, fusionar o descartar ninguna rama. Cada acto requiere
su propia autorización humana conforme a `DEC-010` §18.5.
