# WP-020 — Preparar una excepción de autoría Codex supervisada

estado: in_progress
prioridad: P0
agente_responsable: operador_delegado_codex
agente_revisor: GPT-6 Astra, razonamiento Alto, independiente y solo lectura
requisitos: [REQ-FDA-001, REQ-FDA-002, SEC-001]
adr: [ADR-001, ADR-002 propuesto]
presupuesto_max_eur: 0
max_ciclos_correccion: 2

## Objetivo y contexto

Existe una propuesta completa y revisada para permitir que Codex termine una
única entrega externa de acceso local sin audio, con Astra como revisora,
sin ejecutar esa continuación ni alterar el historial del intento bloqueado.
El operador puede decidir sobre el cambio de autor, coste desconocido y
diferencia de controles con información concreta, sin elegir tecnología por
intuición ni aceptar riesgos por silencio.

Base FDA verificada en GitHub el 2026-10-23:
0205556be8ad9cd7993feeddd0b4347694cf37f8, main. Rama dedicada:
wp/WP-020-excepcion-autoria-codex. Siguiente ID libre comprobado en esa base.
La copia de trabajo personal y el expediente externo se preservan intactos.

Autorización directa: ante la pregunta de preparar una excepción para autoría
Codex y revisión Astra, solo normas y contrato, sin otra llamada Claude ni
programación, Iván respondió «ok, adelante.». El recibo íntegro se conserva
en evidence/WP-020/autorizacion.md. Este es el acto documental delegado del
operador, no ejecución ordinaria ni una aprobación de la propuesta futura.

## Alcance (incluido / fuera de alcance)

Incluido: propuesta ADR-002, decisión de preparación y precedencia DEC-019,
avisos mínimos de coherencia en ocho documentos existentes, contrato futuro
en borrador bajo evidencia, comprobación de capacidades sin producto y una
revisión independiente T3 con lente de seguridad. Un resultado documental.

Fuera: escribir o ejecutar producto, modificar el expediente externo, crear
un WP activo allí, abrir C4, otra invocación Claude, probar micrófono o voz,
llamar a proveedores, instalar herramientas, comprar, modificar permisos o
controles, publicar ramas/PR, fusionar o desplegar. Ninguna nueva plataforma.

## Archivos permitidos

