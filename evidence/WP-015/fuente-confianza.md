# WP-015 — Fuente de confianza y demostración de manipulación ineficaz

## C3 — configuración local de submódulo efectiva

`WP015-F2` quedó cerrado técnicamente sobre
`TESTED_HEAD=333eb072e62f3298f465c32c9d47a69b043cb8c1`. La prueba
`test_gitlink_violation_survives_local_config_ignore_all` usa un gitlink real y
crea, solo en el working tree del repositorio temporal, esta asociación:

```ini
[submodule "vendor"]
    path = vendor
```

No contiene `ignore`. El valor `submodule.vendor.ignore=all` se fija
exclusivamente en la configuración Git local del temporal. La prueba confirma
que esa configuración está realmente activa: para el mismo `base` y `head`,
`git diff -z --name-status -M -C --find-copies-harder` sin override devuelve
inventario vacío.

La CLI real, cuyo diff añade `--ignore-submodules=none`, devuelve exit `1` y
recupera `vendor` con motivo `fuera_de_permitidos`. Una sustitución temporal en
memoria de `_diff_records`, sin editar producción, ejecuta la misma entrada
`check_scope.main` retirando solo el override y obtiene exit `0` y cero
violaciones. Por tanto la regresión es sensible al override y fallaría si se
retirase de producción.

La ejecución real del comando 7 de C3 usó `origin/main...HEAD`, resolvió
`merge_base=7d1b26afcb3285e29ee17dee7548b34351948330`, leyó el contrato blob
`7f52be5a63a588d38f61b6e03e3d7ae48fd0447a` y terminó `OK` con cero
violaciones. La salida íntegra está en
`evidence/WP-015/verificacion-c3-literal.log`.

## Regla implementada

`scripts/check_scope.py` obtiene el `merge-base` mediante `git merge-base
<base> <head>` y localiza y lee el contrato **exclusivamente** mediante
objetos Git:

- `git ls-tree -r -z <merge-base> -- work-packages/` para localizar
  exactamente un blob `work-packages/WP-NNN-*.md` (`_find_contract`);
- `git cat-file blob <sha>` para leer su contenido (`_read_blob_text`).

No hay ninguna llamada a `open()` ni a ninguna API de lectura del
sistema de archivos en `scripts/check_scope.py` ni en `scripts/scope_rules.py`
(acreditado por `tests/scope/test_security_static.py`, en verde). El contrato
se parsea con `scope_rules.parse_contract(contract_text)`, donde `contract_text`
proviene únicamente del blob leído por Git.

## Ejecución real sobre WP-015

Comando 7 de `evidence/WP-015/verification.md`:

```
python3 scripts/check_scope.py WP-015 origin/main...HEAD
```

```
OK
{"base": "origin/main", "contrato": "work-packages/WP-015-check-scope-local.md", "contrato_blob": "7f52be5a63a588d38f61b6e03e3d7ae48fd0447a", "head": "HEAD", "merge_base": "30939377590a3c3b49ba705ef0f20c4832df61bd", "violaciones": [], "wp": "WP-015"}
```

- `merge-base` = `30939377590a3c3b49ba705ef0f20c4832df61bd` = base autorizada
  por el operador para esta sesión.
- `contrato` = `work-packages/WP-015-check-scope-local.md` (único candidato
  canónico en esa revisión).
- `contrato_blob` = `7f52be5a63a588d38f61b6e03e3d7ae48fd0447a`.

## Demostración de manipulación ineficaz del contrato propio (caso 8 de WP-002 / DEC-002)

Cubierta por `TestContractManipulationIgnored` en
`tests/scope/test_check_scope_cli.py`, sobre repositorios Git temporales
desechables:

1. `test_working_tree_contract_edit_has_no_effect` — tras confirmar ambos
   commits (`base`, `head`), se **amplía el contrato en el working tree, sin
   commit**, añadiendo `rogue/**` a los permitidos. Se invoca
   `check_scope.py` con el mismo rango `base...head`. El veredicto sigue
   siendo `VIOLACION` sobre `rogue/new.py`: la ampliación del working tree no
   tuvo ningún efecto, porque `git diff <base> <head>` nunca consulta el
   working tree y la biblioteca nunca lee el archivo del disco.
2. `test_working_tree_contract_removal_has_no_effect` — se **borra el
   contrato del working tree** (sin commit, sin `git rm`) tras confirmar
   `head`. El mismo rango produce el mismo veredicto (`VIOLACION` sobre
   `rogue/new.py`): retirar el archivo del disco no impide leerlo desde el
   blob del `merge-base`.
3. **`WP015-F6` (revisión Astra, C1)** —
   `test_head_committed_contract_expansion_has_no_effect` — la ampliación
   del contrato se **commitea de verdad** en un segundo commit de `head`
   (no solo en el working tree, a diferencia de las dos pruebas anteriores).
   `check_scope.py`, invocado con `base...head2`, sigue leyendo el contrato
   del `merge-base` (= `base`) y sigue señalando `rogue/new.py`: ni siquiera
   un commit real y completo de la ampliación, que forma parte legítima del
   árbol de `HEAD`, altera el veredicto, porque la fuente de confianza es
   `merge-base`, nunca `HEAD`.

Las tres pruebas están en verde (comando 6 de `verification.md`, 134/134).

## Garantías explícitas que el código respeta

- `HEAD`, `ACTIVE` y `specs/decisions/**` nunca son fuentes del contrato en
  tiempo de ejecución: `_find_contract` y `_read_blob_text` solo reciben
  `merge_base` como revisión.
- Cero, más de un contrato, nombre no canónico o blob con UTF-8 inválido
  son exit `2` (`select_contract`, `_read_blob_text`; probado en
  `TestExitTwo.test_contract_missing_is_exit_2`,
  `test_duplicate_contract_is_exit_2`, `test_noncanonical_contract_path_is_exit_2`
  y `TestPureParsers.test_select_contract_zero_matches`,
  `test_select_contract_two_matches`).
- No hay exenciones para `work-packages/**`: `scope_rules.evaluate` no
  distingue esa ruta de ninguna otra (`TestPrecedence.test_own_contract_has_no_exemption`).
