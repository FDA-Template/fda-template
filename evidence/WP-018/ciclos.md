# WP-018 — Registro de ciclos de la actualización del provider de DOR-7

Este registro aplica `DEC-010` §17 y pertenece exclusivamente a la transición
que rederiva `assertion.workflow_sha` sobre la base postfusión congelada. No
activa WP-018, no modifica infraestructura, no autoriza al autor y no habilita
pool, provider, roles, bindings, secretos, dispatch, C0 ni C1 privilegiado.

## Anclajes congelados

- Rama durable: `ops/wp018-dor7-provider-sha-custody`.
- Base exclusiva: `origin/main`
  `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e`.
- Padre único del squash: `6821c0a83efd547b7617a1fed9c168e33224889c`.
- Workflow: `.github/workflows/wp018-dor7-emergency-push.yml`.
- SHA-256 del workflow:
  `7ea50ded863cf57f2cac6916dada3dece9305bb6af60266601ca79ffa76b1594`.
- Preimagen GCP postfusión externa:
  `/private/tmp/wp018-dor7-postmerge-preimage-20261015`; comparación canónica
  exacta contra la última preimagen autorizada, `APTO`; SHA-256 de su
  `SHA256SUMS`:
  `9969b609800d34cde4ea3b4f670d7113a250f28a169f4d70c6f3b2d14aba79a9`.
- Captura GitHub postfusión saneada:
  `/private/tmp/wp018-dor7-postmerge-preimage-20261015/github`; SHA-256 de su
  `SHA256SUMS`:
  `8a58baa4bfd55a57f13cc2b84b52a903416ec927b44f6029877893e215d43ee0`.
- La observación GitHub postfusión confirmó el mismo `main`, cero despachos,
  entorno y OIDC sin deriva, cero secrets y variables de entorno, y
  `secret_scanning` y `secret_scanning_push_protection` habilitados.
- La observación GCP postfusión confirmó proyecto y facturación esperados,
  fixtures y logging sin deriva, cero roles personalizados, bindings o claves
  de usuario y pool/provider deshabilitados.

Cualquier cambio posterior de `main`, workflow o estado externo detiene la
transición y obliga a una decisión previa y rederivación completa. No se
actualizan anclajes en cascada.

## Candidata y revisión de origen

La candidata técnica histórica está preservada fuera del repositorio en
`/private/tmp/wp018-dor7-provider-sha-candidate`. Su digest agregado es
`ad5e237ed687bab12b442d7cb1505b1209f262c6aa8281d6e9f072e471b59591`.
La preimagen administrativa original conserva 37 entradas verificadas y su
`SHA256SUMS` tiene SHA-256
`65f51dd297d6f5e625792856a0529b3b803117db0be50fd0c39e6c2b9a274136`.

La revisión completa independiente GPT-6 Astra, razonamiento Alto, contexto
nuevo y solo lectura emitió `NO APTO` el 2026-10-12. Su transcripción completa,
identidad y hashes están custodiados en `review-astra.md`. DEC-010 §17 asigna
los alias normativos siguientes a los identificadores originales:

| Alias §17 | Identificador del dictamen | Severidad | Resumen cerrado para C1 |
|---|---|---|---|
| `WP018-PSHA-F1` | `WP018-DOR7-SHA-F1` | bloqueante | rollback manual utilizable tras una ejecución fallida |
| `WP018-PSHA-F2` | `WP018-DOR7-SHA-F2` | bloqueante | comparación fresca contra la preimagen autorizada |
| `WP018-PSHA-F3` | `WP018-DOR7-SHA-F3` | importante | restauración exacta del provider completo |
| `WP018-PSHA-F4` | `WP018-DOR7-SHA-F4` | importante | pruebas sin red de mutación, fallo y recuperación |
| `WP018-PSHA-F5` | `WP018-DOR7-SHA-F5` | menor | `--project=fda-template` en toda llamada de recurso |

Los ocho hallazgos cerrados de la transición anterior permanecen criterios de
regresión. C1 solo puede corregir los cinco hallazgos anteriores y sus efectos
directos en los ocho archivos identificados por `review-astra.md`.

## Apertura versionada de C1

