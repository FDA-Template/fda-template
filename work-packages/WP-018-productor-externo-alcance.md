# WP-018 — Productor externo de Alcance FDA

estado: draft
prioridad: P0
agente_responsable: implementer     agente_revisor: code-reviewer
requisitos: [REQ-FDA-001, REQ-FDA-002, SEC-001]     adr: [ADR-001]
decisiones: [DEC-003, DEC-010, DEC-011, DEC-014, DEC-015, DEC-016, DEC-017]
riesgo: T3
presupuesto_max_eur: 100             max_ciclos_correccion: 2

## Objetivo y contexto

Un productor externo mínimo, reproducible y operable publica el check `Alcance FDA` usando bytes confiables de `main`, reconciliación, mínimo privilegio y ensayo aislado. Precede WP-016; no lo ejecuta.

WP-018 es el sucesor limpio reservado por DEC-017. Se redacta desde cero sobre `main`; la candidata histórica y sus bytes, historia y evidencias no son fuente.

## Definition of Ready

- DOR-1 heredada por DEC-017 §3: `ivanes189/fda-template`, Iván propietario, revisión confiable en `main` y artefacto por digest.
- DOR-2 heredada por DEC-017 §3: Google Cloud, proyecto exclusivo, `europe-west1`, facturación humana, `100 EUR` y `<=5 EUR/mes`.
- DOR-3 heredada por DEC-017 §3 y WP-017: minimización, residencia, cifrado, retención, borrado, accesos, copias y telemetría.
- DOR-4 heredada por DEC-017 §3 y WP-017: custodia humana, KMS solo-firma, secretos regionales, mínimo privilegio, rotación y emergencia.
- DOR-5 rederivada y reafirmada íntegramente en este contrato (§§3-8).
- DOR-6 rederivada y reafirmada íntegramente en este contrato (§9).
- **WP018-DOR-7 abierto:** falta la decisión humana de operación y continuidad.
- **WP018-DOR-8 abierto:** falta la política evaluada y sus oráculos completos.
- **WP018-DOR-9 abierto:** falta la regla conservadora para SHA compartido y concurrencia.

Mientras DOR-7, DOR-8 o DOR-9 sigan abiertos, permanece `draft`: no puede aprobarse, admitirse, activarse ni implementarse.

## Alcance

**Incluido:** receptor, cola durable, evaluador, cliente GitHub, reconciliador, estado mínimo, IaC, imagen por digest, pruebas sin red y laboratorio DOR-6.

**Fuera de alcance:** WP-016, ruleset productivo, workflows, cierre de WP-007, runtime, humo, E2, resolver DOR-7/8/9, ejecutar bytes de PR, crear cuentas/facturación o reutilizar la candidata histórica.

## Archivos permitidos

- services/alcance_fda_wp018/.python-version
- services/alcance_fda_wp018/pyproject.toml
- services/alcance_fda_wp018/uv.lock
- services/alcance_fda_wp018/Dockerfile
- services/alcance_fda_wp018/Dockerfile.dockerignore
- services/alcance_fda_wp018/src/alcance_fda_wp018/__init__.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/config.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/models.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/webhook.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/github.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/evaluator.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/store.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/app.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/worker.py
- services/alcance_fda_wp018/src/alcance_fda_wp018/reconcile.py
- services/alcance_fda_wp018/infra/.terraform.lock.hcl
- services/alcance_fda_wp018/infra/versions.tf
- services/alcance_fda_wp018/infra/variables.tf
- services/alcance_fda_wp018/infra/services.tf
- services/alcance_fda_wp018/infra/data.tf
- services/alcance_fda_wp018/infra/iam.tf
- services/alcance_fda_wp018/infra/observability.tf
- services/alcance_fda_wp018/infra/outputs.tf
- tests/alcance_fda_wp018/conftest.py
- tests/alcance_fda_wp018/fixtures.py
- tests/alcance_fda_wp018/test_webhook.py
- tests/alcance_fda_wp018/test_events.py
- tests/alcance_fda_wp018/test_evaluator.py
- tests/alcance_fda_wp018/test_github.py
- tests/alcance_fda_wp018/test_store.py
- tests/alcance_fda_wp018/test_reconcile.py
- tests/alcance_fda_wp018/test_iac.py
- tests/alcance_fda_wp018/test_no_network.py
- tests/alcance_fda_wp018/verify_contract.py
- docs/manual/MANUAL.md
- docs/manual/08-productor-alcance-fda-wp018.md
- evidence/WP-018/manifest.md
- evidence/WP-018/verification.md
- evidence/WP-018/security.md
- evidence/WP-018/review-astra.md
- evidence/WP-018/cost.md
- evidence/WP-018/ciclos.md
- evidence/WP-018/CIERRE.md
- evidence/WP-018/lab/preimage.json
- evidence/WP-018/lab/matrix.json
- evidence/WP-018/lab/commands.log
- evidence/WP-018/lab/postimage.json
- evidence/WP-018/lab/rollback.json
- evidence/WP-018/lab/CIERRE.md

