# DEC-014 — Reserva y límites del sucesor limpio de WP-005

**Estado propuesto:** aceptada únicamente si esta composición se materializa y
fusiona humanamente.
**Fecha propuesta:** 2026-09-27.
**Base:** `origin/main`
`47c4e92a04e17370116fa54b07bf4a35bd6904be`.

**Enmendada el 2026-09-27 por
[`DEC-015`](DEC-015-productor-externo-check-scope.md):** elige una GitHub App
externa como productor previo, distingue seguridad de disponibilidad y fija la
semántica monotónica de la autorización; no modifica WP-016 ni reserva otro
WP-ID.
**Enmendada el 2026-09-27 por
[`DEC-016`](DEC-016-reserva-productor-externo-alcance.md):** reserva `WP-017`
para ese productor previo, todavía sin contrato, y no modifica los gates ni el
estado de WP-016.
**Enmendada el 2026-09-28 por
[`DEC-017`](DEC-017-reserva-sucesor-limpio-wp017.md):** WP-017 queda `blocked`
y `WP-018` se reserva como sucesor limpio del productor previo, sin modificar
los gates ni el estado de WP-016.

Los rótulos `DEC-014` y `WP-016` son propuestas sin efecto normativo hasta esa
eventual fusión.

## Problema

WP-015 está `done` y acredita solo `scripts/check_scope.py` y
`scripts/scope_rules.py` como ejecutable local y biblioteca única. `ACTIVE`
está en reposo. El job de alcance no existe en CI y el ruleset activo no
requiere `check_scope`.

WP-005 permanece `draft`, histórico y no ejecutable. DEC-003 dice que será
sustituido por un sucesor limpio todavía sin identificador ni admisión.
Redactar directamente un `WP-NNN` elegiría el identificador y anticiparía un
contrato sin el acto que enmiende la lista cerrada de DEC-003.

La documentación vigente de GitHub obliga además a mantener separadas estas
realidades:

- un job saltado puede presentarse como `Success`;
- un workflow `pull_request` suprimido por filtros o `[skip ci]` queda
  `Pending`;
- un required status check puede fijar `context` e `integration_id`;
- el listado de historia entrega `version_id`, actor y `updated_at`, mientras
  la versión concreta entrega `state`;
- los endpoints de historia y versión y la mutación requieren actualmente
  `Administration: write`.

REQ-FDA-002 prohíbe actualmente `pull_request_target`. Esta decisión no
resuelve de forma implícita esa tensión.

## Decisión

### 1. Reserva condicionada

Al entrar esta composición en `main`, se reserva inequívocamente `WP-016` como
único identificador del sucesor limpio de WP-005.

Antes de esa fusión, `WP-016` no está reservado. WP-005 continúa `draft` como
historia y no se modifica ni se reactiva.

La reserva no:

- crea el archivo de contrato;
- lo deja `ready`;
- lo admite para ejecución;
- lo activa;
- fija presupuesto o ciclos;
- autoriza Claude Code;
- mueve `ACTIVE`;
- autoriza ramas, worktrees, commits, PRs, runs o mutaciones del ruleset.

Una autorización humana posterior y separada podrá solicitar únicamente una
candidata externa `draft` de WP-016.

### 2. Integración del verificador existente en CI

La futura candidata deberá integrar el `check_scope` ya fusionado y su
biblioteca, sin reabrir WP-002 o WP-005 ni reutilizar sus candidatas.

El ejecutable que decide deberá provenir de una revisión confiable gobernada,
no de bytes modificables por la propia PR juzgada.

El check exacto deberá:

- crearse para toda PR relevante;
- fallar cerrado ante ausencia, error o ambigüedad;
- no poder quedar verde por omisión, `skip`, `neutral`,
  `continue-on-error` o un step posterior.

La ruta de workflow es protegida: Claude solo preparará un parche verificable
y una persona lo aplicará.

Esta integración no modifica todavía el ruleset.

### 3. Pruebas roja y verde antes de hacer requerido el check