| Ciclo | Estado | Fecha de apertura | Invocaciones correctoras | Autor ejecutado | Base | Presupuesto acumulado C1+C2 |
|---|---|---|---:|---|---|---:|
| C1 | `NO APTO — consumido` | 2026-10-15 | 1 | sí; OAuth expirado antes de inferencia, sin cambios | `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e` | 0.00 de 5.00 EUR |
| C2 | `NO APTO — consumido` | 2026-10-15 | 1 | sí; terminó, produjo candidata no apta | `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e` | 3.06 de 5.00 EUR |

Cada estado `abierto` adquirió autoridad únicamente al quedar versionado y
publicado en la rama durable indicada. Su preparación en `/private/tmp`, el
commit y el push no consumieron el ciclo: cada ciclo se consumió cuando
comenzó su primera invocación correctora, aunque C1 falló antes de inferencia.
Nunca se creó una segunda fila para el mismo ciclo.

## Coste y gates anteriores al autor

- Tipo mensual vigente: `1.1298 USD/EUR`, referencia BCE del 2026-10-01.
- Método obligatorio: F1 desde el lanzamiento con
  `claude -p --output-format json`, `WP-018` explícito, versión exacta y sin
  `--continue` o `--resume`.
- La captura cruda queda fuera del repositorio. Tras la invocación, el extracto
  saneado se versiona en `cost-f1.json`; `cost.md` registra su SHA-256, la
  conversión por división y el total acumulado.
- Cero invocaciones no es un importe. No se registra coste cero ni se inventa
  F3. Una invocación sin `total_cost_usd` defendible produce `NO APTO`.
- Antes del autor deben verificarse rama remota, commit de apertura, ausencia
  de deriva, `claude 2.1.272`, captura headless, tipo mensual y presupuesto
  restante. Falta de cualquiera implica parada.

Después de cada invocación se actualiza la misma fila con resultado, coste y
estado. Solo una revalidación enfocada de la misma revisora puede cerrar un
ciclo como `APTO` o mantener hallazgos concretos. C2 se abrió mediante el
mismo procedimiento; no existe C3.

## Resultado de C1

La única invocación correctora comenzó el `2026-10-15T10:05:29Z` y terminó el
`2026-10-15T10:05:32Z` con código `1`. Claude Code `2.1.272` no alcanzó la
inferencia porque la sesión OAuth había expirado y no pudo renovarse. La
captura F1 estructurada registra `is_error: true`, `duration_api_ms: 0`, cero
modelos y tokens, y `total_cost_usd: 0`. El crudo externo tiene SHA-256
`74f2c6cd8f1f79ba91980c3c311a56d49230729b815b877ec303c4516f51896e`;
el extracto saneado y su conversión están en `cost-f1.json` y `cost.md`.

Los ocho archivos técnicos conservaron exactamente sus hashes históricos: no
hubo cambios que materializar o ejecutar. La misma revisora realizó la
revalidación enfocada de solo lectura y emitió `NO APTO`; permanecen abiertos,
sin cambio de severidad, `WP018-PSHA-F1` a `WP018-PSHA-F5`. C1 está consumido,
no se reintenta y no se crea una segunda fila C1.

Al cerrar C1, C2 permanecía **sin abrir**. Antes de cualquier segunda
invocación debían restaurarse las credenciales del instrumento por acto
humano, abrirse y versionarse C2 mediante el mismo procedimiento, y obtener
una autorización humana separada. El resultado de C1 no autorizó al autor,
provider, C0, workflow, infraestructura, PR, fusión ni descarte de la rama.

## Apertura versionable de C2

La revalidación enfocada de la misma revisora mantuvo concretamente abiertos
`WP018-PSHA-F1` a `WP018-PSHA-F5`, sin cambio de severidad. El 2026-10-15 se
restauró humanamente la autenticación del instrumento; una comprobación
saneada en el mismo contexto externo que usaría el autor confirmó
`loggedIn: true`, método `claude.ai`, proveedor `firstParty`. Claude Code
conserva la versión exacta `2.1.272`.

