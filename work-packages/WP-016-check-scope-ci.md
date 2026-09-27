# WP-016 — check_scope en CI y barrera verificable de fusión

estado: draft
prioridad: P0
riesgo: T3
agente_responsable: Claude Code (implementer)
agente_revisor: GPT-6 Astra (Alto, contexto nuevo, solo lectura)
requisitos: [REQ-FDA-001, REQ-FDA-002, SEC-001]
adr: [ADR-001]
decisiones: [DEC-003, DEC-007, DEC-010, DEC-011, DEC-012, DEC-014]
presupuesto_max_eur: 100
max_ciclos_correccion: 2

## Objetivo y contexto

Completar la migración del control de alcance sin reabrir WP-015:
integrar en CI el verificador existente, aplicar políticas verificables a
ramas wp/* y ops/*, demostrar mediante pruebas reales el check terminal
Alcance FDA y preparar —sin ejecutar desde Claude Code— su posterior
incorporación humana al ruleset.

Solo podrá afirmarse que check_scope bloquea fusiones cuando:

1. el job esté fusionado y ejecutándose en main;
2. las cuatro pruebas reales sean conformes;
3. una persona haya añadido al ruleset el par exacto
   {context, integration_id};
4. estén verificadas preimagen, postimagen, delta, historia, custodia y
   rollback;
5. una PR deliberadamente no conforme resulte realmente no fusionable.

## Estado de Definition of Ready

Esta candidata permanece deliberadamente draft y no está lista para aprobar,
admitir, activar ni implementar.

Bloqueo WP016-DOR-1:

Identificar y demostrar un productor y disparador que, sin
pull_request_target, evalúe bytes confiables y publique siempre sobre el HEAD
vigente de toda PR relevante un check terminal elegible como required status
check con el par exacto Alcance FDA + integration_id, incluso ante directivas
de omisión de Actions.

Antes de ready, una autorización humana separada debe permitir una prueba de
diseño acotada o una decisión normativa que demuestre simultáneamente:

1. que los bytes del evaluador no proceden de la cabeza no confiable;
2. que aperturas, reaperturas, sincronizaciones, cambios de base y cambios de
   autorización terminan en una conclusión sobre el HEAD vigente;
3. que existe también una conclusión elegible ante directivas de omisión;
4. que el resultado procede del productor exacto fijado mediante
   integration_id;
5. que no se necesitan pull_request_target, secretos para código no confiable
   ni permisos de escritura superiores a los imprescindibles.

Si la solución necesita una GitHub App, infraestructura externa, workflow
reutilizable externo, servicio, secreto, nuevo archivo protegido o ruta no
incluida, se detiene WP-016 y se tramita primero la decisión o WP separado que
corresponda.

## Alcance incluido y fuera de alcance

Incluido:

- integrar sin modificar scripts/check_scope.py ni scripts/scope_rules.py;
- añadir un adaptador mínimo de políticas wp/* y ops/*;
- preparar un parche exacto de ci.yml para aplicación humana;
- implementar y probar la autorización criptográfica de operador;
- implementar la herramienta offline de evidencia del ruleset;
- actualizar únicamente la documentación operativa afectada;
- conservar evidencias locales, reales y de revisión;
- preparar, sin ejecutar, la posterior mutación humana del ruleset.

Fuera de alcance:

- resolver implícitamente WP016-DOR-1;
- modificar el verificador entregado por WP-015;
- modificar guard, runtime, humo seguro, E2 o WP-007;
- mutar el ruleset desde Claude Code;
- cambiar CODEOWNERS o políticas generales de aprobación;
- tocar candidatas o worktrees históricos.

## Política verificable para ramas y lecturas automáticas

El adaptador acepta exactamente:

- ^wp/(WP-[0-9]{3})-[a-z0-9]+(?:-[a-z0-9]+)*$
- ^ops/[a-z0-9]+(?:-[a-z0-9]+)*$

Mayúsculas, descripción vacía, guiones iniciales, finales o dobles, segmentos
adicionales y cualquier otra rama producen fallo terminal.

### Ramas wp/*

El grupo 1 de la gramática es el único WP-ID que se entrega a:

python3 scripts/check_scope.py <WP-ID> <merge-base>...<HEAD>

La gramática de rama pertenece a WP-016. No se atribuye a WP-015.

El adaptador no reimplementa ni relaja scripts/check_scope.py o
scripts/scope_rules.py. Contrato ausente, rango ambiguo, ruta no permitida,
error interno o resultado distinto de cero fallan cerrados.

### Ramas ops/*

La autorización es un commit vacío, firmado por el propietario y situado como
HEAD vigente de la PR.

Su mensaje UTF-8 coincide byte a byte, con LF y un único LF final, con:

```text
FDA check_scope authorization

FDA-Repository-ID: <repository_id_decimal>
FDA-PR: <pull_number_decimal>
FDA-Base-Ref: refs/heads/main
FDA-Base-SHA: <base_sha_40_hex_minúsculas>
FDA-Merge-Base-SHA: <merge_base_sha_40_hex_minúsculas>
FDA-Diff-SHA256: <sha256_64_hex_minúsculas>
```

El digest es SHA-256 de los bytes producidos por:

```bash
git diff-tree -r --no-commit-id --raw -z --no-renames \
  <merge_base_sha> <parent_sha_del_commit_autorizante>
```

La evaluación usa X-GitHub-Api-Version: 2026-03-10 y comprueba:

1. GET /repos/{owner}/{repo}:
   - id coincide con FDA-Repository-ID;
   - default_branch es main;
   - owner.id se conserva para verificar la identidad.
2. GET /repos/{owner}/{repo}/pulls/{pull_number}:
   - PR abierta y número coincidente;
   - base.ref es main;
   - base.sha coincide con FDA-Base-SHA;
   - head.sha es el HEAD evaluado.
3. GET /repos/{owner}/{repo}/commits/{HEAD} y su padre:
   - exactamente un padre;
   - tree.sha idéntico al árbol del padre;
   - mensaje exacto;
   - verification.verified es true;
   - verification.reason es valid;
   - verification.verified_at no es nulo;
   - author y committer existen, son User y sus id coinciden con owner.id.
4. Con objetos Git obtenidos sin ejecutar bytes de la PR:
   - git merge-base FDA-Base-SHA <parent_sha> coincide con
     FDA-Merge-Base-SHA;
   - el digest canónico coincide con FDA-Diff-SHA256.

Una actualización de main invalida la autorización aunque HEAD no cambie.
Cambiar contenido, padre, árbol, PR, repositorio, base, merge-base o digest
también la invalida. Solo un nuevo commit vacío y firmado situado como nuevo
HEAD puede reautorizar.

Ningún comentario, review, label, login, nombre de rama o
author_association constituye autorización.

Eventos nominales que deben provocar evaluación:

- pull_request opened;
- reopened;
- synchronize;
- ready_for_review;
- converted_to_draft;
- edited.

La modificación de la autorización solo es posible mediante un nuevo commit,
que produce synchronize. El productor que resuelva WP016-DOR-1 debe demostrar
cobertura equivalente.

Lecturas automáticas:

- GET /repos/{owner}/{repo};
- GET /repos/{owner}/{repo}/pulls/{pull_number};
- GET /repos/{owner}/{repo}/commits/{HEAD};
- GET /repos/{owner}/{repo}/commits/{parent_sha}.

Permisos mínimos:

- contents: read;
- pull-requests: read;
- metadata de solo lectura.

No hay paginación, escritura ni secretos distintos del token efímero mínimo
del productor aceptado. Respuesta incompleta, identidad nula, divergencia,
timeout, rate limit, cambio de esquema o error HTTP producen fallo contractual.

## Identidad y conclusiones del check

- Contexto estable: Alcance FDA.
- integration_id se obtiene de un ensayo verde real del productor aceptado.
- Solo success después de completar toda la evaluación sobre el HEAD vigente.
- Configuración inválida, rama desconocida, autorización ausente u obsoleta,
  error o excepción terminan en failure cuando la plataforma permita emitirlo.
- skipped, neutral, cancelled, timed_out, startup_failure, ausente o pendiente
  no son conformidad contractual.
- Un contexto homónimo de otro productor no satisface el contrato.
- Ningún job auxiliar usa el nombre Alcance FDA.
- El gate terminal no puede quedar verde mediante continue-on-error, omisión,
  una dependencia saltada o un step posterior.

## Flujo protegido y aplicación humana

Claude Code no modifica .github/workflows/ci.yml.

Prepara evidence/WP-016/ci.patch contra el blob exacto de la base activada,
junto con SHA-256, blob preimagen, rutas afectadas y comandos de comprobación.

Una persona:

1. comprueba base y worktree limpios;
2. verifica git apply --check;
3. aplica exactamente el parche;
4. confirma que solo cambió la ruta autorizada;
5. registra actor por rol, fecha, commit y hash.

Cualquier deriva invalida el parche y obliga a regenerarlo dentro del ciclo de
corrección vigente.

El workflow mantiene permisos mínimos, acciones externas fijadas por SHA,
ausencia de secretos para código no confiable y prohibición de
pull_request_target.

## Pruebas reales roja y verde

Las pruebas requieren autorización humana propia y se ejecutan con el job en
main pero todavía no requerido. Ninguna sonda roja se fusiona.

1. wp/* rojo: cambio fuera de alcance produce Alcance FDA en failure.
2. wp/* verde: cambio permitido produce success.
3. ops/* rojo: autorización ausente, inválida u obsoleta produce un check
   creado y failure.
4. ops/* verde: autorización firmada vigente produce success.
5. omisión: una prueba con directiva de omisión de Actions debe recibir una
   conclusión terminal elegible; si no, WP016-DOR-1 continúa abierto.

Los casos negativos de ops/* incluyen:

- commit no firmado;
- firma inválida o de otro usuario;
- commit no vacío;
- número de PR diferente;
- reproducción del commit en otro repositorio del mismo propietario;
- avance de main sin cambiar el HEAD de la PR;
- merge-base o digest distintos;
- cambio del diff;
- edición maliciosa de un comentario previo del propietario.

Cada evidencia registra:

- repositorio, PR, rama y base;
- HEAD, padre, árbol, base SHA y merge-base SHA;
- digest del diff;
- commit/base y blob o revisión inmutable del workflow y evaluador confiables;
- prueba de que esos bytes ejecutaron la evaluación;
- contrato del merge-base y rango, para wp/*;
- referencia opaca de la autorización firmada, para ops/*;
- estado e instante de verificación de firma;
- context e integration_id;
- run_id, check_run_id o equivalente;
- URL, evento, status, conclusion, UTC y causa esperada.

Los identificadores personales permanecen únicamente en custodia protegida.

## Mutación humana posterior del ruleset

La mutación no pertenece a la implementación ni a la PR de código.

Solo una persona podrá ejecutarla, mediante autorización posterior, cuando:

- el job esté fusionado en main;
- las cuatro pruebas sean conformes;
- la prueba de omisión sea conforme;
- el par exacto esté identificado.

La única modificación admisible añade:

```json
{"context":"Alcance FDA","integration_id":<ID_VERIFICADO>}
```

No sustituye, renombra o relaja ningún check existente.

## Contrato íntegro de evidencia del ruleset

Se incorpora por referencia vinculante DEC-007, sección «Evidencia de la
mutación del ruleset», grupos A–J, orden 1–13, saneado e indisponibilidad
posterior. Los criterios siguientes lo hacen ejecutable y no lo reducen.

### A — Identidad

Registrar repositorio, rama, ruleset_id, versión de API e instantes UTC.

La credencial pertenece al operador humano, queda separada de las evidencias y
requiere el permiso mínimo vigente Administration: write. Después se revoca si
era efímera o vuelve a su almacén protegido. Su ausencia detiene antes de
mutar.

### B — Versiones y endpoints

Registrar separadamente:

- GET /repos/{owner}/{repo}/rulesets/{ruleset_id};
- GET /repos/{owner}/{repo}/rulesets/{ruleset_id}/history;
- GET /repos/{owner}/{repo}/rulesets/{ruleset_id}/history/{version_id}.

El listado localiza version_id, actor y updated_at. Solo la versión concreta
aporta state completo. El identificador remoto direcciona; no es custodia.

### C — Estado completo

Preimagen y postimagen contienen nombre/id, origen/tipo, destino, enforcement,
condiciones, bypass actors, todas las reglas y parámetros, política estricta y
todos los pares context + integration_id.

### D — Proyecciones

Listas completas antes/después, par añadido y bypass actors. No sustituyen el
estado completo.

### E — Delta

El único delta permitido es añadir el par exacto. Cualquier otra diferencia
detiene y escala.

### F — Canonicalización y huellas

Cada campo se clasifica como:

- semántico;
- identidad/direccionamiento;
- dependiente del lector;
- transporte/hipermedia;
- desconocido.

Un campo desconocido detiene. version_id, updated_at y metadatos de captura no
forman parte del estado semántico comparado.

Cada colección se clasifica individualmente. Las de orden no semántico se
ordenan mediante clave compuesta, declarada e inyectiva, sin deduplicar y
conservando multiplicidad. Una colisión detiene. Los arrays de orden
significativo se enumeran y preservan.

Tras la proyección se aplica RFC 8785 y SHA-256 sobre los bytes JCS exactos,
registrando esquema y versión de herramienta.

### G — Actor

El repositorio conserva únicamente:

- rol público operador humano;
- tipo de actor;
- referencia opaca;
- huella.

La identidad personal queda en historia capturada y custodia protegida.

### H — Concurrencia

Capturar la última versión inmediatamente antes, verificar que continúa
vigente justo antes de:

PUT /repos/{owner}/{repo}/rulesets/{ruleset_id}

Ante deriva se aborta y reinicia desde una nueva preimagen. Después se captura
inmediatamente la postimagen y se comprueba el delta exacto.

### I — Rollback

El rollback mínimo retira únicamente el par añadido y solo si el estado vigente
coincide con la postimagen esperada. La deriva detiene.

Después se captura versión y estado completo, JCS y SHA-256, y se demuestra
equivalencia semántica completa con la preimagen.

### J — Custodia externa

Antes de mutar deben estar acreditados:

- propietario por rol;
- lectores y condición de acceso;
- soporte persistente y ubicación lógica no volátil;
- retención y tratamiento al vencer;
- recuperación y verificación;
- auditabilidad futura;
- huellas.

Se custodian representaciones completas saneadas de preimagen, postimagen,
historia y eventual rollback. El repositorio contiene solo referencias opacas,
huellas y hechos no personales.

### Orden obligatorio

1. acreditar custodia;
2. verificar credencial y endpoints;
3. capturar estado y versión previa;
4. sanear, custodiar y hashear preimagen;
5. comprobar no deriva;
6. ejecutar el único PUT humano;
7. capturar postimagen;
8. verificar delta;
9. localizar nueva versión;
10. obtener state completo;
11. custodiar listado, versión y postimagen;
12. registrar referencias y huellas;
13. solo entonces permitir el cierre.

### Indisponibilidad histórica

Máximo cinco intentos y diez minutos. Esperas antes de los intentos 2–5:
5, 15, 30 y 60 segundos.

Se reintentan timeout/red, 404 de propagación, 409, 429, 500, 502, 503 y 504;
también 403 únicamente con Retry-After o rate limit agotado.

401, 403 sin señal de rate limit, 422, esquema inválido u otras respuestas son
no reintentables.

Cada intento registra UTC, endpoint, código o clase y cabeceras no sensibles.

Si el estado actual acredita el delta pero la historia sigue indisponible:

- se conserva la mutación restrictiva;
- WP-016 continúa activo;
- no existe PR de cierre;
- se custodian los intentos;
- se solicita decisión;
- no hay rollback automático.

Un rollback posterior exige autorización humana nueva y el protocolo del grupo
I. Si su historia tampoco aparece, WP-016 continúa abierto.

El saneado excluye antes de JCS tokens, autenticación, cookies, URLs firmadas y
datos personales innecesarios.

## Herramienta versionada de evidencia

scripts/ruleset_evidence.py es offline: no recibe credenciales ni llama a
GitHub.

Debe:

- validar un esquema versionado;
- aplicar la clasificación A–J;
- conservar multiplicidad;
- rechazar colisiones, campos desconocidos y valores no representables;
- producir proyección, JCS, SHA-256 y delta estable;
- distinguir ausencia de null;
- probarse con vectores RFC 8785 y fixtures de preimagen, postimagen, historia,
  deriva y rollback.

## Archivos permitidos

- .github/workflows/ci.yml
- scripts/check_scope_ci.py
- scripts/ruleset_evidence.py
- tests/scope_ci/**
- tests/ruleset_evidence/**
- evidence/WP-016/**
- CLAUDE.md
- docs/03-hoja-de-ruta.md
- docs/manual/MANUAL.md
- docs/manual/02-ciclo-de-un-wp.md
- docs/manual/05-bloqueos-y-parada.md

## Archivos prohibidos

- scripts/check_scope.py
- scripts/scope_rules.py
- tests/scope/**
- tests/guard/run-suite.sh
- .github/workflows/claude.yml
- .github/workflows/code-review.yml
- work-packages/ACTIVE
- work-packages/WP-005-integracion-ci.md
- specs/**
- .claude/**
- .agents/**
- .codex/**
- AGENTS.md
- CODEOWNERS

## Acciones prohibidas

- Claude Code no modifica directamente ci.yml.
- No se leen, ejecutan, importan, modifican o limpian históricos.
- No se usa pull_request_target.
- No se entregan secretos a código no confiable.
- Claude Code no consulta ni muta administrativamente el ruleset.
- No se afirma enforcement antes de completar el gate de cierre.
- No se amplía el alcance por analogía.

## Entorno autorizado

- Python 3.11 o posterior.
- Biblioteca estándar para código nuevo.
- PyYAML solo como dependencia de verificación ya usada por el CI.
- Runtime headless, sin TTY ni prompts.
- scripts/check_scope.py y scripts/scope_rules.py se consumen sin cambios.
- actionlint 1.7.7 es obligatorio.
- Lecturas GitHub automáticas limitadas a las declaradas.
- API administrativa y credencial exclusivamente en actos humanos.
- Sin servicios, paquetes o secretos nuevos.

actionlint no queda sustituido por el validador Python. El CI vigente lo
instala headlessly y ejecuta actionlint -color. En local se utiliza un binario
1.7.7 ya disponible. Si no está disponible o su versión difiere, la
verificación se declara inejecutable y se detiene.

## Verificación

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scope_ci -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/ruleset_evidence -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_scope.py WP-016 origin/main...HEAD
bash tests/scope/run-suite.sh
bash tests/governance/test-check-active.sh
bash tests/guard/run-suite.sh
actionlint -version
actionlint -color
PYTHONDONTWRITEBYTECODE=1 python3 .claude/skills/run-verification/validate-workflows.py .github/workflows/ci.yml
PYTHONDONTWRITEBYTECODE=1 python3 evidence/WP-000/checks/check-manual.py
git diff --check
```

El registro de actionlint debe acreditar exactamente la versión 1.7.7.

También se comprueba automáticamente:

- acciones externas fijadas por SHA;
- ausencia de pull_request_target;
- un único productor aceptado de Alcance FDA;
- cobertura de la matriz de eventos;
- identidad byte a byte del verificador WP-015 respecto de la base.

## Puertas separadas

0. Draft: WP016-DOR-1 abierto; no se aprueba, admite, activa ni implementa.
1. Ready: solo tras resolución autorizada y revisión del contrato actualizado;
   ACTIVE no cambia.
2. Admisión: acto normativo humano separado; ACTIVE no cambia.
3. Activación: acto humano separado que pone exclusivamente WP-016 en ACTIVE y
   cambia el contrato a in_progress.
4. Fusión de implementación: requiere parche humano, validaciones, CI y la
   única revisión completa Astra de la implementación. No requiere aún mutar
   el ruleset ni permite afirmar enforcement. WP-016 permanece activo.
5. Pruebas reales: job en main y todavía no requerido; cada sonda requiere
   autorización humana y las rojas no se fusionan.
6. Mutación: autorización humana separada, pruebas conformes y protocolo A–J.
7. Cierre: evidencia completa, historia disponible y PR no conforme realmente
   no fusionable. Una PR de operador registra evidencia, cambia WP-016 a done y
   devuelve ACTIVE a reposo en un diff atómico.

Los cambios de admisión, activación y cierre quedan fuera de las rutas de
Claude y requieren autorizaciones propias.

## Criterios de aceptación

### Gate de fusión de implementación

- [ ] WP016-DOR-1 fue resuelto mediante acto autorizado y evidencia falsable.
- [ ] El contrato actualizado fue revisado antes de ready.
- [ ] Los verificadores de WP-015 permanecen idénticos.
- [ ] El adaptador aplica exactamente las dos gramáticas y falla cerrado.
- [ ] La política firmada pasa todos los casos positivos y negativos.
- [ ] El parche de workflow coincide byte a byte con lo aplicado humanamente.
- [ ] Alcance FDA es terminal y su productor queda identificado.
- [ ] Validaciones locales, actionlint 1.7.7 y CI están en verde.
- [ ] Manual, hoja de ruta y CLAUDE.md describen el estado real.
- [ ] La candidata de implementación recibe una única revisión completa Astra.

### Gate de cierre

- [ ] Las cuatro pruebas reales y la prueba de omisión son conformes.
- [ ] El ruleset contiene el par exacto context + integration_id.
- [ ] Los grupos A–J y el orden 1–13 están completos.
- [ ] La historia posterior está disponible y custodiada.
- [ ] El delta contiene únicamente el par añadido.
- [ ] El rollback mínimo está definido y probado en seco.
- [ ] Una PR no conforme queda realmente no fusionable.
- [ ] Solo entonces la documentación afirma que check_scope bloquea fusiones.
- [ ] La PR de operador cambia WP-016 a done y ACTIVE a reposo.

## Evidencias exigidas

En evidence/WP-016:

- verificación local íntegra y códigos de salida;
- versión y salida de actionlint;
- manifiesto, hash y aplicación humana de ci.patch;
- matriz de eventos;
- política y pruebas de autorización ops/*;
- cuatro ensayos reales y prueba de omisión;
- identidad del productor;
- referencias inmutables de workflow y evaluador;
- expediente A–J del ruleset;
- revisión completa de Astra y hasta dos revalidaciones enfocadas;
- ciclos, coste y cierre.

No se versionan tokens, identidades personales, payloads sensibles, rutas
locales, URLs firmadas ni capturas voluminosas.

## Condiciones de parada

Detener y solicitar decisión si:

- la base difiere;
- WP016-DOR-1 no queda demostrado;
- GitHub cambia eventos, esquema, permisos o semántica;
- se necesita otra ruta, servicio, secreto o permiso;
- no puede emitirse un resultado terminal;
- context o integration_id difieren;
- deriva el parche protegido;
- una captura no cubre el estado completo;
- existe concurrencia en el ruleset;
- actionlint o cualquier validación es inejecutable;
- aparece una vulnerabilidad;
- se agotaría el presupuesto;
- se alcanza un tercer ciclo de corrección.

## Migración y rollback

Antes de hacer requerido el check, el rollback es revertir mediante acto humano
la integración de CI preservando las evidencias.

Después de la mutación se retira primero, y solo bajo el protocolo del grupo I,
el par exacto del ruleset. La retirada de código se realiza después mediante
una PR separada.

Nunca se restaura ciegamente una preimagen completa, se sobrescribe deriva
concurrente o se borra historia.

## Fuentes primarias

Al promover a ready y antes de mutar se revalidan:

- documentación oficial de eventos, workflows, omisiones y required checks;
- REST API oficial de commits, checks, PRs, repositorios, rulesets e historia;
- documentación oficial de firmas y permisos de Actions;
- RFC 8785 del RFC Editor.
