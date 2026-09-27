# WP-015 — Verificación

Implementación inicial (no C1 ni C2). Autor único: Claude Code (implementer).

**Los doce comandos de `## Verificación` se ejecutaron literalmente, en el
orden exacto del contrato, con
`HEAD=4876e8be85f615cac92e63c7a58be47c0b1b8b87`.** Ese commit es posterior a
`TESTED_HEAD` y solo añade `evidence/WP-015/**`; las rutas de código, pruebas y
manual eran idénticas bit a bit a `TESTED_HEAD`, como acredita el diff cero
de abajo. La salida íntegra y el código de salida de cada comando están, sin
editar, en `evidence/WP-015/verificacion.log`. Este archivo resume y referencia
esa transcripción; donde ambos difieran en la letra, prevalece el `.log`.

## Identidad de `TESTED_HEAD`

| Campo | Valor |
|---|---|
| Rama | `wp/WP-015-check-scope-local` |
| Base autorizada | `30939377590a3c3b49ba705ef0f20c4832df61bd` (`origin/main`) |
| `TESTED_HEAD` | `718ce294fe592c2b6df7c13c5f56caea4199d7f2` |
| Árbol de `TESTED_HEAD` | `c0f6d7cba2ea9f3ce31a57050b3f441d92e7b7f0` |
| `merge-base(origin/main, TESTED_HEAD)` | `30939377590a3c3b49ba705ef0f20c4832df61bd` (= base autorizada) |

`TESTED_HEAD` consta de dos commits atómicos sobre la base autorizada:

1. `8830028e61b773354fd92c7a8305727f203c4c42` — código, pruebas y manual.
2. `718ce294fe592c2b6df7c13c5f56caea4199d7f2` — `tests/scope/generate-evidence-hashes.sh`,
   utilidad de evidencia dentro de `tests/scope/**` (ruta probada), usada para
   producir el manifiesto de esta misma tabla. Ambos commits están dentro del
   alcance probado; no hay ningún commit "solo de evidencia" con contenido en
   rutas de código todavía.

Antes de generar esta evidencia, el árbol de trabajo coincide exactamente con
`TESTED_HEAD` en las cinco rutas permitidas: sin cambios `staged`, `unstaged`
ni archivos sin seguimiento.

**Commit de evidencia previo, ya versionado.**
`4876e8be85f615cac92e63c7a58be47c0b1b8b87` — "WP-015: registrar evidencias de
la implementación inicial" — añadió `evidence/WP-015/**` (verification.md,
corpus.md, fuente-confianza.md, symlinks.md, aislamiento.md, seguridad.md,
ciclos.md, cost.md, revision-astra.md) sin tocar ninguna ruta probada. Su
diff contra `TESTED_HEAD` en las rutas probadas es cero:

```bash
$ git diff --exit-code 718ce294fe592c2b6df7c13c5f56caea4199d7f2 -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md
[exit_code=0, salida vacía]
```

Esta consolidación (la presente pasada) añade únicamente
`evidence/WP-015/verificacion.log` y corrige el texto de `verification.md` y
`seguridad.md`; el mismo comando, ejecutado sobre el commit que la cierra,
sigue devolviendo exit `0` con salida vacía (ver «Verificación de esta
consolidación» al final de este archivo). Ningún commit posterior a
`TESTED_HEAD` toca código, pruebas ni manual.

## Manifiesto de identidad (ruta, modo, blob Git, SHA-256)

Generado con `bash tests/scope/generate-evidence-hashes.sh` (solo lectura,
`git ls-tree` + `shasum -a 256`) contra `TESTED_HEAD`:

| Ruta | Modo | Blob Git (SHA-1) | SHA-256 del contenido |
|---|---|---|---|
| `scripts/check_scope.py` | `100644` | `ab94ac25b9f90293879ebed28ba58a8b99c77d3f` | `4c6aa2651600100c90328f3d8b19ec759549f3c03631c444cfc4423b5b906005` |
| `scripts/scope_rules.py` | `100644` | `19d425611f1c15c33111db0448261a7dad0c38ad` | `382cbedd9d12179a04f842fabbb2581f9441179c02f5485249b1fb4fcdc2ad78` |
| `tests/scope/_repo.py` | `100644` | `a7a14cdde8937530eb58c4aec9019d020b90ecd3` | `e5951767e152732c18e8f10233cec89e2dfd97a0de44cc61f10a863dbc51e9dd` |
| `tests/scope/run-suite.sh` | `100644` | `17f0ca836cd6b93b694894c53721a09e03dbd93c` | `66afe7375d18466fc2ce0cf9f48465cf6de7b32f82f1697dfb235fb53fbd3201` |
| `tests/scope/test_check_scope_cli.py` | `100644` | `bd2b7b76235c08af5449740f1e8ae82cde026a5b` | `95fd2b93801b34c3ca37a69d375b84456a6a5b16848630b3c5b085bac3411196` |
| `tests/scope/test_scope_rules.py` | `100644` | `ef90adc983c0a30d1569e31989a54281ea73c37b` | `b8ea5e0b46a6c98337a68281bdc46bc38b3025389dcd5e8380f4dc660b1d8b95` |
| `tests/scope/test_security_static.py` | `100644` | `f86d21bc9d6403e3e780b56ac5ddf59835922e60` | `9843460f482f9bd0557bc950a65194b707b4892867849e1418938e86a7f02a50` |
| `tests/scope/generate-evidence-hashes.sh` | `100644` | `9b0360406512594e45b330135a5f7f50aff506b1` | `66596effc2433d2745fc2518be5afc693da117a41a1eb0e2834daa6b878d7b75` |
| `docs/manual/02-ciclo-de-un-wp.md` | `100644` | `81d0f9ba84c60c8087d0cdb1241c0c85f885eac4` | `dc54cd96e996ef8f92f0f364517137a2731c18ced13d3dc9ba66873f6372a18a` |

