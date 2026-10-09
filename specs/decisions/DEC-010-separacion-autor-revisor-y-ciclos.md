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
