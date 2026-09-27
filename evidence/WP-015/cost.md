# WP-015 — Coste

Conforme a [`DEC-001`](../../specs/decisions/DEC-001-divisa-costes.md) y
[`DEC-004`](../../specs/decisions/DEC-004-estados-del-coste.md).

## Registro normativo

| Campo | Valor |
|---|---|
| `estado_coste` | `estimado` |
| `causa` | La captura F1 produjo cifras estructuradas por invocación, pero los envoltorios JSON completos de la implementación inicial y del intento fallido de reanudación no se conservaron como archivos. El resultado completo de la consolidación sí se conservó. Esta incompletitud degrada el agregado a `estimado` conforme a DEC-004 §3 y §12. |
| `coste_usd` | `11.008139000000002` |
| `fuente_coste` | `F1` |
| `base_estimacion` | Suma de las tres invocaciones atribuibles exclusivamente a WP-015: `8.825610200000002 + 0 + 2.1825288 USD`. Los tres valores proceden de `total_cost_usd` de resultados `claude -p --output-format json`; el segundo fue un error de autenticación sin consumo. El desglose y los campos preservados están en `evidence/WP-015/cost-f1.json`. |
| `fecha_medicion` | `2026-09-27` |
| `operador` | Iván (`@ivanes189`), mediante la coordinación Codex de esta sesión autorizada |
| `instrumento` | `claude-code 2.1.272 --output-format json` |
| `wp_id` | `WP-015` |
| `artefacto` | `evidence/WP-015/cost-f1.json` |
| `artefacto_sha256` | `0f58ab69ed37fef3e6b09f37e1f5f3f146eef380add58df238949a06e1a4caeb` |
| `tipo_eurusd` | `1.1590` |
| `fuente` | BCE, referencia EUR/USD del `2026-09-01`, registrada en `specs/finops/fx-rates.md` |
| `coste_eur` | `9.50` |
| `presupuesto_eur` | `40` |
| `consumo` | `23.7 %` |

## Cálculo

`11.008139000000002 / 1.1590 = 9.497962899... EUR`, redondeado a
`9.50 EUR`. El consumo es `9.497962899... / 40 × 100 = 23.7 %`.

La cifra queda dentro del presupuesto máximo de `40 EUR`. `estimado` describe
la conformidad de la captura, no una extrapolación: todos los importes USD son
los valores estructurados de las invocaciones reales de este WP. El artefacto
es un extracto saneado; no contiene prompts, resultados, cargas de herramientas,
identidad de cuenta ni el identificador de sesión en claro.
