# WP-015 — Corpus: correspondencia caso por caso

Todas las pruebas citadas viven en `tests/scope/test_scope_rules.py` salvo que
se indique lo contrario. Ejecutadas y en verde en
`evidence/WP-015/verificacion-c1.log` comando 6 (134/134; las 95 originales
más 39 de C1).

## C1 — correcciones de la revisión Astra (`WP015-F1` a `WP015-F8`)

| Hallazgo | Prueba(s) |
|---|---|
| `WP015-F1` (LF elude `**`/`/`) | `TestDoubleStarAndDirSuffixConsumeLF` (7 unitarias, incluida `test_reproduccion_exacta_del_hallazgo`) + `test_double_star_forbidden_catches_lf_path_via_real_git`, `test_dir_suffix_forbidden_catches_lf_path_via_real_git`, `test_double_star_allowed_authorizes_lf_path_via_real_git` (CLI, Git real, en `test_check_scope_cli.py`) |
| `WP015-F2` (`.gitmodules`/config local oculta gitlink) | Corrección aplicada (`--ignore-submodules=none`); sin prueba de integración con submódulo real — deuda declarada en `verification.md` |
| `WP015-F3` (parsers Git aceptan salidas malformadas) | 15 pruebas en `TestPureParsers` (`test_check_scope_cli.py`): estado con cola arbitraria, puntuación R/C no numérica o vacía, NUL final ausente, rutas vacías, metadata de `ls-tree` inválida (modo/tipo/object id) |
| `WP015-F4` (separadores Unicode fragmentan el log) | Cubierto transversalmente: toda línea JSON de toda la batería de CLI pasa por `_emit_json` con `ensure_ascii=True`; ver `evidence/WP-015/seguridad.md` |
| `WP015-F5` (AST omite `os.path.realpath`/`io.open`/alias) | `TestAnalyzerNegativeSamples` (9 pruebas) en `test_security_static.py` |
| `WP015-F6` (cobertura declarada pero no demostrada) | `test_modified_symlink_target_changed_outside_allowed`, `test_renamed_symlink_target_now_escapes_root`, `test_symlink_target_invalid_utf8_is_exit_2`, `test_contract_blob_invalid_utf8_is_exit_2`, `test_head_committed_contract_expansion_has_no_effect` |
| `WP015-F7` (WP-ID admite dígitos Unicode) | `test_wp_id_with_unicode_digits_is_exit_2` |
| `WP015-F8` (falta manifiesto JSON) | `evidence/WP-015/manifiesto-tested-head-c1.json`, generado por `tests/scope/generate-evidence-hashes.sh` actualizado |

## Corpus previo (implementación inicial)

## DEC-002 §7 — las ocho filas vinculantes de traversal

| # | Ruta | ¿Traversal? | Prueba |
|---|---|---|---|
| 1 | `evidence/WP-002/notas..md` | no | `TestDec002TraversalTable.test_row1_notas_dotdot_md_no_traversal` |
| 2 | `evidence/WP-002/..hidden.md` | no | `TestDec002TraversalTable.test_row2_leading_dotdot_no_traversal` |
| 3 | `evidence/WP-002/bar..` | no | `TestDec002TraversalTable.test_row3_trailing_dotdot_no_traversal` |
| 4 | `evidence/WP-002/foo../bar` | no | `TestDec002TraversalTable.test_row4_foo_dotdot_slash_bar_no_traversal` |
| 5 | `..` | sí | `TestDec002TraversalTable.test_row5_bare_dotdot_is_traversal` |
| 6 | `../x` | sí | `TestDec002TraversalTable.test_row6_leading_component_dotdot_is_traversal` |
| 7 | `evidence/WP-002/../x` | sí | `TestDec002TraversalTable.test_row7_middle_component_dotdot_is_traversal` |
| 8 | `evidence/WP-002/..` | sí | `TestDec002TraversalTable.test_row8_trailing_component_dotdot_is_traversal` |

Cada fila comprueba `scope_rules.has_traversal` (la definición) **y**
`scope_rules.evaluate` (el efecto sobre el veredicto, con `allowed =
["evidence/WP-002/**"]`), reproduciendo ambas columnas de la tabla original.

