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
- **WP017-DOR-3 — resuelto por decisión humana del 2026-09-27.** El cuerpo bruto de cada webhook que posteriormente admita la matriz de WP017-DOR-5 sale de GitHub por HTTPS, puede atravesar y terminar TLS en el Google Front End global antes de llegar a Cloud Run en `europe-west1`, y permanece solo en memoria para verificar firma y esquema durante un máximo de diez segundos; se acepta expresamente esa excepción de tránsito, pero el cuerpo nunca se encola, persiste ni registra.
  Tras validarlo, el único payload persistible en Pub/Sub es un sobre normalizado con `delivery_guid`, `event`, `received_at`, `installation_id` y `evaluator_revision`; solo si la fuente y el evento los aportan puede añadir `action`, `repository_id`, `pull_number`, `head_sha`, `base_sha`, `before_sha`, `after_sha`, `head_ref`, `base_ref`, `check_suite_id`, `check_run_id` y `redelivery`, y un cambio de instalación usa solo identificadores numéricos de repositorio. WP017-DOR-5 fijará obligatoriedad por evento; no se inventa un campo ausente ni se rechaza uno no aplicable, y todo campo desconocido se descarta.
  Solo se consultan endpoints necesarios para esas proyecciones y los objetos Git de la frase siguiente. Sus respuestas brutas inevitables pueden transportar transitoriamente campos incidentales que GitHub no permite excluir —incluidos autor, correo y mensaje de commit, URL y metadatos de objeto—, pero solo dentro de un buffer volátil, sin persistencia ni logs, para extraer: propietario y nombre usados al direccionar la API; número, estado y `draft` de PR; refs, SHA e identificadores de repositorio, instalación, App, check suite y check run; estado y conclusión; metadatos de entrega; y cabeceras numéricas de rate limit. El buffer se descarta inmediatamente tras proyectar y nunca alimenta la decisión.
  Para ejecutar intacto `scripts/check_scope.py` se admiten en almacenamiento volátil los objetos commit y tree necesarios y alcanzables desde `base_sha` y `head_sha`, incluido su merge-base, y los blobs que Git demande para `git diff -M -C --find-copies-harder`, incluido el contrato WP del merge-base y los destinos de symlinks cambiados; no se crean checkout, archive ni almacenamiento durable. Respuestas REST, objetos y repositorio Git efímero desaparecen al obtener resultado terminal o, como máximo, a los quince minutos.
  Firestore solo puede persistir `installation_id`, `repository_id`, `pull_number`, `delivery_guid`, `event`, `action`, `head_sha`, `base_sha`, `before_sha`, `after_sha`, `head_ref`, `base_ref`, `check_suite_id`, `check_run_id`, `redelivery`, `evaluator_revision`, `status`, `conclusion`, `reason_code`, `attempt_count`, `created_at`, `updated_at`, `lease_until` y `expires_at`, con ausencia explícita cuando no aplique; se prohíben payloads, objetos Git, nombres, rutas y texto libre. WP017-DOR-5 fijará esquema y bindings sin añadir campos.
  Cómputo y persistencia de contenido de aplicación quedan en `europe-west1`: Cloud Run regional; política Pub/Sub exactamente `europe-west1` con `enforceInTransit=true`; Firestore Standard regional, incluidas sus réplicas internas entre zonas; y bucket de logs definido por el usuario en esa región. Cloud Scheduler lleva solo un disparador autenticado sin datos de repositorio. Fuera de región se admiten únicamente el tránsito del webhook ya declarado y metadatos de control del proveedor sin contenido GitHub.
  El tránsito usa TLS y la persistencia no secreta usa el cifrado en reposo predeterminado de Google. Solo acceden identidades de servicio dedicadas con mínimo privilegio; Iván es el único acceso humano, solo break-glass para incidente o borrado, con auditoría y sin lectura rutinaria. Los logs obligatorios de auditoría pueden conservar identidad IAM, recurso de infraestructura, operación, tiempo y resultado durante los 400 días de `_Required`; nombres de proyecto y recursos no contendrán datos ni identificadores de GitHub. WP017-DOR-4 conserva íntegra la custodia de secretos y claves, y WP017-DOR-5 los bindings exactos.
  Pub/Sub conserva mensajes no confirmados exactamente tres días, descarta los confirmados sin retención y no habilita retención de topic ni snapshots. Todo registro Firestore nace con `expires_at ≤ created_at + 7 días`; solo una reconciliación satisfactoria de una PR todavía activa puede renovarlo por hasta siete días y un estado terminal fija `expires_at ≤ terminal_at + 7 días`. El servicio borra al vencer, TTL es defensa adicional y una lectura debe acreditar ausencia antes de `expires_at + 24 h`; desinstalación o retirada exige igual comprobación en veinticuatro horas. Esa ausencia es borrado lógico, no prueba física: con PITR deshabilitado pueden subsistir versiones una hora y las copias internas cifradas del proveedor durante su proceso de eliminación, hasta aproximadamente 180 días desde la solicitud; el servicio no puede comprobar su destrucción física. No se configuran backups, PITR, exportaciones, snapshots, retención adicional ni otras copias controlables por el cliente.
  Los logs de aplicación van exclusivamente al bucket regional, catorce días y excluidos de `_Default`; logs, métricas y alertas prohíben secretos, cuerpos, nombres, rutas, refs, SHA, GUID e identificadores GitHub y solo admiten códigos de razón cerrados y agregados de conteo, duración, edad de cola y clase de estado; una alerta añade servicio, región, umbral, severidad, tiempo y enlace. La retención administrada de métricas e incidentes se acepta solo por carecer de contenido identificable. Esta resolución no crea recursos ni resuelve WP017-DOR-5 a DOR-9.
