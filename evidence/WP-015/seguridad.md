# WP-015 — Seguridad: AST, escaneo de secretos y dependencias

## 1. Análisis estático AST (`tests/scope/test_security_static.py`)

Analiza con el módulo `ast` de la biblioteca estándar, sin ejecutar ningún
código de los dos módulos, exactamente `scripts/check_scope.py` y
`scripts/scope_rules.py`. Prohíbe:

- llamadas a `eval`, `exec`, `compile`, `__import__`, `open` (nombres bare);
- llamadas por atributo a `os.system`, `os.popen`, `os.listdir`, `os.walk`,
  `os.scandir`, `os.readlink`, `os.path.exists`, `os.path.isfile`,
  `os.path.isdir`, `os.path.islink`, `os.path.lexists`, `os.stat`,
  `os.lstat`, `os.fstat`, `subprocess.call`, `subprocess.check_call`,
  `subprocess.check_output`, `subprocess.Popen`, `subprocess.getoutput`,
  `subprocess.getstatusoutput`;
- cualquier invocación con la palabra clave `shell=True`;
- importar `pathlib`.

Resultado real (comando 6 de `verification.md`, dentro de la ejecución de
95 pruebas):

```
test_check_scope_has_no_forbidden_apis (test_security_static.TestSecurityStatic.test_check_scope_has_no_forbidden_apis) ... ok
test_check_scope_parses_as_valid_python (test_security_static.TestSecurityStatic.test_check_scope_parses_as_valid_python) ... ok
test_scope_rules_has_no_forbidden_apis (test_security_static.TestSecurityStatic.test_scope_rules_has_no_forbidden_apis) ... ok
test_scope_rules_parses_as_valid_python (test_security_static.TestSecurityStatic.test_scope_rules_parses_as_valid_python) ... ok
```

Cuatro de cuatro en verde: ningún hallazgo en ninguno de los dos módulos de
producción.

**Por qué es fiel al contrato.** `scripts/check_scope.py` solo invoca
`subprocess.run(["git", *args], ..., shell=False)` (lista de argumentos, sin
shell) para las siete operaciones Git de solo lectura que necesita
(`rev-parse --show-toplevel`, `merge-base`, `ls-tree`, `cat-file blob`,
`diff --name-status`); nunca `open()`, nunca una API de lectura del
filesystem sobre rutas de repositorio. `scripts/scope_rules.py` no importa
`os` ni `subprocess` en absoluto: es una biblioteca pura sobre cadenas.

## 2. Escaneo de secretos — **bloqueo declarado, sin fabricar evidencia**

El contrato exige versionar "el resultado del job existente `Escaneo de
secretos` sobre `TESTED_HEAD` u otro commit anterior identificado", y que el
check verde del head final "se verifica externamente" — es decir, mediante
la API o la interfaz de GitHub Actions, no mediante una ejecución local de
gitleaks.

**No se puede cerrar honestamente en esta sesión.** El entorno autorizado de
este WP prohíbe red para el autor («Red: NINGUNA para autor e
implementación»), y esta sesión no tiene acceso a la API de GitHub ni a
`gh`. No existe en `evidence/` de ningún WP anterior un resultado ya
versionado y con identificador de ejecución real de `Escaneo de secretos`
que pueda citarse como «otro commit anterior identificado» (se buscó en
`evidence/WP-006`, `WP-008`, `WP-009`, `WP-013`, `WP-014`; ninguno contiene
una captura con `run_id`, conclusión y SHA verificables, solo menciones
narrativas de que ese check "seguirá pendiente").

**Lo que sí se acredita localmente, sin red:**

- `scripts/check_scope.py` y `scripts/scope_rules.py` no contienen ningún
  literal que gitleaks u otro escáner de secretos suela señalar: no hay
  claves, tokens, URLs con credenciales embebidas ni material criptográfico.
  Una inspección manual del código fuente (íntegro en los commits
  `8830028` y `718ce29`) no encuentra ningún candidato.
- Ningún archivo `.env`, `*.pem`, `id_rsa*` ni bajo `secrets/` se creó,
  leyó o modificó durante esta sesión (denegado además por
  `.claude/settings.json` `permissions.deny` si se intentara).

**Bloqueo residual para el coordinador.** Antes del cierre `APTO`, una
persona con acceso a GitHub debe capturar y versionar en
`evidence/WP-015/seguridad.md` (o en un archivo hermano bajo
`evidence/WP-015/**`) el resultado real del job `Escaneo de secretos` sobre
`TESTED_HEAD` (`718ce294fe592c2b6df7c13c5f56caea4199d7f2`) o sobre el head
final de la PR, con su `run_id`/conclusión, exactamente como exige el
contrato. Este agente no lo fabrica.

## 3. Ausencia de dependencias y lockfiles nuevos

`git show --stat` de ambos commits de `TESTED_HEAD` (`8830028e61b7`,
`718ce294fe59`) lista exactamente nueve archivos, todos `.py`, `.sh` o
`.md`, bajo `scripts/`, `tests/scope/` y `docs/manual/`. Ninguno es
`requirements.txt`, `Pipfile`, `pyproject.toml`, `poetry.lock`,
`package.json`, `package-lock.json`, `go.mod` ni ningún otro manifiesto de
dependencias. `scripts/check_scope.py` y `scripts/scope_rules.py` importan
exclusivamente módulos de la biblioteca estándar de Python 3
(`__future__`, `json`, `os`, `re`, `subprocess`, `sys`, `typing`); no hay
ningún `import` de un paquete de terceros en ninguno de los dos archivos
(verificable leyendo sus cabeceras, ya reproducidas íntegras en este
expediente vía los commits citados).