**No-plegado del componente `..` (DEC-002 §3):**
`TestDec002TraversalTable.test_traversal_component_never_folds` verifica que
`evidence/WP-002/../WP-002/log.txt` se deniega con `motivo="traversal"` aunque
el plegado caería dentro de `evidence/WP-002/log.txt`, que sí está permitido.

## DEC-012 §6 — tabla cerrada de conformidad

| Entrada en la sección | Resultado ejecutable | Efecto sobre `docs/a.md` | Prueba |
|---|---|---|---|
| `- docs/(draft).md` | `docs/(draft).md` | no autoriza | `TestDec012Tabla6.test_parens_in_pattern_are_literal` |
| `- docs/file#v1` | `docs/file#v1` | no autoriza | `TestDec012Tabla6.test_hash_in_pattern_is_literal` |
| `` - `docs/**` `` | `` `docs/**` `` | no autoriza | `TestDec012Tabla6.test_backticks_are_literal_bytes` |
| `- docs/** # nota` | `docs/** # nota` | no autoriza | `TestDec012Tabla6.test_inline_comment_is_literal_in_allowed` |
| `- docs/** (manual)` | `docs/** (manual)` | no autoriza | `TestDec012Tabla6.test_inline_annotation_parens_is_literal` |
| `Nota: solo manuales` | ninguna entrada | no autoriza | `TestDec012Tabla6.test_pure_note_line_produces_no_entry` |
| `- docs/**` | `docs/**` | autoriza | `TestDec012Tabla6.test_plain_glob_authorizes` |
| `- ninguno` en prohibidos | lista vacía | no prohíbe | `TestDec012Tabla6.test_forbidden_ninguno_does_not_forbid` |
| `- -` en prohibidos | lista vacía | no prohíbe | `TestDec012Tabla6.test_forbidden_dash_does_not_forbid` |

**Caso de precedencia complementario** (permitidos `docs/**`, prohibidos
`docs/** # nota` autorizan `docs/a.md`): `TestDec012Tabla6.test_precedence_complementary_case`.

## DEC-012 § Transición — corpus de transición sin falso verde

| Caso | Prueba |
|---|---|
| Permitidos `- *`: solo cubre el nivel superior, no `docs/foo.md` | `TestTransitionCorpus.test_allowed_star_matches_only_top_level` |
| Prohibidos `- -`, ruta literal `-` permitida (el sentinela de contrato no es la ruta juzgada) | `TestTransitionCorpus.test_literal_dash_path_is_independent_of_sentinel` |
| `-` mezclado con un patrón en la misma sección es sentinela mezclado con patrones (malformado) | mismo test, primera mitad, vía `assertRaises(ContractError)` |
| U+000C final tras `docs/`: no se recorta, queda literal en el patrón | `TestTransitionCorpus.test_trailing_form_feed_is_not_stripped` |
| Whitespace Unicode ≠ U+0020/U+0009 (aquí U+00A0) al final: no se recorta | `TestTransitionCorpus.test_trailing_unicode_whitespace_is_not_stripped` |
| Espacio y tabulador ASCII sí se recortan en los extremos | `TestTransitionCorpus.test_ascii_space_and_tab_are_trimmed` |

## Gramática DEC-012 §1-4 — malformaciones que exigen exit 2

| Condición | Prueba |
|---|---|
| Sección permitida ausente | `TestParseContractGrammar.test_allowed_absent_header_is_error` |
| Sección prohibida ausente | `TestParseContractGrammar.test_forbidden_absent_header_is_error` |
| Sección permitida duplicada | `TestParseContractGrammar.test_duplicated_allowed_header_is_error` |
| Permitidos vacío (sentinela solo) | `TestParseContractGrammar.test_allowed_empty_is_error` |
| Entrada vacía tras el recorte (`-   `) | `TestParseContractGrammar.test_empty_entry_after_trim_is_error` |
| Marcador `-` sin separador (`-docs/**`) | `TestParseContractGrammar.test_malformed_marker_without_separator_is_error` |
| Marcador alternativo `*` | `TestParseContractGrammar.test_alternative_marker_asterisk_is_error` |
| Marcador alternativo `+` | `TestParseContractGrammar.test_alternative_marker_plus_is_error` |
| Sentinela mezclado con patrones (prohibidos) | `TestParseContractGrammar.test_sentinel_mixed_with_patterns_is_error` |
| Explicación sin marcador se ignora | `TestParseContractGrammar.test_explanation_line_without_marker_is_ignored` |
| Sentinelas `ninguno`/`none`/`n/a`/`-` en prohibidos | `test_forbidden_sentinel_ninguno`, `_none`, `_n_a`, `_dash` |
| `parse_contract` exige texto ya decodificado (contrato de tipos) | `TestParseContractGrammar.test_invalid_utf8_is_caller_responsibility` |

