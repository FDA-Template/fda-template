# WP-017 — Productor externo de Alcance FDA

estado: draft
prioridad: P0
riesgo: T3
agente_responsable: Claude Code (implementer)
agente_revisor: GPT-6 Astra (Alto, contexto nuevo, solo lectura)
requisitos: [REQ-FDA-001, REQ-FDA-002, SEC-001]
adr: [ADR-001]
decision: [DEC-003, DEC-010, DEC-011, DEC-014, DEC-015, DEC-016]
presupuesto_max_eur: 100
max_ciclos_correccion: 2

Esta candidata es deliberadamente `draft`. Su materialización no la aprueba,
admite, activa ni autoriza ejecutar. La base de redacción es `origin/main`
`9d69fcc6031cd2a4a98621f0e8a17056e172c6c2`.

## Objetivo y contexto

Existe un productor externo desplegable y operable, identificado por una
revisión inmutable, que recibe y recupera eventos de GitHub, evalúa cada PR de
`fda-template` con bytes confiables y publica un check run llamado exactamente
`Alcance FDA` sobre el `HEAD SHA` vigente. Solo una evaluación completa puede
terminar en `success`; cualquier ausencia, pendiente, obsolescencia o productor
distinto nunca equivale a conformidad.

WP-015 entregó únicamente el verificador local. DEC-015 eligió una GitHub App
externa y DEC-016 reservó WP-017 como prerrequisito de WP-016. Este WP no integra
el workflow, no modifica el ruleset y no permite afirmar todavía que el alcance
bloquea fusiones.

## Definition of Ready — bloqueos humanos abiertos

Esta candidata no puede pasar a `ready` mientras permanezca abierto cualquiera:

- **WP017-DOR-1 — resuelto por decisión humana del 2026-09-27.** El servicio permanece en `ivanes189/fda-template`: su única raíz reservada es `services/alcance_fda/**` y la de sus pruebas es `tests/alcance_fda/**`; Iván (`@ivanes189`) es su propietario contractual, en coherencia con el `CODEOWNERS` vigente, sin afirmar que GitHub exija hoy su aprobación. Para este WP se descarta otro repositorio porque no existe como fuente gobernada y exigiría crear y sincronizar un segundo gobierno; el aislamiento se obtiene mediante la revisión y el artefacto fijados a continuación.
  La revisión confiable es exclusivamente un commit Git completo de cuarenta caracteres ya fusionado en `main`. De ese mismo commit se incorporan el servicio bajo la raíz reservada y exactamente `scripts/check_scope.py` y `scripts/scope_rules.py`; el `HEAD` evaluado solo aporta datos. WP017-DOR-5 deberá enumerar los archivos hoja dentro de las raíces, lenguaje, dependencias, lockfiles, IaC y comandos, y WP017-DOR-8 las rutas de política; esta resolución no los anticipa.
  Un build posterior y expresamente autorizado producirá una sola imagen OCI que contenga servicio y evaluador, registrará el commit fuente y las huellas SHA-256 de ambos archivos del evaluador, y la almacenará en Artifact Registry. Despliegue y rollback referenciarán exclusivamente `LOCATION-docker.pkg.dev/PROJECT/REPOSITORY/IMAGE@sha256:<digest>` y registrarán la revisión inmutable de Cloud Run; quedan prohibidos etiquetas, ramas y bytes de la PR como pin o fuente ejecutable. Esta elección no crea repositorio, artefacto, infraestructura ni despliegue.
- **WP017-DOR-2 — resuelto por decisión humana del 2026-09-27.** Google Cloud en `europe-west1`: Cloud Run, Pub/Sub, Firestore Standard y Cloud Scheduler, en proyecto exclusivo bajo responsabilidad de Iván; vincular o crear facturación es otro acto humano.
  Presupuesto WP: `100 EUR`; operación: `≤5 EUR/mes`, protegida con mínimo cero y máximo tres instancias, cuotas, alertas y parada antes de rebasarlo; no se promete corte exacto por latencia de cobro.
  La resolución no crea cuenta, proyecto, infraestructura ni autorización de gasto.
