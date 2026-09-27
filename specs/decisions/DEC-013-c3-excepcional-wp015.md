# DEC-013 — Excepción mínima de C3 para WP-015

**Estado:** aceptada · **Fecha:** 2026-09-27 · **Ámbito:** habilitación previa,
acotada y no autoejecutable de un tercer y último ciclo de corrección de
WP-015; no inicia C3, no modifica su contrato ni autoriza PR o fusión

**Base normativa:** `origin/main` en
`30939377590a3c3b49ba705ef0f20c4832df61bd`.

**Candidata preservada:** rama `wp/WP-015-check-scope-local`, cabeza documental
`4ad9eb354e3ff13c0a936be6c8a0eee691e44246`, candidata C2
`935c3cbc6e366231aa2b69d919100a4178e9da34` y `TESTED_HEAD` C2
`a855c2f2505a0a1a92310d71218444d6a0987bff`.

## 1. Problema y hechos comprobados

WP-015 consumió C1 y C2 y quedó `NO APTO` con `2 / 2` ciclos. La revalidación
enfocada final de la misma Astra cerró `WP015-F3`, `WP015-F4` y `WP015-F6`;
la revisión previa ya había cerrado `WP015-F1`, `WP015-F5`, `WP015-F7` y
`WP015-F8`. El conjunto cerrado pendiente contiene solo `WP015-F2`.

No hay un defecto de producción abierto. `scripts/check_scope.py` fuerza
`git diff --ignore-submodules=none`, y la reproducción efectiva de Astra
confirmó que conserva `M vendor` frente a una configuración local que de otro
modo lo oculta. El defecto está en la prueba
`test_gitlink_violation_survives_local_config_ignore_all`: configura
`submodule.vendor.ignore=all`, pero el fixture no asocia ese nombre con la
ruta `vendor`. Sin una `.gitmodules` que contenga la asociación
`path = vendor`, Git no aplica el `ignore=all`; por eso la prueba permanece
verde aunque se retire el override de producción.

La candidata está limpia y preservada. La suite final registrada acredita
152/152 pruebas, 14/14 comprobaciones AST y los doce comandos contractuales en
verde. El coste acumulado registrado es `22.29 EUR`, clasificado como
`estimado` conforme a DEC-004 por la incompletitud histórica que declara el
expediente, y queda por debajo del máximo contractual de `40 EUR`. Esos verdes
no cierran F2 porque la regresión indicada no demuestra sensibilidad al
defecto.

## 2. Elección excepcional y proporcional

Se elige una excepción C3 mínima en vez de cerrar `blocked`, dividir o
replantear porque concurren conjuntamente estas condiciones:

1. queda un único hallazgo de prueba, exactamente reproducido y sin defecto de
   producción abierto;
2. la corrección técnica cabe en un solo método de prueba y no requiere cambiar
   contrato, producción, biblioteca, manual, decisiones ni `ACTIVE`; la
   materialización normativa previa sí exige la composición atómica de §9;
3. existe una negativa determinista: con la asociación activa y sin
   `--ignore-submodules=none`, el diff debe omitir `vendor`; con el ejecutable
   corregido, `vendor` debe reaparecer como violación;
4. dividir el trabajo produciría otro WP para corregir una sola precondición de
   fixture, sin reducir riesgo técnico ni normativo.

Esta excepción aplica DEC-010; no cambia su regla general, no reinicia la
cuenta y no crea precedente.

## 3. Autoridad concedida y momento de inicio

Una vez materializada y fusionada esta decisión en `main`, WP-015 pasa de
`2 / 2` a un techo excepcional de `2 / 3`. La decisión **habilita**, pero no
inicia, C3. Empezarlo exige una autorización humana posterior y separada que
identifique el commit de esta decisión ya fusionado y la cabeza preservada de
la candidata.

