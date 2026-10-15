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
suscripción individuales. La arquitectura no exige otra decisión previa; la
ruta operativa posterior queda precisada por DEC-010 §§15 a 17.

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

## 9. Replanteamiento del SHA del provider tras DEC-010 §17

La candidata de actualización preparada sobre `main`
`6821c0a83efd547b7617a1fed9c168e33224889c` no se ejecuta: su revisión completa
dejó abiertos `WP018-PSHA-F1` a `WP018-PSHA-F5` sobre recuperación, comparación de preimagen,
restauración exacta, pruebas de caminos reales y direccionamiento explícito del
proyecto. El parche posterior que pretendía abrir C1 tampoco se materializa:
no podía declarar a la vez la fila sin versionar y `abierto`, ni resolvía el
tipo mensual. Ninguno consume ciclo.

La composición de §17 se fusiona antes de rederivar. Su nueva cabeza y el
SHA-256 del workflow se congelan hasta cerrar provider y C0; una modificación
posterior de `main` produce parada, no actualización automática del anclaje.
Con esa base, el orden es:

1. comprobar en solo lectura la preimagen administrativa y su igualdad exacta;
2. crear y publicar por acto humano separado la rama sin fusionar
   `ops/wp018-dor7-provider-sha-custody`;
3. commitear allí C1 `abierto` y la revisión completa antes del autor;
4. con otra autorización, capturar coste F1 desde el inicio y
   rederivar/corregir solo `WP018-PSHA-F1` a `WP018-PSHA-F5`;
5. obtener revalidación enfocada de la misma revisora;
6. solo tras `APTO`, pedir por separado materialización y ejecución de la
   actualización con pool/provider deshabilitados y cero bindings;
7. rederivar C0 sobre la misma base acreditada.

La rama conserva ciclos, revisión y coste sin cambiar `main`; no es
implementación de WP-018 y no se fusiona durante la ceremonia. El ciclo se
consume al comenzar el autor, no al crear o publicar la rama. El tipo de
octubre es `1.1298 USD/EUR` del BCE, fecha 2026-10-01. Si cambia el mes, falta
la captura F1, se supera `5.00 EUR`, deriva la preimagen o cambia `main`, se
detiene antes de otra invocación o mutación. Esta sección no autoriza ramas,
invocaciones, despachos, roles, bindings o cambios de WIF.

## 10. Cierre de la actualización del provider y transición R2

La ruta de §9 agotó C1 y C2 y queda `blocked` por DEC-010 §18. C1 falló antes
de inferencia sin cambios; C2 produjo una candidata con digest agregado
`1625f0666d24c65732bd71d45d92120f4f6c95f2fc861c555f2a9a58aebe91da` y coste
acumulado `3.06 / 5.00 EUR`. La candidata es **`NO APTO — NO EJECUTAR`**. No se
corrige, reejecuta, materializa, importa, mezcla o reutiliza. La rama
`ops/wp018-dor7-provider-sha-custody` sigue congelada y sin fusionar; tampoco se
usa como rama de una transición posterior. No existe C3.

Permanecen abiertos tres controles inseparables del acto mutante: custodia
recuperable ante un corte entre la última ampliación del journal y su sello,
comparación de todas las superficies materiales contra una preimagen
autorizada y ejecución integral de las pruebas de actualización y rollback.
Las correcciones de restauración exacta y direccionamiento explícito de
proyecto permanecen solo como criterios de regresión; no convierten C2 en apta.

El eventual replanteamiento se denomina `WP018-DOR7-PSHA-R2` y todavía no está
abierto. Solo después de fusionar §18 puede otro acto fijar la cabeza exacta de
`main`, comprobar el hash del workflow y adquirir una preimagen administrativa
nueva que incluya pool, provider, IAM de proyecto y cuenta push, suscripciones,
topic, logging y estado GitHub. Cualquier commit posterior o diferencia no
volátil produce parada. La candidata R2 se rederiva desde cero: los bytes C2 no
son andamio ni preimagen.

R2 tendrá como máximo `R2-C1` y `R2-C2`, una rama durable distinta y un
subpresupuesto incremental de `5.00 EUR` dentro de los `100.00 EUR` de WP-018.
Los `3.0626293149... EUR` históricos permanecen acumulados y no liberan ciclos
o presupuesto. Preparar la candidata, revisarla, crear la rama, abrir cada
ciclo, invocar al autor, materializar, ejecutar el provider y rederivar C0 son
actos separados. Esta documentación no realiza ni autoriza ninguno de ellos.

## 11. Cierre bloqueado de `WP018-DOR7-PSHA-R2`