- **WP017-DOR-4 — resuelto por decisión humana del 2026-09-27.** La clave privada de la GitHub App reside como versión importada no exportable de una clave asimétrica `SOFTWARE` de Cloud KMS en `europe-west1`, con propósito `ASYMMETRIC_SIGN` y algoritmo `RSA_SIGN_PKCS1_2048_SHA256`; el secreto del webhook reside en un secreto regional de Secret Manager en `europe-west1`, consumido por número de versión explícito, nunca `latest`. Se prohíben réplicas, exportaciones, copias gestionadas por el cliente y cualquier ubicación alternativa.
  Iván es el único custodio humano. Solo durante ceremonias aprobadas recibe temporalmente `roles/cloudkms.admin` y `roles/cloudkms.importer` sobre el key ring exacto —incluidos la clave y el `ImportJob` exacto, que requiere consulta y `useToImport`—, `roles/cloudkms.signer` y `roles/cloudkms.publicKeyViewer` sobre esa clave solo para la prueba y la huella, y `roles/secretmanager.secretVersionAdder` y `roles/secretmanager.secretVersionManager` sobre el secreto exacto; nunca roles básicos `Owner` o `Editor`, `secretAccessor` ni lectura rutinaria, y al terminar se retiran. La identidad dedicada de firma recibe solo `roles/cloudkms.signer` sobre la clave exacta y la receptora solo `roles/secretmanager.secretAccessor` sobre el secreto exacto; ninguna recibe el rol de la otra, claves de cuenta de servicio ni acceso de agente. WP017-DOR-5 fijará nombres y bindings exactos sin ampliar estos máximos.
  En ejecución el servicio entrega a KMS únicamente el digest SHA-256 para `asymmetricSign`, construye JWT `RS256` con `iat` sesenta segundos atrás y `exp` no superior a diez minutos, y no obtiene el PEM; el receptor obtiene en memoria la versión numérica autorizada del secreto, verifica `X-Hub-Signature-256` en tiempo constante y la descarta. Un valor ausente, inaccesible, no fijado o no verificable falla cerrado y nunca produce éxito.
  El alta de la clave es un acto humano: antes de generar el PEM en GitHub, Iván prepara fuera de todo repositorio un volumen temporal cifrado, sin sincronización ni copia de seguridad, y dirige allí la descarga; comprueba tamaño RSA y huella pública SHA-256 contra la publicada por GitHub, convierte localmente PKCS#1 PEM a PKCS#8 DER, lo importa mediante un import job vigente con envoltura local y verifica huella pública y una firma de mensaje conocido. Una clave divergente, no importable o no verificable mantiene el servicio detenido; si es la única de la App, Iván genera una sustituta bajo esta custodia, elimina y verifica inmediatamente la retirada de la fallida en GitHub, y solo tras importar y verificar la sustituta puede reanudar. El secreto aleatorio de alta entropía del webhook se introduce una sola vez por Iván en Secret Manager y GitHub mediante sus interfaces oficiales, sin argumentos de comando, salida, captura ni agente; cualquier portapapeles temporal se vacía inmediatamente.
  Solo tras ambas verificaciones se destruyen el volumen temporal y su clave de cifrado y se comprueba que las rutas previstas, papelera, historial, portapapeles y destinos configurados de sincronización o backup no contienen copias. La evidencia conserva únicamente identificadores de recurso y versión, huellas públicas, tiempos y resultado; nunca bytes, valores, JWT, firmas, comandos con secretos ni capturas. Esto acredita eliminación lógica o criptográfica de las copias locales controladas, no borrado físico forense; cualquier copia no inventariada o verificación fallida obliga a revocar y rotar.
  La rotación programada máxima es de noventa días y la de emergencia es inmediata. Para la clave se genera otra clave GitHub, se importa y verifica otra versión KMS, se cambia el pin, se prueba con mensaje conocido y se admite solape de las dos claves GitHub durante un máximo de veinticuatro horas; después se elimina la anterior en GitHub, se deshabilita su versión KMS y, tras siete días sin necesidad de rollback, se programa su destrucción conforme al periodo de KMS. Para el webhook se añade otra versión, el receptor acepta exclusivamente las dos versiones numeradas durante un máximo de diez minutos mientras Iván actualiza GitHub, una entrega firmada con la nueva debe validarse, y entonces se deshabilita la anterior; tras siete días se destruye. La clave puede volver al pin anterior solo antes de eliminarla; el webhook nunca revierte solo el pin local: mantiene ambos durante la ventana para realinear GitHub y, si no verifica a tiempo, detiene la recepción y exige otra rotación.
  Ante sospecha de clave se detienen emisión y servicio, se retira el binding de firma y se suspenden humanamente las instalaciones afectadas; si la comprometida es la única clave GitHub, Iván genera primero una sustituta bajo esta custodia, elimina y verifica inmediatamente la ausencia de la afectada en GitHub y deshabilita su versión KMS, sin esperar a importar la nueva. Revoca los tokens conocidos; solo reactiva instalaciones con sustituta importada y verificada, bindings auditados y una vez transcurrida la vida máxima documentada de cualquier token desde la retirada verificada de la última capacidad afectada de emisión, incluida la clave GitHub. Ante sospecha del webhook se detiene la aceptación hasta sustituirlo; ante compromiso de identidad se deshabilita o desvincula y se rota todo secreto que pudiera usar, considerando que `signer` permite firmar aunque no extraer.
  Se habilitan logs de Data Access para acceso al secreto y operaciones criptográficas, además de Admin Activity; alertas y evidencias usan solo identidad, recurso, versión, operación, tiempo, resultado y huella pública. Esta resolución no crea recursos ni resuelve WP017-DOR-5 a DOR-9.
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
Los cinco bloqueos restantes no se sustituyen por defaults o conjeturas.

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
Nota: lista vacía deliberada y fail-closed hasta resolver WP017-DOR-5.

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

- GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-ci-checks-with-a-github-app>, <https://docs.github.com/en/rest/checks/runs>, <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>, <https://docs.github.com/en/webhooks/webhook-events-and-payloads>, <https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries>, <https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks>, <https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries>, <https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/viewing-webhook-deliveries>, <https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/redelivering-webhooks>, <https://docs.github.com/en/rest/apps/webhooks>, <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation>, <https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app>, <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps>, <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app>, <https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app>, <https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/rate-limits-for-github-apps>, <https://docs.github.com/en/rest/git>, <https://docs.github.com/en/rest/git/commits>, <https://docs.github.com/en/rest/git/trees> y <https://docs.github.com/en/rest/git/blobs>.
- Google Cloud Docs, <https://cloud.google.com/run/docs/locations>, <https://cloud.google.com/run/pricing>, <https://cloud.google.com/run/docs/configuring/max-instances>, <https://cloud.google.com/run/docs/deploying>, <https://cloud.google.com/run/docs/managing/revisions>, <https://cloud.google.com/run/docs/container-contract>, <https://cloud.google.com/artifact-registry/docs/docker/names>, <https://cloud.google.com/artifact-registry/docs/container-concepts>, <https://cloud.google.com/pubsub/pricing>, <https://cloud.google.com/pubsub/docs/resource-location-restriction>, <https://cloud.google.com/pubsub/docs/subscription-message-retention>, <https://cloud.google.com/pubsub/docs/subscription-properties>, <https://cloud.google.com/firestore/pricing>, <https://cloud.google.com/firestore/docs/locations>, <https://cloud.google.com/firestore/native/docs/ttl>, <https://cloud.google.com/firestore/docs/backups>, <https://cloud.google.com/firestore/native/docs/use-pitr>, <https://cloud.google.com/scheduler/pricing>, <https://cloud.google.com/logging/docs/region-support>, <https://cloud.google.com/logging/docs/buckets>, <https://cloud.google.com/logging/docs/store-log-entries>, <https://cloud.google.com/logging/docs/audit>, <https://cloud.google.com/monitoring/quotas>, <https://cloud.google.com/docs/security/encryption/default-encryption>, <https://cloud.google.com/security/encryption>, <https://cloud.google.com/docs/security/deletion>, <https://cloud.google.com/run/docs/securing/security> y <https://cloud.google.com/kms/pricing>.
- Google Cloud Docs, <https://cloud.google.com/kms/docs/key-import>, <https://cloud.google.com/kms/docs/importing-a-key>, <https://cloud.google.com/kms/docs/create-validate-signatures>, <https://cloud.google.com/kms/docs/reference/permissions-and-roles>, <https://cloud.google.com/kms/docs/destroy-restore>, <https://cloud.google.com/kms/docs/key-states>, <https://cloud.google.com/kms/docs/audit-logging>, <https://cloud.google.com/secret-manager/docs/locations>, <https://cloud.google.com/secret-manager/regional-secrets/best-practices-rs>, <https://cloud.google.com/secret-manager/regional-secrets/manage-access-regional-secrets>, <https://cloud.google.com/secret-manager/docs/access-control>, <https://cloud.google.com/secret-manager/docs/rotation-recommendations> y <https://cloud.google.com/secret-manager/docs/audit-logging>.
