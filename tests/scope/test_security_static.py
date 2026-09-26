"""test_security_static.py — Análisis estático (AST) de seguridad.

WP-015 §"Verificación": analiza con `ast` ambos módulos de producción y
falla ante shell, evaluación dinámica o APIs de lectura del filesystem
prohibidas por el contrato (la fuente de confianza es exclusivamente Git:
merge-base, ls-tree, cat-file, diff — nunca open()/os.path/pathlib sobre el
working tree). No ejecuta el código analizado: solo lo parsea.
"""

from __future__ import annotations

import ast
import pathlib
import unittest

_SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"

_FORBIDDEN_CALL_NAMES = {"eval", "exec", "compile", "__import__", "open"}

_FORBIDDEN_ATTR_CALLS = {
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
    "os.stat",
    "os.lstat",
    "os.fstat",
    "subprocess.getoutput",
    "subprocess.getstatusoutput",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "subprocess.Popen",
}

_FORBIDDEN_IMPORT_MODULES = {"pathlib"}


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _analyze(source: str, label: str) -> list:
    tree = ast.parse(source, filename=label)
    findings = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = getattr(node, "module", None) or ""
            names = [alias.name for alias in node.names]
            for candidate in ([module] + names):
                top = candidate.split(".")[0]
                if top in _FORBIDDEN_IMPORT_MODULES:
                    findings.append(f"{label}: import prohibido de '{candidate}'")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in _FORBIDDEN_CALL_NAMES:
                findings.append(f"{label}: llamada prohibida a '{node.func.id}(...)'")
            elif isinstance(node.func, ast.Attribute):
                dotted = _dotted(node.func)
                if dotted in _FORBIDDEN_ATTR_CALLS:
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


if __name__ == "__main__":
    unittest.main()
