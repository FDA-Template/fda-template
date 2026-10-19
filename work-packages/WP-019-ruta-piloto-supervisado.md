# WP-019 — Ruta de entregas supervisadas y primer piloto

estado: in_review
prioridad: P0
agente_responsable: operador_delegado_codex
agente_revisor: code-reviewer
requisitos: [REQ-FDA-001, REQ-FDA-002, SEC-001]
adr: [ADR-001]
presupuesto_max_eur: 0
max_ciclos_correccion: 2

## Objetivo y contexto

La hoja de ruta permite preparar una primera entrega externa supervisada antes
de completar la operación autónoma, con garantías verificables, decisiones
técnicas explicadas y medición del resultado. El primer candidato es corregir
la búsqueda de documentos anidados del validador de `ivanes189/knowledge-base`.

Encargo directo del operador de 2026-10-19: «lleva a cabo las modificaciones
que sean necesarias en nuestra actual hoja de ruta para adecuarla al nuevo
camino/método [...] y comencemos a trabajar». Este WP registra ese encargo
normativo delegado; no se presenta como ejecución ordinaria del runtime.
Base: `91d4a7c8af855ebac146c59310e44a20a8e160e4`. Rama dedicada:
`wp/WP-019-ruta-piloto-supervisado`. La copia de trabajo anterior se preserva.

**Parada de permisos, 2026-10-19:** la revisión automática rechazó materializar
DEC-018 y el manual por considerar insuficientemente precisa la autorización
general para enmendar pausa y costes. Se solicitó autorización para esos dos
cambios. Esa parada queda resuelta por la respuesta posterior del operador
«Autorizar ambos cambios acotados», registrada en
`evidence/WP-019/autorizacion.md`. Se reanuda la misma composición y el mismo
presupuesto; no se reinician ciclos ni se amplía el alcance. La vigencia del
modo experimental sigue dependiendo de la fusión humana.

## Alcance (incluido / fuera de alcance)

Incluido: una composición documental de operador, decisión de precedencia,
manual breve, contexto de entrada actualizado y preparación verificable del
primer piloto. Una sola PR; aprobación de integración y fusión humanas.

Fuera: implementar el piloto externo, invocar APIs de pago o Claude CLI,
contratar servicios, desplegar, cambiar CI, credenciales, permisos o hooks,
activar WPs técnicos, reabrir WP-018/OF1, alterar evidencias históricas o limpiar
worktrees. No se acredita aislamiento del piloto ni rentabilidad por escribir
esta documentación.

## Archivos permitidos

- CLAUDE.md
- docs/03-hoja-de-ruta.md
- docs/manual/MANUAL.md
- docs/manual/02-ciclo-de-un-wp.md
- docs/manual/04-agentes.md
- docs/manual/05-bloqueos-y-parada.md
- docs/manual/06-costes-y-metricas.md
- docs/manual/09-piloto-supervisado.md
- specs/decisions/DEC-003-pausa-migracion-y-contencion.md
- specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md
- specs/decisions/DEC-018-entregas-supervisadas.md
- work-packages/WP-019-ruta-piloto-supervisado.md
- evidence/WP-019/**

## Archivos prohibidos

- .github/**
- .claude/**
- .agents/**
- .codex/**
- CODEOWNERS
- work-packages/ACTIVE
- scripts/**
- tests/**
- tests/guard/run-suite.sh
- specs/adr/**

## Contratos técnicos (interfaces, schemas, eventos, invariantes)

Cambio normativo T3, sin código de producto. DEC-018 delimita qué decisiones
previas se enmiendan y mantiene las restricciones fuera de su ámbito. No cambia
ADR-001, el runtime de implementación ni sus criterios de orquestación futura.
`ACTIVE` permanece en reposo: las escrituras son el acto documental delegado
del operador; el guard no se desactiva ni se presenta como autorización de
estas escrituras. El modo experimental no acredita salida de la pausa.

## Entorno autorizado (herramientas, comandos, red, secretos)

- Herramientas: lectura, edición documental, Git local, revisión independiente.
- Comandos: Python 3 de biblioteca estándar, bash y Git para comprobaciones.
- Red: lectura GitHub de FDA y knowledge-base; publicación de esta rama y su PR.
- Secretos: ninguno. No leer credenciales ni contenido comercial de la base.
- Gasto adicional autorizado: 0 EUR; no nuevas invocaciones facturables ni
  recursos. El consumo de cuota de esta sesión y su revisión se declara
  desconocido cuando no hay dato atribuible; no se convierte en coste cero.
- La candidata propone tratar separadamente conformidad documental y resultado
  económico, con precedencia limitada y explícita sobre DEC-004 §11, pendiente
  de aceptación humana de DEC-018. No modifica cuentas históricas ni permite
  ejecutar trabajo facturable con coste desconocido.

## Verificación (comandos de validación + criterios de aceptación)

Desde la raíz, con WP-ID explícito WP-019:

```bash
git diff --check 91d4a7c8af855ebac146c59310e44a20a8e160e4
bash tests/governance/check-active.sh
python3 evidence/WP-000/checks/check-manual.py
python3 scripts/check_scope.py WP-019 "${WP019_CONTRACT_BASE:?}...HEAD"
```

`WP019_CONTRACT_BASE` es el SHA del commit inicial que fija este contrato,
registrado en `evidence/WP-019/CONTRACT_BASE` antes de implementar. Ese primer
commit solo contiene el contrato; la revisión comprueba también ese alcance.
El verificador existente lee el contrato del merge-base, nunca de la candidata.
No se instala un control nuevo ni se acredita bloqueo de integración en CI.

Criterios de aceptación:
1. Ruta vigente breve con primera entrega, siguientes pasos y límites temporales
   que empiezan antes de cerrar la pausa; historial preservado en Git.
2. DEC-018 y manual explicitan autorización, aislamiento previo, presupuesto,
   datos, revisión, correcciones, integración humana y diferencias entre
   preparar, ejecutar, integrar y poner en producción.
3. Ningún texto nuevo declara WP-018 resuelto, piloto ejecutado, aislamiento
   instalado ni aprobación económica inexistente.
4. Decisiones tecnológicas consideran reutilización, coste de mantenimiento,
   capacidad esperada y reversibilidad; no prometen una elección óptima.
5. Primer piloto preparado con referencia de origen y aceptación concreta;
   sin copiar datos ni código privado al repositorio público de FDA.
6. Comandos en verde; revisión independiente técnica y de seguridad sin
   bloqueantes; coste y limitaciones declarados; `ACTIVE` y prohibidos intactos.

## Condiciones de parada específicas

Fuera de alcance, gasto adicional, ejecución de candidata histórica, necesidad
de modificar controles ejecutables o ADR, o tercer ciclo: detener y replantear.
La incorporación del nuevo modo depende de la fusión humana de esta PR; no se
utiliza una propuesta aún no integrada para ejecutar el piloto.

## Migración / rollback

Sin migración de datos. Revertir conjuntamente la composición documental.
Si después se abre un piloto, detenerlo antes de retirar su marco; no restaurar
automáticamente autoridad ni candidatas antiguas. Deuda: las barreras de
operación autónoma siguen pendientes; la medición económica de la sesión no
está disponible y no se atribuye ahorro.