Antes de cualquier corrección del autor, la fila C3 de
`evidence/WP-015/ciclos.md` debe quedar versionada en la rama candidata con:
origen, `WP015-F2`, fecha, estado `abierto`, presupuesto de esta sección y el
commit de DEC-013 ya vigente. Sin ese commit previo, C3 no comienza.

La actualización de la rama candidata frente al `main` que contenga DEC-013
deberá preservar los commits existentes y no podrá reescribir historia. El
método y los SHA exactos deberán formar parte de la autorización posterior;
esta decisión no ejecuta ni autoriza por sí sola ninguna operación Git.

Claude Code continúa como único autor y corrector. La misma Astra que emitió la
revalidación enfocada final de C2 realizará una única revalidación enfocada de
F2 y de los efectos de su corrección. No se abre otra revisión general.

## 4. Hallazgo y cambio técnico autorizable

### Conjunto cerrado

El único hallazgo tratable es `WP015-F2`, y solo su residual final:

> La variante de configuración local no activa realmente
> `submodule.vendor.ignore=all` porque falta asociar el nombre `vendor` con la
> ruta `vendor` mediante `.gitmodules`.

`WP015-F1` y `WP015-F3` a `WP015-F8` permanecen cerrados y no pueden usarse
para justificar cambios.

### Único archivo técnico

Solo puede modificarse:

- `tests/scope/test_check_scope_cli.py`

El cambio queda limitado al fixture y a las aserciones de
`test_gitlink_violation_survives_local_config_ignore_all`:

1. crear en el repositorio temporal una `.gitmodules` **no versionada** con
   exactamente la asociación semántica:

   ```ini
   [submodule "vendor"]
       path = vendor
   ```

2. mantener `submodule.vendor.ignore=all` exclusivamente en la configuración
   Git local del repositorio temporal; `.gitmodules` no puede contener
   `ignore = all` en este caso;
3. demostrar la negativa: con esa asociación y configuración, el mismo diff
   sin el override `--ignore-submodules=none` omite `vendor`;
4. demostrar el positivo por la CLI real: para el mismo `base`, `head` e
   inventario, `scripts/check_scope.py` termina con exit `1` e informa
   `vendor` como `fuera_de_permitidos`;
5. comprobar por prueba de mutación o equivalencia explícita que retirar el
   override de la llamada de producción hace fallar esta regresión.

No se autoriza refactor, limpieza, cambio de comentarios ajenos, nuevas
abstracciones ni corrección oportunista.

## 5. Evidencias autorizables y verificación

Además del único archivo técnico, C3 solo puede crear o actualizar estas rutas
de evidencia:

- `evidence/WP-015/ciclos.md`
- `evidence/WP-015/verification.md`
- `evidence/WP-015/verificacion-c3-literal.log`
- `evidence/WP-015/manifiesto-tested-head-c3.json`
- `evidence/WP-015/fuente-confianza.md`
- `evidence/WP-015/aislamiento.md`
- `evidence/WP-015/revision-astra.md`
- `evidence/WP-015/cost.md`
- `evidence/WP-015/cost-f1.json`

Las secciones históricas de C1 y C2 y sus logs y manifiestos son inmutables.
La evidencia C3 debe identificar un nuevo `TESTED_HEAD`, árbol, merge-base y
manifiesto, registrar el control negativo y el positivo de F2, y acreditar que
la candidata no cambió fuera de las rutas anteriores.

Se ejecutan de nuevo, literalmente y en orden, los doce comandos de
`## Verificación` del contrato vigente. El verde general es necesario pero no
suficiente: la revalidación enfocada debe comprobar también la sensibilidad de
la regresión al retirar `--ignore-submodules=none`. No se ejecuta red ni se
modifica CI, ruleset o configuración real.

## 6. Presupuesto y techo final

- **Presupuesto adicional máximo de C3:** `6.00 EUR`.
- **Coste acumulado de partida:** `22.29 EUR`, estado `estimado` conforme a
  DEC-004.
