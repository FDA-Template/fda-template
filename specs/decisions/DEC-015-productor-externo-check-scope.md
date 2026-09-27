# DEC-015 — Productor externo del check de alcance

**Estado propuesto:** aceptada únicamente si la composición atómica de esta
candidata se materializa y fusiona mediante actos humanos posteriores.
**Fecha propuesta:** 2026-09-27.
**Ámbito:** resolución normativa de `WP016-DOR-1`; no reserva otro WP-ID, no
modifica WP-016 y no autoriza implementación, instalación ni mutación remota.

**Enmendada el 2026-09-27 por
[`DEC-016`](DEC-016-reserva-productor-externo-alcance.md):** reserva `WP-017`
para el prerrequisito aquí decidido, todavía sin contrato, sin alterar esta
arquitectura ni autorizar ejecución.

## Problema

`WP-016` existe en `draft`, `ACTIVE` está en reposo y `WP016-DOR-1` exige un
productor que evalúe bytes confiables y publique `Alcance FDA` sobre el `HEAD`
vigente, con productor fijable por `integration_id`, también ante directivas de
omisión de Actions y sin `pull_request_target`.

La documentación oficial vigente de GitHub acredita:

1. Los checks creados por jobs de Actions solo son elegibles para una PR cuando
   su run nace de determinados eventos; la limitación no alcanza a checks
   creados por una GitHub App externa.
2. Las directivas `[skip ci]` y equivalentes suprimen runs `push` y
   `pull_request`; el required check asociado queda pendiente.
3. Un required status check puede exigir un `context` y el `integration_id` de
   una GitHub App concreta.
4. Una GitHub App con `Checks: write` puede recibir `check_suite` y crear un
   check run para un `head_sha` exacto.
5. Los ruleset workflows se configuran a nivel de organización o empresa. El
   repositorio actual es público pero pertenece a una cuenta `User`, no a una
   organización; además esa regla no conserva el modelo contractual vigente de
   required status check identificado por `{context, integration_id}`.
6. GitHub no reentrega automáticamente un webhook fallido. La ausencia por
   caída de infraestructura no puede convertirse honestamente en una conclusión
   terminal garantizada por la plataforma.
7. El ruleset remoto vigente exige actualmente política estricta
   (`strict_required_status_checks_policy: true`): la rama de la PR debe estar
   actualizada con la base antes de fusionarse. Esta propiedad externa debe
   revalidarse antes de cada prueba y mutación; la candidata no autoriza
   cambiarla.

Por tanto no existe un diseño basado únicamente en workflows del propio
repositorio que cumpla simultáneamente confianza, resistencia a omisión,
elegibilidad y productor exacto. Sí existe un diseño compatible con
`REQ-FDA-002`, pero requiere una GitHub App, servicio externo, secretos,
operación y reconciliación; todo ello está fuera de WP-016 y contradice la
redacción vigente de `SEC-001`, que limita los secretos al almacén de Actions.

## Decisión

### 1. Arquitectura elegida

Se elige una **GitHub App externa** como único productor futuro de
`Alcance FDA`. No se autoriza `pull_request_target` y no se modifica
`REQ-FDA-002`.

La App deberá:

- crear un check run llamado exactamente `Alcance FDA` sobre el `head_sha`
  vigente de la PR;
- ejecutar únicamente evaluador y orquestación provenientes de una revisión
  confiable e inmutable, nunca bytes ejecutables de la cabeza juzgada;
- tratar el árbol y los objetos Git de la PR exclusivamente como datos;
- cargar `scripts/check_scope.py` y `scripts/scope_rules.py` desde la revisión
  confiable que el contrato posterior fije, nunca desde el `HEAD` de la PR;
- emitir `success` solo tras completar toda la evaluación; cualquier
  incumplimiento, entrada inválida o error evaluable termina en `failure`;
- permitir que el ruleset identifique al productor por el par exacto
  `{"context":"Alcance FDA","integration_id":<ID_REAL_DE_LA_APP>}`.

