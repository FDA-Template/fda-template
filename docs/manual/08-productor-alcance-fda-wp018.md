# 08 — Productor Alcance FDA WP-018

## 1. Estado y finalidad

Este capítulo concreta el primer acto técnico mínimo de DEC-010 §14 para
`WP018-DOR-7`. Es diseño contractual, no autorización de ejecución. No crea ni
configura GitHub o Google Cloud, no cierra F2 ni DOR-7 y no resuelve DOR-8 o
DOR-9. F1 y F3 a F7 permanecen cerrados.

La documentación oficial vigente confirma acceso WIF directo y GA para IAM,
sin limitaciones de API conocidas, y para Pub/Sub estándar; la excepción
publicada afecta a Pub/Sub Lite. `iam.serviceAccounts.actAs` y
`pubsub.subscriptions.update` están `SUPPORTED` en roles personalizados y sus
políticas pueden ligarse respectivamente a una cuenta de servicio y a una
suscripción individuales. Procede por tanto una enmienda directa de WP-018;
no hace falta otra decisión previa.

## 2. Identidad y nombres cerrados

- repositorio: `FDA-Template/fda-template`, `repository_id: 1310040618`;
- organización: `FDA-Template`, `repository_owner_id: 340040486`;
- humanos admitidos: `ivanes189`, `actor_id: 74557686`, y `de-lean788`,
  `actor_id: 260103530`;
- proyecto exclusivo de Google Cloud: nombre e ID `fda-template`, número
  `615273535351`, estado `ACTIVE` y parent ausente (`No organization`);
- workflow: `.github/workflows/wp018-dor7-emergency-push.yml`;
- entorno: `wp018-dor7-emergency-push`;
- pool global: `wp018-dor7-emergency`;
- proveedor OIDC: `github-oidc`;
- issuer: `https://token.actions.githubusercontent.com/`;
- audiencia: `//iam.googleapis.com/projects/615273535351/locations/global/workloadIdentityPools/wp018-dor7-emergency/providers/github-oidc`;
- suscripción única: `projects/fda-template/subscriptions/alcance-fda-wp018-worker-push`;
- cuenta única: `alcance-fda-wp018-push@fda-template.iam.gserviceaccount.com`;
- suscripción negativa existente:
  `projects/fda-template/subscriptions/alcance-fda-wp018-worker-push-denied`;
- cuentas negativas existentes: scheduler, ingress, worker y
  `alcance-fda-wp018-push-denied@fda-template.iam.gserviceaccount.com`;
- endpoint y audience de la ceremonia:
  `https://wp018-dor7.invalid/pubsub`;
- roles personalizados de proyecto:
  `projects/fda-template/roles/wp018Dor7SubscriptionUpdate`, con solo
  `pubsub.subscriptions.update`, y
  `projects/fda-template/roles/wp018Dor7PushActAs`, con solo
  `iam.serviceAccounts.actAs`, ambos en fase `GA`.

`PROJECT_ID=fda-template` y `PROJECT_NUMBER=615273535351` son literales cerrados
y no son entradas del workflow. El acto humano del 2026-10-09 ejecutó únicamente
estas dos lecturas canónicas saneadas:

```text
gcloud projects describe fda-template --format='json(projectId,projectNumber,lifecycleState,parent)'
gcloud billing projects describe fda-template --format='json(projectId,billingEnabled)'
```

Las salidas acreditan exactamente `projectId: fda-template`,
`projectNumber: 615273535351`, `lifecycleState: ACTIVE`, parent ausente y
`billingEnabled: true`. Google define este último valor como asociación a una
cuenta abierta. No se solicitó ni conservó `billingAccountName`. La consola
acredita además una única cuenta humana propietaria de Iván, vinculación a una
cuenta directa compartida con otros proyectos y coste observado `0,00 EUR`.
No se creó proyecto, cambió facturación ni aceptó gasto; Cloud Shell se retiró
tras las lecturas. La frontera aprobada es el proyecto exclusivo: la cuenta no
tiene que ser exclusiva y el control de coste debe filtrar por `fda-template`.
`${WORKFLOW_SHA}` es el commit completo de `main`
que contenga los bytes revisados del workflow. La ceremonia no depende de un
Cloud Run existente: usa el endpoint `.invalid` cerrado anterior, sin publicar
mensajes. Ausencia, discrepancia o variable seleccionable detiene el acto.