- CLAUDE.md
- specs/adr/ADR-001-runtime.md
- specs/adr/ADR-002-autoria-codex-supervisada.md
- specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md
- specs/decisions/DEC-018-entregas-supervisadas.md
- specs/decisions/DEC-019-preparar-autoria-codex.md
- docs/manual/02-ciclo-de-un-wp.md
- docs/manual/04-agentes.md
- docs/manual/06-costes-y-metricas.md
- docs/manual/09-piloto-supervisado.md
- work-packages/WP-020-excepcion-autoria-codex.md
- evidence/WP-020/**

Nota: el primer commit añade únicamente este contrato. Después se fija su SHA
en evidence/WP-020/CONTRACT_BASE. El contrato no concede autoridad a su autor:
la preparación procede del encargo humano registrado arriba. ACTIVE no cambia.

## Archivos prohibidos

- .github/**
- .claude/**
- .agents/**
- .codex/**
- CODEOWNERS
- work-packages/ACTIVE
- scripts/**
- tests/**
- specs/finops/**
- evidence/WP-019/**

## Contratos técnicos (interfaces, schemas, eventos, invariantes)

1. La preparación y su revisión están autorizadas; adoptar la propuesta y
   ejecutarla no. ADR-002 y la parte prospectiva de DEC-019 son proposed.
   No entran en vigor por redactarlas, revisarlas o aprobarlas técnicamente.
2. La excepción propuesta identifica una sola instancia externa y conserva
   el régimen general Claude Code, pausa ordinaria e invariantes I1-I4.
   Su adopción requiere decisión humana específica y fusión humana posterior;
   la ejecución requiere autorización del contrato privado fijado y sus gates.
3. La misma entrega ya consumió C0/C1/C2/C3. Terminarla con otro autor es una
   C4 excepcional propuesta, no autorizada; no un WP nuevo con contador cero.
   El borrador incorpora origen parcial y hallazgos, costes e intentos previos.
4. Distinguir edición nativa supervisada de ejecución de código en Docker:
   el perfil actual tiene lecturas amplias, raíces de escritura más amplias
   que seis archivos y conectores. No afirmar ausencia técnica de credenciales
   del autor ni inmutabilidad física del evaluador frente a él. Lista de rutas,
   hashes y revisión post-hoc son controles de política/detección. Cualquier
   aceptación futura de esa diferencia exige decisión humana específica.
5. Mantener aislado el código bajo prueba: contenedor existente sin red, home,
   secretos o socket Docker montados; seis archivos de producto editables,
   evaluador y regresiones conservados. No ejecutar producto en el host.
   No modificar perfiles, hooks o herramientas para simular equivalencia.
6. El contrato futuro es solo borrador dentro de evidence/WP-020/. No incluye
   código ni datos privados. Conserva objetivo, interfaces, seis rutas y
   comandos de la entrega, aceptación independiente y PR solo tras APTO con
   autorización específica de publicación. No reduce calidad ni crea C5.
7. Cuota Codex de esta preparación/revisión: no_disponible, no gratuita.
   Conformidad documental no implica cierre económico. La posible excepción
   de cuota de autoría futura sigue propuesta; no se financia con euros
   inventados ni se permite otra llamada facturable. El techo original del
   piloto y sus consumos históricos no se reinician ni se amplían.

## Entorno autorizado (herramientas, comandos, red, secretos)

- Herramientas: lectura y edición documental, Git, Python stdlib, planner y
  una revisión Astra en contexto nuevo, solo lectura; sin autor externo.
- Comandos: comprobaciones existentes de gobierno, enlaces y alcance; consulta
  de versión del CLI sin autenticarlo y de metadatos de la imagen Docker ya
  existente. La versión del CLI no identifica el modelo del chat ni acredita
  haber ejecutado Codex como autor aislado.
- Red: lectura de GitHub y documentación oficial OpenAI; conexión de esta
  sesión/revisión a su proveedor. Sin publicación ni APIs del producto.
- Secretos: ninguno. No leer claves, credenciales, variables de entorno de
  autenticación, perfiles personales o archivos sensibles para comprobar acceso.
- Facturación adicional autorizada: 0 EUR. Cuota de suscripción y tiempo humano
  sin dato atribuible se registran desconocidos. No invocar Claude CLI ni otra
  API facturable; una revisión Codex consume cuota, no se presenta como gratuita.
- ACTIVE sigue byte a byte en reposo. La preparación es delegación documental
  del operador; no se desactiva ningún hook ni se declara que este la habilita.

## Verificación (comandos de validación + criterios de aceptación medibles)

Desde la raíz, WP-ID explícito WP-020, en este orden:

```bash
git diff --check 0205556be8ad9cd7993feeddd0b4347694cf37f8
bash tests/governance/check-active.sh
python3 evidence/WP-000/checks/check-manual.py
python3 scripts/check_scope.py WP-020 "${WP020_CONTRACT_BASE:?}...HEAD"
```

WP020_CONTRACT_BASE se lee de evidence/WP-020/CONTRACT_BASE, fijado tras el
primer commit exclusivamente contractual. El evaluador existente lee el
contrato del merge-base. Se comprueba también el diff del primer commit y las
rutas prohibidas contra la base. No se cambia ningún verificador para aprobar.

Criterios:
1. Recibo humano exacto, alcance y propuesta separados; no ejecución, publicación
   o aceptación de riesgo deducidas del permiso para preparar.
2. ADR/decisión acotan instancia, precedencia, adopción, futura autorización,
   rollback y continuidad C4 sin reinicio de intentos, costes o requisitos.
3. Capacidades documentadas con procedencia; diferencias nativas explícitas,
   prueba Docker no confundida con aislamiento del autor ni con entrega útil.
4. Borrador futuro completo: origen, rutas, comandos, hallazgos por cerrar,
   aceptación, actores, límites, costes desconocidos y paradas, sin producto
   ejecutado ni contrato activo. El modelo exacto no se inventa desde “Codex”.
5. No hay código/datos privados copiados al repositorio FDA, modificaciones
   del proyecto externo ni cambios en ACTIVE, controles o rutas prohibidas.
6. Manuales y avisos coherentes: régimen general conservado y excepción
   propuesta sin afirmación de coste cero, éxito, fusión o garantía inexistente.
7. Cuatro comandos en verde, alcance de ambos commits comprobado y revisión
   independiente Astra de contrato y seguridad sin hallazgos abiertos.

## Evidencias exigidas (qué debe aparecer en evidence/WP-020/)

Autorización, DoR del planner, CONTRACT_BASE, ciclos, coste, capacidad y fuentes,
borrador futuro, explicación para Iván, logs íntegros/códigos de cada comando,
evaluación de siete criterios y revisión Astra con candidata identificada.
Las evidencias de producto permanecen en su expediente privado original.

## Condiciones de parada específicas

No ejecutar producto o C4 por esta preparación. Fuera de allowlist, cambio de
control técnico, gasto adicional, necesidad de publicar o tercer ciclo de
corrección documental: parar y solicitar decisión. Antes de C1/C2, registrar
apertura versionada; invocaciones fallidas no borran ciclos. El dictamen
documental no acepta el riesgo propuesto ni concede autoría de producto.

## Migración / rollback

Sin migración, instalación ni cambios en producto. Descartar esta rama antes de
adopción; tras una eventual fusión, retirar conjuntamente la composición y
detener previamente cualquier continuación autorizada, sin restaurar autoridad
histórica por accidente. Deuda declarada: capacidad nativa sin confinamiento
físico por archivo, separación de credenciales del autor no acreditada y cuota
no atribuible. Son diferencias propuestas para decidir, no garantías instaladas.
