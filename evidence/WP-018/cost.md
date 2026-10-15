# Coste — WP-018 · transición `WP018-DOR7-PSHA-R2` · R2-C1

Formato según DEC-001 (divisa) y DEC-004 (estados y adquisición).

```text
estado_coste: medido
coste_usd: 4.1209296
fuente_coste: F1
fecha_medicion: 2026-10-15
operador: @ivanes189
instrumento: claude-code 2.1.272
wp_id: WP-018
artefacto: evidence/WP-018/cost-f1.json
artefacto_sha256: 99539462c4c93edb5f8fc0472cc7cf45e8ba97195370eda72d5e8e1b00684cc9
tipo_eurusd: 1.1298
fuente: BCE ref. 2026-10-01
coste_eur: 3.65
presupuesto_eur: 5.00
consumo: 72.9 %
```

| Concepto | Valor |
|---|---:|
| Coste total registrado | 4.1209296 USD |
| Coste de gobierno | 3.65 EUR |
| Subpresupuesto de R2-C1 | 5.00 EUR |
| Consumo | 72.9 % |
| Invocaciones F1 agregadas | 1 |
| Ciclo corrector | R2-C1 · consumido |
| Turnos | 64 |
| Modelo principal | `claude-sonnet-5` |
| Dictamen técnico | `NO APTO — NO EJECUTAR` |

## Adquisición y cálculo

La invocación comenzó el `2026-10-15T16:49:48Z` y terminó el
`2026-10-15T17:19:16Z`. El proceso devolvió código `0`; su resultado F1 declaró
`is_error:false`, subtipo `success` y razón terminal `completed`. Registró 64
turnos, nueve denegaciones de la herramienta Bash, cero subagentes y cero
solicitudes de búsqueda o lectura web.

La conversión usa el tipo mensual congelado de octubre de 2026:
`4.1209296 USD / 1.1298 = 3.6474859267... EUR`, redondeado a `3.65 EUR` solo al
final. Quedan `1.3525140733... EUR` del subpresupuesto de R2-C1.

`evidence/WP-018/cost-f1.json` es el extracto derivado y saneado exigido por
DEC-004. El crudo se conserva únicamente fuera del repositorio en
`/private/tmp/wp018-author-r2-c1-raw.json`, con SHA-256
`d7e389d6f6373bb4e6fc68a1ceec59b8d79515efaaf163cae0a4677a51a2426e`; no es
fuente de verdad versionada ni se incorpora a la evidencia.

## Efecto de gobierno

El éxito del instrumento no acredita la corrección de la candidata. El autor
no pudo ejecutar pruebas por las nueve denegaciones Bash. La verificación
independiente posterior encontró ShellCheck fallido, la batería abortada y el
manifiesto interno obsoleto. La revalidación enfocada mantuvo abiertos F1 y F3,
cerró F2, F4 y F5, y emitió `NO APTO — NO EJECUTAR`.

R2-C1 queda consumido. R2-C2 permanece sin abrir; esta evidencia no autoriza
otra invocación, materialización técnica, ejecución del provider ni ningún
otro acto operativo.