El paso 2 de DEC-010 §15 partió de esta preimagen cerrada: repositorio público
`FDA-Template/fda-template`; rama predeterminada `main`; cero entornos; los
usuarios `74557686` (`ivanes189`) y `260103530` (`de-lean788`) con acceso
administrativo. El acto humano separado creó únicamente
`wp018-dor7-emergency-push`. La postimagen REST saneada acredita exactamente:
un entorno total y con ese nombre; ninguna regla `wait_timer` y, por tanto,
espera efectiva cero; ambos revisores de tipo
`User`; `prevent_self_review: true`; `can_admins_bypass: false`; política
`{protected_branches:false, custom_branch_policies:true}`; una sola regla de
tipo `branch` y nombre exacto `main`; y `total_count: 0` tanto para secrets como
para vars. La interfaz acredita además que el bypass se desmarcó humanamente.

El historial web de la organización registra, en orden, `environment.create`,
la regla de revisores, la política personalizada de ramas y el patrón `main`.
Los detalles no publican tokens o secretos y el registro versionado omite IP,
ubicación, request IDs y demás identificadores innecesarios. La consulta REST
del audit log respondió `404`; no se presenta como captura disponible. El
delta queda reconstruido por preimagen cero, postimagen REST, interfaz e
historial web. Cualquier deriva posterior vuelve a detener la ceremonia.

## 3. Entorno protegido y control dual

El entorno tiene exactamente como revisores a los dos usuarios anteriores,
impide autoaprobación, admite únicamente `main` mediante regla de rama
seleccionada y deshabilita el bypass administrativo. No contiene secretos ni
variables. Solo `workflow_dispatch` puede iniciar el workflow y no admite
inputs. La condición WIF limita `actor_id` a esos dos valores, por lo que otro
usuario no obtiene credenciales aunque pueda despachar Actions.

Un humano inicia y el otro aprueba. GitHub exige solo una aprobación entre los
revisores; `prevent_self_review` convierte esa aprobación en control dual. Los
dos siguen siendo propietarios capaces de administrar el entorno: es una
frontera de confianza aceptada, no una barrera frente a un propietario
malicioso. Antes de cada intento se exportan configuración, revisores,
política de ramas e historial; cualquier cambio, recreación, bypass o falta de
trazabilidad detiene la operación.

## 4. Workflow cerrado

El archivo protegido incorporado por el tercer acto usa exactamente:

```yaml
name: WP018 DOR7 emergency push authentication
on:
  workflow_dispatch:
permissions:
  id-token: write
concurrency:
  group: wp018-dor7-emergency-push
  cancel-in-progress: false
jobs:
  restore:
    if: ${{ github.run_attempt == '1' }}
    runs-on: ubuntu-24.04
    timeout-minutes: 90
    environment: wp018-dor7-emergency-push
```

`ubuntu-24.04` fija la familia del sistema, no una imagen inmutable: GitHub
publica actualizaciones periódicas. Los bytes exactos fijan y comprueban antes
de solicitar OIDC `ImageOS=ubuntu24`, `ImageVersion=20261004.327.1`, Bash
`5.2.21(1)-release`, curl `8.5.0-2ubuntu10.15` y jq
`1.7.1-3ubuntu0.24.04.2`. Cualquier diferencia termina el job sin credencial.
Esta comprobación es fail-closed frente a drift observable, no un pin
criptográfico del host. Exigir una imagen inmutable real obliga a otra decisión
previa porque contenedores y runners propios permanecen fuera de este diseño.

No usa `checkout`, acciones de terceros, reusable workflows, contenedores,
secrets, vars ni inputs. El script único del job está versionado íntegramente
en el mismo YAML, usa `bash --noprofile --norc -euo pipefail`, `curl` y `jq`
preinstalados, y realiza exactamente una mutación idempotente. La preimagen
cerrada es una suscripción push vacía con endpoint
`https://wp018-dor7.invalid/pubsub`, wrapper y atributos acreditados, sin
`oidcToken`. La postimagen conserva endpoint, wrapper y atributos y añade solo
`oidcToken.serviceAccountEmail` igual a la cuenta push y audience igual al
mismo endpoint. No acepta valores proporcionados al despacho.

El SHA-256 de los bytes YAML revisados y `${WORKFLOW_SHA}` se registran antes
de crear el proveedor. Todo rerun está prohibido. El `if` anterior es defensa
local; la barrera de credencial es además `assertion.run_attempt == '1'` en el
proveedor. Un intento posterior es un `workflow_dispatch` nuevo con nueva
aprobación.

## 5. Pool, proveedor y condición

El proveedor usa audiencia predeterminada y este mapping exacto:

```text
google.subject=assertion.sub
attribute.repository_owner_id=assertion.repository_owner_id
attribute.repository_id=assertion.repository_id
attribute.environment=assertion.environment
attribute.event_name=assertion.event_name
attribute.ref=assertion.ref
attribute.ref_type=assertion.ref_type
attribute.workflow_ref=assertion.workflow_ref
attribute.workflow_sha=assertion.workflow_sha
attribute.actor_id=assertion.actor_id
attribute.run_id=assertion.run_id
attribute.run_attempt=assertion.run_attempt
attribute.runner_environment=assertion.runner_environment
```

La condición CEL exacta es:

```text
assertion.repository_owner_id == '340040486' &&
assertion.repository_id == '1310040618' &&
assertion.sub == 'repo:FDA-Template@340040486/fda-template@1310040618:environment:wp018-dor7-emergency-push' &&
assertion.environment == 'wp018-dor7-emergency-push' &&
assertion.event_name == 'workflow_dispatch' &&
assertion.ref == 'refs/heads/main' &&
assertion.ref_type == 'branch' &&
assertion.workflow_ref == 'FDA-Template/fda-template/.github/workflows/wp018-dor7-emergency-push.yml@refs/heads/main' &&
assertion.workflow_sha == '${WORKFLOW_SHA}' &&
assertion.actor_id in ['74557686', '260103530'] &&
assertion.run_attempt == '1' &&
assertion.runner_environment == 'github-hosted'
```

`${WORKFLOW_SHA}` se sustituye en la política por el SHA completo observado;
no queda como texto literal. Antes de crear el proveedor se revalida que el
repositorio conserva subject inmutable, plan y visibilidad compatibles.

El único miembro de ambos bindings es:

```text
principalSet://iam.googleapis.com/projects/615273535351/locations/global/workloadIdentityPools/wp018-dor7-emergency/attribute.repository_id/1310040618
```

El rol `wp018Dor7SubscriptionUpdate` se vincula únicamente en la suscripción;
`wp018Dor7PushActAs`, únicamente en la cuenta push. No hay binding en proyecto,
carpeta u organización, ni `roles/iam.workloadIdentityUser`, cuenta de servicio
intermediaria, claves, tokens firmados o credenciales persistentes.

Pool y proveedor se crean deshabilitados. La habilitación tiene dos fases
cerradas. **C0, canario sin privilegios:** con ambos bindings ausentes se
habilitan temporalmente provider y pool, se hace un único intercambio de §6,
se deshabilita primero pool y luego provider y se espera su expiración. **C1,
intento privilegiado:** ya cerrado C0, con pool/provider deshabilitados se crean
y verifican ambos roles y bindings; se habilita primero provider y al final
pool solo si políticas y ancestros acreditan simultáneamente ambos permisos y
ninguna concesión humana, básica o Cloud Run. Un fallo parcial conserva ambos
deshabilitados, revierte el único cambio aplicado y compara la preimagen.

## 6. Adquisición y cierre de credenciales

Antes de C0, un operador habilita en Cloud Audit Logs Data Access `Admin Read`
para IAM y STS. El canario de §5 confirma exactamente un log exitoso filtrado
por `protoPayload.methodName` igual a
`google.identity.sts.v1.SecurityTokenService.ExchangeToken`, `resourceName`
igual al provider completo, `authenticationInfo.principalSubject` igual al
`sub` exacto y la ventana UTC cerrada. El `run_id` se correlaciona únicamente
con el registro GitHub/OIDC local de esa misma ventana; no se presume presente
en el log STS. Ausencia, duplicado o ambigüedad impide instalar bindings.

En el intento privilegiado, el script comprueba `GITHUB_RUN_ATTEMPT=1` antes de
solicitar OIDC, solicita una sola vez el token GitHub con la audiencia de §2,
valida localmente issuer, audience y todas las claims de §5, y registra solo
`iat`, `exp`, `jti`, IDs y SHA; nunca el token. Lo intercambia una sola vez en
`POST https://sts.googleapis.com/v1/token`, sin cabecera Authorization, con:

- grant type `urn:ietf:params:oauth:grant-type:token-exchange`;
- requested token type `urn:ietf:params:oauth:token-type:access_token`;
- subject token type `urn:ietf:params:oauth:token-type:jwt`;
- scope `https://www.googleapis.com/auth/cloud-platform`;
- audiencia exacta de §2.