La apertura de C2 adquirió autoridad cuando quedó versionada y publicada en la
rama durable mediante el commit
`27d395ab1a3c5d541939d62e21a630652a665140`, hijo de
`02821d7c8a57042d73b2185e74e656342478c4fe`. Su preparación en `/private/tmp`,
el commit y el push no consumieron C2; el ciclo se consumió cuando comenzó su
única invocación correctora.

Al abrir C2, el alcance corrector quedó limitado a `WP018-PSHA-F1` a
`WP018-PSHA-F5` y sus efectos directos en los ocho archivos técnicos
identificados. En ese momento, la candidata conservaba sus bytes históricos
porque C1 no había producido cambios; el coste acumulado era
`0 USD / 0 EUR` y quedaban disponibles `5.00 EUR`. Estos datos describen la
apertura; el estado vigente es el resultado final de C2 consignado a
continuación.

C2 es el último ciclo ordinario. No existe C3. Esta apertura no autoriza la
invocación del autor, materialización o ejecución de la candidata, provider,
rollback, WIF, workflow, dispatch, C0, infraestructura, PR, fusión o descarte
de la rama; cada acto conserva autorización humana separada.

## Resultado final de C2

La única invocación correctora de C2 comenzó el `2026-10-15T10:46:49Z` y
terminó el `2026-10-15T11:18:41Z` con código `0`. Claude Code `2.1.272`
produjo una candidata en
`/private/tmp/wp018-dor7-provider-sha-c2-author`, con digest agregado
`1625f0666d24c65732bd71d45d92120f4f6c95f2fc861c555f2a9a58aebe91da`.
El crudo externo tiene SHA-256
`655a53eaaeba62bd9cadc1399cb2279b87eb589227df9909ae75c7e76f3462dc`.
La captura F1 registra `is_error: false`, 35 turnos, cero denegaciones de
permisos, subagentes o solicitudes web de herramientas, y coste
`3.4601586 USD / 3.0626293149... EUR`, redondeado a `3.06 EUR`.

La verificación local de `tests/run-local-tests.sh` terminó con código `1`.
El caso negativo que altera `result.main` de `"m"` a `"DIFFERENT"` fue
aceptado por `compare_preimage_canonically` cuando se invoca dentro de un
`if`: el primer `cmp` falla, las comparaciones posteriores tienen éxito y la
función devuelve `0`. La batería se detuvo antes de las pruebas posteriores.
Sintaxis y ShellCheck sí pasaron. El manifiesto de la candidata declara además
que no se ejecutaron el preflight completo ni los caminos completos de
actualización exitosa, fallo posterior a la mutación y rollback automático.

La misma revisora independiente realizó una única revalidación enfocada,
estrictamente de solo lectura, y emitió `NO APTO`. El estado final es:

| Hallazgo | Severidad | Estado final |
|---|---|---|
| `WP018-PSHA-F1` | Bloqueante | Abierto: el journal puede quedar con sello inválido tras su última ampliación y antes de la custodia raíz |
| `WP018-PSHA-F2` | Bloqueante | Abierto: la comparación omite superficies materiales y la candidata conserva `NEW_MAIN_SHA=6821c0a...`, no la base congelada |
| `WP018-PSHA-F3` | Importante | Cerrado en el diff; la falta de ejecución integral permanece en F4 |
| `WP018-PSHA-F4` | Importante | Abierto: batería fallida y caminos críticos no ejecutados |
| `WP018-PSHA-F5` | Menor | Cerrado: las llamadas señaladas incluyen el proyecto explícito |

C1 y C2 están consumidos. No existe C3 y no se corrige, reejecuta,
materializa ni ejecuta esta candidata. La transición se detiene de forma
segura y vuelve a decisión humana para elegir cierre `blocked`, división o
replanteamiento. Pool y provider permanecen deshabilitados; no se habilita
WIF, no se despacha el workflow, no se abre C0 y no se modifica
infraestructura.

## Autorizaciones separadas

Este cierre no autoriza otra invocación, una corrección, materialización o
ejecución de la candidata, actualización del provider, rollback, habilitación
de WIF, dispatch, C0, fusión o descarte de la rama. La siguiente decisión
humana debe elegir cierre `blocked`, división o replanteamiento; no puede abrir
C3 por implicación.
