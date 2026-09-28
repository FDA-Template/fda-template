# WP-017 — Productor externo de Alcance FDA

estado: blocked
prioridad: P0
riesgo: T3
agente_responsable: Claude Code (implementer)
agente_revisor: GPT-6 Astra (Alto, contexto nuevo, solo lectura)
requisitos: [REQ-FDA-001, REQ-FDA-002, SEC-001]
adr: [ADR-001]
decision: [DEC-003, DEC-010, DEC-011, DEC-014, DEC-015, DEC-016]
presupuesto_max_eur: 100
max_ciclos_correccion: 2

Este contrato queda `blocked`, nunca `done`, por DEC-010 §10: no fue aprobado,
admitido, activado o implementado; su transición DOR-7 agotó C1/C2 sin coste
reconstruible y DOR-7 a DOR-9 siguen abiertos. Queda retirado de la cola
ejecutable; otro productor exige una decisión posterior y otro WP-ID todavía no
reservado. La base histórica de redacción fue `origin/main` `9d69fcc6031cd2a4a98621f0e8a17056e172c6c2`.

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
- **WP017-DOR-5 — resuelto por decisión humana del 2026-09-27.** DEC-016
  delega estas elecciones al contrato, por lo que no hace falta otra decisión.
  Las listas hoja, stack, recursos, IAM, esquemas, red, matriz de eventos y
  comandos quedan cerrados íntegramente en este contrato. La resolución no crea ni
  ejecuta nada y no eligió entonces propietario, instalación o ensayo real,
  operación, política evaluada ni semántica de SHA compartido; no anticipó DOR-6 a DOR-9.
- **WP017-DOR-6 — resuelto por decisión humana del 2026-09-27.** DEC-016 delega el ensayo al contrato: no hace falta otra decisión. Iván (`@ivanes189`) es el único operador humano del ensayo y el propietario de la GitHub App privada —`Only on this account`— de nombre exacto propuesto `alcance-fda-ivanes189`; el alta futura debe acreditar nombre aceptado, `app.id` y `app.slug` reales o detenerse, y esta función acotada no designa la operación continuada de DOR-7.
  El fixture gobernado es el futuro repositorio público sintético `ivanes189/fda-template-alcance-lab`, hoy inexistente, con `main` por defecto y sin copia de código, historia, datos ni configuración de producción. Un acto humano posterior lo creará exclusivamente desde el manifiesto y bytes de `tests/alcance_fda/fixtures.json` del `TESTED_HEAD` confiable, registrará SHA-256 y commit de cada estado y usará solo `wp/WP-017-dor6-red`, `wp/WP-017-dor6-green`, `ops/wp017-dor6-red`, `ops/wp017-dor6-green`, `wp/WP-017-dor6-source`, `wp/WP-017-dor6-main-b1` y `wp/WP-017-dor6-main-b2`; DOR-8 fijará antes sus contenidos y oráculos de política y DOR-9 el caso concurrente, sin que esta resolución los invente.
  La App se registra sin autorización de usuario, con webhook activo y SSL, permisos y eventos exactamente DOR-5, y se instala mediante `Only select repositories` únicamente en el lab; queda prohibida su instalación en `ivanes189/fda-template`. El ensayo no empieza hasta que DOR-7 a DOR-9 estén resueltos, WP-017 esté aprobado, admitido, activo, implementado y desplegado desde los pins acreditados, custodia y bindings coincidan con DOR-4/5, el lab esté limpio y el ruleset productivo tenga preimagen capturada y cero delta al cierre; cualquier deriva, permiso adicional, plan de pago o nombre no disponible obliga a parar.
  Iván crea en el lab el ruleset `wp017-dor6-lab`, activo, sin bypass ni regla de PR, dirigido solo a `refs/heads/main` y con `strict_required_status_checks_policy:true`: primero incorpora el required check preexistente `Alcance FDA` con cualquier fuente; después de que la App instalada publique allí un check run `success` dentro de los siete días anteriores, cambia únicamente su fuente al par `{"context":"Alcance FDA","integration_id":<app.id real>}`. Se conservan los estados completos ausencia→cualquier fuente→App y su delta; si GitHub no ofrece esa selección con `Statuses:write`, no se amplían permisos ni se prueba en producción.
  La única ventana dura como máximo 120 minutos desde un inicio UTC registrado y admite como máximo `5 EUR` de coste incremental total —sin compra ni cambio de plan—; se detiene al vencer cualquiera de ambos límites. La matriz ejecuta los once casos de DEC-015 §6 sobre fixtures ya aprobados y separa: política inválida, donde la App concluye `failure`; indisponibilidad, ausencia o pendiente, que nunca inventa terminalidad; fuente, donde el workflow sintético `pull_request` y elegible publica el único `Alcance FDA` `success` sobre H desde una App distinta mientras la instalación esperada está suspendida y el par del ruleset más ausencia de check run del `app.id` esperado y `mergeStateStatus=BLOCKED` prueban el rechazo, seguido sobre el mismo H por reconciliación, check esperado `success` y `mergeStateStatus=CLEAN`; y carrera §6.8(a), donde el verde anterior permanece pero, antes de reevaluar, el avance B1 no contenido en H bloquea por strict. §6.8(b) conserva literalmente `B0→B1→P→HEAD` y ambas ancestralidades. Para cada avance, b1/b2 recibe primero `Alcance FDA success` de la App sobre su SHA exacto y luego Iván actualiza `main` por fast-forward protegido a ese mismo SHA, sin force-push ni bypass, verificando igualdad y ancestralidades antes/después; las PR sometidas a oráculo nunca se fusionan.
  `artifacts.json` conserva identidad pública de App, instalación, repositorio y ruleset, pins, huellas, preimagen/postimagen/delta y consultas; `matrix.json`, por caso, PR, evento elegible, ramas, ancestralidades, head/base, check suite/run, `app.id`, conclusiones, rollup, estado de fusión y UTC; `commands.log`, códigos headless redactados; `cost.md`, pre/post y total; `CIERRE.md`, resultado y excepciones, nunca secretos ni payloads. Al terminar o ante el primer fallo Iván cierra sin fusionar las PR de oráculo, restaura la ausencia inicial eliminando el ruleset del lab, desinstala allí la App, verifica instalación ausente y producción idéntica a su preimagen, y archiva el lab; la App privada se conserva sin instalación para DOR-7. Si una comprobación falla, el cierre queda bloqueado y no se declara ensayo limpio.
