# WP-015 — Registro de ciclos de corrección

Conforme a [`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§4 y [`docs/manual/02-ciclo-de-un-wp.md`](../../docs/manual/02-ciclo-de-un-wp.md).

**Presupuesto de ciclos del contrato:** `max_ciclos_correccion: 2`.

**Estado actual: `C1 corregido; revalidación enfocada pendiente` (`1 / 2`).**

La implementación inicial no consumió ciclo. La única revisión completa de
Astra sobre el candidato `b1a8031bf715bff43239e7f835d396f301f5d5a2`
concluyó `NO APTO` y autorizó los ocho hallazgos registrados en
`evidence/WP-015/revision-astra.md`. `C1` quedó abierto y versionado por este
registro antes de que Claude Code empezara ninguna corrección. La pasada ya
terminó; no se abre C2 salvo que la revalidación enfocada de la misma Astra lo
justifique.

| Ciclo | Candidato y revisión de origen | Hallazgos autorizados | Fecha | Estado | Resultado / HEAD / coste |
|---|---|---|---|---|---|
| C1 | `b1a8031bf715bff43239e7f835d396f301f5d5a2`; revisión completa en `evidence/WP-015/revision-astra.md` | `WP015-F1` a `WP015-F8` | 2026-09-27 | `corregido; revalidación pendiente` | `TESTED_HEAD=513d68c422a9d8380e0100944e7eb68d8f42ece9`; árbol `b25e195b072432001c3552c9518a684fa8f632b6`; evidencia de autor `ab8fd84a7bdd01aea05814dd5fec26c7b57d5932`; coste C1 `8.905483599999997 USD` = `7.68 EUR`; 134/134 y doce comandos literales en verde |

El registro de apertura quedó comprometido en `9d5d5dee4bf416786b26ee53e22917a227ccc7c1`
antes de enviar los hallazgos al autor. Cualquier defecto nuevo o corrección
incompleta se tratará únicamente en la revalidación enfocada de la misma Astra.
