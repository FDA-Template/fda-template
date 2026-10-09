# DEC-010 — Separación de autor y revisor y bucle ordinario de dos ciclos

**Estado:** aceptada · **Fecha:** 2026-09-21 · **Ámbito:** revisiones
independientes, correcciones ordinarias, contabilidad de ciclos y aplicación del
nivel T3

**Origen:** investigación externa aceptada por el operador tras el cierre
bloqueado de WP-008 y revisión independiente de esta candidata normativa. Se
materializa desde reposo como acto de operador, sin reanudar la secuencia
técnica detenida por [`DEC-009`](DEC-009-cierre-bloqueado-wp-008.md).

**Enmendada el 2026-09-28 por decisión humana de instancia:** el apartado 8
habilita, sin iniciarlo, un C3 único para la candidata externa que resuelve
`WP017-DOR-7`. No crea otro identificador normativo, no corrige la candidata y
no altera la regla general de dos ciclos.

**Enmendada de nuevo el 2026-09-28 por decisión humana de instancia:** el
apartado 9 constata que el coste acumulado de C1 y C2 no puede reconstruirse,
cierra la transición `WP017-DOR-7` como bloqueada antes de abrir C3 y deja sin
efecto su autorización excepcional todavía no usada.

**Enmendada por tercera vez el 2026-09-28 por decisión humana de instancia:**
el apartado 10 bloquea WP-017 sin declararlo entregado, elige una división
limpia posterior y prohíbe reiniciar ciclos o trasladar la candidata histórica.
No reserva otro WP-ID ni autoriza redactar su sucesor.

**Actualizada el 2026-09-28 por [`DEC-017`](DEC-017-reserva-sucesor-limpio-wp017.md):**
materializa únicamente el siguiente acto previsto por §10 y reserva `WP-018`
como sucesor limpio. No altera los ciclos, el coste irrecuperable, el bloqueo de
WP-017 ni la preservación de su candidata histórica.
**Enmendada por cuarta vez el 2026-10-09 por decisión humana de instancia:**
el apartado 11 cierra `blocked` tras C2 la transición agotada de
`WP018-DOR-7` y elige un replanteamiento como transición nueva. No abre C3,
no reabre los demás hallazgos y no altera la regla general de dos ciclos.
**Enmendada por quinta vez el 2026-10-09 por decisión humana de instancia:**
el apartado 12 elige la decisión previa necesaria para aislar el `actAs` de
emergencia de `WP018-DOR-7`. Acepta de forma condicionada un tag Pre-GA,
pero no abre la transición nueva, resuelve F2 ni modifica WP-018.
**Enmendada por sexta vez el 2026-10-09 por decisión humana de instancia:**
el apartado 13 cierra `blocked`, antes de candidata técnica y ciclos, la
transición nueva de `WP018-DOR-7`: las referencias oficiales PAM v1 y v1beta
siguen excluyendo tags mientras las guías vigentes los declaran compatibles.
F2 y DOR-7 permanecen abiertos; no se simula conformidad ni se modifica WP-018.


## Problema

La FDA ya separaba implementador y revisor, limitaba las correcciones ordinarias
a dos ciclos y obligaba a parar ante el tercero. El flujo, sin embargo, estaba
repartido entre varios documentos y dejaba cuatro ambigüedades operativas:

1. no declaraba en un solo lugar que los hallazgos vuelven inmediatamente al
   autor y que la misma revisora hace después una revalidación enfocada;
2. no decía que la autorización inicial puede cubrir C1 y C2 sin nuevas
   confirmaciones cuando alcance, presupuesto y autoridad no cambian;
3. no exigía un registro durable del ciclo si una invocación falla o no produce
   cambios;
4. la tabla T3 podía leerse como dos revisores y aplicación humana universal,
   aunque la independencia exige una sola revisión completa y la aplicación
   humana corresponde a las rutas o actos protegidos.

WP-008 mostró el coste de estas ambigüedades: cinco ciclos —C1 y C2 ordinarios
y C3–C5 excepcionales— y varias revalidaciones sin convergencia. La respuesta
no es permitir que Astra corrija lo que revisa, porque perdería independencia,
sino cerrar y acelerar el bucle autor → revisión → corrección → revalidación.

## Decisión

### 1. Separación de funciones

- Claude Code es autor: implementa y corrige los WPs expresamente autorizados.
- GPT-6 Astra, razonamiento Alto y contexto nuevo, es revisor independiente y
  estrictamente de solo lectura. Nunca modifica el candidato que revisa.
- Astra recibe normas, contrato, candidato y pruebas; no recibe el `APTO` ni la
  conclusión del autor como premisa.

### 2. Una revisión completa y revalidaciones enfocadas

- Hay una sola revisión completa por candidato o transición.
- Si hay incumplimientos concretos, Claude corrige únicamente esos hallazgos y
  sus efectos directos. Las mejoras laterales se registran y no se incorporan.
- La misma Astra revalida de forma enfocada las correcciones y sus efectos
  directos. No se abre otra revisión general, no se añade otro revisor y no se
  revisa la revisión.
- El dictamen final puede ser `APTO` en la revisión completa inicial o en una
  revalidación enfocada posterior dentro de los ciclos autorizados.

### 3. Autorización cerrada para C1 y C2

Una autorización de ejecución que identifique el WP, el alcance aprobado, el
presupuesto máximo y `max_ciclos_correccion: 2` cubre la implementación inicial
y, si resultan necesarias, C1 y C2. No se pide una confirmación entre esas
pasadas cuando permanecen invariables el alcance, el presupuesto, los archivos
permitidos y la autoridad.

Esta cobertura nunca autoriza por implicación:

- ampliar el contrato o sus archivos permitidos;
- superar el presupuesto;
- aplicar rutas protegidas;
- cambiar `ACTIVE`, crear o fusionar PRs, o ejecutar otros actos reservados;
- resolver una ambigüedad, contradicción, vulnerabilidad o decisión humana;
- iniciar C3.

### 4. Contabilidad durable de ciclos

- La implementación inicial no consume ciclo.
- Cada pasada de corrección del autor posterior a un veredicto consume un ciclo
  desde que comienza, aunque la herramienta falle, se interrumpa, termine sin
  cambios o no cierre el hallazgo.
- Antes de comenzar la corrección, una fila debe quedar efectivamente
  **versionada en la rama candidata** en `evidence/WP-XXX/ciclos.md`, con:
  número, HEAD/candidato y revisión de origen, IDs de hallazgos autorizados,
  fecha y estado `abierto`. Si no existe autoridad para versionarla, la pasada
  no comienza.
- Al terminar se actualiza esa misma fila con resultado, HEAD final o
  `sin cambios`, verificaciones, coste/invocaciones y dictamen enfocado cuando
  exista.
- Al reanudar una sesión, ese registro —no la conversación— determina el
  siguiente número. Los expedientes históricos no se reescriben.
- Una revalidación sin nueva pasada de autor no consume ciclo.

### 5. Parada tras C2; C3 no es la continuación normal

Si el dictamen posterior a C2 no es `APTO`, se preserva el candidato y se para.
La siguiente decisión debe elegir cierre `blocked`, división del problema o
replanteamiento del contrato.

Un C3 solo puede existir mediante una decisión humana nueva, previa, fechada y
versionada que identifique WP, hallazgos cerrados, alcance exacto, presupuesto
adicional y techo final. No reinicia ni renombra el contador y no crea
precedente ni autorización implícita para C4. La opción predeterminada después
de C2 es dividir o replanificar, no conceder excepciones sucesivas.

### 6. Interpretación del nivel T3

- T3 exige una revisión independiente completa con lente conjunta de contrato,
  corrección y seguridad. En el modelo operativo vigente la realiza una sola
  Astra; no se duplica con un segundo revisor general.
- Si hay correcciones, la misma Astra hace las revalidaciones enfocadas.
- T3 no convierte por sí solo todos los archivos en protegidos. La aplicación
  personal por Iván se exige cuando la ruta o el acto está protegido por la
  constitución, permisos, decisiones o contrato. Los archivos no protegidos
  pueden ser escritos por Claude dentro de un WP activo y autorizado.
- La revisión nunca concede autoridad para aplicar protegidos.

### 7. Relación con DEC-009

Esta decisión no elige recuperación, sustitución ni cambio de la secuencia
técnica detenida por DEC-009. Autoriza exclusivamente esta composición normativa
de operador, desde reposo, para hacer coherente el método antes de preparar esa
decisión. `ACTIVE` permanece en reposo; no se crea ni activa WP; las candidatas
históricas permanecen intactas.

DEC-003 admite expresamente esta composición única en su lista cerrada. DEC-010
no se autoautoriza: su materialización y fusión requieren actos humanos
separados. Tras fusionarla, la parada técnica de DEC-009 continúa sin cambios.

## Composición atómica de operador