Con el job reportando pero todavía no requerido, deberán ejecutarse y
conservarse pruebas reales falsables:

1. `wp/*` con archivo fuera de alcance → `failure`;
2. `wp/*` válido → `success`;
3. `ops/*` sin autorización válida y vigente para el `HEAD` → job creado y
   `failure`;
4. `ops/*` con autorización válida y vigente para el `HEAD` → job creado y
   `success`.

Cada evidencia identificará:

- PR;
- `HEAD SHA`;
- `context`;
- `integration_id`;
- `run_id`, `check_run_id` o equivalente;
- conclusión final;
- instante UTC;
- fuente de confianza evaluada.

`skipped`, `neutral`, ausente, pendiente, cancelado, `timed_out`,
`startup_failure` o cualquier conclusión distinta de `success` después de una
verificación completa no constituyen verde contractual.

### 4. Política verificable para ramas de operador

El contrato posterior elegirá una fuente concreta de autorización humana y
fijará:

- consulta exacta;
- eventos;
- permisos mínimos;
- tratamiento fail-closed.

El prefijo `ops/*` no autentica al operador.

La autorización deberá:

- vincularse al `HEAD SHA` vigente;
- invalidarse al cambiar el diff, el SHA o la fuente;
- reevaluarse ante todos los eventos relevantes.

El check se identifica por el par exacto `{context, integration_id}`. Un
contexto homónimo de otro productor no vale.

DEC-015 resuelve la alternativa: una GitHub App externa es el único productor
elegido. WP-017 queda como intento `blocked` y DEC-017 reserva `WP-018` como
sucesor limpio del prerrequisito, todavía sin contrato. WP-016 no
puede pasar a `ready` hasta que ese productor esté implementado, instalado y
probado mediante autorizaciones propias. `pull_request_target` continúa
prohibido y REQ-FDA-002 no cambia.

La seguridad no promete terminalidad absoluta durante una caída: ausencia,
pendiente u obsolescencia nunca equivalen a conformidad. La disponibilidad se
recupera mediante eventos, cola y reconciliación conforme a DEC-015.

Para la base firmada `B0`, base vigente `B1` y padre autorizante `P`, la
autorización continúa vigente si `B1 == B0` o, para un avance monotónico, si
`B0` es ancestro de `B1`, `B1` es ancestro de `P` y verifica el digest firmado
de `B0...P`. Cualquier otro cambio invalida la autorización. El ruleset deberá
conservar política estricta; desviación o imposibilidad de prueba obliga a
parar.

### 5. Mutación humana posterior del ruleset

Solo después de que:

- el job esté fusionado en `main`; y
- las cuatro pruebas anteriores sean conformes,

una persona, nunca un agente, podrá añadir exactamente el par esperado
`{context, integration_id}` como cuarta comprobación dentro de la regla
`required_status_checks` existente.

La credencial administrativa no se entrega al agente ni se versiona.

La mutación no forma parte del código implementado por WP-016 y conserva
autorización humana separada.

### 6. Evidencia de la mutación del ruleset

El futuro contrato incorporará íntegramente, por referencia y mediante
criterios verificables, DEC-007, sección «Evidencia de la mutación del
ruleset»:

- repositorio, rama, `ruleset_id`, API e instantes UTC;
- `version_id` y `updated_at` anterior y posterior;
- listado de historia y estado completo de cada versión;
- preimagen y postimagen semánticas completas;
- listas de checks como pares `{context, integration_id}`;
- delta reducido exactamente al par añadido;
- clasificación de campos y normalización declarada;
- RFC 8785/JCS y SHA-256 mediante herramienta versionada;
- actor como rol público más referencia opaca;
- comprobaciones de no deriva;
- rollback mínimo que retire solo el par tras comprobar ausencia de
  concurrencia;
- postimagen del rollback, si ocurre;
- custodia externa persistente, protegida y no volátil;
- procedimiento fail-closed si la historia posterior no aparece.

