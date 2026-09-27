# DEC-016 — Reserva y límites del productor externo de Alcance FDA

**Estado propuesto:** aceptada únicamente si la composición atómica de esta
candidata se materializa y fusiona mediante actos humanos posteriores.
**Fecha propuesta:** 2026-09-27.
**Base:** `origin/main`
`332e64543164820ca8ca7ee0af30d2c97fe9ada0`.
**Ámbito:** reservar y delimitar un único WP previo a WP-016; no crear su
contrato ni autorizar infraestructura, secretos, implementación o mutaciones
remotas.

## Problema

DEC-015 resolvió `WP016-DOR-1` en el plano arquitectónico: `Alcance FDA` será
producido por una GitHub App externa que evalúe bytes confiables. También exige
que otro acto normativo reserve primero el identificador del prerrequisito y
fije sus límites.

Hoy ese prerrequisito no tiene WP-ID. Crear directamente un contrato elegiría
el identificador y anticiparía alcance, presupuesto y admisión sin el acto que
actualice la secuencia cerrada de DEC-003. Mantenerlo sin identificador impide
tramitar de forma inequívoca el trabajo que bloquea WP-016.

La documentación oficial vigente de GitHub confirma los supuestos que acotan
el futuro encargo:

1. una GitHub App instalada con `Checks: write` puede recibir `check_suite` y
   crear check runs para un SHA concreto;
2. un ruleset puede exigir un status check de una App esperada, que debe estar
   instalada, tener `Statuses: write`, haber publicado recientemente el check y
   estar asociada a un required status check preexistente del ruleset;
3. la política estricta exige que la rama esté actualizada con la base;
4. GitHub no reentrega automáticamente webhooks fallidos; el productor necesita
   reconciliación y recuperación;
5. el receptor debe validar el secreto, deduplicar entregas, responder en menos
   de diez segundos y derivar el trabajo a procesamiento asíncrono;
6. la clave privada de la App debe custodiarse fuera del repositorio, idealmente
   en un almacén con uso solo para firma, y su rotación y revocación son actos
   operativos explícitos.

## Decisión

### 1. Reserva condicionada

Al entrar la composición atómica de esta decisión en `main`, se reserva
inequívocamente `WP-017` para el productor externo de `Alcance FDA` decidido
por DEC-015.

Antes de esa fusión, `WP-017` no está reservado. La reserva no:

- crea `work-packages/WP-017-*.md`;
- deja un contrato `ready`, aprobado, admitido o activo;
- fija presupuesto, proveedor, cuenta, región, repositorio de implementación,
  rutas permitidas o ciclos;
- autoriza Claude Code ni ningún otro implementador;
- modifica WP-016 ni resuelve `WP016-DOR-1`;
- mueve `ACTIVE`;
- autoriza ramas, worktrees, commits, PRs, pruebas reales, infraestructura,
  secretos, despliegues, instalaciones o mutaciones del ruleset.

Una autorización humana posterior y separada podrá solicitar únicamente una
candidata externa `draft` del contrato de WP-017.

### 2. Propósito y límite positivo de WP-017

El futuro WP-017 tendrá un solo resultado: un productor externo desplegable,
operable y verificable que publique el check run `Alcance FDA` conforme a
DEC-015 y deje preparada la evidencia necesaria para que otro acto determine si
el prerrequisito está cumplido.

Su contrato deberá cubrir como una unidad coherente:

- la implementación versionada del servicio y del adaptador de GitHub App;
- evaluación de la PR como datos usando una revisión confiable e inmutable de
  `scripts/check_scope.py` y `scripts/scope_rules.py`;
- creación y actualización idempotente del check para el `head_sha` exacto;
- recepción validada de los eventos mínimos de DEC-015, cola durable,
  deduplicación y prevención de resultados obsoletos;
- reconciliación periódica de PRs abiertas y recuperación de entregas fallidas;
- observabilidad sin secretos, retención mínima, alertas y procedimiento de
  recuperación;
- artefacto inmutable, despliegue reproducible, rollback y desinstalación;
- runbooks humanos para registro, instalación, custodia, rotación y revocación;
- las pruebas falsables enumeradas por DEC-015, ejecutables solo cuando una
  autorización posterior las habilite.

El contrato fijará resultados observables y evidencia; no convertirá en trabajo
del agente los pasos que DEC-015 reserva a una persona.

### 3. Fronteras obligatorias

WP-017 no podrá:

- modificar WP-016 ni afirmar que `WP016-DOR-1` está resuelto por su mera
  existencia;
- integrar `check_scope` en un workflow de este repositorio;
- modificar `.github/workflows/**`, `CODEOWNERS`, `ACTIVE`, el ruleset o
  permisos de rama;
- ejecutar código procedente del `HEAD` juzgado ni usar `pull_request_target`;
- usar un commit status como sustituto del check run `Alcance FDA`;
- introducir permisos superiores a los fijados por DEC-015;
- almacenar secretos, tokens, claves o payloads sensibles en repositorio, logs
  o evidencias;
- registrar, instalar, rotar o revocar por sí mismo la App, ni aceptar gasto o
  términos de un proveedor;
- cerrar WP-016, WP-007, la pausa de DEC-003 ni ningún hito posterior.

La posterior mutación humana del ruleset seguirá fuera de WP-017 y de WP-016.
Solo podrá considerarse cuando el productor y las pruebas de WP-016 hayan sido
acreditados en el orden fijado por DEC-014 y DEC-015.

### 4. Definition of Ready obligatoria del futuro contrato

El contrato de WP-017 deberá tener como máximo 300 líneas y no podrá pasar de
`draft` hasta que el repositorio registre de forma inequívoca:

1. ubicación y propiedad del código, revisión confiable y mecanismo de pin
   inmutable;
2. proveedor de ejecución y almacenamiento, cuenta humana responsable, región,
   límites de datos, retención y presupuesto máximo;
3. rutas exactas permitidas y separación entre código, infraestructura,
   runbooks y evidencia;
4. almacén de secretos aprobado, roles humanos, procedimiento de alta, firma,
   rotación, revocación y eliminación de copias locales;
5. permisos y eventos exactos de la App, sin ampliación respecto de DEC-015;
6. modelo de cola durable, idempotencia, reconciliación, SLO de recuperación y
   tratamiento fail-closed;
7. estrategia de pruebas aisladas y reales, fixture/repositorio de ensayo,
   oráculos, precondiciones, coste y limpieza reversible; el protocolo deberá
   contemplar allí el required status check preexistente necesario para probar
   la selección de fuente, sin anticipar la mutación del ruleset de producción;
8. despliegue, rollback, desinstalación, continuidad y propietario operativo;
9. archivos de evidencia permitidos y redacción que impida registrar secretos;
10. nivel T3, presupuesto, comandos headless, autor y única revisión
    independiente conforme a DEC-010.

Si falta una elección que implique proveedor, gasto, cuenta, tratamiento de
datos o custodia, se detiene el contrato y se solicita decisión humana. Esta
decisión no toma esas elecciones por anticipado.

### 5. Criterio de terminación y relación con WP-016

WP-017 solo podrá proponerse `done` cuando su contrato autorizado y su evidencia
demuestren, en la revisión y entorno exactos que aquel fije:

- artefacto y despliegue inmutables e identificados;
- App registrada e instalada mediante actos humanos trazables;
- permisos mínimos y secretos custodiados sin exposición;
- check `Alcance FDA` sobre el `HEAD SHA` exacto y con el `app.id` real;
- casos rojo y verde, `[skip ci]`, cambio de base, duplicado, obsolescencia,
  reconciliación y recuperación exigidos por DEC-015;
- rollback, revocación y desinstalación practicables.

Ni siquiera ese cierre modifica automáticamente WP-016. Después hará falta un
acto humano separado que valore la evidencia, corrija y reduzca el contrato de
WP-016 a no más de 300 líneas e incorpore literalmente la semántica de DEC-015.
Solo entonces podrá revisarse WP-016 para `ready`. `ACTIVE` permanece en reposo
entre actos.

### 6. Secuencia cerrada resultante

La parte relevante de la pausa queda:

1. WP-015 `done`: verificador local y biblioteca única;
2. WP-017 reservado, todavía sin contrato: productor externo;
3. tras contrato, aprobación, admisión y activación separados, eventual
   implementación y acreditación de WP-017;