## Archivos prohibidos

- work-packages/ACTIVE
- work-packages/WP-016-check-scope-ci.md
- work-packages/WP-017-productor-externo-alcance.md
- tests/guard/run-suite.sh
- scripts/check_scope.py
- scripts/scope_rules.py
- .claude/hooks/guard.sh
- .github/workflows/ci.yml
- .github/workflows/claude.yml
- .github/workflows/code-review.yml
- CODEOWNERS
- AGENTS.md

Todo archivo no enumerado en permitidos queda denegado. También quedan en solo
lectura `.agents/`, `.codex/`, ramas, worktrees y candidatas históricas.

## Contratos técnicos

### 1. Confianza y artefacto
- `TESTED_HEAD` es el SHA completo de `main` revisado, nunca la PR; la imagen contiene servicio y ambos scripts confiables exactamente de ese SHA.
- Base `python:3.13.15-slim-trixie` `linux/amd64` por manifest `sha256:37134a49d21d2120e4c4d73bb76f8a4ab9aef31f096f7ec2ead48c2feead4332`; Git Debian `1:2.47.3-0+deb13u1` exacto.
- `Dockerfile.dockerignore` niega todo el contexto raíz salvo archivos hoja del servicio y ambos scripts; un test compara el contexto admitido.
- La imagen lleva SBOM/procedencia, se publica/despliega solo por digest y registra `TESTED_HEAD`, digest, scripts y lockfiles.
- En repo Git efímero sin checkout invoca `python scripts/check_scope.py <wp_id_evaluado> <base_sha>...<head_sha>`; DOR-8 debe fijar su resolución determinista y `WP-018` queda solo como ejemplo del laboratorio; objetos Git son datos, nunca ejecución/import.

### 2. Runtime, dependencias y herramientas
- Herramientas: Python `3.13.15`; Git `1:2.47.3-0+deb13u1`; uv `0.12.19`; Terraform `1.16.4`; Google `8.4.0`; Engine `29.8.1`; Buildx `0.37.1`; Gitleaks `8.30.1`.
- Producción: `fastapi==0.141.1`, `uvicorn==0.53.0`, `pydantic==2.13.5`, `httpx==0.28.1`, `google-auth==2.58.1`, `google-cloud-pubsub==2.41.0`, `google-cloud-firestore==2.32.0`, `google-cloud-kms==3.17.0`, `google-cloud-secret-manager==2.30.0`.
- Desarrollo: `pytest==9.1.1`, `pytest-cov==7.1.0`, `coverage==7.16.1`, `pytest-socket==0.8.1`, `ruff==0.16.9`, `mypy==2.3.1`, `bandit==1.9.4`, `pip-audit==2.10.1`.
- `uv.lock` fija transitivas/hashes; `.terraform.lock.hcl`, proveedor/checksums; SBOM `docker/scout-sbom-indexer@sha256:4b67f29eb0d1244ab0f62de867ac5dafd7262fcd7ebbdefa6ec8aacd6b15252d`. Sin `latest`, rangos o descargas runtime.

### 3. Recursos exactos en `europe-west1`
- Cloud Run `alcance-fda-wp018-ingress` (min 0, max 1, concurrencia 20, timeout 10 s, ingress `all`) y `alcance-fda-wp018-worker` (min 0, max 2, concurrencia 1, timeout 600 s, ingress `internal`): máximo agregado 3.
- Artifact Registry: repositorio `alcance-fda-wp018`, imagen `producer`.
- Pub/Sub: schema `alcance-fda-wp018-envelope-v1`, topic `alcance-fda-wp018-events`, push `alcance-fda-wp018-worker-push`; no confirmados 3 días, confirmados sin retención, sin topic-retention/snapshots; solo `europe-west1`, `enforceInTransit=true`.
- Firestore Native `alcance-fda-wp018`, sin PITR/backups; TTL `expires_at` dentro del máximo 7 días DOR-3.
- KMS ring `alcance-fda-wp018`, key `github-app-signing`, ImportJob `github-app-signing-import-wp018`; `ASYMMETRIC_SIGN`, PKCS#8 DER, `RSA_SIGN_PKCS1_2048_SHA256`, no exportable.
- Secret regional `github-webhook-secret-wp018`, versión numérica fija; Logging bucket/sink `alcance-fda-wp018`, 14 días; budget `alcance-fda-wp018-monthly`, umbrales 50/80/100% de 5 EUR.
- Scheduler `alcance-fda-wp018-reconcile`, `*/5 * * * *` UTC; SAs `alcance-fda-wp018-ingress`, `alcance-fda-wp018-worker`, `alcance-fda-wp018-push`, `alcance-fda-wp018-scheduler`.

