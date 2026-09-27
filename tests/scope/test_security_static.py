"""test_security_static.py — Análisis estático (AST) de seguridad.

WP-015 §"Verificación": analiza con `ast` ambos módulos de producción y
falla ante shell, evaluación dinámica o APIs de lectura del filesystem
prohibidas por el contrato (la fuente de confianza es exclusivamente Git:
merge-base, ls-tree, cat-file, diff — nunca open()/os.path/pathlib sobre el
working tree). No ejecuta el código analizado: solo lo parsea.

WP015-F5 (revisión Astra, C1): el analizador original solo reconocía la
forma dotted literal ("os.path.exists(...)") y una lista de nombres bare
fijos. No detectaba `os.path.realpath` ni `io.open` (dos APIs que el propio
contrato prohíbe expresamente para symlinks), y una importación con alias
—`from os.path import realpath as rp; rp(...)`— o un alias de módulo
—`import os.path as p; p.realpath(...)`— evadían la detección por completo.
`_analyze` ahora resuelve ambas formas de alias antes de comparar contra la
lista cerrada de operaciones prohibidas, y `TestAnalyzerNegativeSamples`
demuestra con fuentes sintéticas que cada forma sigue detectándose.
"""

from __future__ import annotations

import ast
import pathlib
import unittest

_SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"

# Operaciones prohibidas invocadas como nombre bare (built-ins o importadas
# sin punto): eval/exec/compile/__import__ son evaluación dinámica; open es
# lectura del filesystem por su forma más común.
_FORBIDDEN_CALL_NAMES = frozenset({"eval", "exec", "compile", "__import__", "open"})

# Operaciones prohibidas invocadas como atributo con ruta punteada completa.
# WP015-F5 añade os.path.realpath e io.open: ambas resuelven o abren rutas
# del filesystem real, exactamente lo que el contrato prohíbe para decidir
# sobre symlinks o cualquier ruta juzgada.
_FORBIDDEN_ATTR_CALLS = frozenset(
    {
        "os.system",
        "os.popen",
        "os.listdir",
        "os.walk",
        "os.scandir",
        "os.readlink",
        "os.path.exists",
        "os.path.isfile",
        "os.path.isdir",
        "os.path.islink",
        "os.path.lexists",
        "os.path.realpath",
        "os.stat",
        "os.lstat",
        "os.fstat",
        "subprocess.getoutput",
        "subprocess.getstatusoutput",
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
        "subprocess.Popen",
        "io.open",
    }
)

# Todas las operaciones prohibidas por su ruta canónica (bare o punteada),
# para resolver bindings de "from X import Y [as Z]" sin duplicar la lista.
_FORBIDDEN_CANONICAL = _FORBIDDEN_ATTR_CALLS | _FORBIDDEN_CALL_NAMES

_FORBIDDEN_IMPORT_MODULES = frozenset({"pathlib"})


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _analyze(source: str, label: str) -> list:
    """Analiza `source` (código Python, sin ejecutarlo) y devuelve hallazgos.

    Dos pasadas deliberadas:
      1. recoge bindings de import —alias de nombre y alias de módulo—;
      2. camina las llamadas resolviendo esos bindings antes de comparar
         contra las listas cerradas de operaciones prohibidas.
    Así una llamada dotted ("io.open(...)"), una bare re-importada
    ("from io import open as o; o(...)") o un alias de módulo
    ("import io as i; i.open(...)") se detectan por igual.
    """
    tree = ast.parse(source, filename=label)
    findings = []

    # --- Pasada 1: bindings de import -----------------------------------
    name_bindings: dict = {}  # nombre local bare -> operación canónica
    module_aliases: dict = {}  # alias de módulo -> ruta real del módulo

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                local = alias.asname or alias.name
                canonical = f"{module}.{alias.name}" if module else alias.name
                if canonical in _FORBIDDEN_CANONICAL:
                    name_bindings[local] = canonical
                top = module.split(".")[0] if module else ""
                if top in _FORBIDDEN_IMPORT_MODULES:
                    findings.append(f"{label}: import prohibido de '{module}'")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top in _FORBIDDEN_IMPORT_MODULES:
                    findings.append(f"{label}: import prohibido de '{alias.name}'")
                if alias.asname:
                    module_aliases[alias.asname] = alias.name

    # --- Pasada 2: llamadas, resolviendo los bindings anteriores --------
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name):
            fname = node.func.id
            if fname in _FORBIDDEN_CALL_NAMES:
                findings.append(f"{label}: llamada prohibida a '{fname}(...)'")
            elif fname in name_bindings:
                findings.append(
                    f"{label}: llamada prohibida a '{name_bindings[fname]}(...)' "
                    f"(importada como '{fname}')"
                )
        elif isinstance(node.func, ast.Attribute):
            dotted = _dotted(node.func)
            flagged = dotted in _FORBIDDEN_ATTR_CALLS
            if not flagged and dotted:
                head, _, rest = dotted.partition(".")
                if head in module_aliases:
                    resolved = module_aliases[head] + ("." + rest if rest else "")
                    if resolved in _FORBIDDEN_ATTR_CALLS:
                        findings.append(
                            f"{label}: llamada prohibida a '{resolved}(...)' "
                            f"(vía alias de módulo '{head}')"
                        )
                        flagged = True
            if flagged and dotted in _FORBIDDEN_ATTR_CALLS:
                findings.append(f"{label}: llamada prohibida a '{dotted}(...)'")

        for kw in node.keywords:
            if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                findings.append(f"{label}: invocación con shell=True")

    return findings