La secuencia separada prevista por §10 se ejecutó y agotó sus dos ciclos. R2 se
ancló en `9cdfaefddfdb50fa1fba385e265243022b67061f`, mantuvo el workflow con
SHA-256 `7ea50ded863cf57f2cac6916dada3dece9305bb6af60266601ca79ffa76b1594` y
partió de una preimagen nueva. La candidata se rederivó desde cero; no reutilizó
la candidata C2 histórica.

R2-C1 terminó `NO APTO` con F1 y F3 abiertos y F2, F4 y F5 cerrados. R2-C2 se
limitó a F1/F3, pero su invocación terminó por `budget_exhausted`, sin resultado
final. La verificación posterior encontró:

- validación de captura que acepta un `SHA256SUMS` incompleto o vacío;
- dos casos que no alcanzan los cortes `SIGKILL` que afirman probar;
- ausencia de llamada directa a las funciones bajo inhibición de `errexit`;
- ShellCheck fallido por SC2153 y SC2034;
- 11 hashes obsoletos en el manifiesto interno.

La batería local devolvió `0` e imprimió `APTO`, pero ese resultado no acredita
los casos ausentes o mal planteados. La segunda y última revalidación enfocada
emitió **`NO APTO — NO EJECUTAR`**. F1 y F3 permanecen abiertos; F2, F4 y F5
son regresiones cerradas.

La postimagen R2-C2 se preserva fuera del repositorio y su manifiesto externo
completo de 55 archivos tiene SHA-256
`ffa413fc5f798dc5b640314783ac022aef479427795ace159d033dd1415332ab`. La rama
`ops/wp018-dor7-provider-sha-r2-custody` fusionada por la PR #83 contiene solo
los cuatro archivos de evidencia; ningún byte técnico de la candidata se
materializó.

R2 consumió `5.6754402 USD / 5.023402549123739 EUR`, superando el subpresupuesto
de `5.00 EUR` en `0.023402549123739 EUR`. R2-C1 y R2-C2 están consumidos,
`WP018-DOR7-PSHA-R2` termina `blocked` y no existe R2-C3. No se crea R3 ni se
divide F1/F3 por analogía. DOR-7 continúa abierto. DEC-010 §19 devolvió
cualquier continuación a decisión humana; el §20 posterior la resuelve sin
autorizar todavía autor, provider, WIF, C0, infraestructura o limpieza
destructiva.

## 12. Transición sucesora `WP018-DOR7-PSHA-OF1`

DEC-010 §20 rechaza abandonar WP-018 mientras siga vigente su objetivo y
rechaza dividir F1/F3 en entregas independientes. Elige OF1 como transición
sucesora *oracle-first*. No es R3, no reabre R2 y no reutiliza ninguna candidata
histórica. Esta sección delimita el camino; no lo abre.

### 12.1. Orden obligatorio

1. Tras fusionar la enmienda, fijar por acto humano separado la cabeza exacta
   de `origin/main`, comprobar que el workflow conserva SHA-256
   `7ea50ded863cf57f2cac6916dada3dece9305bb6af60266601ca79ffa76b1594` y
   capturar una preimagen administrativa nueva.
2. Con otra autorización, preparar externamente etapa A: pruebas, fakes,
   runner y manifiesto de oráculos, sin código de mutación ni red.
3. Astra audita de forma acotada la no vacuidad contra fixtures sintéticas de
   control positivo y mutantes defectuosos conocidos. El arnés debe rechazar
   manifiestos vacíos/incompletos, distinguir un `SIGKILL` marcado de una salida
   temprana, llamar directamente a interfaces sintéticas bajo `if`, `!`, `&&`
   y `||`, y fallar con casos omitidos o no alcanzados. Este `APTO` solo prueba
   sensibilidad del arnés, no conformidad de una implementación inexistente.
   Si hay hallazgos, antes de corregir se crea/publica la rama durable con la
   candidata no apta, auditoría, coste y fila de ciclo `abierto`.
4. Si etapa A es apta, sellar sus bytes con manifiesto externo y
   `ORACLE-SHA256SUMS`, registrar ambos hashes y actualizar la rama existente o
   crearla/publicarla si aún no existe, siempre antes de etapa B.
5. Solo entonces otro contexto nuevo puede preparar etapa B. El autor de
   implementación no puede modificar pruebas, fakes, runner o manifiesto de
   oráculos; se comparan byte a byte antes y después.
6. Ejecutar headless la batería sellada sobre paths y funciones reales,
   registrando sus hashes. Debe acreditar en ese sujeto real los `SIGKILL`,
   estados durables y llamadas directas bajo `errexit`; un fake, fixture,
   subprocess sustituto o sujeto no identificable produce `NO APTO`. Después
   se obtiene una revisión completa única independiente. F1/F3 solo cierran
   juntos; F2/F4/F5, `WP018-DOR7-C0-H1` y el catálogo
   `WP018-DOR7-C0-R1` a `WP018-DOR7-C0-R8` son regresiones obligatorias.
