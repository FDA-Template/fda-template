# Capacidades comprobadas y límites

Fecha: 2026-10-23. Preparación sin ejecutar producto o leer secretos.
No es calibración de un autor Codex ni prueba de confinamiento.

| Observación | Procedencia | Lo que acredita |
|---|---|---|
| Perfil: lectura de raíz del sistema; escritura en proyecto, visualizaciones y temporales; auto_review | Perfil comunicado al agente por plataforma | Capacidades declaradas, más amplias que seis archivos; no ensayo exhaustivo. |
| Lectura/edición documental y Git en copia temporal | Contrato 839877355aeb3556a3de5434bf27e178f458978e | Vía nativa disponible para documentos; no autoría de producto demostrada. |
| CLI instalado codex-cli 0.162.0-alpha.17.2 | command -v codex; codex --version, exit 0 con aviso de alias PATH | Versión instalada; no modelo o versión completa del runtime del chat. |
| Consulta GitHub ordinaria denegada y luego correcta con escalación revisada | gh api ref main, exit 1 y después exit 0 | Red del comando ordinario restringida; no ausencia universal de red/conectores. |
| Imagen existente e08cf999…520be8 | docker image inspect, exit 0 tras aprobación técnica | Imagen disponible; no ensayo actual de montajes o ejecución. |
| Socket Docker inaccesible sin escalación | docker image inspect, exit 1 ordinario | Lanzamiento requiere coordinación revisada; no acceso general del autor. |
| Conectores GitHub disponibles | Catálogo de herramientas de plataforma | No se acredita separación física de sus capacidades respecto al editor. No se probaron con mutaciones. |

No se inspeccionó configuración personal, autenticación, variables de entorno
o credenciales. No se intentó leer secretos como prueba negativa. No se cambió
permiso, perfil, hook, política de red o herramienta para conseguir verde.

La propuesta exige aceptar un editor de confianza supervisado con política y
revisión del diff. El perfil no acredita confinamiento físico por archivo,
home inaccesible, ausencia técnica de acceso a credenciales o imposibilidad de
modificar el evaluador. Los hashes detectan alteración, pero no impiden lecturas
ni restauran privacidad. El riesgo ha sido aceptado expresamente en autorizacion-adopcion.md; no queda
materializado un confinamiento físico por aceptarlo.

La ejecución futura conservaría Docker y sus pruebas de perímetro, que se
acreditarán para la configuración final. Ahora no se ha ejecutado producto,
pytest, Ruff o una invocación de autor.

## Documentación oficial consultada y abierta el 2026-10-23

- [Sandboxing](https://learn.chatgpt.com/docs/sandboxing): la frontera del
  sandbox se configura y se aplica a archivos y comandos; un nombre de modo
  no demuestra una lista de seis archivos.
- [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security):
  sandbox y aprobaciones son controles diferentes; una escalación puede ampliar
  capacidades. Hay que contrastar la configuración real.
- [Modelos de Codex](https://learn.chatgpt.com/docs/models) y
  [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol):
  identifican gpt-6.1-sol y esfuerzo medium como configuración válida; la
  disponibilidad depende de cuenta/cliente. Se propone fijarlo para el futuro
  autor, no se afirma que sea el modelo de este chat ni que ya se haya ejecutado.

El catálogo de colaboración de esta sesión enumera gpt-6.1-sol con medium.
La lectura de metadatos del chat no devolvió identidad de modelo; se conserva
desconocida para el coordinador actual en lugar de deducirla del CLI instalado.

Estas páginas describen el producto. El alcance concreto de esta sesión procede
del perfil y observaciones anteriores, no de asumir defaults. No se extrapola
el sandbox de comandos a todos los conectores/herramientas.

## Identidad y privacidad

Metadatos GitHub: canonical FDA-Template/fda-template, público, main
0205556be8ad9cd7993feeddd0b4347694cf37f8. Se usa una copia local nueva; la copia
personal permanece intacta. El expediente externo se conserva privado. Aquí
solo hay identificadores, importes estimados, rutas y hashes de trazabilidad,
sin código de producto/oráculo, raw, claves, audio, datos comerciales o de usuarios.
No se ha publicado esta propuesta.