class TestSecurityStatic(unittest.TestCase):
    def _check_file(self, filename: str) -> None:
        source = (_SCRIPTS / filename).read_text(encoding="utf-8")
        findings = _analyze(source, filename)
        self.assertEqual(findings, [], f"Hallazgos de seguridad en {filename}: {findings}")

    def test_check_scope_has_no_forbidden_apis(self):
        self._check_file("check_scope.py")

    def test_scope_rules_has_no_forbidden_apis(self):
        self._check_file("scope_rules.py")

    def test_check_scope_parses_as_valid_python(self):
        source = (_SCRIPTS / "check_scope.py").read_text(encoding="utf-8")
        ast.parse(source)  # no lanza => sintaxis válida

    def test_scope_rules_parses_as_valid_python(self):
        source = (_SCRIPTS / "scope_rules.py").read_text(encoding="utf-8")
        ast.parse(source)  # no lanza => sintaxis válida


class TestAnalyzerNegativeSamples(unittest.TestCase):
    """WP015-F5: muestras negativas que demuestran que `_analyze` falla.

    Cada snippet es código sintético, nunca ejecutado (solo `ast.parse`),
    que reproduce exactamente una forma de evasión señalada por Astra.
    """

    def test_dotted_os_path_realpath_is_detected(self):
        findings = _analyze('import os.path\nos.path.realpath("x")\n', "muestra")
        self.assertTrue(any("os.path.realpath" in f for f in findings))

    def test_dotted_io_open_is_detected(self):
        findings = _analyze('import io\nio.open("x")\n', "muestra")
        self.assertTrue(any("io.open" in f for f in findings))

    def test_from_import_bare_name_is_detected(self):
        findings = _analyze('from os.path import realpath\nrealpath("x")\n', "muestra")
        self.assertTrue(any("os.path.realpath" in f for f in findings))

    def test_from_import_with_alias_is_detected(self):
        findings = _analyze(
            'from os.path import realpath as rp\nrp("x")\n', "muestra"
        )
        self.assertTrue(any("os.path.realpath" in f for f in findings))

    def test_from_io_import_open_with_alias_is_detected(self):
        findings = _analyze('from io import open as o\no("x")\n', "muestra")
        self.assertTrue(any("io.open" in f for f in findings))

    def test_module_alias_attribute_call_is_detected(self):
        findings = _analyze(
            'import os.path as p\np.realpath("x")\n', "muestra"
        )
        self.assertTrue(any("os.path.realpath" in f for f in findings))

    def test_module_alias_for_io_open_is_detected(self):
        findings = _analyze('import io as i\ni.open("x")\n', "muestra")
        self.assertTrue(any("io.open" in f for f in findings))

    def test_existing_forbidden_names_still_detected(self):
        # No relajado por la reescritura: los casos ya cubiertos siguen igual.
        findings = _analyze('eval("1+1")\n', "muestra")
        self.assertTrue(any("eval" in f for f in findings))
        findings = _analyze('open("x")\n', "muestra")
        self.assertTrue(any("open" in f for f in findings))
        findings = _analyze(
            'import subprocess\nsubprocess.run(["x"], shell=True)\n', "muestra"
        )
        self.assertTrue(any("shell=True" in f for f in findings))

    def test_benign_subprocess_run_without_shell_has_no_findings(self):
        # Control negativo: no se prohíben APIs sin justificación contractual.
        findings = _analyze(
            'import subprocess\n'
            'subprocess.run(["git", "status"], shell=False)\n',
            "muestra",
        )
        self.assertEqual(findings, [])

    def test_unrelated_module_alias_has_no_false_positive(self):
        # Un alias de un módulo NO prohibido no debe producir hallazgos.
        findings = _analyze('import json as j\nj.dumps({})\n', "muestra")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