- **WP017-DOR-3 — datos.** Aprobar qué payloads, objetos Git y metadatos pueden
  salir de GitHub, región de tratamiento, cifrado, retención, borrado, acceso,
  copias y contenido permitido de logs y alertas.
- **WP017-DOR-4 — secretos y custodia.** Elegir key vault y roles humanos; fijar
  alta, importación solo-firma del PEM, secreto de webhook, rotación, revocación,
  emergencia y eliminación verificada de copias locales.
- **WP017-DOR-5 — superficie implementable.** Fijar archivos permitidos y
  prohibidos, lenguaje, dependencias, lockfiles, IaC, versiones y comandos
  headless exactos; cerrar además la matriz de eventos, acciones, eventos
  suscritos y entregas automáticas. Hasta entonces la lista permanece vacía.
- **WP017-DOR-6 — ensayo real.** Elegir App propietaria, repositorio o fixture de
  prueba, instalación limitada, required status check preexistente de ensayo,
  operador, ventana, coste, limpieza y rollback sin tocar el ruleset productivo.
- **WP017-DOR-7 — operación.** Designar responsable de alertas, continuidad,
  recuperación, despliegue, rollback, desinstalación y respuesta a incidentes.
- **WP017-DOR-8 — política evaluada.** Versionar la interfaz completa `wp/*` y
  `ops/*`: gramáticas, autorización, firmante permitido, consultas, digest,
  semántica DEC-015 y oráculos negativos. WP-016 `draft` no es su fuente.
- **WP017-DOR-9 — SHA compartido.** Fijar una regla de publicación conservadora
  y su ensayo concurrente cuando dos PR comparten commit y dan resultados
  opuestos; `pull_number` o `external_id` no demuestran aislamiento en GitHub.

Cada resolución debe quedar versionada en este contrato mediante acto humano.
Los siete bloqueos restantes no se sustituyen por defaults o conjeturas.

## Alcance incluido y fuera de alcance

**Incluido después de resolver la DoR:**

- servicio y adaptador de GitHub App, artefacto inmutable y despliegue
  reproducible en la ubicación aprobada;
- receptor autenticado, cola durable, workers idempotentes, reconciliador,
  recuperación de entregas fallidas, observabilidad y alertas;
- adquisición de metadatos y objetos Git como datos, sin ejecutar bytes de PR;
- carga del verificador WP-015 y de la política resuelta por WP017-DOR-8 desde
  la revisión confiable fijada, nunca desde el `HEAD` juzgado;
- creación y actualización del check run `Alcance FDA`;
- pruebas unitarias, integración aislada y ensayos reales de DEC-015;
- runbooks humanos, evidencias redactadas, coste y ciclos.

**Fuera de alcance:**

- modificar WP-016, `ACTIVE`, WP-015, el guard, WP-007, runtime, humo o E2;
- modificar `.github/workflows/**`, `CODEOWNERS`, ruleset o permisos de rama;
- usar `pull_request_target` o un commit status como sustituto del check run;
- registrar, instalar, rotar, revocar o desinstalar la App mediante un agente;
- aceptar proveedor, gasto, cuenta o tratamiento de datos mediante un agente;
- leer, generar, transportar o revelar valores secretos mediante un agente;
- afirmar que `WP016-DOR-1` está resuelto o que el check bloquea fusiones;
- tocar o importar candidatas y worktrees históricos.

## Archivos permitidos

- ninguno
Nota: lista vacía deliberada y fail-closed hasta resolver WP017-DOR-3 a DOR-5.

## Archivos prohibidos

- **
Nota: antes de `ready`, otro acto humano sustituirá ambas listas por rutas
concretas, disjuntas de WP-016 y de las rutas protegidas excluidas.

## Contratos técnicos

