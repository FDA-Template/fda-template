# WP-015 — Aislamiento: `HEAD` y huella NUL antes/después

## Mecanismo

`tests/scope/run-suite.sh` calcula, antes y después de ejecutar la suite
completa (`python3 -m unittest discover -s tests/scope -p 'test_*.py' -v`):

```bash
head_antes="$(git rev-parse HEAD)"
estado_antes="$(git status --porcelain=v1 -z -uall | shasum -a 256)"
# ... ejecuta la suite ...
head_despues="$(git rev-parse HEAD)"
estado_despues="$(git status --porcelain=v1 -z -uall | shasum -a 256)"
```

y falla (`exit 1`, "FALLO AISLAMIENTO") si cualquiera de las dos huellas
difiere, incluso si las 95 pruebas pasan.

## Ejecución real, C3 (comando 6 de `verificacion-c3-literal.log`)

```text
--- HEAD antes: 333eb072e62f3298f465c32c9d47a69b043cb8c1 ---
[... 152 pruebas, todas "ok" ...]
--- HEAD después: 333eb072e62f3298f465c32c9d47a69b043cb8c1 ---

RESULTADO: OK (pruebas en verde, aislamiento intacto)
```

El script comparó además la huella NUL de
`git status --porcelain=v1 -z -uall` antes y después. El conjunto de rutas era
idéntico; durante la captura ya existía el log C3 no rastreado, pero su
contenido no forma parte de la salida de `git status`. Ningún repositorio de
prueba, fixture ni configuración local sobrevivió fuera de sus temporales.

## Ejecución real, C1 (comando 6 de `evidence/WP-015/verificacion-c1.log`)

```
--- HEAD antes: 513d68c422a9d8380e0100944e7eb68d8f42ece9 ---
[... 134 pruebas, todas "ok" ...]
--- HEAD después: 513d68c422a9d8380e0100944e7eb68d8f42ece9 ---

============================================================
 RESULTADO: OK (pruebas en verde, aislamiento intacto)
============================================================
```

`HEAD` es idéntico byte a byte antes y después:
`513d68c422a9d8380e0100944e7eb68d8f42ece9` (`TESTED_HEAD` de C1). La misma
propiedad se acreditó previamente para el `TESTED_HEAD` de la implementación
inicial (`718ce294fe592c2b6df7c13c5f56caea4199d7f2`), con idéntico mecanismo.

En el instante de esa ejecución, el worktree estaba exactamente en el estado
de `TESTED_HEAD` (sin archivos de evidencia todavía, que se escriben en un
paso posterior de este mismo procedimiento): `git status --porcelain=v1 -z
-uall` produjo la cadena vacía tanto antes como después de la suite, de modo
que sus huellas SHA-256 coinciden trivialmente por ser el mismo flujo de cero
bytes en ambos casos — el valor conocido y documentado
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (SHA-256
de la cadena vacía), no un valor que haya sido necesario calcular aquí para
esta constancia. El propio script comparó ambas huellas internamente
(`shasum` anidado dentro de `bash tests/scope/run-suite.sh`, invocación ya
permitida) y devolvió exit `0` con el mensaje explícito "aislamiento
intacto"; no se relajó ni se omitió esa comparación.

## Por qué es válido: cada repositorio de prueba es su propio `mktemp -d`

`tests/scope/_repo.py` (`TempRepo.__init__`) crea cada repositorio con
`tempfile.mkdtemp(prefix="wp015-scope-")`, fuera de la raíz del repositorio
FDA. Todas las mutaciones Git de las pruebas (`init`, `config`, `add`,
`commit`, `mv`, `rm`) se ejecutan con `cwd=self.path` (el directorio temporal),
nunca contra el repositorio FDA. `TempRepo.cleanup()` (invocado en
`tearDown()` de cada test, y también mediante el gestor de contexto
`__enter__`/`__exit__`) borra únicamente ese directorio temporal propio
(`shutil.rmtree(self.path, ...)`). No se usan remotos ni red en ningún
repositorio temporal (`git init` local, sin `git remote add` en ningún punto
del código).

## Qué demuestra, y qué no

Demuestra que **ejecutar la suite completa de WP-015 no modifica el
repositorio FDA**: ni su `HEAD`, ni el conjunto de rutas Git visibles
(`git status --porcelain=v1 -z -uall`), ni sus bytes rastreados o sin
rastrear. No demuestra nada sobre metadatos de sistema de archivos no
capturados por `git status` (modo, propietario, marcas temporales) de
archivos ajenos al repositorio FDA; eso no es relevante aquí porque ningún
repositorio temporal de la suite comparte inodos ni rutas con el árbol FDA.