El `integration_id` no se inventa: se obtiene de un check run real de la App
instalada y se acredita antes de cualquier mutación del ruleset.

### 2. Disparadores y reconciliación

El diseño deberá cubrir, como mínimo:

- `check_suite` `requested` y `rerequested` para nuevos commits;
- eventos `pull_request` que abran, reabran, sincronicen, editen, cambien el
  estado draft o cambien la base;
- `push` sobre `main`, que obliga a reevaluar toda PR abierta cuya autorización
  dependa de la base;
- reconciliación periódica de todas las PR abiertas al menos cada cinco minutos;
- inventario y reentrega programada de webhooks fallidos de la App.

El servicio valida `X-Hub-Signature-256` antes de procesar, deduplica por
`X-GitHub-Delivery`, acusa recibo en menos de diez segundos y deriva el trabajo
a una cola durable. La evaluación es idempotente por
`repository_id + pull_number + head_sha + base_sha + evaluator_revision`.
Una evaluación obsoleta no puede sobrescribir la conclusión del `HEAD` vigente.

La seguridad ante un avance de `main` no descansa solo en la reconciliación. Se
adopta esta semántica cerrada para la futura autorización `ops/*`, donde `B0`
es la base firmada, `B1` la base vigente y `P` el padre del commit autorizante:

- si `B1 == B0`, la autorización se evalúa normalmente;
- si `B0` es ancestro de `B1` **y** `B1` es ancestro de `P`, el avance es
  monotónico: la PR ya contenía exactamente la nueva base y la autorización
  continúa vigente, siempre que también verifique el digest firmado de
  `B0...P`;
- en cualquier otro caso la autorización es inválida y necesita un nuevo commit
  autorizante.

Esta regla sustituye para el contrato futuro la afirmación «cualquier avance de
`main` invalida». No se aplica todavía porque esta decisión no modifica
WP-016. Antes de `ready`, otro acto humano deberá incorporar literalmente la
semántica anterior y sus pruebas al contrato.

Además, el ruleset debe conservar
`strict_required_status_checks_policy: true`: si `B1` no está contenido en
`HEAD`, GitHub impide fusionar; si ya está contenido, el segundo caso anterior
es seguro sin esperar al webhook. La preimagen y la postimagen de la futura
mutación deben acreditar `true`, y el único delta seguirá siendo añadir el par.
Si la política estricta no está vigente, se detiene el proceso y se solicita
otra decisión; esta candidata no autoriza restaurarla ni modificarla.

Las directivas de omisión de Actions no gobiernan este productor y no impiden
la creación del check de la App.

### 3. Seguridad frente a disponibilidad

Se corrige la exigencia absoluta «siempre terminal» de DEC-014 y
`WP016-DOR-1`:

- **invariante de seguridad:** solo una evaluación completa del `HEAD` vigente
  puede producir `success`; un check ausente, pendiente, obsoleto o de otro
  productor nunca equivale a conformidad; tras hacer requerido el check, la
  combinación del par exacto, la política estricta y la semántica monotónica
  anterior cubre toda base más reciente sin depender de recibir el webhook;
- **objetivo de disponibilidad:** con GitHub y el servicio disponibles, cada
  evento recibido o recuperado concluye en `success` o `failure`; una entrega
  perdida debe recuperarse por reconciliación en un máximo de diez minutos;
- **fallo de infraestructura:** la ausencia o permanencia en pendiente detiene
  el cierre y la operación, pero no se falsifica como `failure` ni como
  `success`.

Esta distinción es obligatoria porque GitHub documenta que no reentrega
automáticamente webhooks fallidos. Ningún contrato posterior podrá prometer
terminalidad absoluta ante una caída simultánea del productor y su mecanismo
de reconciliación.

### 4. Permisos, secretos y custodia

La instalación futura solicita únicamente:

- `Checks: read and write`;
- `Commit statuses: read and write`, exigido por la documentación vigente para
  seleccionar la App como fuente esperada del required status check;