### 4. IAM exacto y oráculos
- `allUsers` recibe `roles/run.invoker` solo en ingress; push y scheduler
  reciben `roles/run.invoker` solo en worker; ninguna clave de cuenta de servicio.
- Ingress recibe `roles/secretmanager.secretAccessor` solo en el secreto
  regional y `roles/pubsub.publisher` solo en el topic.
- Worker recibe `roles/cloudkms.signer` solo en la clave y
  `roles/pubsub.publisher` solo en el topic. `roles/datastore.user` se concede
  en proyecto con condición `resource.name ==
  "projects/${PROJECT_ID}/databases/alcance-fda-wp018"`.
- El service agent Pub/Sub recibe `roles/iam.serviceAccountTokenCreator` solo
  sobre la cuenta push. Runtime no recibe roles básicos ni Admin.
- En ceremonias DOR-4, Iván recibe temporalmente `roles/cloudkms.admin` y
  `roles/cloudkms.importer` en ring/key/ImportJob, `roles/cloudkms.signer` y
  `roles/cloudkms.publicKeyViewer` en key, y `roles/secretmanager.secretVersionAdder`
  y `roles/secretmanager.secretVersionManager` en secreto; nunca accessor; se retiran.
- Verificación obligatoria, sin secretos: pruebas positivas sobre secreto,
  topic, clave y base autorizados y negativas sobre homólogos `-denied`; toda
  desviación o condición no verificable detiene el WP.

### 5. Esquemas cerrados y minimización
- Sobre Pub/Sub cerrado exige `delivery_guid,event,received_at,installation_id,
  evaluator_revision`; opcionales solo `action,repository_id,pull_number,
  head_sha,base_sha,before_sha,after_sha,head_ref,base_ref,check_suite_id,
  check_run_id,redelivery`. Strings/int/bool/timestamp; extras se rechazan.
- `installation_repositories` produce un sobre por ID numérico; array vacío usa
  solo instalación y reconcilia todo, sin inventar ID ni persistir listas.
- Firestore solo `deliveries`, `evaluations`, `access`, con subconjuntos del
  máximo DOR-3: IDs anteriores más `status,conclusion,reason_code,attempt_count,
  created_at,updated_at,lease_until,expires_at`; no payload, código, ruta o texto.
- Cada `expires_at <= created_at+7d`; solo PR activa reconciliada renueva <=7d y
  terminal <= terminal_at+7d. Borrado del servicio al vencer y TTL confirma
  ausencia antes de +24 h; sin PITR, backups, exports, snapshots ni copias propias.
- Telemetría prohíbe GUID, SHA, refs e IDs GitHub: solo reason codes cerrados y
  agregados de conteo, duración, edad de cola y clase de estado; alerta añade
  servicio, región, umbral, severidad, tiempo y enlace. Aplicación solo en bucket
  regional 14 días y excluida de `_Default`; `_Required` conserva auditoría 400d.

### 6. Webhook, eventos y entrega
- `POST /github/webhook`: cuerpo máximo 1 MiB; HMAC-SHA256 constante sobre bytes
  crudos antes de parsear; firma mala 401, schema admitido inválido 400, evento o
  acción no admitido 204 sin persistir, válido 202 tras cola durable y antes de 10 s.
- Matriz: `pull_request` `opened,reopened,synchronize,edited,
  converted_to_draft,ready_for_review,closed`; `check_suite`
  `requested,rerequested,completed`; `check_run`
  `created,rerequested,completed,requested_action` solo anti-bucle; `push` solo
  `refs/heads/main`; `installation` `created,deleted,suspend,unsuspend,
  new_permissions_accepted`; `installation_repositories` `added,removed`; `ping`.
- Encolan evaluación PR salvo `closed` y suite `requested|rerequested`; push y
  cambios de instalación reconcilian; `closed`, suite `completed`, run y ping no
  publican. GUID deduplica; redelivery conserva GUID.