Los siguientes siete archivos viajan juntos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`
3. `CLAUDE.md`
4. `docs/03-hoja-de-ruta.md`
5. `docs/manual/02-ciclo-de-un-wp.md`
6. `docs/manual/04-agentes.md`
7. `docs/manual/05-bloqueos-y-parada.md`

No forman parte de la composición `work-packages/**`, `ACTIVE`, `.claude/**`,
`.github/**`, `CODEOWNERS`, `scripts/**`, `tests/**`, rulesets, candidatas ni
evidencias históricas.

## Revisión independiente de la candidata normativa

La revisión completa de Astra concluyó `NO APTO` por cuatro incumplimientos:
falta de admisión en DEC-003 y conflicto con la parada de DEC-009, tratamiento
T3 no reconciliado, ausencia de un registro durable de ciclos interrumpidos y
un criterio que atribuía indebidamente el `APTO` a la revisión inicial.

La primera corrección eligió esta composición de operador, precisó T3, añadió el
registro de ciclos y permitió que el dictamen final llegase en revalidación. La
primera revalidación enfocada cerró tres hallazgos y mantuvo abierto que
«preparar para versionado» no garantizaba el registro. La segunda corrección
exigió versionar la apertura antes de iniciar la pasada y corrigió la descripción
histórica de C1–C5. La segunda revalidación enfocada emitió `APTO`. No hubo otro
revisor, otra revisión general ni modificación de la candidata por Astra.

## Verificación

```bash
git diff --check
python3 evidence/WP-000/checks/check-manual.py
bash tests/governance/check-active.sh
```

Además:

- el diff contiene exactamente los siete archivos de la composición;
- `ACTIVE` sigue en reposo;
- no cambian workflows, ruleset, agentes, permisos, candidatas ni contratos;
- DEC-009 sigue deteniendo la recuperación técnica.

## Consecuencias

**A favor:** mantiene independencia, reduce esperas humanas dentro de límites
ya autorizados, hace reconstruibles los intentos fallidos y evita repetir la
espiral C3–C5 como flujo normal.

**Coste:** registrar la apertura de cada ciclo añade un commit antes de corregir.
Se acepta porque impide perder contabilidad al interrumpirse una herramienta o
una sesión.

**No autorizado:** fusionar sin acto humano posterior; cambiar `ACTIVE`; crear
o ejecutar un WP; tocar protegidos; decidir o reanudar la recuperación de
WP-008; limpiar ramas, worktrees o candidatas.

## 8. Enmienda de instancia del 2026-09-28 — C3 excepcional de WP017-DOR-7

### 8.1. Hechos, identidad y conjunto cerrado

Sobre `origin/main` `ec8cb8113df8c209e9340d9841192dd46cd11a5a`, la
candidata externa de resolución de `WP017-DOR-7` consumió C1 y C2 y quedó
`NO APTO`. La preimagen agotada y preservada es
`WP017-DOR7-candidata-NO-APTA-C2.patch`, SHA-256
`e4877b02a05ad65be1579d333758808393f3a6b4473e1b719ebaa43e8c4709a7`.
Aplicada solo para reconstrucción sobre esa base, deja
`work-packages/WP-017-productor-externo-alcance.md` con SHA-256
`ad2053893d7416a30a564c33416ddd7ac8e77220575f071906e8c0cb131086ee` y
`docs/manual/05-bloqueos-y-parada.md` con SHA-256
`ae49c644cd7a2361b1ed7e251cf98e5cac1ed026cbb465ba86d1cc6f0cf37206`.

La revisión completa abrió `WP017-DOR7-F1` a `WP017-DOR7-F4`. C1 cerró F2,
F3 y F4 y dejó F1 por la ausencia de autoridad para fijar la política IAM del
secreto. C2 sustituyó los bindings sobre el secreto por bindings de proyecto
condicionados, pero F1 permaneció abierto porque la condición usa `PROJECT_ID`
donde `resource.name` exige el nombre canónico basado en `PROJECT_NUMBER`.
F2, F3 y F4 permanecen cerrados y no autorizan ningún cambio.

La documentación oficial de IAM distingue expresamente ID y número de
proyecto y prohíbe sustituir uno por otro en los formatos de nombres de
recursos. La API regional puede aceptar un ID al direccionar una solicitud,
pero eso no cambia el valor canónico que compara `resource.name`. Por tanto el
residual es único, conocido y comprobable sin elegir nueva política.

### 8.2. Elección excepcional, no transición nueva

Se habilita un C3 mínimo y último. No se replantea como candidata nueva porque
eso reiniciaría de hecho una transición cuyo contrato, alcance y controles no
cambian y ocultaría los dos ciclos ya consumidos. Tampoco se divide o cierra
`blocked`: solo queda una sustitución mecánica dentro de una condición ya
decidida y dos oráculos deterministas. Esta decisión de instancia es la
decisión humana nueva, previa, fechada y versionada que exige el apartado 5;
enmendar DEC-010 evita inventar o reservar otro identificador normativo.

La excepción no empieza C3. Solo entra en vigor tras la materialización y
fusión humana de la composición de §8.7 y requiere después otra autorización
humana que identifique el commit fusionado, la preimagen C2 y el procedimiento
de custodia de §8.3. No existe C4.

### 8.3. Preimagen versionada antes de corregir

La candidata C2 externa no se corrige in situ. Con autorización posterior, se
creará desde la base exacta citada una rama candidata gobernada y se aplicarán
sin cambios sus bytes preservados. El primer commit de custodia contendrá esa
preimagen C2 y `evidence/WP-017/ciclos.md`, que reconstruirá C1 y C2 como
historia consumida mediante sus dictámenes y huellas, sin renombrarlos. Después
se incorporará, sin reescribir historia, el `main` que contenga esta enmienda.

En un commit posterior y todavía anterior a cualquier corrección, la fila C3
de `evidence/WP-017/ciclos.md` quedará versionada con: estado `abierto`, origen
C2, `WP017-DOR7-F1`, fecha, SHA de esta enmienda ya vigente, presupuesto de
§8.5 y cabeza candidata. Solo entonces puede comenzar la pasada. Si la
preimagen reconstruida, cualquiera de sus dos SHA-256 o la historia difieren,
se detiene; no se adapta ni regenera la candidata por conveniencia.

### 8.4. Única corrección autorizable y oráculos

Claude Code sigue siendo el único autor y corrector. C3 solo puede modificar
`work-packages/WP-017-productor-externo-alcance.md` y las evidencias cerradas
de §8.6. En la condición de DOR-4 debe sustituir exclusivamente las dos
apariciones del prefijo
`projects/PROJECT_ID/locations/europe-west1/secrets/github-webhook-secret`
por
`projects/PROJECT_NUMBER/locations/europe-west1/secrets/github-webhook-secret`:
una igualdad para el secreto y un `startsWith` terminado en `/versions/`.

El mismo cambio contractual debe exigir que la futura verificación headless:

1. evalúe positivamente la condición para el secreto autorizado y para una de
   sus versiones numéricas;
2. evalúe negativamente la misma condición para
   `projects/PROJECT_NUMBER/locations/europe-west1/secrets/otro-secreto` y una
   de sus versiones;
3. falle si cualquiera de los cuatro resultados no coincide con lo esperado.

No se autoriza cambiar roles, miembros, ámbito, región, nombre del secreto,
recursos, operación, DOR-8, DOR-9, manual, F2, F3 o F4. La misma Astra que
emitió el dictamen enfocado de C2 realizará una sola revalidación enfocada de
F1 y de los efectos directos de esta corrección; no habrá otra revisión general.

### 8.5. Presupuesto y techo

- Presupuesto adicional máximo para C3: `5.00 EUR`.
- Techo final acumulado de WP-017: `100.00 EUR`, sin modificar el máximo
  contractual vigente.
- Antes de abrir C3, `evidence/WP-017/cost.md` debe fijar el coste acumulado
  verificable. Si no puede reconstruirse, si supera `95.00 EUR` o si C3 alcanza
  `5.00 EUR`, la pasada no comienza o se detiene sin otra invocación del autor.

### 8.6. Evidencia y salida

C3 solo puede crear o actualizar, además del único contrato de §8.4:

- `evidence/WP-017/ciclos.md`;
- `evidence/WP-017/revision-astra.md`;
- `evidence/WP-017/cost.md`;
- `evidence/WP-017/verificacion-dor7-c3.md`, limitado a los cuatro oráculos de
  §8.4, sin secretos, identificadores reales ni prueba sobre infraestructura.

La revalidación `APTO` cerraría exclusivamente F1 y permitiría una autorización
humana posterior para materializar la resolución de DOR-7. No aprueba, admite,
activa o implementa WP-017. Si F1 continúa abierto, aparece otro hallazgo,
resulta necesaria otra ruta o se agota el presupuesto, la candidata se
preserva `NO APTO` y se detiene; no existe corrección posterior.

### 8.7. Composición normativa y límites

Esta enmienda de instancia viaja en una composición atómica de exactamente
tres archivos; todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/manual/05-bloqueos-y-parada.md`.

La composición no modifica WP-017, WP-016, `ACTIVE`, candidatas, evidencias,
código, pruebas, infraestructura, cuentas, roles, secretos, permisos, Google
Cloud, GitHub, workflows o ruleset. No crea rama, worktree, commit o PR y no
inicia C3. Su materialización, publicación y fusión, la custodia de la preimagen
y el inicio de C3 son actos humanos posteriores y separados.

Fuentes primarias revalidadas el 2026-09-28: documentación de Google Cloud
«Resource attributes for IAM Conditions», «Attribute reference for IAM
Conditions» y referencia REST `projects.locations.secrets` de Secret Manager.

## 9. Enmienda de instancia del 2026-09-28 — cierre antes de C3 por coste irrecuperable

### 9.1. Hechos verificables y estado de la candidata

La base normativa es `origin/main`
`d0b01bf7a14beae7ea32aaf5f5c618350e1a6b83`. La rama gobernada
`ops/wp-017-dor7-candidata` está en
`a15483b7c05d64431fde8866aca27e2d339017c6`, merge explícito cuyos padres son
el primer commit de custodia
`7e72df1ce2e061bb7a0471e006a3390115074127` y esa base normativa. La
custodia conserva la postimagen C2 de WP-017 con SHA-256
`ad2053893d7416a30a564c33416ddd7ac8e77220575f071906e8c0cb131086ee` y
`evidence/WP-017/ciclos.md` con SHA-256
`588b2689ffd5ecd6f6b109ea78ba522b096388f3266de903cf9caf66f836f73b`.

El registro versionado dice para C1 y C2 `coste no reconstruido`, no contiene
fila C3 y declara que la pasada no comienza sin coste acumulado verificable.
En ninguna referencia versionada del repositorio existe
`evidence/WP-017/cost.md`, un artefacto F1 o F2 de WP-017, una lectura F3
fechada y atribuible, ni otro importe defendible para esas dos pasadas. La
conversación, una cifra de memoria, una ventana horaria, otro WP o un artefacto
externo no versionado no son fuente de verdad ni satisfacen DEC-004.

Por tanto se ha materializado exactamente la condición de parada de §8.5:
el coste acumulado no puede reconstruirse. C3 nunca se abrió, Claude Code no
fue invocado para C3 y `WP017-DOR7-F1` no fue corregido.

### 9.2. Alternativas comparadas

**Cierre bloqueado de esta transición — elegido.** Conserva el expediente
`NO APTO`, hace explícita la causa y mantiene abiertas las decisiones futuras
sobre WP-017. Es la salida ordinaria de §5 cuando una precondición de C3 falla.

**Excepción económica para continuar — rechazada.** No existe una variante
que preserve simultáneamente la verdad del coste y las normas vigentes:

- `estado_coste: no_disponible` sería veraz, pero DEC-004 §11 lo deja
  `NO APTO` y, mientras dure DEC-003, no existe el registro único de
  excepciones que debe crear WP-010;
- cargar `95.00 EUR` o cualquier otra reserva cautelar al presupuesto no
  transforma esa cifra en coste F1, F2 o F3 y no prueba el umbral de §8.5;
- elevar el techo, excluir retroactivamente C1/C2 o atribuirles cero ocultaría
  la ausencia en vez de reconstruirla;
- crear aquí otro mecanismo de excepción duplicaría el mecanismo único de
  DEC-004 y convertiría una parada concreta en precedente transversal.

La excepción solo desplazaría el mismo bloqueo al cierre de WP-017, después de
consumir otro ciclo. No es una salida proporcional ni verificable.

### 9.3. Decisión y efectos exactos

1. La transición externa que intentaba resolver `WP017-DOR-7` queda cerrada
   `blocked` antes de C3. Los dos ciclos ordinarios permanecen consumidos y no
   se renombran ni reinician.
2. La habilitación excepcional de §8.2 queda sin efecto sin haber sido usada.
   No existe C3 ni C4 y no se crea ninguna fila nueva en el registro de ciclos.
3. La rama `ops/wp-017-dor7-candidata`, sus dos commits y sus bytes se
   preservan como candidata histórica `NO APTO`. No se fusionan, corrigen,
   ejecutan, importan, rebasan ni limpian.
4. F1 permanece abierto. F2, F3 y F4 permanecen cerrados únicamente como
   hechos del expediente preservado y no conceden autoridad adicional.
5. En `main`, WP-017 permanece `draft`: DOR-1 a DOR-6 están resueltos y
   DOR-7 a DOR-9 siguen abiertos. WP-016 y `ACTIVE` permanecen intactos.
6. No se crea `evidence/WP-017/cost.md`: hacerlo con un número inventado o con
   `no_disponible` no satisfaría §8.5 ni abriría C3.
7. No se reserva ni inventa otro WP-ID. Elegir el cierre definitivo de WP-017,
   dividirlo o replantear DOR-7 requiere otra decisión humana nueva, previa y
   versionada. Este acto no prepara ni autoriza esa decisión posterior.

### 9.4. Composición atómica y límites

Esta enmienda viaja en una composición atómica de exactamente cuatro archivos;
todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`.

La composición parte de la base exacta de §9.1. No contiene WP-017, WP-016,
`ACTIVE`, `evidence/**`, código, pruebas, workflows, ruleset, infraestructura,
cuentas, roles, secretos, permisos, ramas, worktrees ni candidatas. Su
materialización, publicación y fusión son actos humanos posteriores y
separados; esta candidata externa no los autoriza.

## 10. Enmienda de instancia del 2026-09-28 — bloqueo de WP-017 y división limpia

### 10.1. Hechos y restricción económica

La base normativa es `origin/main`
`630b095b009211475dd30666f7525a7b7d3eecbe`. WP-017 permanece `draft`, nunca
fue aprobado, admitido, activado o implementado: DOR-1 a DOR-6 están resueltos,
DOR-7 a DOR-9 abiertos y la transición de DOR-7 cerrada `blocked` antes de C3.
La rama `ops/wp-017-dor7-candidata` permanece en
`a15483b7c05d64431fde8866aca27e2d339017c6` como candidata histórica
`NO APTO`; esta enmienda no la lee como fuente de bytes ni la modifica.

DEC-010 §9 acredita que C1 y C2 no tienen coste F1, F2 o F3 reconstruible.
DEC-004 §11 impide cerrar como APTO un WP con `estado_coste: no_disponible`
mientras dure DEC-003 y no exista el registro único que debe crear WP-010.
Medir desde cero un intento posterior no reconstruiría el total de WP-017 y un
contador nuevo bajo el mismo WP ocultaría los dos ciclos ya consumidos.

### 10.2. Alternativas comparadas

**Abandono definitivo de WP-017 como `blocked`, sin sucesor — viable pero no
elegido.** Es una salida administrativa lícita de DEC-010 §5: preservaría el
expediente sin afirmar entrega ni exigir `done`. Se rechaza porque dejaría sin
continuidad el productor externo que DEC-015 y DEC-016 mantienen como
prerrequisito de WP-016, no porque incumpla la regla de parada. `done` sí queda
prohibido: afirmaría una entrega inexistente y criterios no cumplidos. Tampoco
se crea `cost.md`, se inventa coste o se usa `done` como sinónimo de abandono.

**Replanteamiento directo dentro de WP-017 — rechazado.** Una transición nueva
podría medir sus propias invocaciones, pero no el coste acumulado del WP. Darle
C1/C2 propios bajo el mismo identificador convertiría el replanteamiento en un
reinicio material de la cuenta cerrada por §9 y dejaría el mismo bloqueo para
el cierre, después de más gasto.

**División limpia posterior — elegida.** WP-017 queda como expediente bloqueado
y el productor pendiente deberá ser objeto de un sucesor limpio. Es la única
opción que permite que presupuesto, coste y ciclos nazcan juntos y sean
atribuibles desde la primera invocación, sin alterar la historia agotada. Esta
decisión elige la forma, pero no inventa ni reserva el identificador sucesor.

### 10.3. Decisión y límites del siguiente acto

1. WP-017 pasa de `draft` a `blocked`, nunca a `done`. DOR-7 a DOR-9 permanecen
   abiertos y sus criterios no se declaran cumplidos.
2. WP-017 queda retirado de la cola ejecutable: no puede aprobarse, admitirse,
   activarse, implementarse o reactivarse sin otra decisión humana nueva,
   previa, fechada y versionada que resuelva expresamente esta enmienda y
   DEC-004 §11.
3. La candidata histórica, sus dos commits, ciclos reconstruidos y hallazgos se
   preservan íntegros. No se fusionan, corrigen, importan, rebasan, ejecutan,
   limpian ni se copian a un sucesor.
4. El siguiente acto posible es únicamente investigar y, si procede, reservar
   un nuevo WP-ID para un sucesor limpio. Debe fijar antes de redactar contrato:
   adquisición F1 desde la primera invocación con WP-ID explícito, presupuesto
   máximo, `max_ciclos_correccion: 2`, alcance material y relación con DOR-8 y
   DOR-9. No puede abrir una transición o fila de ciclos bajo WP-017.
5. Ese acto posterior no está preparado ni autorizado aquí. La presente
   decisión no asigna identificador, presupuesto o contrato al sucesor, no
   corrige `WP017-DOR7-F1` y no resuelve DOR-8 o DOR-9.
6. WP-016 y `ACTIVE` permanecen intactos; la secuencia continúa detenida.

DEC-017 ejecuta posteriormente y solo ese siguiente acto: identifica `WP-018`,
fija `100 EUR`, F1 desde la primera invocación y `max_ciclos_correccion: 2`, y
clasifica la herencia de DOR-1 a DOR-6. No redacta el contrato, no abre ciclos,
no resuelve DOR-7 a DOR-9 y no modifica ninguno de los hechos de esta §10.

### 10.4. Composición atómica

Esta enmienda y el bloqueo contractual viajan en exactamente cinco archivos;
todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`;
5. `work-packages/WP-017-productor-externo-alcance.md`.

No contiene WP-016, `ACTIVE`, `evidence/**`, código, pruebas, workflows,
ruleset, infraestructura, cuentas, roles, secretos, permisos, ramas,
worktrees o candidatas. No crea `cost.md`, filas de ciclos, otro WP-ID ni una
excepción económica; no autoriza ejecución o actos posteriores. Su
materialización, publicación y fusión requieren autorizaciones humanas
separadas.

## 11. Enmienda de instancia del 2026-10-09 — cierre tras C2 y replanteamiento de WP018-DOR-7

### 11.1. Hechos, identidad y conjunto cerrado

Sobre `origin/main` `10ae4d96e95d8a5ba449420ab35999e56b4860a2`, la
candidata externa del primer acto previo a `WP018-DOR-7` consumió C1 y C2 y
quedó `NO APTO`. La preimagen C2 preservada consta de:

- `DEC-018-continuidad-operativa-wp018.md`, SHA-256
  `f8bf4996ff4fcf86c96356dc13b0478b3f6a926e9067796e3c1c848cb7bfba4f`;
- `PATCH-EXISTING.diff`, SHA-256
  `eafcfb14a9c49b0e88eb0b135d5ef90402642b8c0399268bd00db00c7c9d84a6`.

El parche se limita a siete archivos existentes y sus 22 hunks fueron
contrastados con esa base; junto con la nueva DEC-018 forma una composición
candidata de ocho archivos. Ningún byte está materializado en el repositorio.

La revisión completa abrió F1 a F7. C1 cerró F1, F3, F5, F6 y F7; C2 cerró
F4. Permanece abierto solo F2: restaurar la configuración push autenticada de
`alcance-fda-wp018-worker-push` requiere que el humano que la modifica tenga
`iam.serviceAccounts.actAs` sobre `alcance-fda-wp018-push`, y la matriz C2 no
lo concede. Los demás hallazgos permanecen cerrados como resultados exigibles;
no autorizan otros cambios.

La documentación oficial confirma que `roles/iam.serviceAccountUser` contiene
`iam.serviceAccounts.actAs` y puede ligarse directamente a una cuenta de
servicio. También confirma que quien posee `roles/run.developer` y `actAs`
puede actualizar un servicio Cloud Run para usar esa identidad. Los dos humanos
ya reciben temporalmente `roles/run.developer` en la operación ordinaria de la
candidata C2. Por tanto, un binding directo permanente sobre la identidad push
ampliaría capacidades fuera de la emergencia y no es una corrección mecánica
sin efectos laterales.

Privileged Access Manager concede role bindings sobre su recurso padre —en
este caso el proyecto—, no un binding directo sobre una sola cuenta de servicio.
Conceder allí `roles/iam.serviceAccountUser` ampliaría `actAs` a otras
identidades del proyecto y rompería el límite negativo exigido. La vía C3 no
puede conservar simultáneamente el modelo C2, la temporalidad y el mínimo
privilegio sin elegir un mecanismo nuevo o revisar permisos relacionados.

### 11.2. Alternativas y decisión

**C3 excepcional sobre la candidata C2 — rechazado.** El residual es único,
pero no la corrección: el binding directo permanente interactúa con el acceso
ordinario de Cloud Run y el binding PAM a nivel de proyecto excede la identidad
push. Elegir una de esas variantes como simple F2 ocultaría una ampliación de
autoridad; introducir identidades, condiciones, tags, políticas o servicios
nuevos excedería una revalidación enfocada y requeriría decisiones no cerradas.

**Replanteamiento como transición nueva dentro de `WP018-DOR-7` — elegido.**
La candidata C2 se conserva `NO APTO` y su transición termina `blocked` después
de C2. No se abre C3, no existe C4 y los ciclos consumidos no se renombran,
reinician ni atribuyen a la transición futura. El replanteamiento deberá
rederivar únicamente el mecanismo de autorización que resuelve F2, manteniendo
como restricciones los resultados cerrados de F1 y F3 a F7.

Esta enmienda no inicia ni prepara la transición nueva. Solo entra en vigor
tras materializar y fusionar humanamente los cuatro archivos de §11.5. Después
hará falta otra autorización humana, limitada a investigación en solo lectura y
preparación externa de una candidata nueva. No se crea, inventa o reserva otro
identificador normativo o WP-ID.

### 11.3. Efectos exactos del cierre

1. La transición externa de la candidata identificada en §11.1 queda cerrada
   `blocked` después de C2. Su único residual F2 sigue abierto.
2. La candidata, sus dos archivos y sus huellas se preservan como historia
   externa `NO APTO`; no se materializan, corrigen, importan, ejecutan, mezclan
   ni usan como autorización.
3. F1 y F3 a F7 permanecen cerrados como resultados del expediente. Una futura
   candidata debe conservar esos resultados y demostrar que no regresan, pero
   no recibe autoridad para cambiar otras materias.
4. WP-018 permanece `draft`; `WP018-DOR-7`, DOR-8 y DOR-9 permanecen abiertos.
   WP-017, WP-016 y `ACTIVE` permanecen intactos.
5. No se crea `evidence/WP-018/ciclos.md`, `cost.md`, artefacto F1 o fila C3.
   Esta preparación y su revisión no ejecutaron Claude Code ni generaron coste
   atribuible por ese mecanismo.

### 11.4. Límites de la transición nueva y del siguiente acto

El siguiente acto posible es únicamente autorizar investigación en solo lectura
y preparar fuera del repositorio una candidata nueva para `WP018-DOR-7`. Esa
candidata deberá:

1. rederivar desde fuentes oficiales vigentes un mecanismo que permita a los
   dos humanos ya designados restaurar push autenticado con
   `iam.serviceAccounts.actAs` sobre `alcance-fda-wp018-push` durante la
   emergencia, sin otorgarlo sobre `alcance-fda-wp018-scheduler` ni convertirlo
   en capacidad efectiva durante la operación ordinaria;
2. analizar expresamente la composición de permisos con el entitlement
   ordinario, `roles/run.developer`, `run.services.update` y cualquier permiso
   que permita adjuntar una identidad a Cloud Run;
3. fijar oráculos positivos y negativos que fallen si `actAs` resulta efectivo
   fuera de la emergencia, sobre otra identidad o sin el permiso temporal que
   habilita modificar la suscripción;
4. conservar sin reapertura los resultados cerrados de F1 y F3 a F7, salvo una
   regresión directa y demostrada del nuevo mecanismo;
5. detenerse y pedir decisión si la solución exige una identidad, proveedor,
   servicio, tag, política, condición, permiso o recurso no fijado, o si no puede
   mantener el mínimo privilegio de forma verificable.

La transición futura comienza únicamente cuando una autorización humana
posterior identifique esta enmienda fusionada y autorice preparar y revisar la
candidata nueva. Recibirá una revisión completa independiente de GPT-6 Astra,
razonamiento Alto, contexto nuevo y solo lectura; el autor podrá efectuar como
máximo dos correcciones concretas con revalidaciones enfocadas de la misma
Astra. Su presupuesto propio máximo será `5.00 EUR`, dentro del techo contractual
de `100.00 EUR`; F1 se adquirirá desde la primera futura invocación de Claude
Code atribuible a WP-018. Esta enmienda no autoriza esa invocación ni fija una
solución técnica.

No se puede copiar la candidata C2 como sustituto del replanteamiento. Sus
resultados cerrados son restricciones verificables y sus hashes son custodia,
no una nueva preimagen ejecutable. La autorización posterior deberá fijar la
base, el alcance material, la composición y las evidencias exactas antes de
abrir la transición.

### 11.5. Composición normativa mínima

Esta enmienda de instancia viaja en una composición atómica de exactamente
cuatro archivos; todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`.

La composición no contiene o modifica DEC-018, WP-018, WP-017, WP-016,
`ACTIVE`, `evidence/**`, código, pruebas, infraestructura, cuentas, identidades,
roles, secretos, permisos, Google Cloud, GitHub, workflows, ruleset, ramas,
worktrees o candidatas. Materialización, publicación, fusión y apertura de la
transición nueva son actos humanos posteriores y separados.

Fuentes primarias revalidadas el 2026-10-09:

- Pub/Sub, creación y modificación de push autenticado:
  https://docs.cloud.google.com/pubsub/docs/create-push-subscription
  https://docs.cloud.google.com/pubsub/docs/authenticate-push-subscriptions
- IAM, `actAs` y `roles/iam.serviceAccountUser`:
  https://docs.cloud.google.com/iam/docs/service-account-permissions
  https://docs.cloud.google.com/iam/docs/attach-service-accounts
- PAM, alcance de los entitlements y role bindings:
  https://docs.cloud.google.com/iam/docs/pam-create-entitlements
- Cloud Run, identidad de servicio y permisos para configurarla:
  https://docs.cloud.google.com/run/docs/configuring/services/service-identity
  https://docs.cloud.google.com/run/docs/configuring/services/containers

## 12. Enmienda de instancia del 2026-10-09 — decisión previa para aislar `actAs` en WP018-DOR-7

### 12.1. Hecho nuevo y por qué esta decisión es previa

La base normativa es `origin/main`
`bfed45ec92d53ac2a19272d91fa383963e89735f`. DEC-010 §11 cerró `blocked`
después de C2 la primera transición de `WP018-DOR-7` y autorizó únicamente
investigar una transición nueva. F2 sigue abierto; F1 y F3 a F7 permanecen
cerrados como resultados exigibles. WP-018 continúa `draft`, DOR-7 a DOR-9
abiertos y `ACTIVE` en reposo.

La rederivación desde documentación oficial vigente identifica una vía
potencial: una concesión PAM temporal a nivel de proyecto con role binding
condicionado por tag; el tag puede estar ligado directamente a una cuenta de
servicio y `iam.serviceAccounts.actAs` está soportado en roles personalizados.
Sin embargo, usar tags directamente sobre cuentas de servicio es una capacidad
Preview sujeta a términos Pre-GA. Además, tanto la referencia REST v1 como la
v1beta de PAM afirman que sus condiciones excluyen tags, mientras que la
documentación vigente de PAM, actualizada el 2026-10-06, afirma expresamente
que PAM admite condiciones basadas en tags y todos los atributos admitidos por
los bindings `allow`. Por esa contradicción oficial no se afirma todavía que la
vía sea técnicamente utilizable.

No cabe resolver esa dependencia ni esa divergencia documental como una
corrección técnica de F2. También hacen falta un tag, un rol personalizado, una
condición y un entitlement todavía no fijados. Por tanto, el primer acto es
esta decisión humana previa, sin nuevo identificador normativo ni modificación
del contrato. La transición nueva no comienza aquí.

### 12.2. Alternativas comparadas

**Binding directo permanente sobre la identidad push — rechazado.** Aunque
`roles/iam.serviceAccountUser` puede ligarse a una sola cuenta de servicio,
mantendría `actAs` efectivo fuera de la emergencia. Al combinarse con el
entitlement ordinario y `roles/run.developer`, permitiría usar
`run.services.update` para adjuntar esa identidad a una revisión de Cloud Run.

**PAM de proyecto sin condición — rechazado.** Haría temporal la concesión,
pero `actAs` alcanzaría también `alcance-fda-wp018-scheduler` y las demás
cuentas de servicio del proyecto.

**Condición por `resource.name` — rechazada.** La lista oficial de atributos de
recurso no acredita `resource.name` como filtro válido para
`iam.serviceAccounts.actAs`; un predicado no soportado no es un límite de
seguridad.

**Principal Access Boundary — rechazada.** Su frontera se expresa sobre
organización, carpeta o proyecto y no selecciona una cuenta de servicio dentro
del proyecto; además no sustituye el binding que concede `actAs`.

**Binding temporal añadido y retirado manualmente — rechazado.** Exigiría a los
operadores capacidad para mutar IAM durante cada emergencia, ampliaría la
superficie de recuperación y no aportaría el cierre automático de PAM.

**PAM condicionado por tag directo de cuenta de servicio — elegido con gates.**
Es la única opción oficial encontrada que combina activación temporal con un
predicado dirigido a la identidad objeto. Se acepta de forma expresa y
limitada la dependencia Pre-GA del tag de cuenta de servicio, pero no se da por
demostrada la compatibilidad efectiva de PAM hasta superar los gates de
§12.5. No existe fallback permisivo.

### 12.3. Recursos y política exactos que podrá usar la transición futura

La futura candidata nueva solo podrá proponer los siguientes elementos para
resolver F2; los valores generados se obtendrán de las APIs y nunca se
inventarán:

1. Tag key con nombre corto `wp018-emergency-actas`, parent
   `projects/${PROJECT_NUMBER}` y descripción limitada a aislar el `actAs` de
   emergencia de WP-018.
2. Tag value con nombre corto `push-only`, hijo de esa key.
3. Un único tag binding directo entre el `tagValues/${TAG_VALUE_ID}` obtenido y
   `//iam.googleapis.com/projects/${PROJECT_ID}/serviceAccounts/${PUSH_SA_UNIQUE_ID}`,
   donde `${PUSH_SA_UNIQUE_ID}` es el ID numérico devuelto para
   `alcance-fda-wp018-push`. El mismo tag no se liga al proyecto, carpeta,
   organización ni a otra cuenta de servicio.
4. Rol personalizado de proyecto
   `projects/${PROJECT_ID}/roles/alcanceFdaWp018EmergencyActAs`, con una sola
   permission incluida: `iam.serviceAccounts.actAs`. No incluye `getAccessToken`,
   `getOpenIdToken`, `signBlob`, `signJwt`, creación de claves, `setIamPolicy`,
   gestión de tags ni permisos de Cloud Run o Pub/Sub.
5. Un único entitlement PAM de proyecto
   `alcance-fda-wp018-emergency-push`, ubicación `global`, elegible solo para
   los dos humanos ya designados, justificación obligatoria, duración máxima y
   solicitada `1800s`, sin service accounts, grupos, dominios o identidades
   federadas elegibles. El mismo grant indivisible contiene tanto el role
   binding temporal que F1 ya exige para modificar la suscripción como el role
   binding de `actAs` de (6); no existe entitlement o grant independiente para
   uno de los dos permisos.
6. El segundo role binding del entitlement concede exclusivamente el rol de
   (4) mediante
   `conditionExpression` exacta
   `resource.matchTagId('tagKeys/${TAG_KEY_ID}', 'tagValues/${TAG_VALUE_ID}')`,
   usando los IDs permanentes devueltos, no nombres cortos o namespaced names.
7. La personalización de alcance queda deshabilitada: una solicitud no puede
   seleccionar solo uno de los bindings, acortar su conjunto o activar
   `actAs` sin el permiso temporal de F1. Si PAM no permite garantizar esa
   atomicidad para la versión concreta elegida, esta vía falla.

Crear, enlazar o conceder cualquiera de esos elementos sigue prohibido hasta
que WP-018 esté listo, aprobado, admitido y activo y exista una autorización
humana de implementación. Esta decisión no fija los IDs generados ni permite
simularlos. La futura IaC deberá capturarlos como outputs y fijar su relación
en evidencia saneada.

### 12.4. Composición de permisos y riesgo aceptado

La capacidad solo existe cuando el único grant PAM de emergencia de §12.3 está
`active`; sus dos bindings nacen y caducan juntos. El entitlement ordinario,
incluso si concede temporalmente `roles/run.developer`, no concede
`iam.serviceAccounts.actAs`; por sí solo no permite adjuntar ninguna de las
cuatro identidades de WP-018.

La combinación de `run.services.update` y `actAs` permitiría adjuntar la
identidad push a una revisión de Cloud Run. Esa revisión podría seguir
ejecutándose y obteniendo tokens de la identidad push después de caducar el
grant: retirar `actAs` no revierte una adjunción ya realizada. Por tanto no se
acepta el solapamiento. Antes de solicitar el grant de emergencia, cualquier
grant ordinario de los dos humanos debe estar retirado o expirado y los dos
deben carecer efectivamente de `run.services.create`, `run.services.update`,
`run.jobs.create`, `run.jobs.update`, `run.workerpools.create` y
`run.workerpools.update`. Esa negativa se vigila durante toda la emergencia.

Si aparece cualquiera de esos permisos, un grant ordinario simultáneo o una
mutación Cloud Run durante la ventana, la restauración se detiene y el estado
no vuelve a considerarse ordinario. Se revocan o terminan ambos grants, se
comparan servicios, jobs, worker pools y todas sus revisiones con la preimagen,
se restaura la identidad previa, se retira todo tráfico y se elimina toda
revisión eliminable que use push. Cualquier revisión restante, workload activo
o posible credencial residual mantiene la parada hasta su eliminación y hasta
que expire el máximo oficial de las credenciales potencialmente emitidas; si
ese máximo no puede acotarse sin secretos, se solicita decisión humana.

Fuera de un grant de emergencia activo, incluso aunque el entitlement ordinario
esté activo, ningún operador puede obtener `actAs` por esta política. El rol
personalizado no permite credenciales ni impersonación directa. Ninguna otra
asignación, rol básico, binding directo, herencia, tag o identidad puede actuar
como vía alternativa; si aparece, la transición se detiene.

### 12.5. Gates de contrato y oráculos posteriores fail-closed

La futura candidata puede cerrar F2 **contractualmente**, todavía sin recursos,
solo si una fuente oficial inequívoca resuelve la contradicción de PAM v1 y
v1beta para la versión exacta elegida, confirma tag conditions sobre el permiso
elegido y mantiene disponible el tag directo de service accounts. También debe
validar de forma local y sin aplicación la sintaxis completa de tag, rol,
entitlement, bindings y condición. Una prueba empírica aislada no corrige por sí
sola una contradicción oficial. Si cualquiera de estos gates documentales o de
definición falla, la candidata no es `APTO` y F2 continúa abierto.

Los oráculos siguientes son criterios de aceptación de la implementación y del
ensayo posteriores a que WP-018 esté `ready`, aprobado, admitido, activo y
expresamente autorizado. No son precondición circular para resolver la DoR ni
se ejecutan durante esta transición normativa:

1. **Inventario del tag:** exactamente un binding directo del valor elegido a
   la identidad push por unique ID; cero binding del mismo tag al proyecto o a
   las identidades scheduler, ingress y worker; cero valor heredado que haga
   coincidir la condición.
2. **Rol:** el rol personalizado contiene exactamente
   `iam.serviceAccounts.actAs`; cualquier permiso adicional falla.
3. **Acoplamiento:** una sola solicitud y un solo grant entregan o retiran a la
   vez el permiso temporal de F1 y `actAs`. La configuración no permite elegir
   bindings; no existe estado en que `actAs` esté efectivo y el permiso de
   modificar la suscripción no lo esté.
4. **Operación ordinaria negativa:** para cada uno de los dos humanos,
   con el grant ordinario activo y sin grant de emergencia,
   `projects.serviceAccounts.testIamPermissions` no devuelve `actAs` sobre
   push, scheduler, ingress ni worker.
5. **Emergencia positiva:** para cada humano, con el grant de emergencia
   activo, `testIamPermissions` devuelve `iam.serviceAccounts.actAs` sobre
   `alcance-fda-wp018-push` y el permiso temporal cerrado por F1 permite
   restaurar la suscripción push autenticada con esa cuenta, el endpoint y el
   audience ya gobernados.
6. **Emergencia negativa:** durante el mismo grant, `testIamPermissions` no
   devuelve `actAs` sobre scheduler, ingress, worker ni una quinta cuenta
   sintética `-denied`; tampoco aparecen permisos de token, firma o claves.
7. **Composición Cloud Run:** antes y durante la emergencia ambos humanos
   carecen de los seis permisos de creación o actualización enumerados en
   §12.4, no existe grant ordinario activo y los audit logs no contienen una
   mutación Cloud Run atribuible a ellos. La preimagen y postimagen de servicios,
   jobs, worker pools y revisiones conserva todas las identidades; cualquier
   diferencia activa el saneamiento y la parada de §12.4.
8. **Caducidad:** terminado, retirado o expirado el único grant, tanto el
   permiso de F1 como el oráculo positivo
   de push pasan a negativo tras la propagación oficial; hasta entonces se
   mantiene la parada y no se declara restaurada la operación ordinaria.
9. **Sin fallback:** eliminar o sustituir el tag, fallar la condición, cambiar
   el rol, no poder comprobar un oráculo o hallar una concesión paralela produce
   parada. Nunca se degrada a binding permanente, PAM sin condición o alcance
   de proyecto sin aislamiento.

`testIamPermissions` es un oráculo de evidencia y no una autorización de
aplicación. La futura transición deberá añadir preimagen, postimagen, delta,
grant, tiempos de propagación, audit logs y rollback sin valores secretos. Esta
decisión no ejecuta esos oráculos.

### 12.6. Efectos, límites y siguiente acto

1. Se acepta únicamente como base normativa la solución de §12.3, su riesgo
   temporal de §12.4 y sus gates de §12.5. No se crea ningún recurso ni se
   resuelve F2 o DOR-7.
2. F1 y F3 a F7 continúan cerrados; la futura transición no puede reabrirlos
   salvo regresión directa y demostrada de este mecanismo. DOR-8 y DOR-9
   permanecen abiertos.
3. La candidata C2 continúa preservada `NO APTO`. Sus bytes, diffs, ciclos y
   evidencias no son preimagen ni fuente de la transición nueva.
4. WP-018 permanece `draft`; WP-017, WP-016, `ACTIVE` y `evidence/**` no cambian.
   No se crea C3 o C4, `cost.md` o fila de ciclos.
5. Si se materializa y fusiona esta composición, el único siguiente acto
   posible será autorizar investigación en solo lectura y preparación externa
   desde cero de la nueva candidata `WP018-DOR-7`, limitada a F2 y a demostrar
   la no regresión de los resultados cerrados. Ese acto no queda autorizado
   aquí.
6. La transición futura conserva presupuesto propio máximo `5.00 EUR`, dentro
   del techo contractual de `100.00 EUR`, y `max_ciclos_correccion: 2`. F1 se
   adquiere desde la primera futura invocación de Claude Code atribuible a
   WP-018; esta decisión no autoriza invocarla.

### 12.7. Composición normativa mínima

Esta enmienda de instancia viaja en una composición atómica de exactamente
cuatro archivos; todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`.

La composición no contiene o modifica WP-018, WP-017, WP-016, `ACTIVE`,
`evidence/**`, código, pruebas, infraestructura, cuentas, identidades, roles,
tags, secretos, permisos, Google Cloud, GitHub, workflows, ruleset, ramas,
worktrees o candidatas. Materialización, publicación, fusión y apertura de la
transición nueva requieren actos humanos posteriores y separados.

Fuentes primarias revalidadas el 2026-10-09:

- PAM, alcance, condiciones y temporalidad, incluidas las dos referencias en
  conflicto:
  https://docs.cloud.google.com/iam/docs/pam-overview
  https://docs.cloud.google.com/iam/docs/pam-create-entitlements
  https://docs.cloud.google.com/iam/docs/pam-best-practices
  https://docs.cloud.google.com/iam/docs/reference/pam/rest/v1/PrivilegedAccess
  https://docs.cloud.google.com/iam/docs/reference/pam/rest/v1beta/PrivilegedAccess
- Tags directos de service accounts y su condición Pre-GA:
  https://docs.cloud.google.com/iam/docs/service-accounts-tags
  https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview
- Atributos de condición y `resource.matchTagId`:
  https://docs.cloud.google.com/iam/docs/conditions-attribute-reference
- `actAs`, roles personalizados y adjunción de identidades:
  https://docs.cloud.google.com/iam/docs/service-account-permissions
  https://cloud.google.com/iam/docs/custom-roles-permissions-support
  https://docs.cloud.google.com/iam/docs/attach-service-accounts
- Cloud Run, `roles/run.developer` y `run.services.update`:
  https://docs.cloud.google.com/run/docs/reference/iam/roles
  https://docs.cloud.google.com/run/docs/configuring/services/service-identity
  https://docs.cloud.google.com/run/docs/securing/service-identity
  https://docs.cloud.google.com/run/docs/managing/revisions
- Oráculo por cuenta de servicio:
  https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/testIamPermissions

## 13. Enmienda de instancia del 2026-10-09 — bloqueo documental de la transición nueva de WP018-DOR-7

### 13.1. Base, gate aplicable y hechos revalidados

La base normativa es `origin/main`
`72bae4acfffac30ce655ae6ecb8e6e5d7e747c9e`. DEC-010 §12 admite como única
vía potencial un grant PAM indivisible con un role binding condicionado por el
tag directo de `alcance-fda-wp018-push`, pero prohíbe cerrar F2 mientras una
fuente oficial inequívoca no resuelva la contradicción documental para una
versión concreta de PAM.

La revalidación oficial vigente no supera ese gate:

1. la referencia REST de PAM **v1**, tipo `PrivilegedAccess.RoleBinding`, dice
   que `conditionExpression` admite los atributos de IAM «except tags»;
2. la referencia REST de PAM **v1beta** contiene la misma exclusión;
3. la guía general de PAM, actualizada el 2026-10-06, afirma a la vez que PAM
   admite condiciones basadas en tags y todos los atributos admitidos por los
   role bindings `allow`;
4. la guía de creación de entitlements, también actualizada el 2026-10-06,
   permite añadir condiciones como en los bindings `allow`, y las prácticas
   recomendadas aconsejan usar condiciones por tag;
5. la documentación de IAM Conditions incluye los bindings administrados por
   PAM entre los bindings `allow` condicionables y reconoce tags como atributo;
6. el tag directo de cuentas de servicio continúa disponible, pero sigue en
   **Preview** bajo términos Pre-GA; su guía, actualizada el 2026-10-07, permite
   ligarlo por unique ID y usarlo con IAM Conditions.

Ninguna de esas fuentes declara que la exclusión de v1 o v1beta haya sido
retirada, que una versión concreta acepte tags pese a su contrato REST, ni que
la guía general prevalezca sobre ese contrato. Las notas oficiales de IAM no
publican una resolución específica de la divergencia. La mayor actualidad de
una guía no convierte dos contratos oficiales contradictorios en una garantía
inequívoca. Tampoco una prueba empírica aislada podría sustituir el gate
documental de §12.5.

### 13.2. Decisión: cierre `blocked` antes de candidata técnica

La transición nueva de `WP018-DOR-7` queda cerrada `blocked` antes de preparar
una candidata técnica, abrir ciclos o invocar al autor. No existe una candidata
`APTO`, una versión PAM elegible ni una condición tag que pueda incorporarse
al contrato de WP-018 con la certeza exigida.

- `WP018-DOR7-F2` permanece abierto y, por tanto, `WP018-DOR-7` permanece
  abierto.
- F1 y F3 a F7 continúan cerrados como resultados exigibles. No hay regresión:
  esta transición no acepta otro mecanismo, no propone cambio sobre sus
  restricciones y no reutiliza bytes, diffs, ciclos, hallazgos o evidencias de
  la candidata C2 ni de otra candidata histórica.
- DOR-8 y DOR-9 permanecen abiertos. WP-018 continúa `draft`; WP-017, WP-016 y
  `ACTIVE` permanecen intactos.
- No se crea `evidence/WP-018/cost.md`, fila de ciclo o artefacto F1. No hubo
  invocación de Claude Code atribuible a WP-018. El presupuesto propio máximo
  de `5.00 EUR` y `max_ciclos_correccion: 2` no se consumen ni reinician y
  siguen siendo límites de cualquier transición futura expresamente autorizada.

El dictamen `blocked` no afirma que los tags fallen en ejecución. Afirma algo
más limitado y falsable: hoy la documentación oficial no permite demostrar,
sin contradicción, que PAM v1 o v1beta los admita en `conditionExpression`.

### 13.3. Salida y siguiente decisión posible

No se reintenta esta misma vía mientras las referencias oficiales sigan
contradiciéndose. Solo una decisión humana posterior, nueva y separada, podrá:

1. autorizar una nueva investigación si Google publica una aclaración oficial
   inequívoca para una versión concreta; o
2. elegir previamente otro mecanismo que conserve mínimo privilegio,
   temporalidad, aislamiento de la identidad push y no solapamiento con los
   permisos de mutación de Cloud Run.

Ese acto futuro no queda preparado ni autorizado aquí. No se inventa otro
identificador, no se modifica WP-018, no se crea infraestructura y no se
configura Google Cloud o GitHub. La materialización y fusión de esta declaración
de bloqueo requerirán actos humanos posteriores y separados.

### 13.4. Composición normativa mínima

Esta enmienda viaja en una composición atómica de exactamente cuatro archivos;
todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`.

La composición no contiene o modifica WP-018, WP-017, WP-016, `ACTIVE`,
`evidence/**`, código, pruebas, infraestructura, cuentas, identidades, roles,
tags, secretos, permisos, Google Cloud, GitHub, workflows, ruleset, ramas,
worktrees o candidatas históricas. No crea ciclos, coste o una candidata
técnica.

Fuentes primarias revalidadas el 2026-10-09:

- guía y creación de PAM:
  https://docs.cloud.google.com/iam/docs/pam-overview
  https://docs.cloud.google.com/iam/docs/pam-create-entitlements
  https://docs.cloud.google.com/iam/docs/pam-best-practices
- contratos REST todavía incompatibles con tags:
  https://docs.cloud.google.com/iam/docs/reference/pam/rest/v1/PrivilegedAccess
  https://docs.cloud.google.com/iam/docs/reference/pam/rest/v1beta/PrivilegedAccess
- IAM Conditions y tags:
  https://docs.cloud.google.com/iam/docs/conditions-overview
  https://docs.cloud.google.com/iam/docs/tags-access-control
- tags directos de cuentas de servicio, Preview:
  https://docs.cloud.google.com/iam/docs/service-accounts-tags
- notas de versión de IAM:
  https://docs.cloud.google.com/iam/docs/release-notes

## 14. Enmienda de instancia del 2026-10-09 — decisión previa para sustituir PAM en WP018-DOR-7

### 14.1. Base, residual y hechos oficiales rederivados

La base normativa es `origin/main`
`0b2e63e6f5d26db493e3fbec84fa682f825317d7`. DEC-010 §13 cerró `blocked`
la transición basada en PAM antes de candidata técnica: las referencias REST
v1 y v1beta siguen excluyendo tags aunque las guías generales los admiten.
Esa misma combinación PAM más condición por tag permanece expresamente
excluida mientras continúe la contradicción. F2 y `WP018-DOR-7` siguen
abiertos; F1 y F3 a F7 permanecen cerrados; DOR-8 y DOR-9 siguen abiertos.

La rederivación desde documentación oficial vigente confirma:

1. quien crea o modifica una suscripción push autenticada debe tener
   `iam.serviceAccounts.actAs` sobre la cuenta de autenticación push, y esa
   cuenta debe pertenecer al mismo proyecto que la suscripción;
2. `pubsub.subscriptions.update` puede concederse sobre la suscripción
   individual, y `iam.serviceAccounts.actAs` puede concederse sobre la cuenta
   de servicio individual;
3. Workload Identity Federation permite a un workflow de GitHub Actions usar
   una identidad federada efímera y recibir acceso directo a recursos sin
   exportar una clave de cuenta de servicio;
4. el emisor OIDC de GitHub es compartido: Google exige una condición que
   restrinja la organización y recomienda identificadores numéricos para
   evitar reutilización de nombres; GitHub expone, entre otras, las claims
   `repository_owner_id`, `repository_id`, `environment`, `event_name`,
   `ref`, `workflow_ref`, `actor_id` y `run_id`;
5. un entorno de GitHub puede exigir revisores, impedir la autoaprobación,
   limitar ramas y desactivar el bypass de administradores; en un repositorio
   público esas reglas están disponibles en GitHub Team. Desactivar el bypass
   no elimina la capacidad de los propietarios de administrar, modificar o
   eliminar el propio entorno;
6. una identidad federada distinta de las identidades humanas no compone los
   permisos IAM de estas. Si a esa identidad no se le concede ningún permiso
   de Cloud Run, `roles/run.developer` o `run.services.update` que posea un
   humano no se suma a `actAs`.

La consulta oficial de GitHub realizada en solo lectura registra como
precondición, no como creación: repositorio público canónico
`FDA-Template/fda-template`, `repository_id: 1310040618`, organización
`FDA-Template`, `repository_owner_id: 340040486`, plan `team`, y exactamente
dos propietarios humanos visibles: `ivanes189` (`actor_id: 74557686`) y
`de-lean788` (`actor_id: 260103530`). La candidata técnica futura deberá
revalidar estos valores; cualquier diferencia produce parada.

### 14.2. Alternativas comparadas

**Reintentar PAM condicionado por tag — rechazado.** Es la misma vía cerrada
por §13. No se elige una fuente oficial conveniente ni se sustituye el gate
documental por una prueba empírica.

**Binding humano permanente — rechazado.** Aunque un binding directo sobre
`alcance-fda-wp018-push` aislaría el recurso, haría `actAs` efectivo durante
la operación ordinaria y podría componerse con permisos humanos de Cloud Run.

**Bindings humanos con `request.time` — rechazados.** La caducidad está
soportada, pero cada emergencia exigiría mutar por separado las políticas de
la suscripción y de la cuenta push. El custodio de `setIamPolicy` conservaría
capacidad para recrear el acceso, no habría concesión indivisible y la retirada
no eliminaría automáticamente bindings expirados.

**Grupo de Cloud Identity con membresía expirable — no elegido.** Podría
ligarse a la cuenta push y a la suscripción, pero la expiración requiere Cloud
Identity Premium o ediciones Enterprise compatibles, facturadas fuera del
proyecto Google Cloud. También exige dominio, administradores de grupo,
licencias, coste y custodia todavía no decididos. Un administrador que fuera
además beneficiario conservaría capacidad ordinaria de reactivación.

**Federación de identidades humanas o broker ejecutable — no elegidos.** La
primera exige un IdP humano, organización y gobierno de grupos no fijados. Un
broker en Cloud Run, Workflows o servicio equivalente añade runtime, identidad
de servicio e interfaz operativa, y desplaza el problema a quién puede
invocarlo. Ninguno es una corrección mínima del residual.

**GitHub Actions con entorno protegido y WIF directo — elegido como
arquitectura, no como candidata técnica.** Los dos humanos conservan la
decisión: uno inicia y el otro aprueba; la autoaprobación y el bypass se
deshabilitan. El actor que llama a Google Cloud es una identidad federada
efímera del job, no una cuenta humana ni una cuenta de servicio intermediaria.
Esa identidad recibe simultáneamente; las credenciales solo se emiten tras la
aprobación y conservan validez hasta su propia expiración,
`pubsub.subscriptions.update` sobre `alcance-fda-wp018-worker-push` e
`iam.serviceAccounts.actAs` sobre `alcance-fda-wp018-push`. No recibe permisos
sobre scheduler, ingress, worker, otras suscripciones, tokens, firma, claves,
IAM, Cloud Run ni ningún rol básico.

Esta elección introduce un workflow protegido, un entorno de GitHub, un pool
y proveedor WIF, dos roles mínimos y bindings sobre dos recursos. Ninguno está
fijado por el contrato actual. Por ello este acto se detiene en la decisión
humana previa: no prepara una candidata técnica, no enmienda WP-018 y no crea
ninguno de esos elementos.

### 14.3. Límites vinculantes para el acto técnico posterior

Una autorización humana posterior podrá preparar desde cero el primer acto
técnico solo si conserva acumulativamente estos límites:

1. **Identidad sin claves:** acceso WIF directo; queda prohibida una cuenta de
   servicio intermediaria, una clave JSON, un secreto cloud o credenciales
   persistentes. Si el acceso directo no está soportado inequívocamente por
   ambos recursos, se detiene y vuelve a decisión.
2. **Control dual auditable y frontera administrativa declarada:** solo
   `workflow_dispatch`; exactamente los dos humanos de §14.1 pueden iniciar o
   revisar; quien inicia no puede aprobar; basta la aprobación del otro porque
   GitHub solo exige un revisor; el bypass queda deshabilitado. Ambos son
   propietarios y pueden administrar el entorno: esta decisión acepta esa
   confianza administrativa y no presenta el mecanismo como barrera hermética
   frente a un propietario malicioso o unilateral. Antes de cada intento se
   captura la política e historia del entorno; modificación, eliminación,
   recreación o imposibilidad de acreditar la aprobación produce parada. Un
   modelo de amenaza más fuerte exige custodio o servicio separado y otra
   decisión humana previa.
3. **Procedencia cerrada:** repo y propietario por IDs numéricos de §14.1,
   evento `workflow_dispatch`, `ref` de `main`, entorno y `workflow_ref`
   exactos y `run_attempt == 1`. Nombres sin IDs, otra rama, fork, PR,
   reutilizable no fijado o claim ausente no obtienen credencial. Todo rerun
   queda prohibido, incluso si conserva SHA, ref, evento y privilegios del actor
   original; cada intento exige un `workflow_dispatch` y aprobación nuevos.
4. **Permisos acoplados:** el mismo principal federado y la misma ejecución
   obtienen los dos permisos o ninguno. Falla si `actAs` es efectivo sin
   `pubsub.subscriptions.update` o si se concede a una identidad humana. El fin
   o cancelación del job no equivale a revocar las credenciales ya emitidas.
5. **Cierre verificable de emergencia:** el estado ordinario no se reanuda al
   terminar, fallar o cancelar el job. Se impide nueva emisión para el intento;
   se registran, sin conservar el token, `iat`, `exp`, `jti`, intercambio y
   expiración; se espera hasta la expiración de la última credencial y se
   auditan llamadas posteriores. Emisión no acotada, credencial nueva o uso
   ambiguo mantienen la parada. Una credencial comprometida activa respuesta a
   incidente; no se declara revocada por haber terminado el job.
6. **Aislamiento de recursos:** positivo únicamente sobre la suscripción y la
   cuenta push exactas; negativo sobre scheduler, ingress, worker, una quinta
   cuenta `-denied`, otra suscripción y el proyecto. No hay binding heredado
   que amplíe el resultado.
7. **No composición con Cloud Run:** el principal WIF carece de
   `roles/run.developer`, `run.services.create`, `run.services.update`,
   `run.jobs.create`, `run.jobs.update`, `run.workerpools.create` y
   `run.workerpools.update`. Los permisos de las cuentas humanas no se usan
   para la llamada y no se les concede `actAs`.
8. **Workflow inmutable para la ejecución:** el acto posterior deberá fijar
   ruta, SHA de `main`, acciones por commit completo, permisos GitHub mínimos,
   runner hospedado, concurrencia uno, entrada cerrada sin parámetros capaces
   de elegir recursos y una sola operación de restauración idempotente. Un
   cambio del workflow invalida la preimagen y exige otra revisión.
9. **Fail-closed y evidencia:** preimagen de entorno, OIDC, WIF, roles,
   bindings y push config; aprobación con iniciador y revisor distintos;
   claims saneadas; `testIamPermissions` positivo y negativos; llamada y
   postimagen; caducidad del token; delta y rollback. Ausencia, ambigüedad,
   propagación pendiente o diferencia mantiene la parada.
10. **Rutas protegidas:** `.github/workflows/**`, el entorno y las políticas
   externas no se convierten en archivos implementables por WP-018. Cualquier
   futura composición deberá separar el contrato, el parche de operador y las
   mutaciones humanas, con autorizaciones independientes.

El acto posterior deberá revalidar además que el repositorio siga público y
que el plan mantenga las reglas utilizadas. No se aceptan custom deployment
protection rules en Preview ni GitHub secrets. El presupuesto propio máximo
continúa en `5.00 EUR`, `max_ciclos_correccion: 2`, y F1 se adquiere desde la
primera futura invocación de Claude Code atribuible a WP-018; esta decisión no
autoriza invocarla.

### 14.4. Estado y salida

1. Se elige únicamente la arquitectura federada de §14.2 y los límites de
   §14.3, incluida la frontera de confianza administrativa entre los dos
   propietarios. La decisión humana sobre introducir sus recursos se
   perfecciona solo mediante materialización y fusión humanas de esta
   composición.
2. F2 y `WP018-DOR-7` permanecen abiertos. F1 y F3 a F7 permanecen cerrados;
   la candidata posterior deberá demostrar su no regresión. DOR-8 y DOR-9
   permanecen abiertos.
3. WP-018 continúa `draft`; WP-017, WP-016, `ACTIVE`, `evidence/**` y las
   candidatas históricas permanecen intactos. No se crea otro WP-ID.
4. No se crea workflow, entorno, pool, proveedor, rol, binding, identidad,
   coste o ciclo; no se configura GitHub o Google Cloud y no se ejecuta
   Claude Code ni una prueba real.
5. El siguiente acto no queda autorizado. Si esta decisión se fusiona, hará
   falta otra autorización limitada a investigar y preparar externamente el
   acto técnico mínimo; cualquier incompatibilidad devuelve a decisión, sin
   fallback a PAM por tags, bindings humanos o credenciales persistentes.

### 14.5. Composición normativa mínima

Esta decisión previa viaja en una composición atómica de exactamente cuatro
archivos; todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`.

La composición no contiene o modifica WP-018, WP-017, WP-016, `ACTIVE`,
`evidence/**`, código, pruebas, workflows, infraestructura, cuentas,
identidades, roles, bindings, secretos, GitHub, Google Cloud, ramas, worktrees
o candidatas históricas.

Fuentes primarias revalidadas el 2026-10-09:

- Pub/Sub, push autenticado y acceso por suscripción:
  https://docs.cloud.google.com/pubsub/docs/create-push-subscription
  https://docs.cloud.google.com/pubsub/docs/authenticate-push-subscriptions
  https://docs.cloud.google.com/pubsub/docs/access-control
- IAM, acceso directo WIF y políticas de cuentas de servicio:
  https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines
  https://docs.cloud.google.com/iam/docs/workload-download-cred-and-grant-access
  https://docs.cloud.google.com/iam/docs/manage-access-service-accounts
  https://docs.cloud.google.com/iam/docs/service-account-permissions
  https://docs.cloud.google.com/docs/security/compromised-credentials
- GitHub OIDC, entornos y revisión dual:
  https://docs.github.com/en/actions/reference/security/oidc
  https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
  https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform
  https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
  https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
  https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization
- Alternativas temporales comparadas:
  https://docs.cloud.google.com/iam/docs/temporary-elevated-access
  https://docs.cloud.google.com/iam/docs/configuring-temporary-access
  https://docs.cloud.google.com/identity/docs/how-to/manage-expirations
  https://cloud.google.com/identity/pricing

## 15. Enmienda de instancia del 2026-10-09 — gate previo al workflow de WP018-DOR-7

### 15.1. Base y causa de parada

La base normativa es `origin/main`
`7221571d5c8718398dd71241aab68ffe3bd7e839`. La PR #75 materializó el acto
técnico mínimo de §14 únicamente como contrato y manual. F2 y
`WP018-DOR-7` siguen abiertos; F1 y F3 a F7 permanecen cerrados; DOR-8 y
DOR-9 siguen abiertos; WP-018 continúa `draft` y `ACTIVE` en reposo.

§14.3.10 y `docs/manual/08-productor-alcance-fda-wp018.md` ya separan el
workflow como parche de operador humano, fuera de los archivos implementables
por WP-018. No hace falta otra decisión por esa separación. Sí hace falta este
acto previo porque la revalidación oficial descubre tres gates que impiden
preparar ahora bytes exactos y fail-closed:

1. GitHub crea automáticamente un entorno inexistente cuando se ejecuta un
   workflow que lo referencia. El orden versionado «introducir workflow» antes
   de «configurar entorno» permite por tanto crear el objeto sin los revisores,
   `prevent_self_review`, política de rama y bloqueo de bypass exigidos.
2. La audiencia WIF y los principales federados requieren el número de proyecto
   y las URL de recursos requieren el ID de proyecto. El repositorio contiene
   solo `${PROJECT_NUMBER}` y `${PROJECT_ID}`; no acredita sus literales ni que
   el proyecto exclusivo exista. Una candidata exacta no puede inventarlos ni
   recibirlos mediante inputs, secrets o vars.
3. GitHub considera inmutable únicamente una acción fijada por SHA completo,
   pero el diseño no usa acciones. La etiqueta hospedada `ubuntu-24.04` recibe
   actualizaciones ordinarias y no fija una imagen concreta; `curl` y `jq`
   preinstalados también cambian. Presentarla como pin inmutable sería falso.

El fallo prevenido es ejecutar o aprobar una ceremonia sobre un entorno
auto-creado sin protección, identificadores conjeturados o un runtime descrito
como inmutable cuando no lo es. WIF deshabilitado y los bindings ausentes
reducen impacto, pero no corrigen esas precondiciones. El coste de mantenimiento
se limita a una preimagen humana y, si cambia la imagen antes de la ceremonia,
a una revisión enfocada nueva; no añade servicio permanente.

### 15.2. Decisión y orden fail-closed

Se detiene la candidata directa del workflow. La ceremonia se reordena así;
ningún paso autoriza el siguiente:

1. **Identidad de proyecto:** un acto humano separado crea o selecciona el
   proyecto exclusivo ya aprobado, comprueba su identidad, estado y pertenencia,
   y fija los literales `PROJECT_ID` y `PROJECT_NUMBER` y su correspondencia.
   Crear o vincular facturación requiere su autorización propia. `europe-west1`
   se conserva como restricción para los recursos regionales aplicables cuando
   se preparen; el recurso Project y el pool WIF global no reciben una región
   inventada. Solo se registran identificadores no secretos y lecturas saneadas;
   ausencia o discrepancia detiene el proceso.
2. **Entorno antes del workflow:** otro acto humano separado crea y verifica
   `wp018-dor7-emergency-push` antes de que exista el workflow en `main`, con
   exactamente `ivanes189` y `de-lean788` como revisores,
   `prevent_self_review: true`, política personalizada que admite únicamente la
   rama `main`, bypass administrativo deshabilitado y cero secrets o vars. Se
   capturan inexistencia o preimagen, postimagen, delta e historial. Un entorno
   preexistente no se adopta sin acreditar toda su historia y configuración.
3. **Bytes exactos:** solo con 1 y 2 conformes se prepara externamente el YAML
   completo con los dos literales, sin inputs, secrets, vars, `checkout`,
   acciones, reusable workflows o contenedores. La misma candidata fija el
   `ImageOS` y `ImageVersion` oficiales aceptados y falla antes de pedir OIDC si
   difieren. Registra además versiones de Bash, `curl` y `jq`; una diferencia no
   se corrige ni instala en runtime.
4. **Revisión y custodia:** los bytes exactos reciben una revisión completa
   independiente; correcciones, si existen, siguen DEC-010. SHA-256, diff,
   base, composición y revisión se fijan antes de materialización humana. La
   fusión humana produce `${WORKFLOW_SHA}`; cualquier cambio de bytes o base
   invalida la candidata.
5. **C0 sin privilegios:** solo después puede autorizarse crear fixtures,
   logging y pool/provider inicialmente deshabilitados, todavía sin roles ni
   bindings. Con la preimagen conforme se habilitan temporalmente para un único
   despacho C0, se obtiene e intercambia la credencial sin permisos, se
   deshabilitan, se espera su expiración y se audita. Cualquier permiso efectivo
   o intercambio adicional detiene y revierte; C0 no muta Pub/Sub.
6. **C1 privilegiado posterior:** únicamente tras cerrar C0 pueden instalarse,
   con pool/provider deshabilitados, los dos roles y bindings acoplados. Su
   preimagen, políticas y recursos negativos se verifican antes de habilitar.
   Un despacho C1 adquiere la credencial; ya con ella, los oráculos federados
   positivos y negativos pasan antes de la única mutación. Cierre, expiración,
   evidencia y rollback siguen el manual. C0 y C1 requieren autorizaciones
   humanas separadas y ninguno queda autorizado aquí.

La comprobación de `ImageVersion` no convierte el runner hospedado en artefacto
criptográficamente inmutable. Declara y acota la confianza en GitHub como
proveedor y hace fail-closed el drift observable. Si se exige una imagen
inmutable real, este diseño se detiene: contenedor por digest o runner propio
contradirían §14 y el manual y requieren otra decisión previa. No se relaja esa
frontera por conveniencia.

El workflow no se despacha tras fusionarse. Antes de C0 deben estar conformes
el entorno, los literales, `${WORKFLOW_SHA}`, la imagen aceptada, la condición
WIF, logging y la preimagen completa, y debe acreditarse la ausencia de ambos
bindings. Antes de C1 deben estar conformes ambos roles y bindings, las
políticas y la existencia de todos los recursos negativos; los oráculos que
requieren identidad federada se ejecutan después de obtener la credencial C1 y
antes de mutar. `run_attempt == 1` permanece tanto en YAML como en la condición
WIF; un rerun no obtiene credenciales.

### 15.3. Estado y siguiente acto

1. Este acto corrige únicamente el orden y las precondiciones. No prepara el
   workflow ni autoriza crear proyecto, facturación, entorno, WIF, recursos,
   roles, bindings, logging, costes o ciclos.
2. F2 y `WP018-DOR-7` permanecen abiertos; F1 y F3 a F7 siguen cerrados sin
   regresión; DOR-8 y DOR-9 permanecen abiertos; WP-018 continúa `draft`.
3. WP-017, WP-016, `ACTIVE`, `evidence/**` y todas las candidatas históricas
   permanecen intactos. No se reserva otro WP-ID.
4. Tras la fusión humana de esta composición, el único acto siguiente posible
   es investigar y preparar externamente la preimagen cerrada de los pasos 1 y
   2. Su materialización y cada mutación requieren autorizaciones separadas.

### 15.4. Composición normativa mínima

Esta decisión viaja en una composición atómica de exactamente cinco archivos;
todos o ninguno:

1. `specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md`;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`;
3. `docs/03-hoja-de-ruta.md`;
4. `docs/manual/05-bloqueos-y-parada.md`;
5. `docs/manual/08-productor-alcance-fda-wp018.md`.

No modifica WP-018, WP-017, WP-016, `ACTIVE`, `evidence/**`, workflows,
código, pruebas, infraestructura, GitHub, Google Cloud, cuentas, facturación,
identidades, roles, bindings, secretos, ramas, worktrees o candidatas
históricas.

Fuentes primarias revalidadas el 2026-10-09:

- workflow manual y rama predeterminada:
  https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
- creación y protección de entornos:
  https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
  https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
  https://docs.github.com/en/rest/deployments/environments
  https://docs.github.com/en/rest/deployments/branch-policies
- permisos, OIDC, claims y reruns:
  https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
  https://docs.github.com/en/actions/reference/security/oidc
  https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
- pins y runner hospedado:
  https://docs.github.com/en/actions/reference/security/secure-use
  https://github.com/actions/runner-images
  https://github.com/actions/runner-images/releases
- WIF, audiencia y principales directos:
  https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines
  https://docs.cloud.google.com/iam/docs/workload-identity-federation
  https://docs.cloud.google.com/iam/docs/best-practices-for-using-workload-identity-federation
  https://docs.cloud.google.com/iam/docs/reference/sts/rest/v1/TopLevel/token
