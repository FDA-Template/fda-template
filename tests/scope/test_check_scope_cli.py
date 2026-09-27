"""test_check_scope_cli.py — Suite integral de scripts/check_scope.py.

Construye repositorios Git temporales y desechables (mktemp -d) para cubrir
A/M/D/T/R/C, symlinks, nombres inusuales, todas las violaciones en una sola
ejecución, los tres códigos de salida exactos, la fuente de confianza en el
merge-base (caso 8 de WP-002/DEC-002) y la ausencia de forja de líneas de
log. No toca el repositorio FDA: cada test crea y destruye su propio
repositorio temporal.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import unittest

_TESTS_SCOPE = pathlib.Path(__file__).resolve().parent
_REPO_ROOT = _TESTS_SCOPE.parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
_SCRIPT_PATH = str(_SCRIPTS / "check_scope.py")

if str(_TESTS_SCOPE) not in sys.path:
    sys.path.insert(0, str(_TESTS_SCOPE))
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from _repo import TempRepo, run_check_scope  # noqa: E402
import check_scope  # noqa: E402

WP_ID = "WP-901"


def _contract_text(allowed, forbidden) -> str:
    lines = [
        "# WP-901 — contrato sintético de prueba\n",
        "\n",
        "## Objetivo y contexto\n",
        "\n",
        "Sintético, solo para la suite de WP-015.\n",
        "\n",
        "## Archivos permitidos\n",
        "\n",
    ]
    for p in allowed:
        lines.append(f"- {p}\n")
    lines.append("\n## Archivos prohibidos\n\n")
    if forbidden:
        for p in forbidden:
            lines.append(f"- {p}\n")
    else:
        lines.append("- ninguno\n")
    return "".join(lines)


def _write_contract(repo: TempRepo, allowed, forbidden, name: str = "WP-901-sandbox.md") -> None:
    repo.write_text(f"work-packages/{name}", _contract_text(allowed, forbidden))
    repo.add(f"work-packages/{name}")


class CheckScopeCliTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = TempRepo()

    def tearDown(self) -> None:
        self.repo.cleanup()

    def run_cli(self, range_str: str, wp_id: str = WP_ID):
        return run_check_scope(self.repo, _SCRIPT_PATH, wp_id, range_str)


class TestExitZero(CheckScopeCliTestCase):
    def test_ok_zero_violations(self):
        _write_contract(self.repo, ["scripts/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("scripts/nuevo.py", "print('hola')\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 0)
        self.assertEqual(lines[0], "OK")
        payload = json.loads(lines[1])
        self.assertEqual(payload["violaciones"], [])
        self.assertEqual(payload["wp"], WP_ID)
        self.assertEqual(payload["merge_base"], base)
        # claves ordenadas alfabéticamente (contrato exacto de la CLI).
        keys = list(payload.keys())
        self.assertEqual(keys, sorted(keys))
        for k in ("base", "contrato", "contrato_blob", "head", "merge_base", "violaciones", "wp"):
            self.assertIn(k, payload)


class TestExitOne(CheckScopeCliTestCase):
    def test_added_file_outside_allowed(self):
        _write_contract(self.repo, ["src/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("rogue/new.py", "x = 1\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        self.assertEqual(lines[0], "VIOLACION")
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "rogue/new.py")
        self.assertEqual(payload["rol"], "ruta")
        self.assertEqual(payload["motivo"], "fuera_de_permitidos")
        self.assertEqual(len(lines), 2)

    def test_modified_forbidden_wins_over_allowed(self):
        _write_contract(self.repo, ["src/**"], ["src/secret.py"])
        self.repo.write_text("src/secret.py", "TOKEN = 'v1'\n")
        self.repo.write_text("src/ok.py", "x = 1\n")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.write_text("src/secret.py", "TOKEN = 'v2'\n")
        self.repo.write_text("src/ok.py", "x = 2\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        rutas = {b["ruta"] for b in blocks}
        self.assertEqual(rutas, {"src/secret.py"})
        self.assertEqual(blocks[0]["motivo"], "prohibido")
        self.assertEqual(blocks[0]["patron"], "src/secret.py")

    def test_deleted_file_outside_allowed_is_still_judged(self):
        _write_contract(self.repo, ["src/**"], [])
        self.repo.write_text("legacy/old.txt", "deuda histórica\n")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.rm("legacy/old.txt")
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "legacy/old.txt")
        self.assertEqual(payload["rol"], "ruta")

    def test_rename_destination_outside_allowed(self):
        _write_contract(self.repo, ["src/**"], [])
        self.repo.write_text("src/old.py", "contenido idéntico y largo " * 5)
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.mv("src/old.py", "outside/new.py")
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "outside/new.py")
        self.assertEqual(payload["rol"], "destino")

    def test_copy_destination_outside_allowed(self):
        _write_contract(self.repo, ["src/**"], [])
        contenido = "contenido copiado idéntico " * 10
        self.repo.write_text("src/lib.py", contenido)
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.write_text("other/lib_copy.py", contenido)
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        destinos = [b for b in blocks if b["ruta"] == "other/lib_copy.py"]
        self.assertEqual(len(destinos), 1)
        self.assertEqual(destinos[0]["rol"], "destino")

    def test_typechange_to_symlink_outside_allowed(self):
        _write_contract(self.repo, ["docs/**"], [])
        self.repo.write_text("docs/note.txt", "contenido regular\n")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.remove_from_worktree("docs/note.txt")
        self.repo.symlink("docs/note.txt", b"../secrets/token")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "docs/note.txt")
        self.assertEqual(payload["motivo"], "symlink_fuera_de_permitidos")

    def test_symlink_pointing_inside_allowed_is_ok(self):
        _write_contract(self.repo, ["docs/**"], [])
        self.repo.write_text("docs/target.md", "contenido\n")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.symlink("docs/link.md", b"target.md")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 0)

    def test_symlink_absolute_target_is_violation(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        self.repo.symlink("docs/link.md", b"/etc/passwd")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["motivo"], "symlink_absoluto")

    def test_symlink_escaping_root_is_violation(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        self.repo.symlink("docs/link.md", b"../../../etc/passwd")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["motivo"], "symlink_fuera_de_raiz")

    def test_deleted_symlink_target_judged_from_merge_base(self):
        _write_contract(self.repo, ["docs/**"], [])
        self.repo.symlink("docs/link.md", b"/etc/passwd")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.rm("docs/link.md")
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["motivo"], "symlink_absoluto")

    def test_modified_symlink_target_changed_outside_allowed(self):
        # WP015-F6 (revisión Astra, C1): symlink con estado 'M' — mismo modo
        # 120000 antes y después, solo cambia el blob de destino.
        _write_contract(self.repo, ["docs/**"], [])
        self.repo.write_text("docs/target.md", "x\n")
        self.repo.symlink("docs/link.md", b"target.md")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.remove_from_worktree("docs/link.md")
        self.repo.symlink("docs/link.md", b"../secrets/token")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "docs/link.md")
        self.assertEqual(payload["rol"], "ruta")
        self.assertEqual(payload["motivo"], "symlink_fuera_de_permitidos")

    def test_renamed_symlink_target_now_escapes_root(self):
        # WP015-F6: symlink con estado 'R' — mismo blob de destino
        # ("../../ok.md"), pero el traslado de directorio del enlace cambia
        # la base de resolución: en origen resolvía dentro de lo permitido,
        # en destino sale de la raíz. El contenido del enlace no cambia; lo
        # que cambia es desde dónde se resuelve, y check_scope debe juzgar
        # cada extremo con SU PROPIA revisión (merge-base para origen, head
        # para destino), tal como exige el contrato.
        _write_contract(self.repo, ["docs/**"], [])
        self.repo.write_text("docs/ok.md", "x\n")
        self.repo.symlink("docs/a/b/link.md", b"../../ok.md")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.mv("docs/a/b/link.md", "docs/link.md")
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["ruta"], "docs/link.md")
        self.assertEqual(blocks[0]["rol"], "destino")
        self.assertEqual(blocks[0]["motivo"], "symlink_fuera_de_raiz")

    def test_symlink_target_invalid_utf8_is_exit_2(self):
        # WP015-F6: bytes UTF-8 realmente inválidos en el BLOB del destino
        # del symlink (objeto Git real, vía os.symlink con bytes crudos),
        # no en el nombre de archivo.
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        self.repo.symlink("docs/link.md", b"\xff\xfe-invalido")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 2)
        self.assertEqual(lines[0], "ERROR")
        payload = json.loads(lines[1])
        self.assertIn("destino de symlink", payload["motivo"])
        self.assertIn("codificación", payload["motivo"])

    def test_contract_blob_invalid_utf8_is_exit_2(self):
        # WP015-F6: bytes UTF-8 realmente inválidos en el BLOB del contrato,
        # committeados de verdad (no un archivo con nombre exótico).
        raw = (
            b"# WP-901\n\n## Archivos permitidos\n\n- docs/\xff\xfe**\n\n"
            b"## Archivos prohibidos\n\n- ninguno\n"
        )
        self.repo.write("work-packages/WP-901-sandbox.md", raw)
        self.repo.add("work-packages/WP-901-sandbox.md")
        base = self.repo.commit("base")
        self.repo.write_text("docs/x.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("codificación", payload["motivo"])

    def test_unusual_names_are_judged_correctly(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("docs/informe (borrador) niño.md", "x\n")
        self.repo.write_text("raíz.md", "y\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        rutas = {b["ruta"] for b in blocks}
        self.assertEqual(rutas, {"raíz.md"})

    def test_multiple_violations_in_one_execution_sorted(self):
        _write_contract(self.repo, ["src/**"], ["src/secret.py"])
        self.repo.write_text("src/secret.py", "TOKEN = 'v1'\n")
        self.repo.write_text("src/keep.py", "x = 1\n")
        self.repo.write_text("src/rename_me.py", "contenido renombrable largo " * 5)
        self.repo.write_text("legacy/old.txt", "deuda\n")
        self.repo.add()
        base = self.repo.commit("base")

        self.repo.write_text("rogue/new.py", "x = 1\n")
        self.repo.write_text("src/secret.py", "TOKEN = 'v2'\n")
        self.repo.rm("legacy/old.txt")
        self.repo.mv("src/rename_me.py", "rogue/renamed.py")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        self.assertEqual(len(lines) % 2, 0)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        self.assertEqual(len(blocks), 4)

        rutas_en_orden = [b["ruta"] for b in blocks]
        self.assertEqual(rutas_en_orden, sorted(rutas_en_orden))
        esperado = {"legacy/old.txt", "rogue/new.py", "rogue/renamed.py", "src/secret.py"}
        self.assertEqual(set(rutas_en_orden), esperado)

        # claves ordenadas alfabéticamente en cada línea JSON de violación.
        for i in range(0, len(lines), 2):
            self.assertEqual(lines[i], "VIOLACION")
            body = lines[i + 1]
            idx_motivo = body.index('"motivo"')
            idx_patron = body.index('"patron"')
            idx_rol = body.index('"rol"')
            idx_ruta = body.index('"ruta"')
            self.assertTrue(idx_motivo < idx_patron < idx_rol < idx_ruta)

    def test_double_star_forbidden_catches_lf_path_via_real_git(self):
        # WP015-F6/F1: reproducción de extremo a extremo (Git real, no solo
        # scope_rules.evaluate) de que "docs/**" en prohibidos caza una ruta
        # con LF embebido exactamente igual que "docs/*" en permitidos.
        _write_contract(self.repo, ["docs/*"], ["docs/**"])
        base = self.repo.commit("base")
        self.repo.write_text("docs/a\nb.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "docs/a\nb.md")
        self.assertEqual(payload["motivo"], "prohibido")
        self.assertEqual(payload["patron"], "docs/**")

    def test_dir_suffix_forbidden_catches_lf_path_via_real_git(self):
        _write_contract(self.repo, ["docs/*"], ["docs/"])
        base = self.repo.commit("base")
        self.repo.write_text("docs/a\nb.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["motivo"], "prohibido")
        self.assertEqual(payload["patron"], "docs/")

    def test_double_star_allowed_authorizes_lf_path_via_real_git(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("docs/a\nb.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 0)

    def test_embedded_newline_does_not_forge_log_lines(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        rutas = ["extra/a\nb.md", "extra/c.md"]
        for r in rutas:
            self.repo.write_text(r, "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        # Exactamente dos violaciones -> exactamente cuatro líneas físicas,
        # nunca más, aunque una ruta contenga un salto de línea embebido.
        self.assertEqual(len(lines), 4)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        rutas_recibidas = {b["ruta"] for b in blocks}
        self.assertEqual(rutas_recibidas, set(rutas))


class TestExitTwo(CheckScopeCliTestCase):
    def test_contract_missing_is_exit_2(self):
        self.repo.write_text("README.md", "sin contrato\n")
        self.repo.add()
        base = self.repo.commit("base")
        self.repo.write_text("README.md", "cambio\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 2)
        self.assertEqual(lines[0], "ERROR")
        payload = json.loads(lines[1])
        self.assertIn("contrato ausente", payload["motivo"])

    def test_duplicate_contract_is_exit_2(self):
        _write_contract(self.repo, ["docs/**"], [], name="WP-901-a.md")
        _write_contract(self.repo, ["docs/**"], [], name="WP-901-b.md")
        base = self.repo.commit("base")
        self.repo.write_text("docs/x.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("más de un contrato", payload["motivo"])

    def test_noncanonical_contract_path_is_exit_2(self):
        _write_contract(self.repo, ["docs/**"], [], name="sub/WP-901-nested.md")
        base = self.repo.commit("base")
        self.repo.write_text("docs/x.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("contrato ausente", payload["motivo"])

    def test_malformed_contract_missing_forbidden_header_is_exit_2(self):
        text = (
            "# WP-901\n\n## Archivos permitidos\n\n- docs/**\n"
        )
        self.repo.write_text("work-packages/WP-901-sandbox.md", text)
        self.repo.add("work-packages/WP-901-sandbox.md")
        base = self.repo.commit("base")
        self.repo.write_text("docs/x.md", "x\n")
        self.repo.add()
        head = self.repo.commit("head")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertEqual(payload["motivo"], "contrato malformado")

    def test_invalid_wp_id_format_is_exit_2(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        head = base
        code, lines = self.run_cli(f"{base}...{head}", wp_id="WP-1")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("WP-ID mal formado", payload["motivo"])

    def test_wp_id_with_unicode_digits_is_exit_2(self):
        # WP015-F7 (revisión Astra, C1): "WP-٩٠١" usa dígitos indo-árabes
        # (U+0669 U+0660 U+0661), que \d en modo Unicode aceptaba. El WP-ID
        # debe cumplir ASCII exacto WP-[0-9]{3}.
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        code, lines = self.run_cli(f"{base}...{base}", wp_id="WP-٩٠١")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("WP-ID mal formado", payload["motivo"])

    def test_range_without_triple_dot_is_exit_2(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        code, lines = self.run_cli(base)
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("BASE...HEAD", payload["motivo"])

    def test_range_with_empty_extreme_is_exit_2(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        code, lines = self.run_cli(f"...{base}")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("extremo vacío", payload["motivo"])

    def test_unknown_ref_is_exit_2(self):
        _write_contract(self.repo, ["docs/**"], [])
        base = self.repo.commit("base")
        code, lines = self.run_cli(f"no-existe-esta-ref...{base}")
        self.assertEqual(code, 2)
        payload = json.loads(lines[1])
        self.assertIn("merge-base", payload["motivo"])

    def test_wrong_argument_count_is_exit_2(self):
        import subprocess

        proc = subprocess.run(
            ["python3", _SCRIPT_PATH, WP_ID],
            cwd=self.repo.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.returncode, 2)
        out = proc.stdout.decode("utf-8")
        self.assertTrue(out.startswith("ERROR"))


class TestContractManipulationIgnored(CheckScopeCliTestCase):
    """Caso 8 de WP-002/DEC-002: el merge-base es la única fuente de confianza."""

    def test_working_tree_contract_edit_has_no_effect(self):
        _write_contract(self.repo, ["src/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("rogue/new.py", "x = 1\n")
        self.repo.add()
        head = self.repo.commit("head")

        # Se amplía el contrato SOLO en el working tree, sin commit.
        self.repo.write_text(
            "work-packages/WP-901-sandbox.md",
            _contract_text(["src/**", "rogue/**"], []),
        )

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "rogue/new.py")

    def test_working_tree_contract_removal_has_no_effect(self):
        _write_contract(self.repo, ["src/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("rogue/new.py", "x = 1\n")
        self.repo.add()
        head = self.repo.commit("head")

        self.repo.remove_from_worktree("work-packages/WP-901-sandbox.md")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        payload = json.loads(lines[1])
        self.assertEqual(payload["ruta"], "rogue/new.py")

    def test_head_committed_contract_expansion_has_no_effect(self):
        # WP015-F6 (revisión Astra, C1): la ampliación del contrato NO se
        # deja solo en el working tree, sino que se COMMITEA de verdad en
        # HEAD. check_scope sigue leyendo el contrato del merge-base (=
        # `base`, anterior a ambos commits de `head`), nunca de HEAD.
        _write_contract(self.repo, ["src/**"], [])
        base = self.repo.commit("base")
        self.repo.write_text("rogue/new.py", "x = 1\n")
        self.repo.add()
        self.repo.commit("head con violacion")

        self.repo.write_text(
            "work-packages/WP-901-sandbox.md",
            _contract_text(["src/**", "rogue/**"], []),
        )
        self.repo.add("work-packages/WP-901-sandbox.md")
        head = self.repo.commit("amplia el contrato, committeado en HEAD")

        code, lines = self.run_cli(f"{base}...{head}")
        self.assertEqual(code, 1)
        blocks = [json.loads(lines[i + 1]) for i in range(0, len(lines), 2)]
        rutas = {b["ruta"] for b in blocks}
        self.assertIn("rogue/new.py", rutas)


class TestPureParsers(unittest.TestCase):
    """Parsers puros de check_scope.py, sin invocar git ni el filesystem."""

    def test_unknown_status_letter_is_error(self):
        raw = b"U\x00some/path\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_truncated_record_is_error(self):
        raw = b"A\x00"[:-1]  # status "A" sin ruta siguiente
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_rename_record_consumes_two_paths(self):
        raw = b"R100\x00src/old.py\x00src/new.py\x00"
        records = check_scope.parse_name_status_z(raw)
        self.assertEqual(records, [("R", "src/old.py", "src/new.py")])

    def test_empty_diff_is_no_records(self):
        self.assertEqual(check_scope.parse_name_status_z(b""), [])

    def test_select_contract_zero_matches(self):
        entries = [("100644", "blob", "abc", "work-packages/WP-900-otro.md")]
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.select_contract(entries, WP_ID)

    def test_select_contract_two_matches(self):
        entries = [
            ("100644", "blob", "a1", "work-packages/WP-901-uno.md"),
            ("100644", "blob", "a2", "work-packages/WP-901-dos.md"),
        ]
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.select_contract(entries, WP_ID)

    def test_select_contract_single_match(self):
        entries = [("100644", "blob", "a1", "work-packages/WP-901-uno.md")]
        path, sha = check_scope.select_contract(entries, WP_ID)
        self.assertEqual(path, "work-packages/WP-901-uno.md")
        self.assertEqual(sha, "a1")

    # --- WP015-F3 (revisión Astra, C1): respuestas Git controladas --------

    def test_status_letter_with_garbage_suffix_is_error(self):
        # "AWRONG": letra válida, cola arbitraria. Debe rechazarse, nunca
        # tratarse como "A" seguido de una ruta que no existe.
        raw = b"AWRONG\x00some/path\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_rename_score_non_digit_is_error(self):
        raw = b"Rxxx\x00src/old.py\x00src/new.py\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_rename_score_empty_is_error(self):
        raw = b"R\x00src/old.py\x00src/new.py\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_missing_trailing_nul_is_error(self):
        # Salida bien formada salvo por el NUL final ausente: truncada.
        raw = b"A\x00some/path"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_empty_path_in_add_record_is_error(self):
        raw = b"A\x00\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_empty_destination_in_rename_record_is_error(self):
        raw = b"R100\x00src/old.py\x00\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_name_status_z(raw)

    def test_ls_tree_missing_trailing_nul_is_error(self):
        raw = b"100644 blob " + b"a" * 40 + b"\tdocs/x.md"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_ls_tree_z(raw)

    def test_ls_tree_invalid_mode_is_error(self):
        # "180000" no es un modo Git válido (dígito 8 fuera de octal).
        raw = b"180000 blob " + b"a" * 40 + b"\tdocs/x.md\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_ls_tree_z(raw)

    def test_ls_tree_unknown_object_type_is_error(self):
        raw = b"100644 gitlink " + b"a" * 40 + b"\tdocs/x.md\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_ls_tree_z(raw)

    def test_ls_tree_invalid_object_id_is_error(self):
        raw = b"100644 blob deadbeef\tdocs/x.md\x00"  # demasiado corto
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_ls_tree_z(raw)

    def test_ls_tree_empty_path_is_error(self):
        raw = b"100644 blob " + b"a" * 40 + b"\t\x00"
        with self.assertRaises(check_scope.CheckScopeError):
            check_scope.parse_ls_tree_z(raw)

    def test_ls_tree_valid_entry_parses(self):
        sha = "a" * 40
        raw = f"100644 blob {sha}\tdocs/x.md\x00".encode("utf-8")
        entries = check_scope.parse_ls_tree_z(raw)
        self.assertEqual(entries, [("100644", "blob", sha, "docs/x.md")])

    def test_empty_ls_tree_output_is_no_entries(self):
        self.assertEqual(check_scope.parse_ls_tree_z(b""), [])


if __name__ == "__main__":
    unittest.main()
