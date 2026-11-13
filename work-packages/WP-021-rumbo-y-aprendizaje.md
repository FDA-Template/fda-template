# WP-021 — Mantener el rumbo mediante el trabajo existente

estado: in_review
prioridad: P0
agente_responsable: coordinación documental delegada por el operador
agente_revisor: GPT-6 Astra high, contexto nuevo y solo lectura, autorizada
requisitos: objetivo de DEC-018 y encargo humano del 13-11-2026
adr: no modifica ADR; no cambia runtime ni autonomía
presupuesto_max_eur: 0 # nueva facturación de proveedores; cuota Codex desconocida
max_ciclos_correccion: 2
base_git: 8b0615f367aa153d7b94cfc658845c274e49459d

## Objetivo y contexto

El siguiente encargo y su cierre muestran su relación con la utilidad del producto
y la FDA reutilizada o el problema demostrado del método; el coordinador puede
corregir prioridades sin abrir un informe, gate o aprobación adicionales.

Iván pide volver al objetivo compartido y prevenir desvíos sin ser extremadamente
restrictivos. Iván adopta el ajuste mediante «Autorizar el ajuste documental», respuesta a la
solicitud precisa registrada en evidence/WP-021/adopcion.json. El ID y la base
se han revalidado: main8b0615f y ninguna rama WP-021 existente.
La copia personal del repositorio permanece intacta.

## Alcance (incluido / fuera de alcance)

Incluido: parche exacto de tres documentos, revisión independiente documental,
verificación existente aplicable y una PR para fusión humana tras adopción.
Actualizar la foto de hitos con metadatos ya comprobados, sin código/datos privados.
Se usa una copia limpia de main; la carpeta personal permanece intacta.
La publicación solo procede tras comprobaciones y revisión conformes.

Fuera: producto, agentes, skills, CI, hooks, permisos, costes/ciclos anteriores,
ACTIVE, nuevas automatizaciones, instalación, APIs, micrófono o fusión.
No exige cambiar FDA en cada entrega ni alternar obligatoriamente producto/FDA.

## Archivos permitidos

- docs/03-hoja-de-ruta.md
- docs/manual/09-piloto-supervisado.md
- work-packages/_TEMPLATE.md
- work-packages/WP-021-rumbo-y-aprendizaje.md
- evidence/WP-021/**

## Archivos prohibidos

- .github/**
- .claude/**
- .agents/**
- .codex/**
- CLAUDE.md
- AGENTS.md
- CODEOWNERS
- work-packages/ACTIVE
- specs/adr/**
- specs/decisions/**
- scripts/**
- tests/**

## Contratos técnicos (interfaces, schemas, eventos, invariantes)

Sin cambio de interfaces o de la semántica ejecutable de la plantilla. Los dos
recordatorios son comentarios en secciones existentes. No hay nuevos checks,
paradas, cuotas o formularios. Las señales orientan prioridades; las paradas
vigentes de seguridad, contrato, alcance, coste y autoridad se conservan.
El cierre admite que no haya cambio necesario en FDA. Una subtarea técnica no
se contabiliza como un caso de uso independiente. La mejora real de FDA continúa
necesitando su propio alcance si afecta archivos fuera del encargo del producto.

## Entorno autorizado (herramientas, comandos, red, secretos)

Preparación de lectura GitHub y edición solo de copias temporales, stdlib y Git
para comprobar el parche. Sin ejecutar producto, proveedores, secretos o servicios.
La adopción humana agrupa acto documental desde reposo, preparación de rama,
aplicación de este parche, verificación, revisión Astra y C1/C2 si son necesarias,
y publicación de una PR solo conforme; fusión humana. No agrupa ampliaciones.
La decisión acepta cuota Codex desconocida para esta única entrega;
no reabre la operación ordinaria ni reutiliza permisos de WP-019/020/voice-WP014.
Cuota Codex desconocida, no gratuita; 0 EUR de facturación adicional de proveedores.

## Verificación (comandos de validación + criterios de aceptación medibles)

La preparación comprueba que propuesta.diff aplica sobre tres copias exactas de
la base y produce los hashes candidatos. Esta comprobación no es APTO de PR.
Para la materialización se fijan estos comandos existentes, en orden, desde el
repo limpio y con WP-ID explícito. No se ejecutan ni se declaran verdes desde
este borrador:

```bash
git diff --check 8b0615f367aa153d7b94cfc658845c274e49459d
bash tests/governance/check-active.sh
python3 evidence/WP-000/checks/check-manual.py
python3 scripts/check_scope.py WP-021 "${WP021_CONTRACT_BASE:?}...HEAD"
```

WP021_CONTRACT_BASE será el SHA del primer commit solo contractual; se registra
en evidence/WP-021/CONTRACT_BASE antes del parche. Comprobar también que ese
commit solo añade el contrato y que ACTIVE/prohibidos se conservan contra la base.
No hay validador nuevo. Las comprobaciones del borrador no sustituyen estos
comandos ni la revisión independiente antes de publicar una PR.

Aceptación de la propuesta:
- Tres documentos normativos/procedimentales y ninguna dependencia nuevos.
- Vínculo objetivo/producto/FDA y cierre breve dentro de secciones existentes.
- Ninguna alternancia, porcentaje fijo, nuevo gate o mejora de FDA obligatoria.
- Prioridad diferenciada de parada por incumplimiento; reglas vigentes intactas.
- Metadatos de hitos contrastados, sin código, datos, saldos o claves privados.
- La aplicación futura exige una sola entrega documental y revisión independiente.

## Evidencias exigidas (qué debe aparecer en evidence/WP-XXX/)

Encargo/adopción, base y parche, fuentes de hitos, verificación completa y coste
real conocido o desconocido. No repetir expedientes históricos ni copiar logs
privados de producto. El coste de esta preparación y revisión no se presume cero.

## Condiciones de parada específicas

No aplicar el parche hasta DoR y revisión documental conformes. Conflicto real con
una decisión vigente, necesidad de nueva precedencia, fuera de alcance o tercer
ciclo: concretar la decisión necesaria; no expandir el cambio por propia iniciativa.

## Migración / rollback

Sin migración. Descartar antes de integración no cambia las normas oficiales.
Después de integración, revertir la composición documental sin borrar historial.
No se afirma una garantía automática de alineación: es disciplina comprobable
mediante contrato, cierre, revisión y evidencia. Deuda nueva propuesta: ninguna.

## Autoridad documental adoptada

La decisión humana del 13-11-2026 autoriza este único acto desde reposo,
conservando ACTIVE, sin cambios de agentes, controles, permisos o producto.
No reabre operación ordinaria ni hereda excepciones de otros WPs. Se aplica el
parche exacto preparado y revisado; revisión Astra high independiente, C1/C2
si son necesarias y PR solo conforme. Fusión exclusivamente humana. Los gates
pendientes se acreditan antes de cada fase; nadie obtiene autoridad del dictamen.
