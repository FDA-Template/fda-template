# DEC-018 — Validar la FDA mediante entregas supervisadas

**Fecha:** 2026-10-19. **Estado:** autorizada para materialización y revisión;
vigencia operativa únicamente tras fusión humana de la composición en `main`.
**Ámbito:** WP-019 y el modo de piloto externo supervisado. No declara habilitada
la fábrica autónoma ni concede presupuesto a un piloto concreto.

## 1. Autoridad y entrada en vigor

El operador encargó cambiar la hoja de ruta y, ante la parada de permisos,
autorizó expresamente las dos enmiendas: piloto supervisado antes del cierre
general de la pausa y revisión de esta reforma con cuota Codex desconocida,
sin coste cero ficticio ni llamadas facturables con coste desconocido. La
respuesta «Autorizar ambos cambios acotados» y su pregunta están registradas en
[la autorización](../../evidence/WP-019/autorizacion.md).

[WP-019](../../work-packages/WP-019-ruta-piloto-supervisado.md) fija base, alcance,
límites y verificación de la composición documental delegada a Codex. Se puede
preparar, revisar y publicar su rama y PR; el agente no puede fusionar.
La autoridad procede del operador, no de este texto ni del dictamen de un agente.

El régimen nuevo entra en vigor únicamente al fusionarse humanamente la
composición completa en `main`. Hasta entonces no ampara ejecución externa.
La integración registrada en Git acredita esa vigencia; después se registra
el cierre de WP-019, sin confundirlo con entrega o ejecución del piloto.

## 2. Precedencia cerrada

La composición enmienda únicamente lo siguiente:

- **DEC-003 §§2, 4 y 6; DEC-007 D1/D2/D6; DEC-009/011 y la secuencia de v2:**
  el cierre integral de la pausa deja de ser requisito para preparar y, tras sus
  gates propios, ejecutar el piloto supervisado. WP-019 se añade a los actos
  documentales de operador admitidos desde reposo. La pausa y sus condiciones
  de salida siguen rigiendo la operación ordinaria/autónoma. No se altera la
  congelación de `tests/guard/run-suite.sh` ni la cuarentena de adaptaciones
  locales de runtimes.
- **DEC-010 §§1, 3, 4 y 6:** WP-019 es autoría documental delegada a Codex;
  no es implementación ordinaria de Claude Code ni validación de otro runtime.
  Conserva revisión Astra con contexto nuevo, solo lectura y lente de seguridad,
  una revisión completa y hasta C1/C2 enfocados por la misma revisora. El futuro
  piloto puede agrupar autorizaciones para pasos reversibles enumerados en su
  contrato, incluyendo publicación y PR, sin agrupar fusión, despliegue,
  permisos, gasto nuevo o ampliación del alcance. Los ciclos siguen contando
  desde el comienzo de cada corrección, incluso fallida; no se reclasifican
  retrospectivamente. WP-019 se corrige por el mismo autor delegado.
- **DEC-004 §11, exclusivamente para WP-019:** la cuota no atribuible de la
  sesión se declara `no_disponible`. Por la autorización precisa del operador,
  la revisión puede emitir **APTO documental** y preparar la PR de esta reforma
  sin declarar cierre económico ni coste cero. No es un registro F1/F2/F3, una
  excepción de facturación ni un cierre del WP bajo el régimen económico
  ordinario. No permite invocaciones facturables con coste desconocido ni
  modifica costes o rechazos históricos. Fuera de WP-019, DEC-001/004 siguen
  aplicando; un piloto necesita su presupuesto y medición antes de ejecutar.
- **Lectura y prioridad de CLAUDE.md/hoja v2:** entrada breve vigente, manual
  del modo y contrato, seguidos de decisiones relevantes. El historial sigue
  disponible; no se elimina su autoridad aplicable por no leerlo íntegramente.
  El clasificador ejecutable de v2 deja de ser prerrequisito del piloto: su WP
  registra riesgo y justificación, revisados independientemente.

DEC-014/015/016/017 y DEC-010 §§8–21 siguen gobernando sus trabajos históricos.
WP-016/018 y OF1 se posponen como prioridad, no se cierran `done`, no se reabren
ni se renumeran sus ciclos. ADR-001 y sus invariantes no cambian: Claude Code
continúa siendo el runtime de implementación; Codex puede ser la entrada y la
coordinación, sin utilizar adaptaciones locales en cuarentena para implementar.