### 1. Identidad, autenticación y permisos

- GitHub App cuya propiedad y visibilidad fija WP017-DOR-6, instalada solo en
  los repositorios expresamente aprobados.
- Autenticación como App mediante JWT solo para generar tokens de instalación y
  administrar recursos propios de la App, incluida la recuperación de webhooks.
- API de repositorio mediante installation access token efímero; nunca PAT,
  contraseña ni user access token.
- Permisos exactos: `Checks: read and write`, `Commit statuses: read and write`,
  `Contents: read`, `Pull requests: read` y `Metadata: read` implícito.
- Eventos de evaluación: `check_suite` `requested`/`rerequested`; `pull_request` para
  apertura, reapertura, sincronización, edición, draft/ready y cambio de base;
  y `push` de `main`. `installation` e `installation_repositories`, entregados
  automáticamente, se tratan como control de acceso y disparan reconciliación.
- No se amplían permisos o eventos sin corregir y volver a aprobar el contrato.

`Commit statuses: write` existe únicamente para que GitHub permita seleccionar
la App como fuente esperada. El productor emite un check run, no un status.

### 2. Entrada de webhooks y cola

- Se valida el cuerpo bruto con `X-Hub-Signature-256`, HMAC-SHA-256 y comparación
  de tiempo constante antes de parsear o encolar; ausencia o fallo se rechazan.
- Se validan tipo, acción, repositorio, instalación y esquema contra allowlists.
- `X-GitHub-Delivery` es clave de deduplicación; una redelivery conserva el GUID.
- El receptor persiste duraderamente la entrega aceptada y responde `2xx` en
  menos de diez segundos; la evaluación ocurre fuera de la petición.
- Payloads rechazados no llegan a la cola y no se registran íntegros.

### 3. Trabajo idempotente y fuente confiable

La identidad de una evaluación es:

```text
repository_id + pull_number + head_sha + base_sha + evaluator_revision
```

- un duplicado no crea doble efecto;
- reintentos usan backoff y respetan `Retry-After` y `x-ratelimit-*`;
- antes de publicar la conclusión se reobtienen PR, `HEAD`, base y revisión;
- un trabajo obsoleto no sobrescribe ni concluye el check del estado vigente;
- árbol, blobs, commits, diffs y mensajes de la PR son datos no confiables;
- solo se ejecutan servicio, política y `scripts/check_scope.py` /
  `scripts/scope_rules.py` de la revisión inmutable aprobada;
- no se hace checkout ejecutable ni se importan módulos desde la PR juzgada.

### 4. Política y check run

- WP017-DOR-8 versiona la política completa en rutas propias de WP-017; el
  contrato actual de WP-016 no es dependencia ejecutable ni fuente aprobada.
- El nombre es exactamente `Alcance FDA` y el `head_sha` coincide con la PR.
- `wp/*` extrae el WP-ID con la gramática que el contrato revisado fije y delega
  el alcance exclusivamente en el verificador WP-015 confiable.
- `ops/*` aplica la autorización firmada, digest y semántica `B0`/`B1`/`P` de
  DEC-015; el prefijo de rama no autentica a nadie.
- Rama inválida, contrato ausente o ambiguo, bytes no verificables, política
  incumplida o error evaluable terminan en `failure`.
- Solo una evaluación completa del estado vigente termina en `success`.
- Caída de infraestructura deja ausencia, cola o ejecución no exitosa y alerta;
  nunca inventa `success` ni `failure` como si hubiera evaluado.
- No se usan `neutral`, `skipped` o `success` parcial como verde contractual.
- GitHub asocia checks externamente al repositorio y SHA, no a la PR: mientras
  WP017-DOR-9 no cierre el caso de SHA compartido, no existe verde admisible.

### 5. Reconciliación y recuperación

- Cada cinco minutos como máximo se enumeran PRs abiertas y se garantiza una
  evaluación para la identidad vigente.
