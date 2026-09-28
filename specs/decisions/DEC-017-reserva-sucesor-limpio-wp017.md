# DEC-017 — Reserva y límites del sucesor limpio de WP-017

**Estado propuesto:** aceptada únicamente si esta composición se materializa y
fusiona humanamente.
**Fecha propuesta:** 2026-09-28.
**Base:** `origin/main`
`6d9ac8f3583a2869ad73afe62c18c619295d39c9`.
**Ámbito:** reserva de un único identificador y límites previos a contrato; no
crea, aprueba, admite, activa ni implementa el sucesor.

## Problema

DEC-010 §10 dejó WP-017 `blocked`, nunca `done`, con DOR-7 a DOR-9 abiertos y
eligió una división limpia porque el coste de C1/C2 no puede reconstruirse. El
siguiente acto permitido es investigar y, si procede, reservar un identificador
nuevo con presupuesto, coste F1 y ciclos atribuibles desde el inicio. Redactar
directamente un contrato elegiría el identificador y trasladaría decisiones sin
el acto normativo previo exigido.

El inventario versionado contiene contratos `WP-000` a `WP-009` y `WP-013` a
`WP-017`; además, `WP-010`, `WP-011` y `WP-012` están reservados expresamente.
No existe archivo, reserva ni mención normativa de `WP-018`. Por tanto,
`WP-018` es el primer identificador libre y no reservado.

La candidata histórica `ops/wp-017-dor7-candidata` permanece `NO APTO`. Sus
bytes, ciclos y hallazgos no pueden convertirse en punto de partida del trabajo
nuevo. A la vez, las decisiones humanas ya registradas en `main` no deben
reabrirse indiscriminadamente: hay que separar elecciones estables de detalles
técnicos temporales y de elementos ligados al identificador agotado.

## Decisión

### 1. Reserva condicionada de WP-018

Al entrar esta composición completa en `main`, `WP-018` queda reservado como
único identificador del sucesor limpio de WP-017 y como prerrequisito productor
anterior a WP-016.

Antes de esa fusión, `WP-018` no está reservado. La reserva no crea
`work-packages/WP-018-*.md`, no cambia `ACTIVE`, no abre C1, no crea evidencia y
no autoriza contrato, aprobación, admisión, activación, implementación,
infraestructura, secretos, pruebas reales, rama, worktree, commit o PR.

### 2. Propósito y alcance material mínimo

El eventual WP-018 tendrá un solo resultado: un productor externo mínimo,
desplegable, operable y verificable que publique el check run exacto
`Alcance FDA` conforme a DEC-015, como prerrequisito de WP-016. El contrato
posterior deberá partir de `main` limpio y redactarse de nuevo; no reabre ni
continúa WP-017.

Quedan dentro únicamente el servicio y la infraestructura mínima que el
contrato demuestre indispensables para recibir o recuperar eventos, evaluar con
bytes confiables, publicar el resultado exacto, reconciliar fallos y operar o
retirar el productor. Permanecen fuera la integración en CI de WP-016, la
mutación del ruleset productivo, el cierre de WP-007, el runtime, el humo, E2 y
el cierre de la pausa.

### 3. Herencia y reafirmación de DOR-1 a DOR-6

La herencia es normativa por referencia; no autoriza copiar texto, código,
parches ni evidencias de la candidata histórica.