- `Contents: read`;
- `Pull requests: read`;
- `Metadata: read` implícito.

No solicita `Administration`, escritura de contenidos, Actions, Issues ni
Secrets. `Commit statuses: write` no autoriza a sustituir `Alcance FDA` por un
commit status: el productor contractual sigue siendo un check run y la prueba
futura debe acreditar que la App resulta seleccionable como fuente esperada
con esos permisos exactos. Si GitHub no lo permite, se detiene; no se amplían
permisos por conjetura. El procesador no recibe secretos del repositorio y no
expone credenciales a código de PR.

`SEC-001` queda enmendada de forma mínima: los secretos operativos pueden vivir
en el almacén de GitHub Actions **o** en el gestor de secretos del servicio
externo expresamente aprobado. En ambos casos quedan fuera del repositorio,
logs y evidencias, con acceso por rol, rotación y revocación; ningún agente lee
sus valores. La clave privada de la App y el secreto del webhook pertenecen al
segundo caso.

Su criterio 6 se sustituye también: `gh secret set` sigue siendo la vía para
secretos de Actions; para la App, una persona genera el PEM en GitHub, lo recibe
en una ubicación local protegida fuera de cualquier repositorio, verifica su
huella, lo importa inmediatamente en un key vault con uso solo para firma y
elimina de forma segura la copia local después de verificar la importación.
Nombre de archivo, huella pública, roles, fechas de alta/rotación/revocación y
resultado pueden registrarse; el valor, los bytes y cualquier salida que los
revele no. Ningún agente participa ni obtiene acceso a ese procedimiento.

### 5. Prerrequisito separado y situación de WP-016

La App y su servicio son un prerrequisito independiente de WP-016. Esta
decisión **no reserva ni inventa su WP-ID**. Un acto normativo humano posterior
deberá reservarlo, fijar sus límites y admitir después un contrato propio de no
más de 300 líneas antes de cualquier implementación.

DEC-016 satisface posteriormente solo el primer paso: reserva `WP-017` y fija
sus límites. Su contrato sigue sin existir y requiere creación, aprobación,
admisión y activación separadas antes de cualquier implementación.

Hasta que ese prerrequisito esté implementado, desplegado, instalado y probado
mediante autorización separada:

- WP-016 permanece `draft` y bloqueado;
- no puede aprobarse, admitirse, activarse ni implementarse;
- `WP016-DOR-1` no se considera resuelto;
- `ACTIVE` permanece en reposo;
- el ruleset no cambia.

Después de acreditar el productor, otro acto humano deberá corregir y reducir
el contrato de WP-016 antes de revisarlo para `ready`. La versión actual tiene
645 líneas y excede el límite transversal de 300; esta decisión registra el
incumplimiento, pero no modifica el archivo. Esa corrección deberá sustituir la
invalidación incondicional por avance de `main` por la semántica cerrada de §2.

### 6. Límites de la futura prueba falsable

La prueba del productor, todavía no autorizada, deberá acreditar al menos:

1. check run sobre el `HEAD SHA` exacto y `app.id` real;
2. evaluador y revisión confiable identificados por huella inmutable;
3. rojo y verde para `wp/*` y `ops/*`;
4. directiva `[skip ci]` sin ausencia del check de la App;
5. avance de `main` con `HEAD` de PR invariable y reevaluación de la autorización;
6. entrega duplicada sin doble efecto y evaluación obsoleta sin sobrescritura;
7. entrega fallida recuperada por el reconciliador dentro del límite;
8. tras un verde sobre `B0`, dos avances de `main` e intento de fusión anterior
   a la reevaluación: *(a)* si `B1` no es ancestro de `P`, GitHub bloquea por
   política estricta y actualizar la rama exige nuevo check; *(b)* para el
   historial `B0 → B1 → P → HEAD`, la autorización continúa vigente únicamente
   porque se verifican ambas ancestralidades y el digest firmado de `B0...P`;