- Un `push` a `main` reevalúa las PRs abiertas afectadas por la base.
- Se inventariarán y reentregarán programáticamente webhooks fallidos de la App
  mediante endpoints autenticados con JWT; GitHub no los reentrega solo.
- Una entrega perdida se recupera en diez minutos como máximo cuando GitHub y
  el servicio están disponibles.
- Reinicio, duplicado, desorden y concurrencia preservan idempotencia y evitan
  conclusiones obsoletas.

### 6. Datos, secretos y artefactos

- La resolución de WP017-DOR-3 aplica minimización y tiempos de borrado
  verificables a payload, cola, objetos Git, logs, métricas, backups y alertas.
- Ningún secreto, token, PEM, cuerpo sensible, URL firmada o variable de entorno
  aparece en repositorio, salida, evidencia, commit o PR.
- La clave privada reside en key vault con uso solo para firma; ningún agente
  accede a ella ni al secreto del webhook.
- Tokens de instalación se limitan al repositorio y permisos necesarios, se
  cachean solo durante su vigencia y no se persisten en claro.
- Artefacto, configuración no secreta y revisión del evaluador quedan fijados
  por identificadores y SHA-256 reproducibles.

## Entorno autorizado

- Herramientas: PENDIENTE (WP017-DOR-5)
- Comandos: PENDIENTE (WP017-DOR-5)
- Red: NINGUNA mientras el contrato sea `draft`; antes de `ready` se enumerarán
  hosts, métodos y finalidad exactos, limitados a GitHub y proveedor aprobado.
- Secretos: NINGUNO para agentes. Los actos humanos usarán solo el key vault
  aprobado y nunca expondrán valores a comandos, logs o evidencias del agente.
- Infraestructura, cuentas y gasto: no autorizados por este contrato `draft`.

## Verificación

No hay comandos de implementación ejecutables mientras la DoR esté abierta.
Antes de `ready`, WP017-DOR-5 y DOR-6 deberán sustituir este párrafo por comandos
headless exactos que cubran, al menos:

1. lint, tipos, tests, SAST cuando aplique, dependencias, verificación de
   lockfiles y escaneo de secretos; toda no aplicabilidad queda justificada;
2. firma válida/ausente/incorrecta y comparación constante;
3. eventos y acciones permitidos/rechazados;
4. idempotencia, duplicado, desorden, reintento y obsolescencia;
5. rojo y verde para `wp/*` y `ops/*`, incluido SHA compartido con resultados
   opuestos, sin ejecutar bytes de PR;
6. `[skip ci]` con check de la App presente;
7. avance de `main` en los dos casos de DEC-015;
8. caída, reinicio, reconciliación y recuperación dentro del límite;
9. permisos exactos, token efímero, rate limit y redacción de logs;
10. rollback y desinstalación en seco, más ensayo real autorizado.

## Criterios de aceptación

- [ ] Los nueve bloqueos DoR están resueltos y versionados antes de `ready`.
- [ ] Archivos, comandos, presupuesto, proveedor y entorno son inequívocos.
- [ ] Artefacto y evaluador coinciden con sus revisiones y huellas inmutables.
- [ ] Ningún caso ejecuta bytes de PR ni obtiene permisos adicionales.
- [ ] El receptor autentica antes de procesar y responde tras encolado durable.
- [ ] Duplicados y trabajos obsoletos no producen conclusiones incorrectas.
- [ ] Reconciliación y redelivery cumplen los límites de DEC-015.
- [ ] `Alcance FDA` se publica para el `HEAD SHA` exacto con el `app.id` real.
- [ ] Solo la evaluación completa vigente produce `success`.
- [ ] La matriz de once pruebas de DEC-015 queda acreditada.
- [ ] Registro, instalación, despliegue, configuración administrativa y
  custodia son humanos; tras habilitación, el servicio solo obtiene tokens,
  publica checks y solicita redeliveries dentro de su contrato.