## 3. Composición de WP-019 y límites presentes

Viajan en una única PR los doce documentos enumerados en el alcance de WP-019
y sus evidencias bajo `evidence/WP-019/`. El contrato se fija en un primer commit
para usar el verificador local existente sobre la composición posterior.
`ACTIVE` se conserva byte a byte en reposo. El estado de WP-019 describe el
encargo de operador; no implica que el runtime ordinario esté activo.

No se cambian agentes, hooks, settings, workflows, `CODEOWNERS`, permisos,
infraestructura, código de producto ni contratos históricos. Los avisos de
precedencia en DEC-003/010 no borran su contenido previo. Las correcciones de
descripción de controles en el manual no implantan esos controles.

Presupuesto adicional autorizado: **0 EUR**. No se invoca Claude CLI ni APIs
facturables, no se contratan servicios y no se despachan workflows de agentes.
La cuota de autor/revisor y minutos humanos sin medición atribuible se declaran
desconocidos. No se hace una afirmación de gasto global cero.

## 4. Qué permite el piloto una vez integrado este marco

Se puede preparar un encargo pequeño en un repositorio destinatario, con base
fijada, archivos exactos, pruebas y resultado demostrable. No requiere instalar
toda la plantilla, resolver WP-018 ni cerrar la pausa. El expediente se guarda
en el repositorio destinatario con su misma visibilidad, nunca copiando datos
o código privado al repositorio público FDA.

Antes de ejecutar deben quedar acreditados todos los gates del
[manual 09](../../docs/manual/09-piloto-supervisado.md): autorización del WP,
presupuesto/medición, runtime, entorno aislado, datos y verificación. Si falta
uno, solo continúa preparación de lectura y definición; no se ejecuta código
del producto ni se concede autoridad por calendario o por este documento.

El primer candidato es el descubrimiento de Markdown anidado en
`ivanes189/knowledge-base`; su preparación está en
[piloto-kb.md](../../evidence/WP-019/piloto-kb.md). WP-019 no crea un contrato
ejecutable allí, no reserva otro WP-ID y no autoriza escribir en ese proyecto.

## 5. Flujo y seguridad

El operador expresa la necesidad y prioridades. El agente inspecciona el
proyecto, aclara decisiones de negocio, recomienda la alternativa técnica
proporcionada y prepara el contrato. Una autorización cerrada puede incluir
la implementación, pruebas, C1/C2 y PR enumeradas en ese contrato.

No hay fusión automática. El implementador no recibe credenciales para fusionar,
desplegar o administrar. La publicación de rama/PR corresponde al operador o
coordinador con autorización específica del WP, fuera del entorno ejecutor;
el contenido exportado se revisa antes de publicarlo. Una política escrita o
un worktree no acreditan esa separación técnica.

Seguridad, integridad de datos y pruebas falsamente verdes bloquean. Las mejoras
laterales se registran sin ampliar la entrega. Se conserva el límite ordinario
de dos correcciones y la parada ante tercero, ADR, alcance, gasto o riesgo nuevo.

## 6. Resultado y revisión de la decisión

Dos días laborables desde la fusión: revisar preparación si no hay primer WP
listo. Diez días laborables: balance del experimento, incluso con cero entregas.
Registrar entregas, bloqueos, tiempo humano, consumo, revisiones, errores e
incidentes. No hay continuación o autorización automática por vencer el plazo.

Hasta cinco tareas reales sirven de muestra exploratoria. Cada una debe tener
utilidad propia. Tras la primera entrega técnica se prioriza un recorrido útil
de AI-Comercial-System; Agent OS emerge de necesidades repetidas, no de un
catálogo previo. No abrir dos WPs consecutivos de FDA sin entrega externa,
salvo excepción de seguridad concreta, registrada y limitada.

## 7. Riesgos, deuda y reversión

Riesgos: confundir propuesta con autorización ejecutable, revisión humana con
aislamiento técnico, y consumo de cuota desconocido con gratuidad. Los gates,
el inventario de capacidades y la revisión independiente deben detectar esas
confusiones. Continúan pendientes las barreras de integración autónoma y la
medición económica completa; no se presentan como deuda saldada.

Reversión: revertir la composición conjuntamente. Si hay un piloto posterior
abierto, detenerlo y preservar sus resultados antes de retirar su marco. No se
restauran permisos, presupuestos ni candidatas históricas automáticamente.