| Resolución | Tratamiento en el futuro contrato de WP-018 |
|---|---|
| DOR-1 | **Heredada por referencia:** repositorio `ivanes189/fda-template`, propiedad contractual de Iván, revisión confiable ya fusionada en `main` y artefacto fijado por digest. El contrato fijará rutas hoja nuevas y no reutilizará una candidata. |
| DOR-2 | **Heredada y reafirmada aquí:** Google Cloud, proyecto exclusivo bajo responsabilidad de Iván, región `europe-west1`, creación o vinculación de facturación como acto humano, presupuesto máximo del WP de `100 EUR` y objetivo operativo de `≤5 EUR/mes`. No se autoriza gasto ni creación de recursos. |
| DOR-3 | **Heredada por referencia:** minimización, región, tránsito, cifrado, retención, borrado, acceso, copias y contenido permitido en telemetría. El contrato revalidará contra fuentes oficiales cualquier comportamiento vigente del proveedor antes de declararse `ready`. |
| DOR-4 | **Heredada por referencia:** custodia humana, KMS solo-firma, Secret Manager regional, mínimo privilegio, rotación, revocación, emergencia y eliminación verificable de copias locales. Nombres y bindings exactos se reconstruyen con DOR-5. |
| DOR-5 | **Debe reafirmarse íntegramente en el contrato:** rutas hoja, lenguaje y runtime, dependencias y lockfiles, herramientas y versiones, IaC, artefactos, recursos, IAM, esquemas, red, eventos y comandos son temporales y quedaron ligados a WP-017. Se rederivan de las decisiones heredadas y de fuentes primarias oficiales vigentes, sin copiar sus bytes. |
| DOR-6 | **Debe reafirmarse íntegramente en el contrato:** propietario y visibilidad de la App, laboratorio, instalación limitada, nombres de ramas y recursos, check requerido de ensayo, ventana, coste, oráculos, evidencias, limpieza y rollback deben usar identidad propia de WP-018 y depender de DOR-8/DOR-9 todavía abiertos. No se presume que existan la App, el laboratorio o recurso alguno. |

Una referencia heredada conserva la decisión humana y sus máximos, pero no
convierte una afirmación cambiante en hecho actual ni exime de revalidarla. Si
una fuente oficial vigente contradice un detalle heredado, el contrato se
detiene y solicita una decisión humana; no lo corrige por conjetura.

### 4. DOR-7 a DOR-9 permanecen abiertos

Esta reserva no resuelve ni anticipa:

- DOR-7: operación, continuidad, alertas, despliegue, rollback, incidentes,
  suspensión, desinstalación y parada por coste;
- DOR-8: política evaluada, interfaz completa y oráculos de todas las ramas;
- DOR-9: regla conservadora para SHA compartido y concurrencia.

El futuro contrato deberá formularlos como bloqueos explícitos y no podrá pasar
de `draft` a `ready` hasta resolverlos mediante decisiones humanas verificables.
No se traslada `WP017-DOR7-F1`: el contrato nuevo debe especificar y revisar de
nuevo su propia condición IAM y sus oráculos desde cero.

### 5. Prohibición de trasladar la candidata histórica

La rama `ops/wp-017-dor7-candidata`, su preimagen, sus commits, diffs, ciclos,
hallazgos, evidencias y bytes permanecen históricos e intactos. WP-018 no puede
copiarlos, importarlos, transcribirlos, aplicarlos, hacerles cherry-pick,
rebasearlos, ejecutarlos ni usarlos como fuente de implementación o de texto.

Las únicas fuentes normativas reutilizables son los archivos fusionados en
`main`, citados por referencia y sometidos a la clasificación de §3. La
eventual implementación se escribe desde cero sobre una base limpia y dentro
de rutas nuevas enumeradas hoja a hoja por su contrato.

### 6. Coste F1, presupuesto y ciclos desde el inicio

La preparación externa del contrato y el futuro contrato quedan sujetos a:

- `presupuesto_max_eur: 100`;
- `max_ciclos_correccion: 2`;
- adquisición F1 desde la primera invocación de Claude Code atribuible a
  WP-018, incluida la preparación externa del contrato si usa Claude Code, la
  implementación inicial, cada corrección y cualquier intento fallido que
  reporte coste;
- WP-ID `WP-018` pasado explícitamente al capturador, nunca inferido de
  `ACTIVE`, la sesión o el horario;
- ejecución no interactiva con `claude -p --output-format json`; las
  invocaciones contabilizadas no usarán `--continue` ni `--resume`, para no
  sumar otra vez totales acumulados de conversaciones anteriores;
- un extracto saneado por invocación y una suma verificable conforme a DEC-004,
  sin versionar el JSON crudo, prompts, resultados, secretos o identificadores
  de sesión en claro.

La preparación externa del contrato puede autorizarse desde reposo antes de que
exista un contrato aprobado; esa autorización separada deberá exigir F1 y
custodiar fuera del repositorio cada extracto saneado para incorporarlo después
al expediente de coste de WP-018. Solo la implementación exige previamente un
contrato aprobado, admitido y activo mediante actos separados.