- **Techo final acumulado de WP-015:** `28.29 EUR`.

El techo de esta decisión es más estricto que el máximo contractual de
`40 EUR` y no lo modifica. El coste se registra con el mismo instrumento y
tipo de cambio ya gobernados por el expediente. Una captura completa de C3 no
convierte en `medido` el agregado mientras persista la causa histórica que lo
clasifica como `estimado`. Si la pasada alcanza `6.00 EUR`, si no puede medirse
conforme a las decisiones vigentes o si el acumulado supera `28.29 EUR`, se
detiene sin iniciar otra invocación de autor.

## 7. Cierre y parada

C3 es una sola pasada final del autor. Después:

- si la misma Astra cierra F2 y no aparece un efecto adverso, el candidato
  puede declararse `APTO` para una autorización humana posterior de PR;
- si F2 sigue abierto, aparece otro hallazgo, se necesita otra ruta o se agota
  el presupuesto, WP-015 se preserva y se detiene para cierre `blocked` o nueva
  decisión humana;
- no existe C4, corrección adicional ni ampliación implícita.

Esta decisión no autoriza crear la PR de WP-015, fusionarla, marcar el contrato
`done`, retirar WP-015 de `ACTIVE` ni cerrar la pausa.

## 8. Compatibilidad normativa

- **DEC-003:** mantiene la pausa y no altera `ACTIVE`; el trabajo continúa en
  el WP ya admitido y activo, sin introducir otro WP. DEC-013 se admite
  modificando directamente su lista cerrada en la misma composición atómica;
  no se autoautoriza.
- **DEC-011:** conserva el orden “juez local primero” y no atribuye todavía CI,
  ruleset ni prueba real de fábrica.
- **DEC-012:** no altera la gramática; la prueba sigue juzgando el contrato
  versionado con sus patrones literales.
- **DEC-010:** identifica WP, conjunto cerrado, alcance exacto, presupuesto
  adicional y techo final; preserva autor/revisor, cuenta C3 y parada sin C4.

## 9. Composición normativa y actos no autorizados

La materialización normativa es atómica y consta exactamente de tres archivos;
viajan juntos o ninguno:

1. `specs/decisions/DEC-013-c3-excepcional-wp015.md`, con el texto íntegro de
   esta decisión;
2. `specs/decisions/DEC-003-pausa-migracion-y-contencion.md`, limitado a:
   añadir en la cabecera la enmienda fechada del 2026-09-27; incorporar en §4
   una fila `DEC-013` que describa esta excepción C3 mínima y no autoejecutable;
   añadir el párrafo de admisión atómica que fija estos tres archivos y niega
   autoautorización, C3 inmediato, C4, cambio de contrato o cambio de `ACTIVE`;
   y añadir DEC-013 a sus referencias;
3. `docs/manual/05-bloqueos-y-parada.md`, limitado a añadir al final de
   «Tercer ciclo de corrección» una nota de instancia que enlace DEC-013 y deje
   inequívoco que, solo para WP-015, el techo pasa de `2 / 2` a `2 / 3` una vez
   fusionada la composición, pero C3 no empieza sin otra autorización y su
   fila previa versionada. La regla general de dos ciclos, la salida ordinaria
   tras C2 y la prohibición de C4 no cambian.

La enmienda de DEC-003 evita circularidad: una decisión ausente de la lista
cerrada no puede admitirse a sí misma. La nota del manual refleja la transición
operativa concreta sin convertirla en regla general. Ninguna otra sección o
ruta puede cambiar.

La materialización, commit, PR y fusión de esta composición requieren
autorizaciones humanas posteriores y separadas. Hasta que los tres archivos
estén fusionados y exista otra autorización expresa de inicio, quedan
prohibidos C3, cualquier cambio de código o evidencia, cualquier operación
sobre la rama candidata y cualquier modificación del contrato o de `ACTIVE`.