4. corrección, reducción, revisión y eventual admisión separadas de WP-016;
5. implementación de WP-016 y pruebas reales con el check reportando;
6. mutación humana posterior del ruleset y evidencia de enforcement;
7. convergencia del guard y cierre de WP-007 por superación;
8. runtime, humo seguro y E2 mediante actos posteriores independientes.

Esta secuencia expresa dependencias. No autoriza en cadena ninguno de sus pasos.

## Composición atómica mínima

Los siguientes siete archivos viajan juntos o ninguno:

1. `specs/decisions/DEC-016-reserva-productor-externo-alcance.md` — esta
   decisión;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md` — admite la
   composición y registra WP-017 como reservado, no creado ni admitido;
3. `specs/decisions/DEC-011-recuperacion-post-dec009.md` — sustituye el
   prerrequisito sin ID por WP-017 reservado;
4. `specs/decisions/DEC-014-reserva-sucesor-wp005.md` — refleja que el productor
   previo a WP-016 ya tiene identificador reservado;
5. `specs/decisions/DEC-015-productor-externo-check-scope.md` — refleja la
   reserva sin alterar su arquitectura ni autorizar ejecución;
6. `docs/03-hoja-de-ruta.md` — registra el hito y la secuencia vigente;
7. `docs/manual/05-bloqueos-y-parada.md` — refleja el estado operativo y la
   parada hasta un contrato posterior.

No forman parte de la composición WP-016, `ACTIVE`, ningún archivo
`work-packages/WP-017-*`, código, tests, workflows, evidencias, ruleset,
infraestructura, secretos, ramas, worktrees, candidatas históricas, `.agents/`,
`.codex/` ni `AGENTS.md`.

## Enmiendas exactas de los seis archivos existentes

- **DEC-003:** añadir DEC-016 a las notas y lista cerrada; en la secuencia
  sustituir «prerrequisito sin WP-ID» por «WP-017 reservado, sin contrato»;
  añadir WP-017 a la tabla de estado sin admitirlo para ejecución; registrar la
  admisión atómica de estos siete archivos.
- **DEC-011:** añadir nota de enmienda y sustituir en §3.1 el productor sin ID
  por WP-017 reservado; conservar intacto el orden posterior.
- **DEC-014:** añadir nota de enmienda y sustituir las menciones «todavía sin
  WP-ID» por la reserva condicionada de WP-017; no cambiar los gates de WP-016.
- **DEC-015:** añadir nota de enmienda; en §5 identificar WP-017 como el
  prerrequisito reservado, todavía sin contrato, y mantener todas sus
  condiciones técnicas.
- **docs/03:** añadir el hito fechado de DEC-016 y actualizar únicamente las
  menciones del prerrequisito sin ID y la secuencia.
- **manual/05:** registrar WP-017 como reservado, sin contrato, y mantener la
  parada, WP-016 bloqueado y `ACTIVE` en reposo.

## Fuera de alcance

Esta decisión no autoriza:

- crear, materializar, aprobar, admitir, activar o implementar WP-017;
- modificar WP-016 o `ACTIVE`;
- registrar, desplegar o instalar la GitHub App;
- elegir proveedor, aceptar coste, crear cuentas o infraestructura;
- generar, leer, importar o usar secretos;
- ejecutar pruebas reales;
- modificar workflows o ruleset;
- reservar otro WP-ID;
- continuar con ningún acto posterior de la secuencia;
- tocar o limpiar candidatas y worktrees históricos.

## Fuentes primarias revalidadas el 2026-09-27

- GitHub Docs, *Building CI checks with a GitHub App*:
  <https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-ci-checks-with-a-github-app>
- GitHub Docs, *Using the REST API to interact with checks*:
  <https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks>
- GitHub Docs, *Available rules for rulesets*:
  <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>
- GitHub Docs, *Best practices for using webhooks*:
  <https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks>
- GitHub Docs, *Handling failed webhook deliveries*:
  <https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries>
- GitHub Docs, *Managing private keys for GitHub Apps*:
  <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps>

## Condición de efecto

Esta candidata no tiene efecto por existir fuera del repositorio. Solo una
autorización humana posterior puede materializar exactamente su composición;
otra autorización separada podrá crear rama, commit o PR, y otra podrá
fusionarla tras verificar base, alcance y checks.