El token devuelto se enmascara antes de cualquier uso y solo vive en memoria.
Se registran UTC de intercambio, `expires_in` y expiración. Inmediatamente tras
la única mutación, o ante fallo/cancelación, el operador de guardia deshabilita
primero el pool y después el proveedor y acredita ambos estados. El pool
deshabilitado bloquea intercambios y uso de tokens activos; no se reabre porque
al reactivarlo un token aún vigente recuperaría acceso.

Si el runner sobrevive, espera hasta el máximo de las expiraciones OIDC y STS
más 60 segundos y el mismo token debe recibir `401`. Si se pierde el runner o
`expires_in`, el cierre humano usa como límite conservador una hora más 60
segundos desde la deshabilitación del pool, máximo oficial del token WIF. En
ambos casos, una consulta STS con los campos documentados anteriores debe
mostrar solo el intercambio esperado y ningún intercambio posterior. Una
consulta separada de Admin Activity de Pub/Sub filtra por principal federado,
suscripción, ventana y método `google.pubsub.v1.Subscriber.ModifyPushConfig` o
`tech.pubsub.SubscriberService.ModifyPushConfig`: espera exactamente los dos
intentos negativos denegados y la única mutación positiva, y ninguna mutación
posterior. Hasta vencer el límite no se retiran bindings ni se reabre o elimina
el pool; ausencia, resultado adicional o ambigüedad activa incidente.

## 7. Oráculos obligatorios

El operador acredita primero por lectura administrativa que todos los recursos
positivos y negativos de §2 existen; `NOT_FOUND` nunca equivale a denegación.
Con la credencial federada, cada llamada envía una lista no vacía exacta:

1. `subscriptions.testIamPermissions` sobre la autorizada, body
   `{"permissions":["pubsub.subscriptions.update"]}`, devuelve exactamente esa
   permission;
2. la misma llamada y body sobre la suscripción `-denied` devuelve `[]`;
3. `serviceAccounts.testIamPermissions` sobre la cuenta push, body
   `{"permissions":["iam.serviceAccounts.actAs"]}`, devuelve exactamente esa
   permission;
4. la misma llamada y body sobre scheduler, ingress, worker y la quinta cuenta
   `-denied` devuelve `[]` en cada caso;
5. `projects.testIamPermissions` consulta ambos permisos y
   `run.services.create`, `run.services.update`, `run.jobs.create`,
   `run.jobs.update`, `run.workerpools.create` y `run.workerpools.update`, y
   devuelve `[]`;
6. políticas efectivas acreditan ningún binding equivalente heredado, humano,
   básico, de tokens, firma, claves, IAM o Cloud Run.

Cada respuesta debe ser HTTP `200`; `401`, `403`, `404`, lista distinta o error
no prueba aislamiento. Las llamadas, URL, actor, request, response y existencia
previa se guardan saneadas.

La preimagen administrativa enumera y falla si el principal WIF posee
`roles/run.developer`, `run.services.create`, `run.services.update`,
`run.jobs.create`, `run.jobs.update`, `run.workerpools.create` o
`run.workerpools.update`, o cualquier rol básico. La llamada de mutación debe
pasar únicamente cuando los dos positivos y todos los negativos pasan; si
solo uno de los permisos es efectivo, no muta.

Antes de la positiva, dos llamadas `modifyPushConfig` negativas usan el mismo
body cerrado: sobre la suscripción autorizada con scheduler deben devolver
`403 PERMISSION_DENIED` por falta de `actAs`; sobre la suscripción `-denied`
con la cuenta push deben devolver `403 PERMISSION_DENIED` por falta de
`pubsub.subscriptions.update`. Ambas conservan su preimagen. Solo entonces se
ejecuta una mutación positiva. La postimagen prueba el único delta descrito en
§4; una comparación local del request contra la postimagen demuestra
idempotencia sin una segunda mutación.

## 8. Evidencia, rollback y separación de actos

La evidencia saneada contiene: base y SHA del workflow; configuración e
historia del entorno; iniciador y revisor distintos; pool/proveedor y claims;
definición de roles; políticas de los dos recursos y ancestros; preimagen y
postimagen push; respuestas exactas de oráculos; llamada idempotente; `iat`,
`exp`, `jti`, intercambio, expiración y `401`; auditoría posterior; delta,
coste y rollback. No contiene tokens, secretos ni payloads.

Rollback empieza deshabilitando pool y proveedor y verificando el bloqueo. Un
operador humano restaura la preimagen push. Solo después del cierre temporal y
de auditoría de §6 retira los dos bindings; si una retirada falla, el pool
continúa deshabilitado hasta restaurar simetría o retirar ambos. Después elimina
roles, provider/pool, workflow, entorno y fixtures, tras exportar postimágenes.
Cada mutación se verifica por lectura y delta; no se reabre el pool.

