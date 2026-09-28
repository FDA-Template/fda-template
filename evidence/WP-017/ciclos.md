# WP-017 — Registro de ciclos de la candidata DOR-7

Conforme a [`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§§4, 5 y 8.3.

**Base de la candidata:**
`ec8cb8113df8c209e9340d9841192dd46cd11a5a`.

**Presupuesto ordinario del contrato:** `max_ciclos_correccion: 2`.

**Estado actual:** `NO APTO tras C2` (`2 / 2`; ciclos ordinarios agotados;
C3 no abierto).

Este archivo reconstruye únicamente la historia consumida de la candidata
externa de `WP017-DOR-7`. No inventa `HEAD`, huellas intermedias, invocaciones
ni costes que no quedaron versionados. Los hechos reconstruidos son los que
adopta normativamente DEC-010 §8.1: una única revisión completa abrió F1–F4;
C1 cerró F2–F4 y dejó F1; C2 mantuvo F1 como único residual.

| Ciclo | Candidato y revisión de origen | Hallazgos autorizados | Fecha | Estado | Resultado / huella / coste |
|---|---|---|---|---|---|
| C1 | Candidata externa inicial; revisión completa independiente adoptada por DEC-010 §8.1; sin `HEAD` ni huella intermedia versionados | `WP017-DOR7-F1` a `WP017-DOR7-F4` | 2026-09-28 · registro reconstruido | `NO APTO tras revalidación enfocada` | F2, F3 y F4 cerrados; F1 pasa a C2 por falta de autoridad para fijar la política IAM del secreto; coste no reconstruido |
| C2 | Revalidación enfocada de C1 adoptada por DEC-010 §8.1; sin `HEAD` ni huella intermedia versionados | `WP017-DOR7-F1` | 2026-09-28 · registro reconstruido | `NO APTO; ciclos ordinarios agotados` | Candidata final preservada `WP017-DOR7-candidata-NO-APTA-C2.patch`, SHA-256 `e4877b02a05ad65be1579d333758808393f3a6b4473e1b719ebaa43e8c4709a7`; postimagen WP-017 `ad2053893d7416a30a564c33416ddd7ac8e77220575f071906e8c0cb131086ee`; postimagen manual/05 `ae49c644cd7a2361b1ed7e251cf98e5cac1ed026cbb465ba86d1cc6f0cf37206`; bindings de proyecto condicionados incorporados, residual `PROJECT_ID` donde el nombre canónico IAM exige `PROJECT_NUMBER`; coste no reconstruido |

F2, F3 y F4 permanecen cerrados. No existe fila C3: este registro no abre la
pasada, no corrige F1 y no concede autoridad a Claude Code. Antes de C3 deben
incorporarse sin reescribir historia el `main` que contiene DEC-010 §8, quedar
fijado el coste acumulado verificable conforme a §8.5 y versionarse en un
commit posterior la fila C3 con estado `abierto`. Si cualquiera de esas
precondiciones falta o difiere, C3 no comienza.