Lo disponible antes de mutar es precondición. La entrada histórica posterior
impide cerrar; no puede ser una precondición temporalmente imposible de la
mutación.

### 7. Condición para afirmar que `check_scope` bloquea fusiones

Solo podrá escribirse esa afirmación cuando concurran todas estas condiciones:

1. job fusionado y ejecutándose;
2. pruebas roja y verde conformes;
3. par exacto incorporado al ruleset activo por una persona;
4. postimagen y delta exacto verificados;
5. historia y custodia exigidas capturadas;
6. una PR no conforme sobre el `HEAD` vigente queda efectivamente no
   fusionable por ese check.

Antes de ello solo se dirá «ejecutable local» o «job en CI no requerido»,
según corresponda.

### 8. Contrato posterior

La futura candidata `draft` deberá ser T3, breve y headless, usar el
subconjunto temporal de DEC-012 y fijar:

- presupuesto;
- `max_ciclos_correccion: 2`;
- archivos mínimos;
- evidencia permitida;
- revisión completa única de Astra;
- aplicación humana de rutas protegidas.

Si la herramienta de evidencia del ruleset no cabe sin desproporcionar el WP,
su segregación requerirá otra decisión que reserve un identificador propio
antes de aprobar WP-016. Esta DEC no lo inventa.

La investigación cambiante se revalidará contra fuentes oficiales al aprobar
el contrato y antes de mutar. No se convierte la ventana visible de 180 días
en garantía REST ni `version_id` en custodia.

Un cambio de esquema, permisos, eventos o política de Actions obliga a parar y
actualizar el contrato mediante autoridad humana.

## Fuera de alcance

- redactar o materializar WP-016;
- aprobar, admitir o activar ningún WP;
- modificar `ACTIVE`;
- implementar CI;
- ejecutar pruebas reales;
- mutar el ruleset;
- tocar guard o WP-007;
- runtime, humo, E2 o cierre de la pausa;
- `CODEOWNERS` o aprobación humana general;
- workflows de agente;
- candidatas y worktrees históricos;
- `.agents/`, `.codex/` o `AGENTS.md`.

## Composición atómica mínima

Exactamente cinco archivos; todos o ninguno:

1. `specs/decisions/DEC-014-reserva-sucesor-wp005.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`, limitado a
   cabecera, lista cerrada, admisión atómica y referencia;
3. `specs/decisions/DEC-011-recuperacion-post-dec009.md`, limitado a añadir al
   inicio de §3.1 una nota que identifique `WP-016` como sucesor reservado por
   `DEC-014` únicamente desde la fusión humana de esta composición, enlace
   `DEC-014` y declare que la reserva no crea, aprueba, admite ni activa el
   contrato, no autoriza ejecutar el hito y no cambia las demás cláusulas de
   §3;
4. `docs/03-hoja-de-ruta.md`, limitado al registro y a la secuencia
   condicionada;
5. `docs/manual/05-bloqueos-y-parada.md`, limitado al estado operativo y al
   límite de la reserva.

Quedan fuera `CLAUDE.md`, `docs/manual/MANUAL.md`, requisitos, ADR, plantilla,
`work-packages/**`, `ACTIVE`, `evidence/**`, `.github/**`, scripts, tests,
hooks, ruleset y candidatas.

DEC-014 no se autoautoriza: DEC-003 se modifica en el mismo diff para
admitirla. El diff no contiene implementación ni transición de `ACTIVE`.

## Verificación de la eventual materialización

- base exacta;
- diff limitado a las cinco rutas;
- `git diff --check`;
- comprobación del manual;
- `check-active` devuelve `REPOSO`;
- ausencia de `work-packages/WP-016-*`;
- cero cambios en workflow, ruleset, código, tests o candidatas;
- revisión completa Astra independiente antes de cualquier autorización de
  materialización.

## Qué no autoriza

Ningún acto posterior.

Contrato, aprobación, admisión, activación, implementación, ruleset y cierre
conservan autorizaciones separadas.