- [ ] WP-016, `ACTIVE`, workflows y ruleset permanecen sin cambios.
- [ ] Una única Astra revisa la candidata T3; C1/C2 son revalidaciones enfocadas.

## Evidencias exigidas

Cuando exista implementación autorizada, `evidence/WP-017/` contendrá:

- base, `TESTED_HEAD`, árbol, revisión del evaluador y manifiesto de artefactos;
- comandos íntegros, códigos de salida y matriz de pruebas;
- permisos/eventos/configuración no secreta e identidad pública de la App;
- referencias a checks y ensayos: PR, head/base SHA, check_run_id, `app.id`,
  conclusión y UTC;
- métricas de cola, duplicados, obsolescencia, reconciliación y recuperación;
- evidencia redactada de despliegue, rollback, instalación y custodia humana;
- inventario de datos, retención/borrado y comprobación de logs sin secretos;
- `ciclos.md`, revisión Astra y revalidaciones enfocadas; `cost.md`.

Nunca contendrá valores o bytes secretos, payloads íntegros, tokens, PEM, rutas
locales sensibles, variables de entorno, URLs firmadas o capturas voluminosas.

## Puertas y condiciones de parada

0. `draft`: DoR abierta; no se aprueba, admite, activa ni implementa.
1. `ready`: solo tras resolver DOR-1 a DOR-9 y revisar el contrato actualizado.
2. Admisión y activación: actos humanos posteriores y separados.
3. Implementación: solo Claude Code autorizado, dentro de rutas y presupuesto.
4. Registro, despliegue, instalación, configuración administrativa y secretos:
   actos humanos expresos. Una habilitación posterior permite al servicio solo
   tokens de instalación, checks y redeliveries; nunca administración o secretos
   a agentes de desarrollo.
5. Ensayos reales y cierre: autorizaciones separadas y evidencia completa.

Además de CLAUDE.md, se detiene ante cualquier cambio de base, permiso, evento,
API, proveedor, coste, datos, secreto, ruta o comando; necesidad de
`Administration` o escritura adicional; prueba inejecutable; deriva del
ruleset; vulnerabilidad; presupuesto agotado; o tercer ciclo.

## Migración y rollback

No existe migración mientras sea `draft`. Antes de `ready` se fijarán despliegue
reversible, revisión anterior, vaciado seguro de cola, revocación de tokens,
rotación de claves, desinstalación, borrado de datos y responsable humano.

El rollback nunca modifica automáticamente el ruleset ni restaura secretos,
payloads o configuraciones no verificadas.

## Fuentes primarias revalidadas el 2026-09-27

- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-ci-checks-with-a-github-app>.
- GitHub Docs, <https://docs.github.com/en/rest/checks/runs>.
- GitHub Docs, <https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries>.
- GitHub Docs, <https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks>.
- GitHub Docs, <https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries>.
- GitHub Docs, <https://docs.github.com/en/rest/apps/webhooks>.
- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation>.
- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app>.
- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps>.
- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app>, <https://docs.github.com/en/rest/commits/commits> y <https://docs.github.com/en/rest/git/commits>.
- GitHub Docs, <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>.
- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/rate-limits-for-github-apps>.
- Google Cloud Docs, <https://cloud.google.com/run/docs/locations>, <https://cloud.google.com/run/pricing>, <https://cloud.google.com/run/docs/configuring/max-instances>, <https://cloud.google.com/run/docs/deploying>, <https://cloud.google.com/run/docs/managing/revisions> y <https://cloud.google.com/pubsub/pricing>.
- Google Cloud Docs, <https://cloud.google.com/artifact-registry/docs/docker/names>, <https://cloud.google.com/artifact-registry/docs/container-concepts>, <https://cloud.google.com/firestore/pricing>, <https://cloud.google.com/scheduler/pricing>, <https://cloud.google.com/kms/docs/key-import> y <https://cloud.google.com/kms/pricing>.
