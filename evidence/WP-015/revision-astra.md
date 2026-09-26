# WP-015 — Revisión independiente (GPT-6 Astra)

**Estado: pendiente.** Esta entrega es la implementación inicial del
candidato, entregada por Claude Code (implementer) como autor único, sobre
`TESTED_HEAD` = `718ce294fe592c2b6df7c13c5f56caea4199d7f2`. Conforme a
[`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md)
§1, el autor no se autorrevisa ni se autodeclara `APTO`: ese veredicto
corresponde en exclusiva a GPT-6 Astra, con razonamiento Alto, contexto
nuevo y modo estrictamente de solo lectura, sin recibir la conclusión del
autor como premisa.

Este archivo se completará, en su totalidad o mediante un archivo hermano
versionado en `evidence/WP-015/**`, cuando exista:

1. la revisión completa inicial de Astra sobre este candidato (contrato,
   corrección y seguridad, en una sola pasada, conforme a DEC-010 §2 y §6);
   y, si hubiera hallazgos,
2. las revalidaciones enfocadas de la misma Astra sobre las correcciones de
   `C1` y, si hiciera falta, `C2`, registradas en `evidence/WP-015/ciclos.md`.

Nada en este documento ni en el resto de la entrega afirma o insinúa un
veredicto `APTO`. No lo declara Claude Code: corresponde a Astra.

## Qué recibe Astra para su revisión completa

- El contrato: `work-packages/WP-015-check-scope-local.md` (sin
  modificaciones de este agente).
- Las normas citadas: `CLAUDE.md`, `REQ-FDA-001`, `ADR-001`, `DEC-002`,
  `DEC-003`, `DEC-007`, `DEC-010`, `DEC-011`, `DEC-012` y los manuales
  pertinentes (sin modificaciones de este agente, salvo
  `docs/manual/02-ciclo-de-un-wp.md`, que sí forma parte del candidato).
- El candidato: `scripts/check_scope.py`, `scripts/scope_rules.py`,
  `tests/scope/**` y `docs/manual/02-ciclo-de-un-wp.md`, en el estado exacto
  de `TESTED_HEAD` = `718ce294fe592c2b6df7c13c5f56caea4199d7f2`.
- Las pruebas y su salida íntegra: `evidence/WP-015/verification.md`,
  `corpus.md`, `fuente-confianza.md`, `symlinks.md`, `aislamiento.md` y
  `seguridad.md`.
- Los bloqueos declarados sin fabricar evidencia: el resultado externo del
  job `Escaneo de secretos` (pendiente de captura por una persona con acceso
  a GitHub, ver `seguridad.md` §2) y la medición estructurada de coste F1/F2
  o F3 con base concreta (ver `cost.md`).