- **WP017-DOR-7 — operación.** Designar responsable de alertas, continuidad,
  recuperación, despliegue, rollback, desinstalación y respuesta a incidentes.
- **WP017-DOR-8 — política evaluada.** Versionar la interfaz completa `wp/*` y
  `ops/*`: gramáticas, autorización, firmante permitido, consultas, digest,
  semántica DEC-015 y oráculos negativos. WP-016 `draft` no es su fuente.
- **WP017-DOR-9 — SHA compartido.** Fijar una regla de publicación conservadora
  y su ensayo concurrente cuando dos PR comparten commit y dan resultados
  opuestos; `pull_number` o `external_id` no demuestran aislamiento en GitHub.

Cada resolución debe quedar versionada en este contrato mediante acto humano.
Los tres bloqueos restantes no se sustituyen por defaults o conjeturas.

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

- services/alcance_fda/.dockerignore
- services/alcance_fda/.python-version
- services/alcance_fda/Dockerfile
- services/alcance_fda/OPERATION.md
- services/alcance_fda/pyproject.toml
- services/alcance_fda/uv.lock
- services/alcance_fda/src/alcance_fda/__init__.py
- services/alcance_fda/src/alcance_fda/app.py
- services/alcance_fda/src/alcance_fda/config.py
- services/alcance_fda/src/alcance_fda/evaluator.py
- services/alcance_fda/src/alcance_fda/gcp.py
- services/alcance_fda/src/alcance_fda/github.py
- services/alcance_fda/src/alcance_fda/models.py
- services/alcance_fda/src/alcance_fda/policy.py
- services/alcance_fda/src/alcance_fda/storage.py
- services/alcance_fda/src/alcance_fda/telemetry.py
- services/alcance_fda/infra/.terraform.lock.hcl
- services/alcance_fda/infra/iam.tf
- services/alcance_fda/infra/logging.tf
- services/alcance_fda/infra/main.tf
- services/alcance_fda/infra/outputs.tf
- services/alcance_fda/infra/schemas/event-v1.avsc
- services/alcance_fda/infra/variables.tf
- services/alcance_fda/infra/versions.tf
- tests/alcance_fda/conftest.py
- tests/alcance_fda/fixtures.json
- tests/alcance_fda/test_container.py
- tests/alcance_fda/test_evaluator.py
- tests/alcance_fda/test_events.py
- tests/alcance_fda/test_github.py
- tests/alcance_fda/test_iac.py
- tests/alcance_fda/test_idempotency.py
- tests/alcance_fda/test_models.py
- tests/alcance_fda/test_policy.py
- tests/alcance_fda/test_reconcile.py
- tests/alcance_fda/test_security.py
- tests/alcance_fda/test_shared_sha.py
- tests/alcance_fda/test_webhook.py
- tests/alcance_fda/verify.py
- work-packages/WP-017-productor-externo-alcance.md
- evidence/WP-017/CIERRE.md
- evidence/WP-017/artifacts.json
- evidence/WP-017/ciclos.md
- evidence/WP-017/commands.log
- evidence/WP-017/cost.md
- evidence/WP-017/matrix.json

