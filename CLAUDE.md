# Constitución de la FDA

Normas que todo agente carga siempre. Son vinculantes y no se negocian en conversación.
Documento fundacional: [`docs/02-guia-fabrica-desarrollo-agentica.md`](docs/02-guia-fabrica-desarrollo-agentica.md).
Rumbo vigente: [`docs/03-hoja-de-ruta.md`](docs/03-hoja-de-ruta.md) — entregas supervisadas, medición y ampliación por necesidades demostradas. [`DEC-018`](specs/decisions/DEC-018-entregas-supervisadas.md) habilita el modo experimental únicamente tras fusión humana de su composición; la pausa ordinaria continúa. La procedencia histórica está en [`docs/04-analisis-conversaciones-ia.md`](docs/04-analisis-conversaciones-ia.md) y [`docs/05-analisis-investigacion-leandro-y-revalidacion.md`](docs/05-analisis-investigacion-leandro-y-revalidacion.md).
Manual de operación: [`docs/manual/MANUAL.md`](docs/manual/MANUAL.md).

**Preparación autorizada, excepción pendiente.**
[`DEC-019`](specs/decisions/DEC-019-preparar-autoria-codex.md) registra la
delegación documental de WP-020 desde reposo, con cuota desconocida.
[`ADR-002`](specs/adr/ADR-002-autoria-codex-supervisada.md) propone autoría
Codex para una sola continuación externa C4, todavía no autorizada. Preparar
o revisar esa propuesta no cambia el runtime, acepta su riesgo ni ejecuta
producto. Sigue rigiendo ADR-001 hasta aceptación e integración humanas.

**Orden de lectura obligatorio.** Esta constitución → [`docs/03-hoja-de-ruta.md`](docs/03-hoja-de-ruta.md) → [`docs/manual/MANUAL.md`](docs/manual/MANUAL.md) y el capítulo del modo aplicable → el WP → las decisiones y requisitos que gobiernan su alcance. Consultar la historia cuando resuelva una dependencia o contradicción; esta lectura dirigida no elimina ninguna restricción aplicable.

## Fuente de verdad

- La fuente de verdad es **este repositorio** (`specs/`, `work-packages/`, `specs/adr/`). La memoria conversacional no lo es.
- Todo el estado operativo vive en archivos versionados: `work-packages/ACTIVE`, estado de cada WP en su frontmatter, evidencias en `evidence/`. Nada de estado en la sesión.
- Si un dato no está en un archivo del repo, no existe. No lo asumas: pídelo.

## Alcance del trabajo

- Un agente trabaja sobre **un único WP aprobado**. Sin WP, no hay cambios.
- WP-019 es el acto documental delegado del operador definido en DEC-018 y su autorización versionada. No es ejecución ordinaria: no activa `ACTIVE`, no invoca el runtime en cuarentena ni habilita el piloto antes de la fusión humana. Cada piloto posterior necesita contrato, autoridad y controles propios según [manual 09](docs/manual/09-piloto-supervisado.md).
- Solo se modifican los archivos permitidos por el WP activo (`## Archivos permitidos`). El hook `.claude/hooks/guard.sh` da **feedback inmediato best-effort**: deniega en el momento las escrituras fuera de alcance que reconoce, y por eso sigue siendo obligatorio. **No es una garantía hermética**: falla abierto si no es ejecutable o si no llega a invocarse (`DEC-003` §1) y su analizador de `Bash` no cubre todos los vectores (`docs/manual/04-agentes.md`).
- **Estado del control de alcance:** `scripts/check_scope.py` existe como verificador local entregado por WP-015. Su integración como check requerido y el sandbox de operación autónoma siguen pendientes. **La protección de rama no comprueba el alcance del WP.** Se revisa el diff completo contra el contrato fijado previamente; la ejecución local del verificador no acredita un bloqueo de integración en CI. El piloto requiere su propio aislamiento demostrado antes de ejecutar código, según el manual 09.
- **Qué impone hoy la plataforma, y qué no.** No confundas cinco cosas distintas. *Impuesto técnicamente por el ruleset:* PR obligatoria, los tres checks bloqueantes, `non_fast_forward` y `deletion` bloqueados — **esas cuatro reglas son todo lo acreditado por el expediente actual**. *Práctica del operador, no impuesta:* la lectura del diff y la fusión humana. *Política vigente, no impuesta técnicamente:* la prohibición de esta constitución de que un agente fusione su propia PR. *Restricciones operativas actuales:* las allowlists de herramientas de `.claude/agents/*.md` y los workflows de agente desactivados (`DEC-003` §3); **no son garantía universal** mientras no se auditen todos los actores y credenciales. *Declarado necesario y todavía NO impuesto técnicamente:* al menos una aprobación humana y la revisión de `CODEOWNERS` —hoy `required_approving_review_count: 0` y `require_code_owner_review: false`, riesgo abierto de `DEC-003` con destino WP-011—. **Riesgo pendiente:** con cero aprobaciones exigidas, el ruleset **no impide por sí solo** que el autor de una PR la fusione si tiene permisos suficientes; **no lo des por impuesto**. **La capa de plataforma está por tanto parcialmente materializada, no entera.**
- Si necesitas tocar un archivo fuera de esa lista: **detente y solicita decisión**. No amplíes el alcance por tu cuenta.

## Calidad

- Todo cambio lleva pruebas. Toda función nueva lleva pruebas.
- Antes de dar nada por terminado, ejecuta los comandos de validación del WP y guarda las salidas en `evidence/WP-XXX/`.
- La deuda técnica se declara explícitamente. Deuda no declarada = trabajo no entregado.

## Autoría, revisión y correcciones

- Claude Code implementa y corrige; GPT-6 Astra revisa con contexto nuevo y en
  modo solo lectura. El revisor nunca modifica el candidato que revisa.
  Excepción acotada: el operador delega en Codex la autoría documental y las
  correcciones de WP-019; no cambia el runtime de implementación de ADR-001.
- Hay una sola revisión completa por candidato o transición. Después solo hay
  revalidaciones enfocadas, por la misma Astra, de las correcciones concretas y
  sus efectos directos.
- Una autorización de ejecución puede cubrir C1 y C2 si mantiene el mismo
  alcance, archivos permitidos, presupuesto y autoridad. Antes de cada pasada,
  su apertura queda versionada en `evidence/WP-XXX/ciclos.md`, incluso si la
  pasada acaba fallando o sin cambios.
- Tras C2 se para: la salida predeterminada es dividir, replanificar o cerrar
  `blocked`. C3 exige una decisión humana nueva, previa, fechada y versionada;
  no reinicia el contador ni autoriza C4.
- Un hallazgo no amplía autoridad: protegidos, cambios de contrato, presupuesto,
  `ACTIVE`, PRs y fusiones conservan sus autorizaciones separadas. Norma
  completa: [`DEC-010`](specs/decisions/DEC-010-separacion-autor-revisor-y-ciclos.md).
  Para el piloto de DEC-018, un WP puede agrupar los pasos reversibles y la
  apertura de su PR con autorización explícita; no incluye fusión, despliegue,
  permisos, gasto nuevo ni ampliación de alcance. `ACTIVE` sigue reservado al
  operador cuando corresponda.

## Prohibiciones absolutas

Nunca: exponer o leer secretos; modificar CI/CD, `CODEOWNERS` o permisos; fusionar tus propias PRs; hacer force-push; borrar historial; introducir deuda no declarada; desactivar o eludir hooks, linters o pruebas para que algo pase.

## Condiciones de parada obligatoria

Detente y solicita decisión humana ante: requisito ambiguo, contradicción entre requisitos, cambio de ADR necesario, migración con riesgo de pérdida de datos, vulnerabilidad detectada, pruebas inejecutables, coste fuera de presupuesto, o tercer ciclo de corrección.
Detalle y protocolo de cada una: [`docs/manual/05-bloqueos-y-parada.md`](docs/manual/05-bloqueos-y-parada.md).

## Ejecución headless

Nada en agentes, skills o hooks puede asumir una sesión interactiva. Todo comando de verificación debe poder ejecutarse sin humano delante (sin prompts, sin TTY, con código de salida significativo). Ver [`specs/adr/ADR-001-runtime.md`](specs/adr/ADR-001-runtime.md).

## Documentación

Todo cambio de proceso, contrato o agente actualiza `docs/manual/` en la misma PR. Manual desactualizado = PR incompleta.

## Convenciones

- Ramas: `wp/WP-XXX-descripcion` · Un WP = una rama = una PR.
- Commits: `WP-XXX: <cambio>` en imperativo, pequeños y atómicos.
- Evidencias: `evidence/WP-XXX/`. Coste: `evidence/WP-XXX/cost.md`.
- Decisiones: `specs/decisions/DEC-xxx.md` · Arquitectura: `specs/adr/ADR-xxx.md` · Requisitos: `specs/requirements/`.
