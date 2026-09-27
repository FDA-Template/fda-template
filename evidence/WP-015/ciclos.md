# WP-015 — Registro de ciclos de corrección

Conforme a [`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§4 y [`docs/manual/02-ciclo-de-un-wp.md`](../../docs/manual/02-ciclo-de-un-wp.md).

**Presupuesto de ciclos del contrato:** `max_ciclos_correccion: 2`.

**Estado actual: `C2 abierto` (`2 / 2`, último ciclo permitido).**

La implementación inicial no consumió ciclo. La única revisión completa de
Astra sobre el candidato `b1a8031bf715bff43239e7f835d396f301f5d5a2`
concluyó `NO APTO` y autorizó los ocho hallazgos registrados en
`evidence/WP-015/revision-astra.md`. `C1` quedó abierto y versionado por este
registro antes de que Claude Code empezara ninguna corrección. La revalidación
enfocada de la misma Astra cerró cuatro hallazgos y dejó incompletos F2, F3, F4
y F6, por lo que justificó `C2`. Este registro abre y consume el último ciclo
antes de cualquier corrección de C2.

| Ciclo | Candidato y revisión de origen | Hallazgos autorizados | Fecha | Estado | Resultado / HEAD / coste |
|---|---|---|---|---|---|
| C1 | `b1a8031bf715bff43239e7f835d396f301f5d5a2`; revisión completa en `evidence/WP-015/revision-astra.md` | `WP015-F1` a `WP015-F8` | 2026-09-27 | `NO APTO tras revalidación enfocada` | `TESTED_HEAD=513d68c422a9d8380e0100944e7eb68d8f42ece9`; F1/F5/F7/F8 cerrados; F2/F3/F4/F6 pasan a C2; coste C1 `8.905483599999997 USD` = `7.68 EUR` |
| C2 | `ce17110a71c39eb6533ae54ca438ededf765fceb`; revalidación enfocada de C1 en `evidence/WP-015/revision-astra.md` | `WP015-F2`, `WP015-F3`, `WP015-F4`, `WP015-F6` | 2026-09-27 | `abierto` | Corrección aún no iniciada; HEAD y coste se registrarán al terminar |

La apertura de C1 quedó comprometida en
`9d5d5dee4bf416786b26ee53e22917a227ccc7c1`. Esta apertura de C2 debe quedar
comprometida antes de devolver los cuatro puntos al autor. Tras C2 no se abre
un tercer ciclo: cualquier incumplimiento restante obliga a parar y dividir,
replantear o cerrar `blocked` mediante una decisión humana nueva.