**Nota sobre el bit ejecutable.** `chmod` y `git update-index --chmod` están
denegados por el permiso de herramienta de esta sesión (sin superficie de
aprobación). `tests/scope/run-suite.sh` y `tests/scope/generate-evidence-hashes.sh`
quedan con modo `100644` (no `100755`), a diferencia de `tests/guard/run-suite.sh`
(`100755`). No afecta a ninguna verificación: todas se invocan explícitamente
como `bash <script>`, nunca como `./<script>`. Deuda declarada — ver resumen
final.

**Prueba de identidad frente al head presentado.** El head presentado es el
`HEAD` actual de `wp/WP-015-check-scope-local`. Es posterior a `TESTED_HEAD` y
sus commits posteriores modifican exclusivamente `evidence/WP-015/**`. Antes
de esta actualización quedaron identificados los commits de evidencia
`4876e8be85f615cac92e63c7a58be47c0b1b8b87`,
`acaaf340236da84fc91b2890de48f101c781490d` y
`dd5b8abf99ea88de7a9df0980f9cf26a0537e955`; este propio archivo vuelve a
registrar la comprobación sin intentar incluir recursivamente el SHA del commit
que lo contiene. La identidad de las rutas probadas frente a `TESTED_HEAD` se
demuestra mediante:

```bash
git diff --exit-code 718ce294fe592c2b6df7c13c5f56caea4199d7f2 -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md
```

## Comandos de verificación, salida y código de salida

Todos ejecutados desde la raíz del repositorio con
`HEAD=4876e8be85f615cac92e63c7a58be47c0b1b8b87`, cuyas rutas probadas eran
idénticas a `TESTED_HEAD`.

### 1. `git diff --exit-code HEAD -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md`

Salida: vacía. Exit: `0`.

### 2. `git diff --cached --exit-code HEAD -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md`

Salida: vacía. Exit: `0`.

### 3. Comprobación de archivos sin seguimiento en las rutas probadas (forma literal del contrato)

```bash
bash -o pipefail -c 'git ls-files --others --exclude-standard -z -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md | python3 -c "import sys; raise SystemExit(bool(sys.stdin.buffer.read()))"'
```

Ejecutado en su forma literal exacta del contrato, con acceso operativo más
amplio que el de la sesión de implementación inicial. Exit: `0`. Salida
íntegra registrada en `evidence/WP-015/verificacion.log` (líneas 13-15):
vacía salvo el marcador `[exit_code=0]`. Cero archivos sin seguimiento en las
rutas probadas.

### 4. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scope -p 'test_*.py'`

Ejecutado en su forma literal exacta del contrato. Exit: `0`. Salida íntegra
registrada en `evidence/WP-015/verificacion.log` (líneas 17-24):

```
...............................................................................................
----------------------------------------------------------------------
Ran 95 tests in 6.461s

OK
```

**95/95 pruebas en verde**, incluidas las de `test_security_static.py`.
Coincide con el resultado ya obtenido por la vía anidada dentro de
`bash tests/scope/run-suite.sh` (comando 6).

### 5. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scope -p 'test_security_static.py'`

Ejecutado en su forma literal exacta del contrato. Exit: `0`. Salida íntegra
registrada en `evidence/WP-015/verificacion.log` (líneas 26-33):

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.014s

OK
```

Las cuatro pruebas: `test_check_scope_has_no_forbidden_apis`,
`test_check_scope_parses_as_valid_python`,
`test_scope_rules_has_no_forbidden_apis`,
`test_scope_rules_parses_as_valid_python`.

### 6. `bash tests/scope/run-suite.sh`

Exit: `0`. Salida íntegra (95 pruebas, aislamiento acreditado):

```
============================================================
 WP-015 — suite de scripts/check_scope.py y scripts/scope_rules.py
============================================================

--- HEAD antes: 718ce294fe592c2b6df7c13c5f56caea4199d7f2 ---
test_working_tree_contract_edit_has_no_effect (test_check_scope_cli.TestContractManipulationIgnored.test_working_tree_contract_edit_has_no_effect) ... ok
test_working_tree_contract_removal_has_no_effect (test_check_scope_cli.TestContractManipulationIgnored.test_working_tree_contract_removal_has_no_effect) ... ok
test_added_file_outside_allowed (test_check_scope_cli.TestExitOne.test_added_file_outside_allowed) ... ok
test_copy_destination_outside_allowed (test_check_scope_cli.TestExitOne.test_copy_destination_outside_allowed) ... ok
test_deleted_file_outside_allowed_is_still_judged (test_check_scope_cli.TestExitOne.test_deleted_file_outside_allowed_is_still_judged) ... ok
test_deleted_symlink_target_judged_from_merge_base (test_check_scope_cli.TestExitOne.test_deleted_symlink_target_judged_from_merge_base) ... ok
test_embedded_newline_does_not_forge_log_lines (test_check_scope_cli.TestExitOne.test_embedded_newline_does_not_forge_log_lines) ... ok
test_modified_forbidden_wins_over_allowed (test_check_scope_cli.TestExitOne.test_modified_forbidden_wins_over_allowed) ... ok
test_multiple_violations_in_one_execution_sorted (test_check_scope_cli.TestExitOne.test_multiple_violations_in_one_execution_sorted) ... ok
test_rename_destination_outside_allowed (test_check_scope_cli.TestExitOne.test_rename_destination_outside_allowed) ... ok
test_symlink_absolute_target_is_violation (test_check_scope_cli.TestExitOne.test_symlink_absolute_target_is_violation) ... ok
test_symlink_escaping_root_is_violation (test_check_scope_cli.TestExitOne.test_symlink_escaping_root_is_violation) ... ok
test_symlink_pointing_inside_allowed_is_ok (test_check_scope_cli.TestExitOne.test_symlink_pointing_inside_allowed_is_ok) ... ok
test_typechange_to_symlink_outside_allowed (test_check_scope_cli.TestExitOne.test_typechange_to_symlink_outside_allowed) ... ok
test_unusual_names_are_judged_correctly (test_check_scope_cli.TestExitOne.test_unusual_names_are_judged_correctly) ... ok
test_contract_missing_is_exit_2 (test_check_scope_cli.TestExitTwo.test_contract_missing_is_exit_2) ... ok
test_duplicate_contract_is_exit_2 (test_check_scope_cli.TestExitTwo.test_duplicate_contract_is_exit_2) ... ok
test_invalid_wp_id_format_is_exit_2 (test_check_scope_cli.TestExitTwo.test_invalid_wp_id_format_is_exit_2) ... ok
test_malformed_contract_missing_forbidden_header_is_exit_2 (test_check_scope_cli.TestExitTwo.test_malformed_contract_missing_forbidden_header_is_exit_2) ... ok
test_noncanonical_contract_path_is_exit_2 (test_check_scope_cli.TestExitTwo.test_noncanonical_contract_path_is_exit_2) ... ok
test_range_with_empty_extreme_is_exit_2 (test_check_scope_cli.TestExitTwo.test_range_with_empty_extreme_is_exit_2) ... ok
test_range_without_triple_dot_is_exit_2 (test_check_scope_cli.TestExitTwo.test_range_without_triple_dot_is_exit_2) ... ok
test_unknown_ref_is_exit_2 (test_check_scope_cli.TestExitTwo.test_unknown_ref_is_exit_2) ... ok
test_wrong_argument_count_is_exit_2 (test_check_scope_cli.TestExitTwo.test_wrong_argument_count_is_exit_2) ... ok
test_ok_zero_violations (test_check_scope_cli.TestExitZero.test_ok_zero_violations) ... ok
test_empty_diff_is_no_records (test_check_scope_cli.TestPureParsers.test_empty_diff_is_no_records) ... ok
test_rename_record_consumes_two_paths (test_check_scope_cli.TestPureParsers.test_rename_record_consumes_two_paths) ... ok
test_select_contract_single_match (test_check_scope_cli.TestPureParsers.test_select_contract_single_match) ... ok
test_select_contract_two_matches (test_check_scope_cli.TestPureParsers.test_select_contract_two_matches) ... ok
test_select_contract_zero_matches (test_check_scope_cli.TestPureParsers.test_select_contract_zero_matches) ... ok
test_truncated_record_is_error (test_check_scope_cli.TestPureParsers.test_truncated_record_is_error) ... ok
test_unknown_status_letter_is_error (test_check_scope_cli.TestPureParsers.test_unknown_status_letter_is_error) ... ok
test_row1_notas_dotdot_md_no_traversal (test_scope_rules.TestDec002TraversalTable.test_row1_notas_dotdot_md_no_traversal) ... ok
test_row2_leading_dotdot_no_traversal (test_scope_rules.TestDec002TraversalTable.test_row2_leading_dotdot_no_traversal) ... ok
test_row3_trailing_dotdot_no_traversal (test_scope_rules.TestDec002TraversalTable.test_row3_trailing_dotdot_no_traversal) ... ok
test_row4_foo_dotdot_slash_bar_no_traversal (test_scope_rules.TestDec002TraversalTable.test_row4_foo_dotdot_slash_bar_no_traversal) ... ok
test_row5_bare_dotdot_is_traversal (test_scope_rules.TestDec002TraversalTable.test_row5_bare_dotdot_is_traversal) ... ok
test_row6_leading_component_dotdot_is_traversal (test_scope_rules.TestDec002TraversalTable.test_row6_leading_component_dotdot_is_traversal) ... ok
test_row7_middle_component_dotdot_is_traversal (test_scope_rules.TestDec002TraversalTable.test_row7_middle_component_dotdot_is_traversal) ... ok
test_row8_trailing_component_dotdot_is_traversal (test_scope_rules.TestDec002TraversalTable.test_row8_trailing_component_dotdot_is_traversal) ... ok
test_traversal_component_never_folds (test_scope_rules.TestDec002TraversalTable.test_traversal_component_never_folds) ... ok
test_backticks_are_literal_bytes (test_scope_rules.TestDec012Tabla6.test_backticks_are_literal_bytes) ... ok
test_forbidden_dash_does_not_forbid (test_scope_rules.TestDec012Tabla6.test_forbidden_dash_does_not_forbid) ... ok
test_forbidden_ninguno_does_not_forbid (test_scope_rules.TestDec012Tabla6.test_forbidden_ninguno_does_not_forbid) ... ok
test_hash_in_pattern_is_literal (test_scope_rules.TestDec012Tabla6.test_hash_in_pattern_is_literal) ... ok
test_inline_annotation_parens_is_literal (test_scope_rules.TestDec012Tabla6.test_inline_annotation_parens_is_literal) ... ok
test_inline_comment_is_literal_in_allowed (test_scope_rules.TestDec012Tabla6.test_inline_comment_is_literal_in_allowed) ... ok
test_parens_in_pattern_are_literal (test_scope_rules.TestDec012Tabla6.test_parens_in_pattern_are_literal) ... ok
test_plain_glob_authorizes (test_scope_rules.TestDec012Tabla6.test_plain_glob_authorizes) ... ok
test_precedence_complementary_case (test_scope_rules.TestDec012Tabla6.test_precedence_complementary_case) ... ok
test_pure_note_line_produces_no_entry (test_scope_rules.TestDec012Tabla6.test_pure_note_line_produces_no_entry) ... ok
test_case_sensitive_matching (test_scope_rules.TestGlobMatching.test_case_sensitive_matching) ... ok
test_double_star_crosses_slash (test_scope_rules.TestGlobMatching.test_double_star_crosses_slash) ... ok
test_literal_regex_metacharacters_are_not_special (test_scope_rules.TestGlobMatching.test_literal_regex_metacharacters_are_not_special) ... ok
test_question_mark_is_single_non_slash_char (test_scope_rules.TestGlobMatching.test_question_mark_is_single_non_slash_char) ... ok
test_star_does_not_cross_slash (test_scope_rules.TestGlobMatching.test_star_does_not_cross_slash) ... ok
test_trailing_slash_covers_all_content (test_scope_rules.TestGlobMatching.test_trailing_slash_covers_all_content) ... ok
test_allowed_absent_header_is_error (test_scope_rules.TestParseContractGrammar.test_allowed_absent_header_is_error) ... ok
test_allowed_empty_is_error (test_scope_rules.TestParseContractGrammar.test_allowed_empty_is_error) ... ok
test_alternative_marker_asterisk_is_error (test_scope_rules.TestParseContractGrammar.test_alternative_marker_asterisk_is_error) ... ok
test_alternative_marker_plus_is_error (test_scope_rules.TestParseContractGrammar.test_alternative_marker_plus_is_error) ... ok
test_duplicated_allowed_header_is_error (test_scope_rules.TestParseContractGrammar.test_duplicated_allowed_header_is_error) ... ok
test_empty_entry_after_trim_is_error (test_scope_rules.TestParseContractGrammar.test_empty_entry_after_trim_is_error) ... ok
test_explanation_line_without_marker_is_ignored (test_scope_rules.TestParseContractGrammar.test_explanation_line_without_marker_is_ignored) ... ok
test_forbidden_absent_header_is_error (test_scope_rules.TestParseContractGrammar.test_forbidden_absent_header_is_error) ... ok
test_forbidden_sentinel_dash (test_scope_rules.TestParseContractGrammar.test_forbidden_sentinel_dash) ... ok
test_forbidden_sentinel_n_a (test_scope_rules.TestParseContractGrammar.test_forbidden_sentinel_n_a) ... ok
test_forbidden_sentinel_ninguno (test_scope_rules.TestParseContractGrammar.test_forbidden_sentinel_ninguno) ... ok
test_forbidden_sentinel_none (test_scope_rules.TestParseContractGrammar.test_forbidden_sentinel_none) ... ok
test_invalid_utf8_is_caller_responsibility (test_scope_rules.TestParseContractGrammar.test_invalid_utf8_is_caller_responsibility) ... ok
test_malformed_marker_without_separator_is_error (test_scope_rules.TestParseContractGrammar.test_malformed_marker_without_separator_is_error) ... ok
test_sentinel_mixed_with_patterns_is_error (test_scope_rules.TestParseContractGrammar.test_sentinel_mixed_with_patterns_is_error) ... ok
test_simple_allowed_and_forbidden (test_scope_rules.TestParseContractGrammar.test_simple_allowed_and_forbidden) ... ok
test_forbidden_wins_over_allowed (test_scope_rules.TestPrecedence.test_forbidden_wins_over_allowed) ... ok
test_outside_allowed_is_denied (test_scope_rules.TestPrecedence.test_outside_allowed_is_denied) ... ok
test_own_contract_has_no_exemption (test_scope_rules.TestPrecedence.test_own_contract_has_no_exemption) ... ok
test_absolute_target_is_violation (test_scope_rules.TestSymlinkResolution.test_absolute_target_is_violation) ... ok
test_deep_escape_root_is_violation (test_scope_rules.TestSymlinkResolution.test_deep_escape_root_is_violation) ... ok
test_escape_root_is_violation (test_scope_rules.TestSymlinkResolution.test_escape_root_is_violation) ... ok
test_evaluate_symlink_absolute_target (test_scope_rules.TestSymlinkResolution.test_evaluate_symlink_absolute_target) ... ok
test_evaluate_symlink_target_inside_allowed (test_scope_rules.TestSymlinkResolution.test_evaluate_symlink_target_inside_allowed) ... ok
test_evaluate_symlink_target_inside_forbidden (test_scope_rules.TestSymlinkResolution.test_evaluate_symlink_target_inside_forbidden) ... ok
test_evaluate_symlink_target_outside_allowed (test_scope_rules.TestSymlinkResolution.test_evaluate_symlink_target_outside_allowed) ... ok
test_relative_target_resolves_textually (test_scope_rules.TestSymlinkResolution.test_relative_target_resolves_textually) ... ok
test_relative_target_within_same_dir (test_scope_rules.TestSymlinkResolution.test_relative_target_within_same_dir) ... ok
test_symlink_never_amplifies_scope (test_scope_rules.TestSymlinkResolution.test_symlink_never_amplifies_scope) ... ok
test_allowed_star_matches_only_top_level (test_scope_rules.TestTransitionCorpus.test_allowed_star_matches_only_top_level) ... ok
test_ascii_space_and_tab_are_trimmed (test_scope_rules.TestTransitionCorpus.test_ascii_space_and_tab_are_trimmed) ... ok
test_literal_dash_path_is_independent_of_sentinel (test_scope_rules.TestTransitionCorpus.test_literal_dash_path_is_independent_of_sentinel) ... ok
test_trailing_form_feed_is_not_stripped (test_scope_rules.TestTransitionCorpus.test_trailing_form_feed_is_not_stripped) ... ok
test_trailing_unicode_whitespace_is_not_stripped (test_scope_rules.TestTransitionCorpus.test_trailing_unicode_whitespace_is_not_stripped) ... ok
test_check_scope_has_no_forbidden_apis (test_security_static.TestSecurityStatic.test_check_scope_has_no_forbidden_apis) ... ok
test_check_scope_parses_as_valid_python (test_security_static.TestSecurityStatic.test_check_scope_parses_as_valid_python) ... ok
test_scope_rules_has_no_forbidden_apis (test_security_static.TestSecurityStatic.test_scope_rules_has_no_forbidden_apis) ... ok
test_scope_rules_parses_as_valid_python (test_security_static.TestSecurityStatic.test_scope_rules_parses_as_valid_python) ... ok

----------------------------------------------------------------------
Ran 95 tests in 6.844s

OK

--- HEAD después: 718ce294fe592c2b6df7c13c5f56caea4199d7f2 ---

============================================================
 RESULTADO: OK (pruebas en verde, aislamiento intacto)
============================================================
```

### 7. `python3 scripts/check_scope.py WP-015 origin/main...HEAD`

Exit: `0`. Salida íntegra:

```
OK
{"base": "origin/main", "contrato": "work-packages/WP-015-check-scope-local.md", "contrato_blob": "7f52be5a63a588d38f61b6e03e3d7ae48fd0447a", "head": "HEAD", "merge_base": "30939377590a3c3b49ba705ef0f20c4832df61bd", "violaciones": [], "wp": "WP-015"}
```

Ejecutado inmediatamente después del commit `8830028` (antes del segundo
commit `718ce29`); el `HEAD` de esa ejecución era `8830028e61b773354fd92c7a8305727f203c4c42`.
`merge_base` coincide exactamente con la base autorizada. Repetido tras el
segundo commit con el mismo resultado (`OK`, cero violaciones): el propio
verificador certifica que su diff completo respeta su propio contrato.

### 8. `shellcheck --severity=warning --shell=bash tests/scope/run-suite.sh`

Salida: vacía. Exit: `0`. Repetido para `tests/scope/generate-evidence-hashes.sh`:
salida vacía, exit `0`.

### 9. `bash tests/governance/test-check-active.sh`

Exit: `0`. Salida íntegra:

```
==============================================================
 Validación del estado operativo — check-active.sh
 0=REPOSO o ACTIVO · 1=ERROR de coherencia · 2=ERROR sin archivo
==============================================================

--- Los cuatro estados ---
  OK    exit=0  marca=REPOSO   ACTIVE vacío (solo comentarios) → reposo
  OK    exit=0  marca=REPOSO   ACTIVE con archivo totalmente vacío → reposo
  OK    exit=0  marca=ACTIVO   ACTIVE con WP existente y con alcance → activo
  OK    exit=1  marca=ERROR    ACTIVE apunta a WP inexistente → error
  OK    exit=2  marca=ERROR    no existe el archivo ACTIVE → error

--- Coherencia adicional ---
  OK    exit=1  marca=ERROR    identificador mal formado (WP-7) → error
  OK    exit=1  marca=ERROR    identificador mal formado (basura) → error
  OK    exit=1  marca=ERROR    WP existente pero SIN rutas permitidas → error

--- Los mensajes son distinguibles entre sí ---
  OK    los 4 mensajes de primera línea son distintos
        reposo     : REPOSO: no hay WP activo.
        activo     : ACTIVO: WP-042
        inexistente: ERROR: ACTIVE apunta a 'WP-999' pero no existe work-packages/WP-999*.md
        sin archivo: ERROR: no existe work-packages/ACTIVE

--- INVARIANTE: el reposo sigue siendo fail-closed para escrituras ---
    (que el CI acepte ACTIVE vacío no relaja el guard)
  OK    exit=2  el guard DENIEGA una escritura con ACTIVE vacío

==============================================================
 RESULTADO: 10 correctas, 0 fallidas
==============================================================
```

### 10. `bash tests/guard/run-suite.sh`

Exit: `0`. Salida íntegra:

```
==============================================================
 Suite adversarial del guard
 Guard bajo prueba: /private/tmp/fda-template-wp015-implementation/.claude/hooks/guard.sh
 Convención: exit 0 = permite · exit 2 = BLOQUEA
==============================================================

--- A. Rutas DENTRO del alcance de WP-000 ---
  OK    exit=0  CLAUDE.md
  OK    exit=0  CODEOWNERS
  OK    exit=0  .claude/agents/planner.md
  OK    exit=0  docs/manual/MANUAL.md
  OK    exit=0  specs/adr/ADR-001-runtime.md
  OK    exit=0  .github/workflows/ci.yml
  OK    exit=0  ruta absoluta interna

--- B. REGRESIÓN: rutas permitidas que aún no existen en disco ---
  OK    exit=0  docs/inexistente/futuro.md
  OK    exit=0  evidence/WP-777/nuevo/log.txt
  OK    exit=0  tests/scope/test_nuevo.py

--- C. Fuera del alcance por omisión ---
  OK    exit=2  src/pagos/cobros.py
  OK    exit=2  package.json
  OK    exit=2  CLAUDE.md.bak (no es prefijo)
  OK    exit=2  docsX/otro.md (no es docs/)

--- D. Prohibidos explícitos (prohibido gana a permitido) ---
  OK    exit=2  .env.production
  OK    exit=2  docs/secrets/clave.txt
  OK    exit=2  specs/cert.pem

--- E. Evasión por forma de la ruta ---
  OK    exit=2  traversal ../fuera.txt
  OK    exit=2  traversal docs/../../fuera.txt
  OK    exit=2  absoluta fuera del repo
  OK    exit=2  NotebookEdit fuera de alcance

--- F. FAIL-CLOSED ---
  OK    exit=2  sin archivo ACTIVE
  OK    exit=2  ACTIVE vacío
  OK    exit=2  ACTIVE apunta a WP inexistente
  OK    exit=2  WP sin rutas permitidas

--- G. BASH: escrituras vía shell ---
  OK    exit=2  echo > src/y.py (redirección)
  OK    exit=2  echo >> package.json (append)
  OK    exit=2  tee src/z.py
  OK    exit=2  sed -i sobre src/
  OK    exit=2  cp hacia src/
  OK    exit=2  mv hacia src/
  OK    exit=2  rm -rf src/
  OK    exit=2  dd of=src/big.bin
  OK    exit=2  redirección con ruta entrecomillada
  OK    exit=2  truncate sobre src/
  OK    exit=2  ln -s hacia src/

--- H. BASH: lo que NO debe bloquearse (falsos positivos) ---
  OK    exit=0  echo > docs/ok.md (en alcance)
  OK    exit=0  echo >> evidence/WP-000/log.txt
  OK    exit=0  redirección a /dev/null
  OK    exit=0  escritura en /tmp
  OK    exit=0  commit con > dentro de comillas
  OK    exit=0  pytest (sin escrituras)
  OK    exit=0  grep con > en el patrón

--- I. AUTOPROTECCIÓN (fixture WP-900: solo docs/manual/**) ---
    Si el implementer pudiera escribir aquí, podría ampliarse el alcance
    a sí mismo y todo el enforcement colapsaría.
  OK    exit=0  docs/manual/x.md (en alcance)
  OK    exit=2  work-packages/ACTIVE
  OK    exit=2  work-packages/WP-900-realista.md
  OK    exit=2  work-packages/WP-001-otro.md
  OK    exit=2  .claude/settings.json
  OK    exit=2  .claude/hooks/guard.sh
  OK    exit=2  .claude/agents/implementer.md
  OK    exit=2  CODEOWNERS
  OK    exit=2  CLAUDE.md
  OK    exit=2  .github/workflows/ci.yml
  OK    exit=2  Bash: echo > ACTIVE
  OK    exit=2  Bash: cp sobre CLAUDE.md
  OK    exit=2  Bash: mv sobre settings.json
  OK    exit=2  Bash: sed -i sobre el WP activo

--- J. HUECOS CONOCIDOS (expected-fail, no se corrigen en el Paso 0) ---
    El guard es preventivo y best-effort. La defensa concluyente es la
    verificación post-hoc del diff (check_scope, WP-002), sobre la que no
    hay bypass posible sea cual sea la herramienta empleada.
  xfail exit=0 (se desea 2)  symlink en alcance que apunta fuera  [WP-002]
  xfail exit=0 (se desea 2)  python -c con open(...,'w')  [WP-002]
  xfail exit=0 (se desea 2)  subshell con redirección entrecomillada  [WP-002]
  xfail exit=0 (se desea 2)  git apply de parche fuera de alcance  [WP-002]
  xfail exit=0 (se desea 2)  tar extrayendo sobre ruta fuera de alcance  [WP-002]
  OK    exit=2  APFS: CLAUDE.md prohibido se bloquea
  xfail exit=0 (se desea 2)  APFS: 'claude.md' elude el prohibido  [WP-002 (macOS case-insensitive)]
  xfail exit=2 (se desea 0)  falso positivo: '>' entrecomillado seguido de cadena  [defecto del analizador Bash]
  xfail exit=2 (se desea 0)  falso positivo: ruta exenta tras variable sin expandir  [defecto del analizador Bash]
  xfail exit=0 (se desea 2)  git push -f (control en settings.json, no en guard)  [capa de permisos, no guard.sh]
  xfail exit=0 (se desea 2)  git push --force (idem)  [capa de permisos, no guard.sh]

--- K. REPOSO: ACTIVE vacío (estado normal entre dos WPs) ---
    Debe seguir siendo fail-closed para escrituras REALES, sin bloquear
    comandos de diagnóstico cuyos únicos destinos son exentos.
  OK    exit=2  Write a docs/ (fail-closed intacto)
  OK    exit=2  Write a cualquier ruta
  OK    exit=2  Bash: echo > src/y.py
  OK    exit=2  Bash: cp hacia el repo
  OK    exit=0  Bash: 2>/dev/null (solo diagnóstico)
  OK    exit=0  Bash: >/dev/null y stderr
  OK    exit=0  Bash: escritura en /tmp
  OK    exit=0  Bash: sin destinos (pytest)
  OK    exit=0  Bash: mezcla exento + sin destino
  OK    exit=2  Bash: mezcla exento + destino real

==============================================================
 RESULTADO: 68 correctas · 0 fallidas · 10 huecos conocidos · 0 huecos cerrados
==============================================================
```

Este WP no modifica `.claude/hooks/guard.sh` ni `tests/guard/run-suite.sh`; el
comando se ejecuta sin cambios respecto de la base autorizada, como
comprobación de no regresión.

### 11. `PYTHONDONTWRITEBYTECODE=1 python3 evidence/WP-000/checks/check-manual.py`

Exit: `0`. Salida íntegra:

```
==============================================================
 Manual — enlaces internos y placeholders de instalación
==============================================================

--- Enlaces internos (9 archivos) ---
  OK    docs/manual/01-instalacion.md
  OK    docs/manual/02-ciclo-de-un-wp.md
  OK    docs/manual/03-redactar-un-wp.md
  OK    docs/manual/04-agentes.md
  OK    docs/manual/05-bloqueos-y-parada.md
  OK    docs/manual/06-costes-y-metricas.md
  OK    docs/manual/07-troubleshooting.md
  OK    docs/manual/MANUAL.md
  OK    CLAUDE.md

  Enlaces internos comprobados: 66

--- Placeholders en docs/manual/01-instalacion.md ---
  OK    {{COMANDOS_VALIDACION}}
  OK    {{PROPIEDAD_COMPONENTES}}
  OK    {{PRESUPUESTOS_Y_MODELOS}}

--- Estado de los archivos parametrizables (informativo) ---
  instanciado CODEOWNERS                        sin marcador (valor real aplicado)
  plantilla  .github/workflows/ci.yml           conserva {{COMANDOS_VALIDACION}}
  plantilla  .github/workflows/claude.yml       conserva {{PRESUPUESTOS_Y_MODELOS}}
  plantilla  .github/workflows/code-review.yml  conserva {{PRESUPUESTOS_Y_MODELOS}}

  3 sin instanciar · 1 instanciados
  Nota: instalación parcial. Es lo esperado mientras el repo sirva
        de plantilla y de sandbox a la vez.

==============================================================
 RESULTADO: 0 fallos
==============================================================
```

### 12. `git diff --check`

Salida: vacía. Exit: `0`.

## Resumen de criterios de aceptación

- [x] La suite cubre las tablas completas de DEC-002 (8 filas, `TestDec002TraversalTable`)
  y DEC-012 (tabla §6, `TestDec012Tabla6`), el corpus de transición
  (`TestTransitionCorpus`), precedencia (`TestPrecedence`), globs
  (`TestGlobMatching`), directorios (sufijo `/`) y mayúsculas.
- [x] Repositorios temporales cubren `A/M/D/T/R/C`, nombres inusuales, todas
  las violaciones en una ejecución (`test_multiple_violations_in_one_execution_sorted`)
  y los tres códigos exactos (`TestExitZero`, `TestExitOne`, `TestExitTwo`).
- [x] Symlinks añadidos, modificados, eliminados, renombrados y con cambio de
  tipo se juzgan desde modos y blobs Git, incluida salida de raíz.
- [x] Ausencia, duplicidad, manipulación del contrato propio, rango inválido,
  UTF-8 inválido (a nivel de biblioteca, `test_invalid_utf8_is_caller_responsibility`),
  marcador alternativo y sentinela mezclado fallan cerrados.
- [x] Modificar o retirar el contrato del working tree no altera el veredicto
  obtenido desde el `merge-base` (`TestContractManipulationIgnored`).
- [x] La suite deja idénticos `git status --porcelain=v1 -z -uall` y `HEAD`
  del repositorio FDA antes y después (acreditado por `run-suite.sh`).
- [x] La CLI enumera el inventario completo en JSON de una línea y
  `docs/manual/02-ciclo-de-un-wp.md` documenta que es local y no bloquea
  fusiones.
- [x] `scripts/check_scope.py` importa `scope_rules` y no reimplementa
  gramática ni matching (`import scope_rules`, sin duplicación).
- [x] La evidencia identifica los bytes probados (manifiesto de arriba) y
  acredita el suelo T3 (ver `evidence/WP-015/seguridad.md`).
- [x] Los doce comandos de `## Verificación`, en su forma literal exacta,
  terminan en verde (`evidence/WP-015/verificacion.log`); el diff queda
  limitado a los cinco patrones de archivos permitidos del contrato (ver
  `git diff --check` y el listado de `git show --stat` en cada commit).

## Deuda y bloqueos declarados

1. **Bit ejecutable ausente** en los dos `.sh` nuevos (`chmod`/`git
   update-index --chmod` denegados por el permiso de herramienta de la
   sesión de implementación). No afecta a ninguna verificación porque se
   invocan siempre como `bash <script>`. Sigue sin resolverse: no es objeto
   de esta consolidación de evidencias, que no modifica código ni pruebas.

**Resuelto en esta consolidación.** La sesión de implementación inicial no
pudo invocar en su forma literal exacta los comandos 3, 4 y 5 del contrato
(`python3 -c "..."`, los dos `python3 -m unittest discover ...`) por la
lista `allow` de `.claude/settings.json` vigente en esa sesión concreta —no
por `guard.sh` ni por el contrato de WP-015— y documentó en su momento una
comprobación funcionalmente equivalente. El coordinador, con acceso
operativo más amplio, ejecutó después los doce comandos en su forma literal
exacta; la salida íntegra de esa ejecución real está en
`evidence/WP-015/verificacion.log` y queda resumida en las secciones 1-12 de
arriba. Ningún resultado se fabricó, ni en la comprobación equivalente
original ni en esta ejecución literal posterior.

## Verificación de las consolidaciones de evidencia

Las consolidaciones posteriores a `TESTED_HEAD` solo modifican
`evidence/WP-015/**`: incorporan el expediente inicial, `verificacion.log`, la
captura externa anterior de secretos, el registro de coste y este ajuste de
identidad. Se comprobó sobre el head presentado:

```bash
git diff --exit-code 718ce294fe592c2b6df7c13c5f56caea4199d7f2 -- scripts/check_scope.py scripts/scope_rules.py tests/scope docs/manual/02-ciclo-de-un-wp.md
```

exit `0`, salida vacía: código, pruebas y manual permanecen bit a bit
idénticos a `TESTED_HEAD`.
