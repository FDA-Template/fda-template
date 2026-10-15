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
| C1 | `abierto` | 2026-10-15 | 0 | no | `2f7fc1ce0bcab69d9157067445d7e6d60a593d5e` | 5.00 EUR |

`abierto` describe la postimagen que adquiere autoridad únicamente al quedar
versionada y publicada en la rama durable indicada. Mientras estos bytes solo
existan en `/private/tmp`, C1 no está abierto. Crear, commitear o publicar esa
rama tampoco consume C1: el ciclo se consume solo cuando comienza la primera
invocación correctora del autor, aunque falle, se interrumpa o no produzca
cambios. Nunca se crea una segunda fila C1.

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

Después de la primera invocación se actualiza esta misma fila con resultado,
coste y estado. Solo una revalidación enfocada de la misma revisora puede
cerrar C1 como `APTO` o mantener hallazgos concretos. C2 solo se abre mediante
el mismo procedimiento; no existe C3.

## Autorizaciones separadas

Esta apertura no autoriza la invocación del autor, materialización o ejecución
de la candidata corregida, actualización del provider, rollback, habilitación
de WIF, dispatch, C0, fusión o descarte de la rama. Cada acto requiere su propia
autorización humana conforme a DEC-010 §17.