7. Solo un dictamen final `APTO` permite pedir por separado materialización,
   actualización del provider y rederivación de C0.

### 12.2. Ciclos, coste y custodia

OF1 comparte un máximo total de dos correcciones entre ambas etapas:
`OF1-C1` y `OF1-C2`. Una corrección de oráculos consume uno de esos ciclos y no
reaparece en implementación. Hay como máximo cuatro invocaciones de autor: una
inicial de etapa A, una inicial de etapa B y dos correctoras. Fallo,
interrupción, ausencia de cambios o de resultado final no repone invocación ni
ciclo. No existe OF1-C3.

El subpresupuesto incremental es `6.00 EUR`; etapa A, etapa B y correcciones lo
comparten. Los límites nominales de invocación no pueden superar `5.90 EUR`
acumulados y `0.10 EUR` queda sin asignar como reserva frente al sobrepaso de
corte observado en R2. F1 se captura desde cada lanzamiento; cambio de mes o
tipo, F1 no defendible, coste real superior a `6.00 EUR` o falta de remanente
nominal produce parada.

El coste histórico del provider permanece en `8.086031864023739 EUR`. Con OF1
y la reserva separada de `5.00 EUR` del laboratorio DOR-6, el compromiso
aritmético sería `19.086031864023739 / 100.00 EUR`, dejando
`80.913968135976261 EUR` sin autorizar para el resto de WP-018.

La rama durable prevista es
`ops/wp018-dor7-psha-of1-custody`, todavía inexistente. Antes de etapa B o de
una corrección, lo que ocurra primero, debe estar publicada con base, preimagen,
hashes de oráculos, auditoría y coste. Antes de una corrección añade una única
fila de ciclo `abierto`. La rama custodia evidencia; no materializa la candidata
ni se fusiona durante una cabeza operativa congelada.

La fusión de esta documentación no prepara bytes de OF1 ni autoriza base,
preimagen, rama, ciclo, actor de etapa A, autor de etapa B, materialización,
provider, WIF, C0, infraestructura o limpieza.

### 12.3. Catálogo operativo de regresiones C0

DEC-010 §21 corrige el hueco que obligó a detener etapa A antes de invocar al
actor: la normativa decía «ocho hallazgos» sin enumerarlos. Desde la fusión de
esa enmienda, el inventario cerrado del arnés usa estos IDs:

| ID | El control positivo acredita | El mutante demuestra fallo |
|---|---|---|
| `WP018-DOR7-C0-R1` | reloj compatible o rechazo de Bash incompatible antes de mutar | `EPOCHSECONDS` bajo Bash 3.2 aborta con `set -u` |
| `WP018-DOR7-C0-R2` | señal C0 observable y acotada sin logs parciales no acreditados | el endpoint live devuelve `404` y el diseño dependiente no converge |
| `WP018-DOR7-C0-R3` | parser que excluye código impreso y cuenta salidas exactas | búsqueda por subcadena confunde código y resultados |
| `WP018-DOR7-C0-R4` | cierre intentado y verificado pese a fallo diagnóstico | un `503` anterior al cierre evita todo `update --disabled` |
| `WP018-DOR7-C0-R5` | supervisor por llamada y global que termina el grupo hijo | una llamada bloqueada evade el deadline |
| `WP018-DOR7-C0-R6` | ventana completa de 600 s y consulta final | salida al primer registro omite un segundo intercambio tardío |
| `WP018-DOR7-C0-R7` | hash previo de toda preimagen consumida | una captura local sustituida llega hasta la habilitación |
| `WP018-DOR7-C0-R8` | plan y propietarios exactos revalidados antes de mutar | cambio de plan o propietarios pasa el preflight |

Cada fila exige ejecución de un positivo que pasa y un mutante que falla, una
sola entrada en el inventario y evidencia de que el punto de prueba fue
alcanzado. `WP018-DOR7-C0-H1` no es uno de los ocho: permanece abierto y añade
su matriz propia para código de salida, canales, LF terminal, CR, espacios,
salida vacía y varias líneas. F2, F4 y F5 conservan asimismo sus oráculos
independientes. El inventario completo contiene doce grupos: F2, F4, F5, H1 y
R1 a R8.

Si la enmienda de catálogo se fusiona, la base `921210ff…` y su preimagen pasan
a ser históricas. Antes de reabrir etapa A se fija la nueva cabeza de `main`, se
revalida el workflow y se captura otra preimagen. La fusión del catálogo no
crea bytes, coste, invocación, ciclo ni autoridad para WIF o infraestructura.
