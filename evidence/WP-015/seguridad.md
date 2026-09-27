# WP-015 — Seguridad: AST, escaneo de secretos y dependencias

## 1. Análisis estático AST (`tests/scope/test_security_static.py`)

Analiza con el módulo `ast` de la biblioteca estándar, sin ejecutar ningún
código de los dos módulos, exactamente `scripts/check_scope.py` y
`scripts/scope_rules.py`. Prohíbe:

- llamadas a `eval`, `exec`, `compile`, `__import__`, `open` (nombres bare);
- llamadas por atributo a `os.system`, `os.popen`, `os.listdir`, `os.walk`,
  `os.scandir`, `os.readlink`, `os.path.exists`, `os.path.isfile`,
  `os.path.isdir`, `os.path.islink`, `os.path.lexists`, `os.path.realpath`,
  `os.stat`, `os.lstat`, `os.fstat`, `subprocess.call`, `subprocess.check_call`,
  `subprocess.check_output`, `subprocess.Popen`, `subprocess.getoutput`,
  `subprocess.getstatusoutput`, `io.open`;
- cualquier invocación con la palabra clave `shell=True`;
- importar `pathlib`;
- las mismas operaciones anteriores invocadas a través de un alias de
  importación —`from os.path import realpath as rp; rp(...)`— o de un alias
  de módulo —`import os.path as p; p.realpath(...)`—.

**`WP015-F5` (revisión Astra, C1).** Las dos últimas líneas (`os.path.realpath`,
`io.open` y la resolución de alias) se añadieron en C1: el analizador
original solo reconocía la forma dotted literal y una lista fija de nombres
bare, y ni `os.path.realpath` ni `io.open` estaban en esa lista, de modo que
una llamada directa a cualquiera de las dos, o la misma llamada tras un
alias de import, pasaba desapercibida. `TestAnalyzerNegativeSamples` (9
pruebas) demuestra con fuentes sintéticas —nunca ejecutadas, solo
analizadas— que las siete formas señaladas por Astra se detectan, y dos
controles negativos (`subprocess.run(..., shell=False)` y un alias de un
módulo no prohibido) demuestran que no se prohíbe nada sin justificación
contractual.

Resultado real (comando 6 de `verificacion-c1.log`, dentro de la ejecución
de 134 pruebas):

```
test_check_scope_has_no_forbidden_apis (test_security_static.TestSecurityStatic.test_check_scope_has_no_forbidden_apis) ... ok
test_check_scope_parses_as_valid_python (test_security_static.TestSecurityStatic.test_check_scope_parses_as_valid_python) ... ok
test_scope_rules_has_no_forbidden_apis (test_security_static.TestSecurityStatic.test_scope_rules_has_no_forbidden_apis) ... ok
test_scope_rules_parses_as_valid_python (test_security_static.TestSecurityStatic.test_scope_rules_parses_as_valid_python) ... ok
```

más las 9 muestras negativas de `TestAnalyzerNegativeSamples`, también en
verde (ver el listado completo en `verificacion-c1.log`). Trece de trece:
ningún hallazgo en ninguno de los dos módulos de producción, y el analizador
demuestra positivamente que sabe fallar ante las formas que antes eludía.

**`WP015-F4` (revisión Astra, C1) — separadores Unicode en la salida JSON.**
`scripts/check_scope.py._emit_json` serializa ahora con
`json.dumps(obj, sort_keys=True, ensure_ascii=True)`. Antes, con
`ensure_ascii=False`, una ruta con U+0085, U+2028 o U+2029 se emitía como el
byte Unicode literal; los tres son límites de línea para
`str.splitlines()` (y U+2028/U+2029 para el estándar Unicode de límites de
línea en general), de modo que un lector que no reconstruyera el JSON de
verdad podía leer una sola violación como si fueran varias líneas de log,
incluida una línea `VIOLACION` forjada. Con `ensure_ascii=True` todo carácter
no ASCII se escapa como `\uXXXX`: la línea física sigue siendo una sola.
Esto no tiene una prueba dedicada nueva en `test_security_static.py` —no es
una API prohibida, es un parámetro de serialización—; su corrección está
cubierta transversalmente porque cada línea JSON de las 134 pruebas de la
batería pasa por esa misma función, y de forma más directa por
`test_embedded_newline_does_not_forge_log_lines` (que ya cubría LF antes de
C1 y sigue en verde) y por la ausencia de cualquier regresión en las
aserciones de `json.loads(...)` de toda la suite, que dependen de que la
línea sea JSON válido de una sola pieza.

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
  `8830028`, `718ce29` y, para las correcciones de C1, `513d68c`) no
  encuentra ningún candidato.
- Ningún archivo `.env`, `*.pem`, `id_rsa*` ni bajo `secrets/` se creó,
  leyó o modificó durante esta sesión ni durante la de implementación
  inicial (denegado además por `.claude/settings.json` `permissions.deny`
  si se intentara).

**Bloqueo residual, más acotado que antes.** Sigue pendiente que una persona
con acceso a GitHub capture el resultado real de `Escaneo de secretos` sobre
el `TESTED_HEAD` vigente (`513d68c422a9d8380e0100944e7eb68d8f42ece9`, tras
`C1`) o sobre el head final de la PR que efectivamente se abra — el
candidato, no la base—, con su propio `run_id`/conclusión. Este agente no lo
fabrica.

## 3. Ausencia de dependencias y lockfiles nuevos

`git show --stat` de los tres commits del candidato (`8830028e61b7`,
`718ce294fe59` y, para `C1`, `513d68c422a9d`) toca exactamente nueve rutas
distintas en total (las dos primeras las crean; la tercera solo las
modifica, no añade ninguna nueva), todas `.py`, `.sh` o `.md`, bajo
`scripts/`, `tests/scope/` y `docs/manual/`. Ninguna es
`requirements.txt`, `Pipfile`, `pyproject.toml`, `poetry.lock`,
`package.json`, `package-lock.json`, `go.mod` ni ningún otro manifiesto de
dependencias. `scripts/check_scope.py` y `scripts/scope_rules.py` importan
exclusivamente módulos de la biblioteca estándar de Python 3
(`__future__`, `json`, `os`, `re`, `subprocess`, `sys`, `typing`); no hay
ningún `import` de un paquete de terceros en ninguno de los dos archivos
(verificable leyendo sus cabeceras, ya reproducidas íntegras en este
expediente vía los commits citados).