## Matching de globs, directorios y mayúsculas

| Caso | Prueba |
|---|---|
| `*` no cruza `/` | `TestGlobMatching.test_star_does_not_cross_slash` |
| `**` sí cruza `/` | `TestGlobMatching.test_double_star_crosses_slash` |
| `?` es un carácter distinto de `/` | `TestGlobMatching.test_question_mark_is_single_non_slash_char` |
| Sufijo `/` cubre todo el directorio | `TestGlobMatching.test_trailing_slash_covers_all_content` |
| Metacaracteres de regex son literales | `TestGlobMatching.test_literal_regex_metacharacters_are_not_special` |
| Comparación distingue mayúsculas | `TestGlobMatching.test_case_sensitive_matching` |

## Precedencia y ausencia de exenciones

| Caso | Prueba |
|---|---|
| Prohibido gana sobre permitido | `TestPrecedence.test_forbidden_wins_over_allowed` |
| Fuera de permitidos se deniega | `TestPrecedence.test_outside_allowed_is_denied` |
| Sin exención para `work-packages/**` (caso 8 de WP-002) | `TestPrecedence.test_own_contract_has_no_exemption` |

## Integración end-to-end (`tests/scope/test_check_scope_cli.py`)

| Estado del diff | Escenario | Prueba |
|---|---|---|
| `A` | archivo añadido fuera de permitidos | `TestExitOne.test_added_file_outside_allowed` |
| `M` | modificación con prohibido ganando | `TestExitOne.test_modified_forbidden_wins_over_allowed` |
| `D` | eliminación de ruta fuera de permitidos, juzgada igual | `TestExitOne.test_deleted_file_outside_allowed_is_still_judged` |
| `T` | cambio de tipo a symlink, destino fuera de permitidos | `TestExitOne.test_typechange_to_symlink_outside_allowed` |
| `R` | renombrado con destino fuera de permitidos | `TestExitOne.test_rename_destination_outside_allowed` |
| `C` | copia con destino fuera de permitidos (`--find-copies-harder`) | `TestExitOne.test_copy_destination_outside_allowed` |
| Nombres inusuales (espacios, paréntesis, `ñ`, acentos) | `TestExitOne.test_unusual_names_are_judged_correctly` |
| Todas las violaciones en una ejecución, orden estable | `TestExitOne.test_multiple_violations_in_one_execution_sorted` |
| Ruta con salto de línea embebido no forja otra línea de log | `TestExitOne.test_embedded_newline_does_not_forge_log_lines` |
| Los tres códigos exactos (`0`, `1`, `2`) | clases `TestExitZero`, `TestExitOne`, `TestExitTwo` completas |
| Contrato ausente / duplicado / no canónico | `TestExitTwo.test_contract_missing_is_exit_2`, `test_duplicate_contract_is_exit_2`, `test_noncanonical_contract_path_is_exit_2` |
| Contrato malformado (sección prohibida ausente) | `TestExitTwo.test_malformed_contract_missing_forbidden_header_is_exit_2` |
| WP-ID mal formado / rango inválido / extremo vacío / ref inexistente / argc incorrecto | `TestExitTwo.*` (seis pruebas) |
| Manipulación del contrato en el working tree (edición y borrado) sin efecto | `TestContractManipulationIgnored.*` (dos pruebas) |
| Estado de diff desconocido/no fusionado, registro truncado, diff vacío | `TestPureParsers.*` (parsers puros, sin git) |
| Selección de contrato: cero, uno, dos candidatos | `TestPureParsers.test_select_contract_*` |
