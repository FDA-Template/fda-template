# WP-015 — Revisión independiente (GPT-6 Astra)

## Identidad y veredicto

| Campo | Valor |
|---|---|
| Revisor | GPT-6 Astra |
| Razonamiento | Alto |
| Contexto | Nuevo |
| Modo | Solo lectura |
| Fecha | 2026-09-27 |
| Base | `30939377590a3c3b49ba705ef0f20c4832df61bd` |
| Candidato revisado | `b1a8031bf715bff43239e7f835d396f301f5d5a2` |
| Tipo de revisión | Única revisión completa independiente de la implementación inicial |
| Veredicto | **NO APTO — cambios solicitados** |

La revisión se realizó conforme a
[`DEC-010`](../../specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md),
sin recibir como premisa una conclusión de aptitud del autor. Astra no modificó
archivos, no hizo commits, no cambió ramas y no delegó la revisión.

## Hallazgos autorizados para C1

### WP015-F1 — Bloqueante: LF elude patrones prohibidos recursivos

- **Ubicación:** `scripts/scope_rules.py`, traducción de `**` y del sufijo `/`.
- **Reproducción:** `evaluate("docs/a\nb.md", ["docs/*"], ["docs/**"])`
  permite la ruta; la CLI también devuelve exit `0` en un repositorio Git real.
- **Causa:** `.*` no consume LF sin `DOTALL`, mientras `[^/]*` sí lo hace.
- **Norma:** WP-015 §4, DEC-002, precedencia de prohibidos y nombres hostiles.
- **Corrección mínima:** hacer que `**` y `/` incluyan LF y añadir regresiones
  unitarias y de CLI para permitidos y prohibidos.

### WP015-F2 — Bloqueante: `.gitmodules` local puede ocultar gitlinks

- **Ubicación:** `scripts/check_scope.py`, `_diff_records`.
- **Reproducción:** el mismo rango con un gitlink `vendor` modificado pasa de
  exit `1` a exit `0` al crear un `.gitmodules` no versionado con
  `submodule.vendor.ignore=all`.
- **Norma:** WP-015 §2; diff completo e independencia del working tree.
- **Corrección mínima:** forzar `--ignore-submodules=none` y probar tanto
  `.gitmodules` no versionado como configuración local de ignorado.

### WP015-F3 — Media: parsers Git aceptan salidas truncadas o desconocidas

- **Ubicación:** `scripts/check_scope.py`, `parse_name_status_z` y
  `parse_ls_tree_z`.
- **Reproducciones aceptadas indebidamente:** falta de NUL final, estados
  `AWRONG`/`Rxxx`, ruta vacía y metadata `ls-tree` inválida.
- **Norma:** WP-015 §§1-2; salida truncada o registro desconocido es exit `2`.
- **Corrección mínima:** validar terminación NUL, rutas no vacías, gramática
  completa de estados/puntuaciones y estructura estricta de `ls-tree`, con
  regresiones que alcancen el código de salida CLI.

### WP015-F4 — Media: separadores Unicode fragmentan entradas del log

- **Ubicación:** `scripts/check_scope.py`, serialización JSON.
- **Reproducción:** una ruta con U+2028 produce varias entradas para lectores
  que usan `splitlines()`, incluida una línea independiente `VIOLACION`.
- **Norma:** WP-015 §1; strings escapados y no forja por rutas no ASCII.
- **Corrección mínima:** escapar U+0085, U+2028 y U+2029 —por ejemplo con
  `ensure_ascii=True`— y probar la salida completa junto con LF y tabulador.

### WP015-F5 — Media: el control AST omite APIs prohibidas

- **Ubicación:** `tests/scope/test_security_static.py`, `_analyze`.
- **Reproducción:** acepta `os.path.realpath("docs/link")` y `io.open`.
- **Norma:** WP-015 §5 y su verificación estática de APIs prohibidas.
- **Corrección mínima:** detectar las APIs y formas importadas pertinentes y
  añadir muestras negativas del propio analizador.

### WP015-F6 — Media: cobertura declarada pero no demostrada

- **Ubicación:** pruebas de CLI/biblioteca y
  `evidence/WP-015/{verification,symlinks}.md`.
- **Ausencias:** symlinks `M` y `R`; bytes UTF-8 realmente inválidos;
  ampliación del contrato propio comprometida en HEAD; identificadores de
  revisión y blob por estado de symlink.
- **Norma:** criterios de aceptación y evidencias exigidas de WP-015; caso
  vinculante de manipulación del contrato de DEC-002.
- **Corrección mínima:** añadir integraciones reales y regenerar la evidencia
  con revisión, modo, blob y veredicto concretos.

### WP015-F7 — Baja: el WP-ID admite dígitos Unicode

- **Ubicación:** `scripts/check_scope.py`, expresión regular de WP-ID.
- **Reproducción:** `WP-٩٠١` puede ser aceptado y devolver exit `0`.
- **Norma:** WP-015 §1 exige exactamente `WP-[0-9]{3}`.
- **Corrección mínima:** usar `[0-9]{3}` o semántica ASCII equivalente y una
  prueba negativa de CLI.

### WP015-F8 — Baja: falta el manifiesto JSON ordenado

- **Ubicación:** `evidence/WP-015/verification.md` y
  `tests/scope/generate-evidence-hashes.sh`.
- **Hecho:** existe una tabla Markdown y el generador produce texto; no existe
  el manifiesto JSON ordenado exigido por WP-015 §6.
- **Corrección mínima:** generar y versionar el manifiesto JSON ordenado,
  ligado explícitamente a `TESTED_HEAD`.

## Comprobaciones favorables independientes

- 95/95 pruebas y 4/4 controles AST existentes en verde.
- Shellcheck, manual y gobierno en verde; guard con 68 correctas, cero fallos
  nuevos y diez huecos conocidos.
- Código, pruebas y manual idénticos entre `TESTED_HEAD`
  `718ce294fe592c2b6df7c13c5f56caea4199d7f2` y el candidato revisado; los
  commits posteriores solo modifican evidencia.
- Literalidad de `docs/(draft).md`, comentarios, paréntesis y backticks conforme
  a DEC-012 en los casos examinados.
- Coste de `9.50 EUR` coherente con el estado `estimado`, artefacto y hash
  verificados, sin identidad ni secretos detectados.
- El escaneo externo se presenta correctamente como relativo a la base, no al
  candidato; el check del futuro head de PR sigue fuera de esta revisión.

## Transición

Los falsos verdes activan la parada contractual. La corrección requiere `C1`
abierto y versionado antes de editar. Después, esta misma Astra realizará una
revalidación enfocada de los ocho hallazgos y de sus efectos; no se repetirá la
revisión completa.
