# Coste — WP-018 · transición del provider DOR-7

Formato según DEC-001, DEC-004 y DEC-010 §17.

```text
estado_coste: medido
coste_usd: 0
fuente_coste: F1
fecha_medicion: 2026-10-15
operador: Iván (operador humano; invocación y captura autorizadas expresamente)
instrumento: claude-code 2.1.272 --output-format json
wp_id: WP-018
artefacto: evidence/WP-018/cost-f1.json
artefacto_sha256: a52367e4788a576c18e89956c943680564c9d946e9b456b8f4843a7c5926bcd8
tipo_eurusd: 1.1298
fuente: BCE ref. 2026-10-01
coste_eur: 0.00
presupuesto_eur: 5.00
consumo: 0.0 %
```

## Resultado medido

La única invocación C1 comenzó el `2026-10-15T10:05:29Z` y terminó el
`2026-10-15T10:05:32Z` con código `1`. El resultado estructurado registra
`is_error: true`, `terminal_reason: api_error`, `duration_api_ms: 0`, ningún
modelo, token, subagente o denegación de permisos, cero solicitudes web de
herramientas registradas, y
`total_cost_usd: 0`.

El cero es una cifra F1 defendible de una invocación efectivamente iniciada:
la sesión OAuth había expirado y no pudo renovarse antes de la inferencia. No
es un cero de relleno ni significa cero invocaciones. El campo bruto
`subtype: success` describe la emisión del resultado estructurado y no supera
`is_error: true`, el fallo terminal ni el código de proceso.

El JSON crudo permanece fuera del repositorio en
`/private/tmp/wp018-author-c1-raw.json`; su SHA-256 es
`74f2c6cd8f1f79ba91980c3c311a56d49230729b815b877ec303c4516f51896e`.
El artefacto versionable es el extracto saneado `cost-f1.json`; no contiene el
prompt, la salida en claro ni el identificador de sesión en claro.

Conversión: `0 USD / 1.1298 USD/EUR = 0 EUR`. El presupuesto de `5.00 EUR` es
el subtecho propio acumulado de C1+C2 fijado por DEC-010 §17, dentro del techo
contractual de `100.00 EUR` de WP-018.

## Efecto operativo

C1 quedó consumido desde el lanzamiento, sin cambios técnicos. La
revalidación enfocada de la misma revisora emitió `NO APTO` y mantuvo abiertos
`WP018-PSHA-F1` a `WP018-PSHA-F5`. Este registro no abre C2, no autoriza otra
invocación y no autoriza ejecutar el provider, C0 o infraestructura.
