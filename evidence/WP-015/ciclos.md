# WP-015 — Registro de ciclos de corrección

Conforme a [`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§4 y [`docs/manual/02-ciclo-de-un-wp.md`](../../docs/manual/02-ciclo-de-un-wp.md).

**Presupuesto de ciclos del contrato:** `max_ciclos_correccion: 2`.

**Estado actual: `C2 corregido; revalidación enfocada final pendiente` (`2 / 2`).**

La implementación inicial no consumió ciclo. La única revisión completa de
Astra sobre el candidato `b1a8031bf715bff43239e7f835d396f301f5d5a2`
concluyó `NO APTO` y autorizó los ocho hallazgos registrados en
`evidence/WP-015/revision-astra.md`. `C1` quedó abierto y versionado por este
registro antes de que Claude Code empezara ninguna corrección. La revalidación
enfocada de la misma Astra cerró cuatro hallazgos y dejó incompletos F2, F3, F4
y F6, por lo que justificó `C2`. La apertura quedó comprometida antes de
corregir y la pasada terminó con código, pruebas y evidencias verificadas. No
queda ningún ciclo disponible.

| Ciclo | Candidato y revisión de origen | Hallazgos autorizados | Fecha | Estado | Resultado / HEAD / coste |
|---|---|---|---|---|---|
| C1 | `b1a8031bf715bff43239e7f835d396f301f5d5a2`; revisión completa en `evidence/WP-015/revision-astra.md` | `WP015-F1` a `WP015-F8` | 2026-09-27 | `NO APTO tras revalidación enfocada` | `TESTED_HEAD=513d68c422a9d8380e0100944e7eb68d8f42ece9`; F1/F5/F7/F8 cerrados; F2/F3/F4/F6 pasan a C2; coste C1 `8.905483599999997 USD` = `7.68 EUR` |
| C2 | `ce17110a71c39eb6533ae54ca438ededf765fceb`; revalidación enfocada de C1 en `evidence/WP-015/revision-astra.md` | `WP015-F2`, `WP015-F3`, `WP015-F4`, `WP015-F6` | 2026-09-27 | `corregido; revalidación final pendiente` | `TESTED_HEAD=a855c2f2505a0a1a92310d71218444d6a0987bff`; árbol `8f04016927bed6b21a284ad25ab198536e8675f4`; 152/152 y doce comandos literales en verde; coste C2 `5.9228439999999996 USD` = `5.11 EUR` |

La apertura de C1 quedó comprometida en
`9d5d5dee4bf416786b26ee53e22917a227ccc7c1` y la de C2 en
`d59c9c64d0401032768530cea8010dff2f314ccf`, ambas
antes de sus correcciones. Tras esta revalidación no se abre un tercer ciclo:
cualquier incumplimiento restante obliga a parar y dividir, replantear o
cerrar `blocked` mediante una decisión humana nueva.
