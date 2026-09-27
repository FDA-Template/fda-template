# WP-015 — Registro de ciclos de corrección

Conforme a [`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§4 y [`docs/manual/02-ciclo-de-un-wp.md`](../../docs/manual/02-ciclo-de-un-wp.md).

**Presupuesto de ciclos del contrato:** `max_ciclos_correccion: 2`.

**Estado actual: `C1 abierto` (`1 / 2`).**

La implementación inicial no consumió ciclo. La única revisión completa de
Astra sobre el candidato `b1a8031bf715bff43239e7f835d396f301f5d5a2`
concluyó `NO APTO` y autorizó los ocho hallazgos registrados en
`evidence/WP-015/revision-astra.md`. `C1` queda abierto y versionado por este
registro antes de que Claude Code empiece ninguna corrección.

| Ciclo | Candidato y revisión de origen | Hallazgos autorizados | Fecha | Estado | Resultado / HEAD / coste |
|---|---|---|---|---|---|
| C1 | `b1a8031bf715bff43239e7f835d396f301f5d5a2`; revisión completa en `evidence/WP-015/revision-astra.md` | `WP015-F1` a `WP015-F8` | 2026-09-27 | `abierto` | Corrección aún no iniciada; HEAD y coste se registrarán al cerrarlo |

Este archivo debe quedar comprometido en la rama antes de enviar los hallazgos
al autor. Al terminar C1 se sustituirá `abierto` por el resultado, el HEAD y el
coste de la pasada; cualquier defecto nuevo o corrección incompleta se tratará
en la revalidación enfocada de la misma Astra.