Lista cerrada: toda ruta no enumerada queda denegada. `OPERATION.md`,
`policy.py`, `test_policy.py` y `test_shared_sha.py` reservan el destino de las
resoluciones DOR-7 a DOR-9, pero DOR-5 no autoriza ni inventa su contenido.

## Archivos prohibidos

- .github/**
- .claude/**
- .agents/**
- .codex/**
- AGENTS.md
- CLAUDE.md
- CODEOWNERS
- work-packages/ACTIVE
- work-packages/WP-016-check-scope-ci.md
- scripts/check_scope.py
- scripts/scope_rules.py
- tests/guard/run-suite.sh
- specs/**
- docs/**

Estas prohibiciones son redundantes y explícitas: prevalecen ante cualquier
solapamiento accidental. Los dos scripts se importan desde la revisión
confiable, pero WP-017 no los modifica.

## Contratos técnicos

**Stack cerrado.** CPython `3.11.16`, Git Debian `1:2.47.3-0+deb13u1` e imagen `ghcr.io/astral-sh/uv:0.12.19-python3.11-trixie-slim@sha256:e8375931acd70cca124f409b4b80316f78dd9c6c55e2563795bed61495952ae4`, OCI `linux/amd64`. Producción fija Flask `3.1.3`, Gunicorn `26.2.0`, HTTPX `0.28.1`, Pydantic `2.13.5`, google-cloud-firestore `2.32.0`, google-cloud-kms `3.17.0`, google-cloud-pubsub `2.41.0` y google-cloud-secret-manager `2.30.0`; desarrollo fija pytest `9.1.1`, pytest-cov `7.1.0`, Ruff `0.16.9`, mypy `2.3.1`, pip-audit `2.10.1`, respx `0.23.1`, pytest-socket `0.8.1`, Bandit `1.9.4` y python-hcl2 `8.1.4`. `pyproject.toml` usa igualdad exacta; `uv.lock` se versiona. IaC fija Terraform `1.16.4`, proveedor `hashicorp/google` `8.4.0` y lockfile con checksums firmados; verificación fija uv `0.12.19`, Gitleaks `8.30.0` con canarios, Docker Engine `29.7.2` y Buildx `0.37.1`; toda deriva detiene.

**Artefacto e IaC.** Artifact Registry: repositorio Docker `alcance-fda`, imagen `producer`, tags inmutables y despliegue exclusivo de `europe-west1-docker.pkg.dev/PROJECT_ID/alcance-fda/producer@sha256:DIGEST`; la imagen etiqueta revisión fuente, `evaluator_revision` y SHA-256 de los dos scripts confiables. No se autoriza backend ni bucket: solo `init -backend=false` y `validate`; `plan`, `apply` y estado real siguen bloqueados hasta DOR-7.

**Recursos exactos.** En `europe-west1`: Cloud Run `alcance-fda-ingress` —ingress `all`, 1 CPU, 512 MiB, concurrencia 20, timeout 10 s, min 0, máximo de servicio 1— y `alcance-fda-worker` —ingress `internal`, 1 CPU, 1 GiB, concurrencia 1, timeout 600 s, min 0, máximo de servicio 2—; todo rollout conserva máximo agregado 3. Pub/Sub: schema Avro/JSON `alcance-fda-envelope-v1`, topic `alcance-fda-events`, push subscription `alcance-fda-worker-push`, no confirmados 3 días, sin retención de topic ni snapshots, ack 600 s. Firestore Standard regional: database_id `alcance-fda`, no `(default)`, PITR ni backups. Scheduler: `alcance-fda-reconcile`, `*/5 * * * *`, UTC, POST OIDC a `/reconcile`. Logging: bucket regional `alcance-fda-app` 14 días, sink `alcance-fda-app`, exclusión `alcance-fda-app-default` de aplicación en `_Default`. KMS: ring `alcance-fda`, key `github-app-signing`; secreto regional `github-webhook-secret`. Se reservan, sin crear, `alcance-fda-monthly-budget`, `alcance-fda-queue-age`, `alcance-fda-errors` y `alcance-fda-cost-stop`; no hay VPC, NAT, SQL, Storage, Functions, GKE ni otros recursos.

**IAM exacto de runtime.** SAs `alcance-fda-ingress`, `alcance-fda-worker`, `alcance-fda-push` y `alcance-fda-scheduler` bajo `PROJECT_ID.iam.gserviceaccount.com`, sin keys. `allUsers` obtiene `roles/run.invoker` solo en ingress; push y scheduler, solo en worker. Ingress obtiene `roles/secretmanager.secretAccessor` solo en el secreto regional —configuración fija versión numérica— y `roles/pubsub.publisher` solo en el topic. Worker obtiene `roles/cloudkms.signer` solo en la key, `roles/datastore.user` condicionado a `resource.name == "projects/PROJECT_ID/databases/alcance-fda"` y publisher solo en el topic; nunca el secreto. `service-PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com` obtiene `roles/iam.serviceAccountTokenCreator` solo sobre la SA push; se conservan sin ampliar roles administrados Pub/Sub/Scheduler. Sin roles básicos, humanos ni de build/deploy; DOR-7 fija operador dentro de DOR-4.

**Pub/Sub cerrado.** Cada sobre exige `delivery_guid:string`, `event` enum `check_suite|pull_request|push|installation|installation_repositories`, `received_at:timestamp-millis`, `installation_id:long`, `evaluator_revision:string`; solo admite nullable `action:string`, `repository_id:long`, `pull_number:long`, `head_sha:string`, `base_sha:string`, `before_sha:string`, `after_sha:string`, `head_ref:string`, `base_ref:string`, `check_suite_id:long`, `check_run_id:long`, `redelivery:boolean`. Schema Pub/Sub y Pydantic rechazan extras.

**Firestore cerrado.** `deliveries/{delivery_key}` contiene exclusivamente `delivery_guid,event,installation_id,evaluator_revision,action,repository_id,pull_number,head_sha,base_sha,before_sha,after_sha,head_ref,base_ref,check_suite_id,check_run_id,redelivery,status,reason_code,attempt_count,created_at,updated_at,lease_until,expires_at`: no persiste `received_at`; `delivery_key` es GUID, `GUID:repository_id` o `GUID:all`. `evaluations/{sha256(identity)}` contiene exclusivamente `installation_id,repository_id,pull_number,head_sha,base_sha,evaluator_revision,status,conclusion,reason_code,attempt_count,check_suite_id,check_run_id,created_at,updated_at,lease_until,expires_at`. `access/{installation_id}--{repository_id}` contiene exclusivamente ambos IDs, `status,created_at,updated_at,expires_at`. IDs/contadores son integer, fechas timestamp y el resto string salvo redelivery boolean; `status=queued|leased|evaluating|reported|stale|disabled|error`, `conclusion=success|failure`, `reason_code=duplicate|unsupported|invalid_schema|installation_disabled|stale|rate_limited|github_unavailable|evaluator_error|policy_failure|timeout`; extra falla cerrado y `expires_at` cumple DOR-3.

**Entrada y matriz.** Primero HMAC de bytes brutos, `X-GitHub-Event`, `X-GitHub-Delivery` y, salvo `ping`, `installation.id`; firma mala/ausente: 401 sin cola; schema admitido inválido: 400; tipo/acción no admitido: 204 sin persistencia; válido: 202 solo tras cola durable y antes de 10 s. Seleccionados únicamente `pull_request` y `push`; automáticos por GitHub: `check_suite`, `check_run`, `installation`, `installation_repositories` y `ping`.

| Evento | Acciones admitidas | Obligatorios además de los comunes | Efecto |
|---|---|---|---|
| `check_suite` | `requested,rerequested` | `action,repository_id,check_suite_id,head_sha`; PR solo si viene | evaluar/reconciliar |
| `check_suite` | `completed` | ninguno persistido | 204 |
| `check_run` | `created,completed,rerequested,requested_action` | ninguno persistido | 204 anti-bucle |
| `pull_request` | `opened,reopened,synchronize,edited,converted_to_draft,ready_for_review,closed` | `action,repository_id,pull_number,head_sha,base_sha,head_ref,base_ref` | evaluar/invalidar/cerrar evaluación |
| `push` | sin acción; solo `refs/heads/main` | `repository_id,before_sha,after_sha` | reconciliar PR abiertas |
| `installation` | `created,deleted,suspend,unsuspend,new_permissions_accepted` | `action`; repo ausente | reconciliar/deshabilitar instalación |
| `installation_repositories` | `added,removed`, array no vacío | `action` y sobre por `repository_id` | reconciliar/borrar acceso |
| `installation_repositories` | `added,removed`, array vacío | `action`; repo ausente, key `GUID:all` | reconciliar instalación completa sin inventar ID |
| `ping` | ninguna | nada persistido | validar firma y 204 |

Permisos exactos: `Checks: read/write`, `Commit statuses: read/write`, `Contents: read`, `Pull requests: read`, `Metadata: read` implícito; no `installation_target`. Statuses write solo permite seleccionar productor; no se publica status. REST fija `X-GitHub-Api-Version: 2026-03-10`; campo ausente se resuelve por API o falla, nunca se inventa. Redelivery conserva GUID; GitHub no reentrega fallos solo, por lo que el reconciliador inventariaría las entregas fallidas y solicitaría redelivery cuando DOR-6 lo autorice.

**Red exacta.** Entrada: ingress `POST /webhook`; worker interno `POST /pubsub` OIDC y `POST /reconcile` OIDC; ambos tokens fijan `audience` a la URI base exacta del worker devuelta por Cloud Run, sin ruta ni parámetros, y IaC verifica esa igualdad. Runtime saliente: `api.github.com:443` HTTPS `GET|POST|PATCH`; `github.com:443` Git smart HTTP `GET|POST` a bare efímero, token solo en `http.extraHeader` por entorno; `pubsub.europe-west1.rep.googleapis.com:443` RPC `Publish`; `firestore.europe-west1.rep.googleapis.com:443` RPC `BatchGetDocuments|RunQuery|Commit`; `secretmanager.europe-west1.rep.googleapis.com:443` RPC `AccessSecretVersion`; `europe-west1-cloudkms.googleapis.com:443` RPC `AsymmetricSign`; `metadata.google.internal:80` GET para ADC/OIDC. Build únicamente: `ghcr.io:443` HEAD/GET; `pypi.org|files.pythonhosted.org|deb.debian.org|registry.terraform.io|releases.hashicorp.com:443` GET; `europe-west1-docker.pkg.dev:443` HEAD/GET/POST/PUT, carga monolítica. Pub/Sub usa endpoint regional con `enforceInTransit=true`; tests niegan red salvo loopback. Otro host, puerto, método o RPC falla cerrado.

**Invariantes.** JWT App solo para tokens de instalación y redelivery; token efímero y limitado; check run exacto `Alcance FDA`; identidad `repository_id+pull_number+head_sha+base_sha+evaluator_revision`; repositorio Git bare sin checkout; solo se ejecutan servicio, política y scripts de revisión confiable; cola antes de 202; dedupe/reintento/obsolescencia y reconciliación cada cinco minutos; ningún byte de PR se ejecuta o importa. DOR-8 y DOR-9 impiden todo verde admisible hasta resolverse.

## Entorno autorizado

Secretos: ninguno para agentes; actos humanos usan exclusivamente DOR-4. Infraestructura, cuenta, facturación, estado Terraform, build, push y despliegue no quedan autorizados por este contrato `draft`. Las únicas herramientas, versiones y comunicaciones futuras permitidas son las anteriores.

## Verificación

Contrato de comandos futuro, no autorización actual; una sola cadena headless conserva todo fallo:

```bash
uv lock --project services/alcance_fda --check && uv sync --project services/alcance_fda --frozen --all-groups --no-python-downloads && uv run --project services/alcance_fda --frozen ruff check services/alcance_fda tests/alcance_fda && uv run --project services/alcance_fda --frozen mypy services/alcance_fda tests/alcance_fda && uv run --project services/alcance_fda --frozen bandit -q -r services/alcance_fda/src && uv run --project services/alcance_fda --frozen pip-audit && uv run --project services/alcance_fda --frozen pytest -q --disable-socket --cov=alcance_fda --cov-fail-under=100 tests/alcance_fda && terraform -chdir=services/alcance_fda/infra fmt -check -recursive && env TF_DATA_DIR=/tmp/wp017-terraform-data terraform -chdir=services/alcance_fda/infra init -backend=false -input=false -lockfile=readonly && env TF_DATA_DIR=/tmp/wp017-terraform-data terraform -chdir=services/alcance_fda/infra validate && gitleaks dir --no-banner --redact --exit-code 1 services/alcance_fda && gitleaks dir --no-banner --redact --exit-code 1 tests/alcance_fda && uv run --project services/alcance_fda --frozen python tests/alcance_fda/verify.py
```

`verify.py` rechaza TTY/prompts/derivas; valida canario positivo y control limpio Gitleaks, esquemas, IAM, red, recursos, matriz positiva/negativa, HMAC, dedupe, fan-out incluido array vacío, desorden, obsolescencia, rate limit, reconciliación, redacción, código confiable, `terraform apply` ausente, imagen desde digest y autoensayo `--network none`. Los oráculos DOR-6/8/9 fallan cerrado hasta existir.

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

0. `blocked`: retirado de la cola ejecutable por DEC-010 §10; no se aprueba,
   admite, activa, implementa o reactiva mediante este contrato.
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
- Fuentes de DOR-5: GitHub Docs, <https://docs.github.com/en/rest/about-the-rest-api/api-versions>; Google Cloud Docs, <https://docs.cloud.google.com/pubsub/docs/authenticate-push-subscriptions>, <https://docs.cloud.google.com/pubsub/docs/reference/service_apis_overview>, <https://docs.cloud.google.com/run/docs/securing/ingress>, <https://cloud.google.com/firestore/docs/manage-databases>, <https://docs.cloud.google.com/firestore/native/docs/regional-endpoints>, <https://docs.cloud.google.com/secret-manager/regional-secrets/config-sm-rs> y <https://docs.cloud.google.com/kms/docs/reference/service-apis-overview>; Python.org, <https://www.python.org/downloads/release/python-31116/>; Astral, <https://docs.astral.sh/uv/concepts/projects/sync/> y <https://github.com/astral-sh/uv/pkgs/container/uv>; HashiCorp, <https://releases.hashicorp.com/terraform/>, <https://releases.hashicorp.com/terraform-provider-google/> y <https://developer.hashicorp.com/terraform/cli/commands/init>; proyectos oficiales, <https://github.com/gitleaks/gitleaks/releases/tag/v8.30.0>, <https://docs.docker.com/engine/release-notes/29/> y las páginas de versión fijadas en <https://pypi.org/>. Fuentes de DOR-6: GitHub Docs, <https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app>, <https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app>, <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>, <https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks>, <https://docs.github.com/en/rest/repos/rules>, <https://docs.github.com/en/rest/checks/runs>, <https://docs.github.com/en/graphql/reference/pulls>, <https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps> y <https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories>; Google Cloud Docs, <https://cloud.google.com/run/pricing>, <https://cloud.google.com/pubsub/pricing>, <https://cloud.google.com/firestore/pricing> y <https://cloud.google.com/scheduler/pricing>.
