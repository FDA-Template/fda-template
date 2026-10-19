# WP-019 — Informe independiente

Fecha: 2026-10-19. Revisor: `review_wp019`, GPT-6 Astra, razonamiento Alto,
contexto nuevo, rol `code-reviewer`, solo lectura. Transcripción íntegra del
dictamen recibido; no es aprobación formal de GitHub ni fusión.

VEREDICTO: APRUEBA

**APTO documental para WP-019. Sin hallazgos bloqueantes, importantes o menores.**

Revisión completa independiente, de solo lectura, con lente conjunta de contrato, corrección documental y seguridad T3.

Identidad comprobada:

- Base: `91d4a7c8af855ebac146c59310e44a20a8e160e4`.
- Contrato congelado: `ffdf5d942222188b5a0c5461647185a506e7fe3b`.
- Contenido normativo: `6455f85437847cab8d7b392a5b07e61194cfc03e`.
- Candidata revisada: `15b2bdac07f50733be5af123a93f14c0afffa0b2`.

El primer commit añade exclusivamente el contrato. El diff completo contiene 20 archivos, todos permitidos. Los cambios posteriores del contrato se limitan al estado `in_review` y al registro de la autorización humana; no amplían su alcance. `ACTIVE` y todas las rutas prohibidas permanecen intactos.

| Criterio | Resultado y evidencia contrastada |
|---|---|
| 1. Ruta y plazos | Cumple. `docs/03-hoja-de-ruta.md:68` fija entregas y revisiones a dos y diez días desde la fusión, sin esperar al cierre general de la pausa. Conserva la versión anterior mediante referencia Git. |
| 2. Autorización y garantías | Cumple. `specs/decisions/DEC-018-entregas-supervisadas.md:8` y `docs/manual/09-piloto-supervisado.md:34` distinguen autorización, ejecución, aislamiento comprobado, presupuesto, publicación e integración humana. |
| 3. Ausencia de éxitos ficticios | Cumple. WP-018/OF1 siguen pendientes; el piloto y su aislamiento no se presentan como ejecutados o instalados. La cuota desconocida no se convierte en coste cero. |
| 4. Elección tecnológica | Cumple. `docs/03-hoja-de-ruta.md:54` exige reutilización, mantenimiento, capacidad, reversibilidad e incertidumbre declarada. |
| 5. Preparación del piloto | Cumple. Contrasté mediante GitHub el commit y blob citados en `evidence/WP-019/piloto-kb.md:6`: búsqueda y contador no recursivos, documentos anidados y prueba propuesta todavía inexistente. La aceptación es concreta; el diff FDA no incorpora código privado ni contenido comercial. |
| 6. Verificación y límites | Cumple documentalmente. Repetí las cuatro comprobaciones del WP: todas devolvieron `0`. Comprobé además prohibidos intactos y 147 enlaces locales sin roturas. |

`verificacion-final.json` corresponde al commit normativo indicado; el único cambio posterior es la incorporación de ese mismo archivo de evidencia. Las comprobaciones repetidas cubren la candidata exacta. No hay funciones nuevas de producto ni modificaciones de pruebas.

La precedencia queda acotada y respaldada por la autorización humana proporcionada: pausa experimental, autoría documental delegada y aptitud documental con cuota desconocida. No deriva autoridad del dictamen del autor ni de esta revisión.

**Límites del dictamen:** no constituye aprobación económica, fusión, autorización de gasto ni permiso para ejecutar el piloto. No acredita aislamiento instalado ni controles remotos actuales. No ejecuté Claude CLI, llamadas facturables, producto, infraestructura o mutaciones; tampoco modifiqué archivos. La cuota de esta revisión continúa desconocida y no se declara cero.