9. App seleccionable como fuente esperada con los permisos exactos, sin usar un
   commit status como sustituto del check run;
10. ausencia de ejecución de bytes de PR y permisos exactos;
11. ningún secreto en repositorio, logs o evidencias.

Nada de lo anterior se ejecuta mediante esta decisión.

## Composición atómica mínima

Los siguientes siete archivos viajan juntos o ninguno:

1. `specs/decisions/DEC-015-productor-externo-check-scope.md` — esta decisión;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md` — admite la
   composición, registra que WP-016 ya existe en `draft` y antepone el
   prerrequisito externo sin asignarle WP-ID;
3. `specs/decisions/DEC-011-recuperacion-post-dec009.md` — enmienda el orden de
   dependencias para colocar el productor externo antes de WP-016;
4. `specs/decisions/DEC-014-reserva-sucesor-wp005.md` — registra la resolución
   de su parada, la arquitectura elegida y la distinción seguridad/disponibilidad;
5. `specs/requirements/SEC-001-sin-secretos.md` — admite únicamente el gestor
   de secretos del servicio externo expresamente aprobado;
6. `docs/03-hoja-de-ruta.md` — refleja el contrato `draft`, el bloqueo y el
   nuevo prerrequisito;
7. `docs/manual/05-bloqueos-y-parada.md` — refleja el mismo estado operativo y
   la parada hasta una futura reserva.

No forman parte de la composición WP-016, `ACTIVE`, código, tests, workflows,
evidencias, ruleset, ramas, worktrees, candidatas históricas, `.agents/`,
`.codex/` ni `AGENTS.md`.

## Enmiendas exactas que deben expresar los seis archivos existentes

- **DEC-003:** añadir DEC-015 a la lista cerrada; sustituir «WP-016 todavía sin
  contrato» por «contrato `draft`, no aprobado/admitido/activo»; insertar antes
  de WP-016 un prerrequisito externo sin WP-ID cuya reserva exige otro acto;
  añadir una cláusula de admisión atómica con los siete archivos anteriores.
- **DEC-011:** añadir nota de enmienda por DEC-015; en §3.1 anteponer el
  productor externo y conservar después WP-016, la mutación humana y el resto
  de la secuencia.
- **DEC-014:** añadir nota de enmienda por DEC-015; sustituir la alternativa
  abierta por la GitHub App elegida; sustituir terminalidad absoluta por la
  separación de §3 de esta decisión; sustituir la invalidación incondicional
  ante avance de `main` por la semántica monotónica cerrada de §2; mantener
  intactos los demás gates posteriores.
- **SEC-001:** sustituir «exclusivamente en el almacén de secretos de GitHub
  Actions» por los dos almacenes admitidos de §4; sustituir también su criterio
  6 por las dos vías humanas de incorporación allí descritas; añadir acceso por
  rol, rotación, revocación y ausencia de valores en evidencias.
- **docs/03:** añadir el hito fechado de DEC-015; registrar WP-016 `draft`,
  bloqueado y con 645 líneas; anteponer el prerrequisito externo sin ID.
- **manual/05:** reflejar la misma secuencia y aclarar que ninguna ausencia por
  infraestructura puede contarse como terminal ni como verde.

Estas enmiendas no pueden añadir un WP-ID, autorizar pruebas o describir el
check como bloqueante antes de la prueba real y la mutación humana del ruleset.

## Fuera de alcance

- reservar, crear, aprobar, admitir, activar o implementar otro WP;
- modificar WP-016 o `ACTIVE`;
- registrar, desplegar o instalar la GitHub App;
- crear servicio, cola, scheduler, secretos o infraestructura;
- ejecutar pruebas reales;
- modificar workflows o ruleset;
- abrir rama, worktree, commit o PR;
- tocar o ejecutar candidatas históricas o adaptaciones locales no gobernadas.

## Fuentes oficiales revalidadas

- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs
- https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-ci-checks-with-a-github-app
- https://docs.github.com/en/rest/repos/rules
- https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
- https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
- https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries
- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps
