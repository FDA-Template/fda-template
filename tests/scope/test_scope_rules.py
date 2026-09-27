"""test_scope_rules.py — Suite unitaria pura de scripts/scope_rules.py.

Cubre la gramática de DEC-012 (incluida la tabla cerrada de §6 y el corpus de
transición), la tabla de 8 casos de traversal de DEC-002 §7, el matching de
globs, la precedencia "prohibidos gana" y la resolución textual de destinos
de symlink. No toca disco ni red: son funciones puras sobre texto.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

_SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import scope_rules  # noqa: E402


def _contract(permitidos: str, prohibidos: str) -> str:
    return (
        "# WP-999 — contrato sintético de prueba\n\n"
        "## Objetivo y contexto\n\n"
        "Sintético.\n\n"
        "## Archivos permitidos\n\n"
        f"{permitidos}\n\n"
        "## Archivos prohibidos\n\n"
        f"{prohibidos}\n"
    )


class TestParseContractGrammar(unittest.TestCase):
    """DEC-012 §1-4: gramática léxica de las entradas ejecutables."""

    def test_simple_allowed_and_forbidden(self):
        text = _contract("- docs/**\n- scripts/**", "- secrets/**")
        allowed, forbidden = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["docs/**", "scripts/**"])
        self.assertEqual(forbidden, ["secrets/**"])

    def test_forbidden_sentinel_ninguno(self):
        text = _contract("- docs/**", "- ninguno")
        _allowed, forbidden = scope_rules.parse_contract(text)
        self.assertEqual(forbidden, [])

    def test_forbidden_sentinel_none(self):
        text = _contract("- docs/**", "- none")
        _allowed, forbidden = scope_rules.parse_contract(text)
        self.assertEqual(forbidden, [])

    def test_forbidden_sentinel_n_a(self):
        text = _contract("- docs/**", "- n/a")
        _allowed, forbidden = scope_rules.parse_contract(text)
        self.assertEqual(forbidden, [])

    def test_forbidden_sentinel_dash(self):
        # DEC-012 §6: "- -" en prohibidos es lista vacía, no prohibición literal.
        text = _contract("- docs/**", "- -")
        _allowed, forbidden = scope_rules.parse_contract(text)
        self.assertEqual(forbidden, [])

    def test_explanation_line_without_marker_is_ignored(self):
        text = _contract("Nota: solo manuales\n- docs/**", "- ninguno")
        allowed, _forbidden = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["docs/**"])

    def test_allowed_empty_is_error(self):
        text = _contract("- ninguno", "- ninguno")
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_allowed_absent_header_is_error(self):
        text = (
            "# WP-999\n\n## Objetivo\n\nx\n\n## Archivos prohibidos\n\n- ninguno\n"
        )
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_forbidden_absent_header_is_error(self):
        text = "# WP-999\n\n## Objetivo\n\nx\n\n## Archivos permitidos\n\n- docs/**\n"
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_duplicated_allowed_header_is_error(self):
        text = (
            "## Archivos permitidos\n- docs/**\n"
            "## Archivos permitidos\n- scripts/**\n"
            "## Archivos prohibidos\n- ninguno\n"
        )
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_empty_entry_after_trim_is_error(self):
        text = _contract("-   \n- docs/**", "- ninguno")
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_malformed_marker_without_separator_is_error(self):
        text = _contract("-docs/**", "- ninguno")
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_alternative_marker_asterisk_is_error(self):
        text = _contract("* docs/**", "- ninguno")
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_alternative_marker_plus_is_error(self):
        text = _contract("+ docs/**", "- ninguno")
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_sentinel_mixed_with_patterns_is_error(self):
        text = _contract("- docs/**", "- ninguno\n- secrets/**")
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(text)

    def test_invalid_utf8_is_caller_responsibility(self):
        # parse_contract recibe SIEMPRE texto ya decodificado (str); no le
        # corresponde decodificar bytes. Verificamos el contrato de tipos.
        with self.assertRaises(scope_rules.ContractError):
            scope_rules.parse_contract(b"no soy texto")  # type: ignore[arg-type]


class TestDec012Tabla6(unittest.TestCase):
    """Reproduce íntegramente la tabla cerrada de DEC-012 §6."""

    def _allowed_only(self, entry_line: str):
        text = _contract(entry_line, "- ninguno")
        return scope_rules.parse_contract(text)

    def test_parens_in_pattern_are_literal(self):
        allowed, _ = self._allowed_only("- docs/(draft).md")
        self.assertEqual(allowed, ["docs/(draft).md"])
        self.assertIsNone(scope_rules.match_any("docs/a.md", allowed))
        self.assertEqual(scope_rules.match_any("docs/(draft).md", allowed), "docs/(draft).md")

    def test_hash_in_pattern_is_literal(self):
        allowed, _ = self._allowed_only("- docs/file#v1")
        self.assertEqual(allowed, ["docs/file#v1"])
        self.assertIsNone(scope_rules.match_any("docs/a.md", allowed))

    def test_backticks_are_literal_bytes(self):
        allowed, _ = self._allowed_only("- `docs/**`")
        self.assertEqual(allowed, ["`docs/**`"])
        self.assertIsNone(scope_rules.match_any("docs/a.md", allowed))

    def test_inline_comment_is_literal_in_allowed(self):
        allowed, _ = self._allowed_only("- docs/** # nota")
        self.assertEqual(allowed, ["docs/** # nota"])
        self.assertIsNone(scope_rules.match_any("docs/a.md", allowed))

    def test_inline_annotation_parens_is_literal(self):
        allowed, _ = self._allowed_only("- docs/** (manual)")
        self.assertEqual(allowed, ["docs/** (manual)"])
        self.assertIsNone(scope_rules.match_any("docs/a.md", allowed))

    def test_pure_note_line_produces_no_entry(self):
        text = _contract("Nota: solo manuales\n- docs/**", "- ninguno")
        allowed, _ = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["docs/**"])

    def test_plain_glob_authorizes(self):
        allowed, _ = self._allowed_only("- docs/**")
        self.assertEqual(scope_rules.match_any("docs/a.md", allowed), "docs/**")

    def test_forbidden_ninguno_does_not_forbid(self):
        text = _contract("- docs/**", "- ninguno")
        allowed, forbidden = scope_rules.parse_contract(text)
        verdict = scope_rules.evaluate("docs/a.md", allowed, forbidden)
        self.assertTrue(verdict.ok)

    def test_forbidden_dash_does_not_forbid(self):
        text = _contract("- docs/**", "- -")
        allowed, forbidden = scope_rules.parse_contract(text)
        verdict = scope_rules.evaluate("docs/a.md", allowed, forbidden)
        self.assertTrue(verdict.ok)

    def test_precedence_complementary_case(self):
        # permitidos docs/**; prohibidos "docs/** # nota" no coincide con
        # docs/a.md literalmente, así que sigue autorizado.
        text = _contract("- docs/**", "- docs/** # nota")
        allowed, forbidden = scope_rules.parse_contract(text)
        verdict = scope_rules.evaluate("docs/a.md", allowed, forbidden)
        self.assertTrue(verdict.ok)


class TestTransitionCorpus(unittest.TestCase):
    """DEC-012 § Transición: subconjunto temporal y casos discriminantes."""

    def test_allowed_star_matches_only_top_level(self):
        text = _contract("- *", "- ninguno")
        allowed, _ = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["*"])
        self.assertIsNotNone(scope_rules.match_any("foo.md", allowed))
        self.assertIsNone(scope_rules.match_any("docs/foo.md", allowed))

    def test_literal_dash_path_is_independent_of_sentinel(self):
        # prohibidos "- -" es lista vacía (sentinela). Permitidos contiene un
        # patrón que autoriza la ruta LITERAL "-" (un archivo real llamado
        # "-"). El sentinela de la gramática del contrato no afecta al
        # juicio sobre una ruta versionada llamada "-".
        text = _contract("- -\n- docs/**", "- -")
        with self.assertRaises(scope_rules.ContractError):
            # "- -" mezclado con "- docs/**" en PERMITIDOS es sentinela
            # mezclado con patrones: se prueba aparte, sin mezcla.
            scope_rules.parse_contract(text)

        text2 = _contract("- *", "- -")
        allowed, forbidden = scope_rules.parse_contract(text2)
        verdict = scope_rules.evaluate("-", allowed, forbidden)
        self.assertTrue(verdict.ok)

    def test_trailing_form_feed_is_not_stripped(self):
        # U+000C (form feed) no es H: no se recorta y queda dentro del patrón.
        entry = "- docs/\x0c"
        text = _contract(entry, "- ninguno")
        allowed, _ = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["docs/\x0c"])
        self.assertIsNone(scope_rules.match_any("docs/", allowed))
        self.assertIsNotNone(scope_rules.match_any("docs/\x0c", allowed))

    def test_trailing_unicode_whitespace_is_not_stripped(self):
        # U+00A0 (NBSP) no es espacio ASCII ni tabulador: se conserva literal.
        entry = "- docs/ "
        text = _contract(entry, "- ninguno")
        allowed, _ = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["docs/ "])
        self.assertIsNotNone(scope_rules.match_any("docs/ ", allowed))
        self.assertIsNone(scope_rules.match_any("docs/", allowed))

    def test_ascii_space_and_tab_are_trimmed(self):
        entry = "-  docs/**  "
        text = _contract(entry, "- ninguno")
        allowed, _ = scope_rules.parse_contract(text)
        self.assertEqual(allowed, ["docs/**"])


class TestGlobMatching(unittest.TestCase):
    def test_star_does_not_cross_slash(self):
        rx = scope_rules.compile_glob("src/*.py")
        self.assertTrue(rx.fullmatch("src/a.py"))
        self.assertFalse(rx.fullmatch("src/sub/a.py"))

    def test_double_star_crosses_slash(self):
        rx = scope_rules.compile_glob("docs/**")
        self.assertTrue(rx.fullmatch("docs/a.md"))
        self.assertTrue(rx.fullmatch("docs/x/y/z.md"))

    def test_question_mark_is_single_non_slash_char(self):
        rx = scope_rules.compile_glob("a?.md")
        self.assertTrue(rx.fullmatch("ab.md"))
        self.assertFalse(rx.fullmatch("a/.md"))
        self.assertFalse(rx.fullmatch("abc.md"))

    def test_trailing_slash_covers_all_content(self):
        rx = scope_rules.compile_glob("build/")
        self.assertTrue(rx.fullmatch("build/a.txt"))
        self.assertTrue(rx.fullmatch("build/x/y.txt"))
        self.assertFalse(rx.fullmatch("build"))

    def test_literal_regex_metacharacters_are_not_special(self):
        rx = scope_rules.compile_glob("CLAUDE.md")
        self.assertTrue(rx.fullmatch("CLAUDE.md"))
        self.assertFalse(rx.fullmatch("CLAUDEXmd"))

    def test_case_sensitive_matching(self):
        rx = scope_rules.compile_glob("CLAUDE.md")
        self.assertFalse(rx.fullmatch("claude.md"))


class TestDoubleStarAndDirSuffixConsumeLF(unittest.TestCase):
    """WP015-F1 (revisión Astra, C1): '**' y el sufijo '/' deben cubrir LF
    exactamente igual que '*', para que un prohibido recursivo no pueda ser
    eludido con una ruta que contenga un salto de línea embebido."""

    def test_double_star_matches_path_with_embedded_lf(self):
        rx = scope_rules.compile_glob("docs/**")
        self.assertTrue(rx.fullmatch("docs/a\nb.md"))

    def test_trailing_slash_matches_path_with_embedded_lf(self):
        rx = scope_rules.compile_glob("docs/")
        self.assertTrue(rx.fullmatch("docs/a\nb.md"))

    def test_reproduccion_exacta_del_hallazgo(self):
        # evaluate("docs/a\nb.md", ["docs/*"], ["docs/**"]) NO debe permitir:
        # el prohibido "docs/**" debe cazar la misma ruta que el permitido
        # "docs/*" ya cazaba, precisamente porque contiene un LF.
        verdict = scope_rules.evaluate(
            "docs/a\nb.md", ["docs/*"], ["docs/**"]
        )
        self.assertFalse(verdict.ok)
        self.assertEqual(verdict.motivo, "prohibido")
        self.assertEqual(verdict.patron, "docs/**")

    def test_single_star_already_matched_lf_before_the_fix(self):
        # Control: '*' ([^/]*) siempre cubrió LF; lo que fallaba era '**'.
        rx = scope_rules.compile_glob("docs/*")
        self.assertTrue(rx.fullmatch("docs/a\nb.md"))

    def test_dir_suffix_forbidden_wins_over_star_allowed(self):
        verdict = scope_rules.evaluate(
            "docs/a\nb.md", ["docs/*"], ["docs/"]
        )
        self.assertFalse(verdict.ok)
        self.assertEqual(verdict.motivo, "prohibido")
        self.assertEqual(verdict.patron, "docs/")

    def test_double_star_allowed_authorizes_path_with_lf(self):
        verdict = scope_rules.evaluate("docs/a\nb.md", ["docs/**"], [])
        self.assertTrue(verdict.ok)

    def test_dir_suffix_allowed_authorizes_path_with_lf(self):
        verdict = scope_rules.evaluate("docs/a\nb.md", ["docs/"], [])
        self.assertTrue(verdict.ok)


class TestDec002TraversalTable(unittest.TestCase):
    """Las ocho filas de DEC-002 §7, vinculantes."""

    ALLOWED = ["evidence/WP-002/**"]
    FORBIDDEN: list = []

    def _ok(self, path: str) -> bool:
        return scope_rules.evaluate(path, self.ALLOWED, self.FORBIDDEN).ok

    def test_row1_notas_dotdot_md_no_traversal(self):
        self.assertFalse(scope_rules.has_traversal("evidence/WP-002/notas..md"))
        self.assertTrue(self._ok("evidence/WP-002/notas..md"))

    def test_row2_leading_dotdot_no_traversal(self):
        self.assertFalse(scope_rules.has_traversal("evidence/WP-002/..hidden.md"))
        self.assertTrue(self._ok("evidence/WP-002/..hidden.md"))

    def test_row3_trailing_dotdot_no_traversal(self):
        self.assertFalse(scope_rules.has_traversal("evidence/WP-002/bar.."))
        self.assertTrue(self._ok("evidence/WP-002/bar.."))

    def test_row4_foo_dotdot_slash_bar_no_traversal(self):
        self.assertFalse(scope_rules.has_traversal("evidence/WP-002/foo../bar"))
        self.assertTrue(self._ok("evidence/WP-002/foo../bar"))

    def test_row5_bare_dotdot_is_traversal(self):
        self.assertTrue(scope_rules.has_traversal(".."))
        self.assertFalse(self._ok(".."))

    def test_row6_leading_component_dotdot_is_traversal(self):
        self.assertTrue(scope_rules.has_traversal("../x"))
        self.assertFalse(self._ok("../x"))

    def test_row7_middle_component_dotdot_is_traversal(self):
        self.assertTrue(scope_rules.has_traversal("evidence/WP-002/../x"))
        self.assertFalse(self._ok("evidence/WP-002/../x"))

    def test_row8_trailing_component_dotdot_is_traversal(self):
        self.assertTrue(scope_rules.has_traversal("evidence/WP-002/.."))
        self.assertFalse(self._ok("evidence/WP-002/.."))

    def test_traversal_component_never_folds(self):
        # DEC-002 §3: un componente ".." nunca se resuelve, aunque el
        # plegado caería dentro del alcance.
        allowed = ["evidence/WP-002/log.txt"]
        verdict = scope_rules.evaluate("evidence/WP-002/../WP-002/log.txt", allowed, [])
        self.assertFalse(verdict.ok)
        self.assertEqual(verdict.motivo, "traversal")


class TestPrecedence(unittest.TestCase):
    def test_forbidden_wins_over_allowed(self):
        allowed = ["src/**"]
        forbidden = ["src/secret.py"]
        v_ok = scope_rules.evaluate("src/a.py", allowed, forbidden)
        v_blocked = scope_rules.evaluate("src/secret.py", allowed, forbidden)
        self.assertTrue(v_ok.ok)
        self.assertFalse(v_blocked.ok)
        self.assertEqual(v_blocked.motivo, "prohibido")

    def test_outside_allowed_is_denied(self):
        v = scope_rules.evaluate("other/file.py", ["src/**"], [])
        self.assertFalse(v.ok)
        self.assertEqual(v.motivo, "fuera_de_permitidos")

    def test_own_contract_has_no_exemption(self):
        # WP-002 caso 8 / WP-015 §2: no hay exenciones para work-packages/**.
        v = scope_rules.evaluate("work-packages/WP-015-check-scope-local.md", ["docs/**"], [])
        self.assertFalse(v.ok)


class TestSymlinkResolution(unittest.TestCase):
    def test_absolute_target_is_violation(self):
        ok, motivo, resolved = scope_rules.resolve_symlink_target("docs/link", "/etc/passwd")
        self.assertFalse(ok)
        self.assertEqual(motivo, "symlink_absoluto")
        self.assertIsNone(resolved)

    def test_escape_root_is_violation(self):
        ok, motivo, _ = scope_rules.resolve_symlink_target("link", "../outside")
        self.assertFalse(ok)
        self.assertEqual(motivo, "symlink_fuera_de_raiz")

    def test_deep_escape_root_is_violation(self):
        ok, motivo, _ = scope_rules.resolve_symlink_target("a/b/link", "../../../outside")
        self.assertFalse(ok)
        self.assertEqual(motivo, "symlink_fuera_de_raiz")

    def test_relative_target_resolves_textually(self):
        ok, _motivo, resolved = scope_rules.resolve_symlink_target("docs/sub/link", "../other.md")
        self.assertTrue(ok)
        self.assertEqual(resolved, "docs/other.md")

    def test_relative_target_within_same_dir(self):
        ok, _motivo, resolved = scope_rules.resolve_symlink_target("docs/link", "other.md")
        self.assertTrue(ok)
        self.assertEqual(resolved, "docs/other.md")

    def test_evaluate_symlink_target_inside_allowed(self):
        v = scope_rules.evaluate_symlink("docs/link", "other.md", ["docs/**"], [])
        self.assertTrue(v.ok)

    def test_evaluate_symlink_target_outside_allowed(self):
        v = scope_rules.evaluate_symlink("docs/link", "../secrets/token", ["docs/**"], [])
        self.assertFalse(v.ok)
        self.assertEqual(v.motivo, "symlink_fuera_de_permitidos")

    def test_evaluate_symlink_target_inside_forbidden(self):
        v = scope_rules.evaluate_symlink(
            "docs/link", "secret.md", ["docs/**"], ["docs/secret.md"]
        )
        self.assertFalse(v.ok)
        self.assertEqual(v.motivo, "symlink_prohibido")

    def test_evaluate_symlink_absolute_target(self):
        v = scope_rules.evaluate_symlink("docs/link", "/etc/passwd", ["docs/**"], [])
        self.assertFalse(v.ok)
        self.assertEqual(v.motivo, "symlink_absoluto")

    def test_symlink_never_amplifies_scope(self):
        # DEC-002 §6 / _TEMPLATE.md: un enlace dentro de lo permitido que
        # apunte fuera del alcance no autoriza a escribir en el destino.
        v = scope_rules.evaluate_symlink("evidence/WP-015/link", "../../etc/passwd", ["evidence/WP-015/**"], [])
        self.assertFalse(v.ok)


if __name__ == "__main__":
    unittest.main()
