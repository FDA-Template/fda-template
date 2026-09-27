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

## 2. Escaneo de secretos — resultado sobre la base, capturado externamente

El contrato exige versionar "el resultado del job existente `Escaneo de
secretos` sobre `TESTED_HEAD` u otro commit anterior identificado", y que el
check verde del head final "se verifica externamente" — es decir, mediante
la API o la interfaz de GitHub Actions, no mediante una ejecución local de
gitleaks.

**Resultado capturado por el coordinador, sobre la base autorizada — no
sobre el candidato.** El entorno autorizado de este WP prohíbe red para el
autor, y ni la sesión de implementación inicial ni esta consolidación tienen
acceso a la API de GitHub ni a `gh`. El coordinador, con ese acceso, capturó
la siguiente ejecución existente del workflow `CI` sobre
`30939377590a3c3b49ba705ef0f20c4832df61bd` (la base autorizada de esta rama,
= `origin/main` en el momento de crear `wp/WP-015-check-scope-local`):

| Campo | Valor |
|---|---|
| Workflow | `CI` |
| `run_id` | `35900251941` |
| Run URL | `https://github.com/ivanes189/fda-template/actions/runs/35900251941` |
| Head SHA de la ejecución | `30939377590a3c3b49ba705ef0f20c4832df61bd` |
| Conclusión de la ejecución | `success` |
| Job | `Escaneo de secretos` |
| `job_id` | `107314291136` |
| Job URL | `https://github.com/ivanes189/fda-template/actions/runs/35900251941/job/107314291136` |
| Conclusión del job | `success` |
| `startedAt` | `2026-09-23T18:07:08Z` |
| `completedAt` | `2026-09-23T18:07:18Z` |
| Step `gitleaks` | `success` |
| Step `Ningún archivo de secretos versionado` | `success` |

Esto es exactamente «otro commit anterior identificado» en el sentido del
contrato: un resultado ya existente en GitHub, sobre un SHA anterior al
candidato, con identificador de ejecución y de job verificables.

**Qué NO afirma esta tabla, y por qué se dice expresamente.** El SHA
escaneado (`3093937...`) es la **base**, no el candidato: no incluye
`scripts/check_scope.py`, `scripts/scope_rules.py` ni ningún archivo de
`tests/scope/`, porque esos archivos no existían todavía en ese commit. Esta
tabla no sustituye, y no se presenta como si sustituyera, el check verde que
el **head final de una futura PR** de WP-015 deberá obtener sobre **sus
propios bytes**, verificado externamente en su momento. Lo único que
acredita aquí es que el mecanismo del job existe, está `success` sobre la
línea base, y que no hay ninguna razón estructural (secretos ya presentes,
job roto) para esperar que el candidato lo tiña de rojo.

**Lo que además se acredita localmente, sin red, sobre el propio candidato:**

- `scripts/check_scope.py` y `scripts/scope_rules.py` no contienen ningún
  literal que gitleaks u otro escáner de secretos suela señalar: no hay
  claves, tokens, URLs con credenciales embebidas ni material criptográfico.
  Una inspección manual del código fuente (íntegro en los commits
  `8830028` y `718ce29`) no encuentra ningún candidato.
- Ningún archivo `.env`, `*.pem`, `id_rsa*` ni bajo `secrets/` se creó,
  leyó o modificó durante esta sesión ni durante la de implementación
  inicial (denegado además por `.claude/settings.json` `permissions.deny`
  si se intentara).

**Bloqueo residual, más acotado que antes.** Sigue pendiente que una persona
con acceso a GitHub capture el resultado real de `Escaneo de secretos` sobre
`TESTED_HEAD` (`718ce294fe592c2b6df7c13c5f56caea4199d7f2`) o sobre el head
final de la PR que efectivamente se abra — el candidato, no la base—, con su
propio `run_id`/conclusión. Este agente no lo fabrica.

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