La preparación contractual y la implementación inicial no consumen ciclo de
corrección. La fila C1 se versiona `abierto` en
`evidence/WP-018/ciclos.md` únicamente antes de la primera corrección posterior
al dictamen completo, con candidata/revisión de origen y hallazgos autorizados;
C2 se abre del mismo modo antes de la segunda. Si cualquier invocación no
produce una cifra F1 defendible, se registra la causa, no se inventa coste y no
se realiza otra invocación hasta una decisión humana. C1 y C2 no se renombran
ni se reinician; una tercera corrección exige la parada de DEC-010.

La documentación oficial vigente confirma que `-p` ejecuta sin interacción,
que `--output-format json` incluye `total_cost_usd` y que una continuación o
reanudación informa el total completo de la conversación, incluidos runs
anteriores. La cifra sigue siendo estimación del cliente conforme a DEC-004.

### 7. Contrato posterior y secuencia

Una autorización humana posterior y separada podrá pedir únicamente una
candidata externa `draft` de WP-018. El contrato será T3, tendrá como máximo
300 líneas, enumerará archivos hoja, mantendrá `ACTIVE` en reposo durante su
redacción y recibirá la revisión única independiente y los ciclos que exige
DEC-010.

La secuencia queda: WP-015 `done` → WP-017 `blocked` e histórico → WP-018
reservado, sin contrato → eventual contrato, aprobación, admisión, activación e
implementación de WP-018 mediante actos separados → corrección y eventual
admisión de WP-016 → resto de la secuencia vigente. Ningún eslabón autoriza el
siguiente.

## Composición atómica mínima

Los siguientes nueve archivos viajan juntos o ninguno:

1. `specs/decisions/DEC-017-reserva-sucesor-limpio-wp017.md` — esta decisión;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md` — admite la
   composición, registra la reserva y mantiene la pausa y `ACTIVE` en reposo;
3. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md` — registra el
   acto posterior previsto por §10 sin alterar la historia de WP-017;
4. `specs/decisions/DEC-011-recuperacion-post-dec009.md` — sustituye el
   prerrequisito bloqueado por el sucesor reservado en la secuencia;
5. `specs/decisions/DEC-014-reserva-sucesor-wp005.md` — mantiene el gate de
   WP-016 apuntando al productor sucesor correcto;
6. `specs/decisions/DEC-015-productor-externo-check-scope.md` — conserva la
   arquitectura y registra que WP-018 sucede limpiamente a WP-017;
7. `specs/decisions/DEC-016-reserva-productor-externo-alcance.md` — conserva la
   reserva histórica de WP-017 y registra su sustitución sin reescribirla;
8. `docs/03-hoja-de-ruta.md` — actualiza el hito y la secuencia condicionada;
9. `docs/manual/05-bloqueos-y-parada.md` — actualiza el estado operativo.

No forman parte de la composición `work-packages/**`, `ACTIVE`, `evidence/**`,
código, pruebas, workflows, ruleset, infraestructura, cuentas, roles, secretos,
permisos, ramas, worktrees, candidatas, `.agents/`, `.codex/` ni `AGENTS.md`.

## Fuera de alcance

Esta decisión no autoriza materializar o redactar el contrato de WP-018;
aprobar, admitir, activar o implementar ningún WP; modificar WP-017, WP-016 o
`ACTIVE`; crear `cost.md` o filas de ciclos; corregir F1; crear o configurar
GitHub o Google Cloud; crear infraestructura, cuentas, Apps, repositorios,
artefactos, claves, secretos o permisos; ejecutar Claude Code o pruebas reales;
modificar workflows o ruleset; crear ramas, worktrees, commits o PRs; reservar
otro WP-ID; ni tocar o limpiar ramas y candidatas históricas.

## Fuente primaria revalidada

- Claude Code Docs, *Run Claude Code programmatically*, consultada el
  2026-09-28: <https://code.claude.com/docs/en/headless>.

No se incorporan aquí afirmaciones nuevas sobre GitHub o Google Cloud. Sus
aspectos cambiantes deberán revalidarse contra documentación oficial vigente al
redactar el contrato y antes de cualquier operación real.

## Condición de efecto

Esta candidata no tiene efecto fuera del repositorio. Solo una autorización
humana posterior puede materializar exactamente los nueve archivos sobre la
base declarada; rama, commit, PR y fusión requieren autorizaciones separadas.
