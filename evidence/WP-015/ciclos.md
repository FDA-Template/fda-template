# WP-015 — Registro de ciclos de corrección

Conforme a [`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§4 y [`docs/manual/02-ciclo-de-un-wp.md`](../../docs/manual/02-ciclo-de-un-wp.md).

**Presupuesto de ciclos del contrato:** `max_ciclos_correccion: 2`.

**Estado actual: `C3 excepcional abierto` (`2 / 3`; C3 pendiente de
corrección).**

La implementación inicial no consumió ciclo. La única revisión completa de
Astra sobre el candidato `b1a8031bf715bff43239e7f835d396f301f5d5a2`
concluyó `NO APTO` y autorizó los ocho hallazgos registrados en
`evidence/WP-015/revision-astra.md`. `C1` quedó abierto y versionado por este
registro antes de que Claude Code empezara ninguna corrección. La revalidación
enfocada de la misma Astra cerró cuatro hallazgos y dejó incompletos F2, F3, F4
y F6, por lo que justificó `C2`. La apertura quedó comprometida antes de
corregir y la pasada terminó con código, pruebas y evidencias verificadas. La
revalidación final cerró F3, F4 y F6, pero dejó F2 incompleto por una regresión
de configuración local inefectiva. No quedaba ningún ciclo ordinario;
`DEC-013` habilitó después el C3 excepcional registrado abajo.

| Ciclo | Candidato y revisión de origen | Hallazgos autorizados | Fecha | Estado | Resultado / HEAD / coste |
|---|---|---|---|---|---|
| C1 | `b1a8031bf715bff43239e7f835d396f301f5d5a2`; revisión completa en `evidence/WP-015/revision-astra.md` | `WP015-F1` a `WP015-F8` | 2026-09-27 | `NO APTO tras revalidación enfocada` | `TESTED_HEAD=513d68c422a9d8380e0100944e7eb68d8f42ece9`; F1/F5/F7/F8 cerrados; F2/F3/F4/F6 pasan a C2; coste C1 `8.905483599999997 USD` = `7.68 EUR` |
| C2 | `ce17110a71c39eb6533ae54ca438ededf765fceb`; revalidación enfocada de C1 en `evidence/WP-015/revision-astra.md` | `WP015-F2`, `WP015-F3`, `WP015-F4`, `WP015-F6` | 2026-09-27 | `NO APTO; ciclos agotados` | `TESTED_HEAD=a855c2f2505a0a1a92310d71218444d6a0987bff`; F3/F4/F6 cerrados; F2 residual: fixture local no activa `ignore=all`; coste C2 `5.9228439999999996 USD` = `5.11 EUR`; candidato revalidado `935c3cbc6e366231aa2b69d919100a4178e9da34` |
| C3 | `4ad9eb354e3ff13c0a936be6c8a0eee691e44246`; revalidación enfocada final de C2 en `evidence/WP-015/revision-astra.md`; autoridad `DEC-013` fusionada en `7d1b26afcb3285e29ee17dee7548b34351948330` | Residual cerrado `WP015-F2`: asociación `path = vendor` y sensibilidad efectiva del fixture de configuración local | 2026-09-27 | `abierto` | Merge previo sin reescritura `9b66c8e75b1aa37574b151bb5821ef9dc648d9a7`; presupuesto adicional máximo `6.00 EUR`; techo acumulado `28.29 EUR`; corrección pendiente |

La apertura de C1 quedó comprometida en
`9d5d5dee4bf416786b26ee53e22917a227ccc7c1` y la de C2 en
`d59c9c64d0401032768530cea8010dff2f314ccf`, ambas
antes de sus correcciones. `DEC-013`, fechada y fusionada antes de esta fila,
concede exclusivamente C3 para el residual `WP015-F2`. La fila se versiona
antes de cualquier corrección de Claude Code. C3 no reinicia la cuenta, no
reabre los hallazgos cerrados y no autoriza C4.