La prueba es una ceremonia humana preadmisión, no implementación de WP-018.
DEC-010 §15 corrige su orden. El primer acto humano separado acreditó
canónicamente `fda-template` y `615273535351` sin mutar proyecto o facturación;
el segundo creó y verificó el entorno protegido completo antes de que existiera
el workflow en `main`. El tercer acto incorpora el workflow exacto de 281 líneas
y SHA-256
`7ea50ded863cf57f2cac6916dada3dece9305bb6af60266601ca79ffa76b1594`
sobre base `9093182a5c15699e9c33836e752fe63fb9ee88fc`, pero no lo despacha. Crear
topic, suscripciones, cuentas, pool/provider y logging sin bindings; ejecutar y
cerrar C0; instalar
después roles y bindings con todo deshabilitado; ejecutar C1; capturar
evidencia; y eliminar fixtures siguen requiriendo autorizaciones separadas. No
usa Claude Code ni código del servicio. Esta excepción acotada rompe la
dependencia circular: el WP continúa `draft` hasta que ceremonia y rollback sean
APTO; solo entonces puede cerrarse F2/DOR-7 y evaluarse su futura admisión.

La composición mínima de esta enmienda contractual es exactamente estos tres
archivos: WP-018, `MANUAL.md` y este capítulo. No incluye workflow ni políticas.
Su materialización no autoriza las mutaciones externas. Los actos (1), fijar la
identidad no secreta del proyecto, (2), crear y verificar el entorno protegido,
y (3), preparar, revisar y materializar los bytes exactos del workflow sin
despacharlo, están cumplidos por composiciones humanas separadas. Siguen
requiriéndose, en orden, actos humanos separados para: (4) configurar fixtures,
logging y WIF inicialmente deshabilitado, sin roles o
bindings; (5) ejecutar y cerrar C0 sin privilegios; (6) instalar y verificar
los dos roles y bindings con WIF deshabilitado; y (7) ejecutar C1, sus oráculos,
la única mutación y el rollback. El workflow no se despacha entre los pasos 3
y 5 ni entre C0 y C1. Solo evidencia real completa puede cerrar F2 y DOR-7.

La acreditación versionada del segundo acto usa la misma composición atómica
mínima de cuatro archivos: WP-018, la hoja de ruta,
`05-bloqueos-y-parada.md` y este capítulo. No modifica DEC-010 ni DEC-003 porque
ejecuta el orden ya fijado por §15; no incluye `MANUAL.md` porque no crea
capítulo; y no crea `evidence/**` porque no abre un ciclo. Materializar esos
cuatro archivos no crea o modifica el entorno, no incorpora el workflow y no
autoriza el tercer acto.

La composición atómica mínima del tercer acto contiene exactamente cinco
archivos: el workflow, WP-018, la hoja de ruta, `05-bloqueos-y-parada.md` y
este capítulo. Los cuatro documentos acompañan el cambio protegido, eliminan
las afirmaciones que lo describían como inexistente y satisfacen la regla de
gobierno que exige actualizar `docs/manual/**` al cambiar `.github/**`. No
modifica decisiones, `MANUAL.md`, `ACTIVE`, evidencias, infraestructura o
configuración externa. La revisión completa y C1 enfocada dejaron APTO los
bytes del workflow; el fallo posterior de gobierno solo corrige esta
composición documental y requiere revalidación enfocada C2 antes de tocar la
rama. Ni esa revalidación ni la futura fusión autorizan despachar el workflow o
avanzar al paso 4.

Fuentes primarias revalidadas el 2026-10-09: documentación oficial de Google
Cloud sobre productos compatibles con identidad federada, WIF para pipelines,
acceso directo, políticas de cuentas de servicio, IAM de Pub/Sub, permisos en
roles personalizados, STS y autenticación push; y documentación oficial de
GitHub sobre OIDC y entornos protegidos. Para este acto se revalidaron además:
`https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects`,
`https://docs.cloud.google.com/resource-manager/docs/view-update-projects`,
`https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled`,
`https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments`,
`https://docs.github.com/en/rest/deployments/environments`,
`https://docs.github.com/en/rest/deployments/branch-policies`,
`https://docs.github.com/en/rest/actions/secrets`,
`https://docs.github.com/en/rest/actions/variables` y
`https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization`.
