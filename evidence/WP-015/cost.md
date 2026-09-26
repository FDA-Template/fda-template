# WP-015 — Coste

Conforme a [`DEC-001`](../../specs/decisions/DEC-001-divisa-costes.md) y
[`DEC-004`](../../specs/decisions/DEC-004-estados-del-coste.md).

## Registro

| Campo | Valor |
|---|---|
| `estado_coste` | `no_disponible` |
| `causa` | El agente autor, en este entorno de ejecución, no tiene acceso a un capturador F1 (JSON estructurado por invocación) ni F2 (agregación OpenTelemetry) instrumental sobre su propia sesión. No existe ningún comando en el entorno autorizado de este WP (`python3`, `bash`, `git` de solo lectura, `shellcheck`, `shasum`, `find`, `sort`, `mktemp`) que produzca ese artefacto. La adquisición F3 exige una persona leyendo un panel (`/usage` o `/cost`), lo que este agente tampoco puede ejecutar por sí mismo. |
| `coste_usd` | *(ausente — prohibido en `no_disponible`)* |
| `fuente_coste` | *(ausente)* |
| `base_estimacion` | *(ausente)* |
| `fecha_medicion` | *(ausente)* |
| `operador` | Claude Code (implementer) — automatización que registra esta entrada; no sustituye a la persona que debe aportar F1/F2/F3 |
| `instrumento` | *(ausente)* |
| `wp_id` | WP-015 |
| `artefacto` · `artefacto_sha256` | *(ausentes)* |
| `excepcion` | *(ausente)* |
| `tipo_eurusd` · `fuente` · `coste_eur` · `consumo` | *(ausentes)* |
| `presupuesto_eur` | 40 |

## Bloqueo residual para el coordinador

Este dato no se fabrica. El coordinador (u otra persona con acceso a la
telemetría real de esta sesión) debe aportar la medición estructurada F1 o
F2 — o, en su defecto, F3 con base concreta y reconstruible — y completar
este archivo con los campos que exige `DEC-004` §4 antes de que el WP pueda
declararse `APTO`. Mientras `estado_coste` sea `no_disponible`, el resultado
es `NO APTO` por este concepto exclusivamente de coste (`DEC-004` §11), con
independencia del resultado técnico de la implementación.

## Contexto informativo, explícitamente no conformante con F1/F2

Durante esta sesión, el propio entorno de ejecución mostró, en avisos de
sistema sucesivos, una cifra acumulada de presupuesto en USD que fue
creciendo a lo largo de la conversación (última observada, antes de escribir
este archivo: del orden de 7,7 USD sobre un tope de sesión de 46,36 USD). Se
menciona **solo como contexto para el coordinador**, no como `coste_usd`:
carece de los campos obligatorios de un artefacto F1 o F2 —instrumento y
versión exacta, ruta y SHA-256 del extracto, atribución explícita a
`WP-015`— y no se sabe si esa cifra de la interfaz corresponde a la misma
definición de "coste de la sesión" que `DEC-004` exige medir. Presentarla
como `coste_usd` sin esos requisitos sería fabricar una cifra sin origen
verificable, exactamente lo que `DEC-004` §10.3 prohíbe.
