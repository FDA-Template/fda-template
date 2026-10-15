# Coste — WP-018 · transición del provider DOR-7

Formato según DEC-001, DEC-004 y DEC-010 §17.

```text
estado_coste: medido
coste_usd: 3.4601586
fuente_coste: F1
fecha_medicion: 2026-10-15
operador: Iván (operador humano; invocaciones y capturas autorizadas expresamente)
instrumento: claude-code 2.1.272 --output-format json
wp_id: WP-018
artefacto: evidence/WP-018/cost-f1.json
artefacto_sha256: b6be6cb610edf6f6ab562d89580e9e166a6af0688ab3592a660dd3790605bf94
tipo_eurusd: 1.1298
fuente: BCE ref. 2026-10-01
coste_eur: 3.06
presupuesto_eur: 5.00
consumo: 61.3 %
```

## Resultado medido

Se registraron dos invocaciones correctoras. C1 comenzó el
`2026-10-15T10:05:29Z` y terminó el `2026-10-15T10:05:32Z` con código `1`.
Su resultado estructurado registra `is_error: true`,
`terminal_reason: api_error`, `duration_api_ms: 0`, ningún modelo, token,
subagente o denegación de permisos, cero solicitudes web de herramientas y
`total_cost_usd: 0`.

El cero es una cifra F1 defendible de una invocación efectivamente iniciada:
la sesión OAuth había expirado y no pudo renovarse antes de la inferencia. No
es un cero de relleno ni significa cero invocaciones. El campo bruto
`subtype: success` describe la emisión del resultado estructurado y no supera
`is_error: true`, el fallo terminal ni el código de proceso.

El JSON crudo de C1 permanece fuera del repositorio en
`/private/tmp/wp018-author-c1-raw.json`; su SHA-256 es
`74f2c6cd8f1f79ba91980c3c311a56d49230729b815b877ec303c4516f51896e`.

C2 comenzó el `2026-10-15T10:46:49Z` y terminó el
`2026-10-15T11:18:41Z` con código `0`. El resultado registra
`is_error: false`, `terminal_reason: completed`, `duration_ms: 1911370`,
`duration_api_ms: 1912686`, 35 turnos, cero denegaciones de permisos,
subagentes o solicitudes web de herramientas, y
`total_cost_usd: 3.4601586`. Ese éxito describe la ejecución del instrumento;
la misma revisora emitió `NO APTO` sobre la candidata resultante.

El JSON crudo de C2 permanece fuera del repositorio en
`/private/tmp/wp018-author-c2-raw.json`; su SHA-256 es
`655a53eaaeba62bd9cadc1399cb2279b87eb589227df9909ae75c7e76f3462dc`.
El artefacto versionable es el extracto saneado acumulado `cost-f1.json`; no
contiene prompts, salidas en claro ni identificadores de sesión en claro.

Conversión acumulada:
`3.4601586 USD / 1.1298 USD/EUR = 3.0626293149... EUR`, redondeado a
`3.06 EUR`. El consumo es
`3.0626293149... / 5.00 × 100 = 61.3 %`. El presupuesto de `5.00 EUR` es el
subtecho propio acumulado de C1+C2 fijado por DEC-010 §17, dentro del techo
contractual de `100.00 EUR` de WP-018.

## Efecto operativo

C1 y C2 quedaron consumidos. La revalidación final de la misma revisora emitió
`NO APTO`: `WP018-PSHA-F1`, `WP018-PSHA-F2` y `WP018-PSHA-F4` permanecen
abiertos; `WP018-PSHA-F3` y `WP018-PSHA-F5` quedan cerrados. No existe C3.
Este registro no autoriza otra invocación, corregir o ejecutar la candidata,
actualizar el provider, abrir C0 ni modificar infraestructura.
