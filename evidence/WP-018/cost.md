# Coste — WP-018 · transición `WP018-DOR7-PSHA-R2` · cierre R2

Formato según DEC-001 (divisa) y DEC-004 (estados y adquisición).

```text
estado_coste: medido
estado_transicion: blocked
coste_usd: 5.6754402
fuente_coste: F1
fecha_medicion: 2026-10-15
operador: @ivanes189
instrumento: claude-code 2.1.272
wp_id: WP-018
artefacto: evidence/WP-018/cost-f1.json
artefacto_sha256: 038cbf09095c0a7df4a5d8412a66672ce9192cfd34480271ba62b948246e181b
tipo_eurusd: 1.1298
fuente: BCE ref. 2026-10-01
coste_eur_exacto: 5.023402549123739
coste_eur_redondeado: 5.02
presupuesto_eur: 5.00
exceso_eur_exacto: 0.023402549123739
consumo_exacto: 100.46805098247478 %
```

| Ciclo | Estado del instrumento | Coste USD | Coste EUR exacto | Turnos |
|---|---|---:|---:|---:|
| R2-C1 | `success`; candidata `NO APTO` | 4.1209296 | 3.6474859267126925 | 64 |
| R2-C2 | `error_max_budget_usd`; `budget_exhausted`; candidata `NO APTO` | 1.5545106 | 1.3759166224110462 | 38 |
| **Total R2** | **`blocked`; 2/2 ciclos consumidos** | **5.6754402** | **5.023402549123739** | **102** |

El subpresupuesto incremental de R2 era `5.00 EUR`. El coste excede ese límite
en `0.023402549123739 EUR`; el redondeo monetario a `5.02 EUR` no elimina el
exceso. Sumado al coste histórico preservado de `3.0626293149 EUR`, el total es
`8.086031864023739 EUR`, también `0.023402549123739 EUR` por encima del techo
combinado de `8.0626293149 EUR`.

## Adquisición de R2-C1

La invocación comenzó el `2026-10-15T16:49:48Z` y terminó el
`2026-10-15T17:19:16Z`. El proceso devolvió código `0`; su resultado F1 declaró
`is_error:false`, subtipo `success` y razón terminal `completed`. Registró 64
turnos, nueve denegaciones de la herramienta Bash, cero subagentes, cero
solicitudes web y coste `4.1209296 USD / 3.6474859267126925 EUR`.

El crudo se conserva únicamente fuera del repositorio en
`/private/tmp/wp018-author-r2-c1-raw.json`, con SHA-256
`d7e389d6f6373bb4e6fc68a1ceec59b8d79515efaaf163cae0a4677a51a2426e`.
El éxito del instrumento no acreditó la postimagen: la primera revalidación
enfocada mantuvo F1 y F3 abiertos.

## Adquisición de R2-C2

La única invocación de R2-C2 comenzó el `2026-10-15T17:54:14Z` y terminó el
`2026-10-15T18:07:22Z`. Se lanzó con límite `--max-budget-usd 1.52`; el proceso
devolvió código `1` y el JSON F1 válido declaró `is_error:true`, subtipo
`error_max_budget_usd`, razón terminal `budget_exhausted`, resultado ausente y
38 turnos. No registró denegaciones ni solicitudes web. Su coste fue
`1.5545106 USD / 1.3759166224110462 EUR`, por lo que superó tanto el límite de
la propia invocación como el remanente exacto de R2.

El crudo se conserva únicamente fuera del repositorio en
`/private/tmp/wp018-author-r2-c2-raw.json`, con SHA-256
`cc1b8536f097e79bfbcd709f5e4104c70544ab4e9ca235ac0aeb1b6c0a45a2cc`.
El prompt tiene SHA-256
`e661a5aba51e61c599a17e4e00587998ba509ff4a4f8666a3d846208f484a9b2` y
el wrapper SHA-256
`9f642455ec5cdb5062aabdd324ce6d8548b7c4b7f469f6ff0c7547c9a804fad6`.

## Efecto de gobierno

R2-C1 y R2-C2 están consumidos. La verificación independiente y la segunda
revalidación enfocada emitieron `NO APTO — NO EJECUTAR`: F1 y F3 permanecen
abiertos; F2, F4 y F5 permanecen cerrados. El exceso de presupuesto constituye
además una condición de parada vinculante.

La transición `WP018-DOR7-PSHA-R2` termina `blocked`. No existe R2-C3. Esta
evidencia no autoriza otra invocación, materialización técnica, actualización o
recuperación del provider, habilitación de WIF, despacho del workflow ni C0.
