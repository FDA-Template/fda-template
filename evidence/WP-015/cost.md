# WP-015 — Coste

Conforme a [`DEC-001`](../../specs/decisions/DEC-001-divisa-costes.md) y
[`DEC-004`](../../specs/decisions/DEC-004-estados-del-coste.md).

## Registro normativo

| Campo | Valor |
|---|---|
| `estado_coste` | `estimado` |
| `causa` | La captura F1 produjo cifras estructuradas por invocación, pero los envoltorios JSON completos de la implementación inicial y del intento fallido de reanudación no se conservaron como archivos. Los resultados completos de la consolidación, C1 y C2 sí se conservaron. Esta incompletitud degrada el agregado a `estimado` conforme a DEC-004 §3 y §12. |
| `coste_usd` | `26.6207455999999986` |
| `fuente_coste` | `F1` |
| `base_estimacion` | Suma de las seis invocaciones atribuibles exclusivamente a WP-015: `8.825610200000002 + 0 + 2.1825288 + 8.905483599999997 + 5.9228439999999996 + 0.784279 USD`. Los seis valores proceden de `total_cost_usd` de resultados `claude -p --output-format json`; el segundo fue un error de autenticación sin consumo, el cuarto corresponde a C1, el quinto a C2 —incluido pese a terminar por límite temporal porque consumió tokens y dejó comprometido el código— y el sexto al C3 excepcional de `WP015-F2`. El desglose y los campos preservados están en `evidence/WP-015/cost-f1.json`. |
| `fecha_medicion` | `2026-09-27` |
| `operador` | Iván (`@ivanes189`), mediante la coordinación Codex de esta sesión autorizada |
| `instrumento` | `claude-code 2.1.272 --output-format json` |
| `wp_id` | `WP-015` |
| `artefacto` | `evidence/WP-015/cost-f1.json` |
| `artefacto_sha256` | `9fdba3d2bc7b6fa74593d425cd5c9960a78e83ef626c5c55551971dab4794e8f` |
| `tipo_eurusd` | `1.1590` |
| `fuente` | BCE, referencia EUR/USD del `2026-09-01`, registrada en `specs/finops/fx-rates.md` |
| `coste_eur` | `22.97` |
| `presupuesto_eur` | `40` |
| `consumo` | `57.4 %` |

## Cálculo

`26.6207455999999986 / 1.1590 = 22.968719240... EUR`, redondeado a
`22.97 EUR`. El consumo es `22.968719240... / 40 × 100 = 57.4 %`.

El C3 excepcional consumió `0.784279 USD / 1.1590 = 0.676685936... EUR`,
redondeado a `0.68 EUR`: `11.3 %` de su presupuesto adicional máximo de
`6.00 EUR`. El acumulado `22.97 EUR` queda por debajo del techo final de
`28.29 EUR` fijado por DEC-013 (`81.2 %`).

La cifra queda dentro del presupuesto máximo de `40 EUR` y del techo más
estricto de DEC-013. `estimado` describe
la conformidad de la captura, no una extrapolación: todos los importes USD son
los valores estructurados de las invocaciones reales de este WP. El artefacto
es un extracto saneado; no contiene prompts, resultados, cargas de herramientas,
identidad de cuenta ni el identificador de sesión en claro.