- Obligatorios: PR `action,repository_id,pull_number,head/base_sha,head/base_ref`;
  suite `action,repository_id,head_sha,check_suite_id`; run `action,repository_id,
  head_sha,check_run_id`; push `repository_id,before/after_sha` sin `action`;
  installation solo `action`; installation_repositories añade cada ID. Ausente: 400.
- GitHub App: Checks rw, Commit statuses rw, Contents r, Pull requests r,
  Metadata implícito; sin Administration, Actions, Issues, Secrets ni escritura
  de contenido. REST header `X-GitHub-Api-Version: 2026-03-10`.
- Check exacto `Alcance FDA` en `head_sha`: evaluación completa conforme termina
  `success`; incumplimiento, entrada inválida o error evaluable, `failure`.
  Indisponibilidad deja ausente/pendiente, recupera o para; nunca inventa terminal.
- Idempotencia `repository_id+pull_number+head_sha+base_sha+evaluator_revision`;
  reintento actualiza su `check_run_id`; evaluación obsoleta nunca sobrescribe HEAD.
- Cada 5 min inventaría todas las PR abiertas y entregas fallidas, solicita
  redelivery por API y reevalúa; normal <=5 min, pérdida recuperada <=10 min.

## DOR-6: ensayo aislado reafirmado

- Iván es propietario y operador; App privada `Only on this account`, nombre
  propuesto `alcance-fda-wp018-ivanes189`; ID/slug real se acredita o se para.
- Lab propuesto `ivanes189/fda-template-alcance-wp018-lab`, público, sintético,
  sin secretos ni copia de producción; instalación `Only select repositories`
  solo en lab. Producción queda prohibida.
- Ruleset `wp018-dor6-lab`, solo `refs/heads/main`, activo, sin bypass ni regla
  de PR, `strict_required_status_checks_policy:true`; parte de required
  `Alcance FDA` con cualquier fuente y solo tras check real fija `{context:
  "Alcance FDA",integration_id:<app.id>}`. Si GitHub no lo ofrece, parada.
- Ramas reservadas: `wp/WP-018-dor6-red`, `wp/WP-018-dor6-green`,
  `ops/wp018-dor6-red`, `ops/wp018-dor6-green`, `wp/WP-018-dor6-source`,
  `wp/WP-018-dor6-main-b1`, `wp/WP-018-dor6-main-b2`.
- Ventana 120 min, coste incremental 5 EUR. Antes: DOR-7/8/9 resueltos,
  contrato ready/activo, factura humana, pins/IDs/permisos verificados,
  lab limpio, preimagen exportada y rollback ensayado en seco.
- Matriz obligatoria DEC-015 §6: (1) SHA/App real; (2) digest confiable; (3)
  rojo/verde `wp/*` y `ops/*`; (4) `[skip ci]`; (5) avance `main` y reevaluación;
  (6) duplicado y obsoleto; (7) entrega fallida recuperada <=10 min; (8a) B1 no
  ancestro de P bloqueado por strict y (8b) `B0→B1→P→HEAD` con ancestralidades y
  digest; (9) productor homónimo rechazado y App seleccionable sin status; (10)
  cero ejecución de PR/permisos extra; (11) cero secretos. DOR-8 fija bytes y
  oráculos de política; DOR-9 fija SHA compartido/concurrencia antes del ensayo.
- `matrix.json` registra por caso PR, ramas, SHAs, checks, `app.id`, rollup,
  mergeability y UTC; expediente añade pre/postimagen/delta, deliveries, digest,
  permisos, comandos, tiempos, coste y logs saneados. Ninguna PR se fusiona.
- Fallo: cerrar PRs, restaurar/eliminar ruleset según preimagen, borrar ramas y
  desinstalar App; App queda privada sin instalación y lab se archiva. IAM se
  retira; servicios/datos se restauran a preimagen; versiones KMS/secretos se
  deshabilitan o destruyen según DOR-4, respetando esperas, TTL, `_Required` y
  residuos inevitables documentados. No se exige ausencia física imposible.

## Entorno autorizado

- Entrada: `POST /github/webhook`; worker interno `POST /pubsub|/reconcile`, OIDC
  con audience igual a URI base Cloud Run. Salida runtime exacta: `api.github.com`
  HTTPS `GET|POST|PATCH`; `github.com` Git smart HTTP `GET|POST` a repo efímero;
  `pubsub.europe-west1.rep.googleapis.com` RPC `Publish`;
  `firestore.europe-west1.rep.googleapis.com` RPC `BatchGetDocuments|RunQuery|Commit`;
  `secretmanager.europe-west1.rep.googleapis.com` RPC `AccessSecretVersion`;
  `europe-west1-cloudkms.googleapis.com` RPC `AsymmetricSign`;
  `metadata.google.internal:80` GET. Otro host/método/RPC falla cerrado.
- Build/verificación solo `pypi.org`, `files.pythonhosted.org`, `deb.debian.org`,
  `security.debian.org`, `registry.terraform.io`, `releases.hashicorp.com`, `*.pkg.dev`,
  `registry-1.docker.io`, `auth.docker.io`, `production.cloudfront.docker.com`.
- Secretos: ninguno durante implementación local. En ensayo, solo referencias a
  KMS/Secret Manager; nunca leer, imprimir, versionar o transportar valores.
- La primera futura invocación Claude atribuible a WP-018 usa `claude -p
  --output-format json`, WP-ID explícito y sin `--continue/--resume`; el F1
  saneado se suma en `evidence/WP-018/cost.md`. Esta preparación no usa Claude.

## Verificación y aceptación

Comandos headless futuros, en orden y con código de salida significativo:

```bash
uv lock --project services/alcance_fda_wp018 --check
uv sync --project services/alcance_fda_wp018 --frozen --all-groups --no-python-downloads
uv run --project services/alcance_fda_wp018 --locked ruff format --check services/alcance_fda_wp018 tests/alcance_fda_wp018
uv run --project services/alcance_fda_wp018 --locked ruff check services/alcance_fda_wp018 tests/alcance_fda_wp018
uv run --project services/alcance_fda_wp018 --locked mypy --strict services/alcance_fda_wp018/src tests/alcance_fda_wp018
uv run --project services/alcance_fda_wp018 --locked bandit -r services/alcance_fda_wp018/src
uv run --project services/alcance_fda_wp018 --frozen pip-audit
uv run --project services/alcance_fda_wp018 --locked pytest -q --disable-socket --cov=alcance_fda_wp018 --cov-fail-under=95 tests/alcance_fda_wp018
terraform -chdir=services/alcance_fda_wp018/infra fmt -check -recursive
env TF_DATA_DIR=/tmp/wp018-terraform-data terraform -chdir=services/alcance_fda_wp018/infra init -backend=false -input=false -lockfile=readonly
env TF_DATA_DIR=/tmp/wp018-terraform-data terraform -chdir=services/alcance_fda_wp018/infra validate -no-color
docker buildx build --platform linux/amd64 --attest type=provenance,mode=max --attest type=sbom,generator=docker/scout-sbom-indexer@sha256:4b67f29eb0d1244ab0f62de867ac5dafd7262fcd7ebbdefa6ec8aacd6b15252d --metadata-file /tmp/wp018-image.json --output type=oci,dest=/tmp/wp018-image.tar -f services/alcance_fda_wp018/Dockerfile .
gitleaks dir --no-banner --redact --exit-code 1 services/alcance_fda_wp018
gitleaks dir --no-banner --redact --exit-code 1 tests/alcance_fda_wp018
uv run --project services/alcance_fda_wp018 --locked python tests/alcance_fda_wp018/verify_contract.py
```

- [ ] Todas las pruebas unitarias y de contrato pasan sin red ni secretos.
- [ ] Cobertura >=95%; schemas rechazan extra/faltantes; HMAC, dedupe,
  anti-bucle, reconciliación, fallos cerrados e IAM positivo/negativo probados.
- [ ] Imagen reproducible, SBOM/procedencia y digest ligados a `TESTED_HEAD`.
- [ ] Ensayo DOR-6 completa los 11 casos y rollback sin tocar producción.
- [ ] Revisión completa única y dictamen final Astra APTO, inicial o enfocado,
  sin hallazgos abiertos y dentro de dos correcciones.

## Evidencias, parada y rollback

Los archivos enumerados en `evidence/WP-018/` contienen salidas íntegras,
códigos de salida, manifest, revisión Astra, seguridad, F1 por invocación,
ciclos y expediente del laboratorio; nunca secretos ni payloads brutos.

Parada adicional: DOR-7/8/9 abierto; F1 no defendible; coste >100 EUR o ensayo
>5 EUR; versión/digest/fuente cambiante; permiso, región o IAM no demostrable;
payload/evento fuera del esquema; necesidad de archivo no permitido; tercer
ciclo; incertidumbre o contaminación con la candidata histórica.

Rollback de implementación: revertir el único commit/PR de WP-018. Rollback de
infraestructura o laboratorio requiere acto humano y sigue la preimagen de §9;
no se ejecuta desde este contrato `draft`.
