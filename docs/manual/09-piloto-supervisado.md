[← Manual](MANUAL.md)

# 09 — De una necesidad a una entrega supervisada

Rige exclusivamente el modo experimental de
[DEC-018](../../specs/decisions/DEC-018-entregas-supervisadas.md), después de su
fusión humana. No acredita salida de la pausa ni una plataforma autónoma lista.

## 1. Cómo encargar trabajo

El operador explica qué quiere conseguir en una tarea vinculada al repositorio
destinatario. El coordinador consulta código y documentación, y pregunta solo
por decisiones de negocio que no pueda resolver con las fuentes disponibles.
No exige que el operador elija lenguajes o bibliotecas sin una recomendación.

Ejemplo de petición, no autorización ya concedida: «Quiero descargar las
oportunidades pendientes para revisarlas en Excel. Examina lo existente,
propón el cambio más pequeño que resuelva esto y cómo comprobaremos el resultado».

## 2. Decidir una solución proporcionada

Primero reutilizar la arquitectura adecuada existente. Si hace falta una
decisión material, registrar en el WP unas pocas alternativas, recomendación,
motivo, coste total estimado, limitaciones, riesgo, capacidad esperada y señal
para revisar la decisión. Declarar supuestos e incertidumbre; consultar fuentes
actuales para soporte, precios o compatibilidad. Una prueba exploratoria requiere
alcance y presupuesto propios dentro del mismo encargo, no autorización abierta.

Lo profesional incluye pruebas, seguridad y mantenimiento. Escalar significa
soportar el crecimiento previsto y conservar una vía de ampliación comprobable.
La IA no garantiza la mejor opción universal. Una decisión ya aceptada no se
reabre por preferencia de un modelo nuevo sin evidencia relevante.

## 3. Gates antes de ejecutar

| Gate | Evidencia necesaria |
|---|---|
| Encargo | WP aprobado, revisión de origen fija, resultado, rutas, exclusiones, comandos, riesgo y rollback. |
| Autoridad | Acciones incluidas, quién ejecuta/revisa/publica e identidad del humano que acepta y fusiona. La autorización queda registrada en el repo destinatario. |
| Presupuesto | Techo y fuente de coste admitida antes de invocar al autor; sumar intentos y revisiones, con margen dentro del techo. Sin gasto nuevo autorizado no se crean servicios ni se hacen llamadas de pago. |
| Runtime | Claude Code conforme a ADR-001; versión, acceso y disponibilidad comprobados sin leer secretos. Codex como coordinador no implica migración de runtime. |
| Entorno | Entorno desechable con escritura limitada al proyecto y pruebas; sin credenciales de GitHub/producción, sin home del operador montado y sin permisos de fusión, despliegue o administración. |
| Red y datos | Datos sintéticos o autorizados; red del código bajo prueba cerrada salvo destinos explícitos imprescindibles. La conexión del runtime al proveedor del modelo se distingue del acceso del código a la red. No se presume aislamiento por usar worktree. |
| Verificación del perímetro | Pruebas inocuas negativas demuestran denegación fuera de la raíz y de red no autorizada, sin intentar leer secretos. Registrar capacidades reales y fallos; ninguna solicitud de escalación amplía el piloto. |
| Aceptación | Casos que fallan antes y pasan después, regresiones pertinentes y demostración reproducible; evaluador conservado fuera de la autoridad de modificación del implementador. |

Un gate pendiente deja el WP sin ejecutar. La preparación de lectura puede
continuar; no se construye un orquestador para solucionar el gate por defecto.
Si el entorno disponible no puede cumplirlo, reducir la tarea o elegir un
entorno existente apto mediante decisión concreta. No declarar capacidades
instaladas por la mera existencia de este manual.

## 4. Contrato y autorización agrupada

Un WP breve en el repositorio destinatario fija: objetivo, aceptación,
permitidos/prohibidos, base Git, herramientas/red/datos, presupuesto, ciclos,
responsables, verificación y rollback. El operador aprueba el resultado,
prioridades y límites; la revisión técnica no se delega a su intuición.

La aprobación puede incluir los pasos reversibles enumerados: rama, ejecución,
pruebas, registro de evidencias, C1/C2, publicación y apertura de PR. No implica
fusión, despliegue, compras, permisos, migraciones destructivas ni cambios de
contrato. Una sola aprobación de alcance no elimina los controles técnicos de
las herramientas ni autoriza a eludirlos.

Si el destinatario utiliza `ACTIVE`, el operador registra su transición dentro
del acto autorizado de apertura y la revierte al cerrar; el implementador no
la puede modificar. `ACTIVE` de `fda-template` sigue en reposo. Contrato y
pruebas de aceptación se fijan antes de implementar, y el revisor contrasta
contra esa versión, no contra una modificación propuesta por el autor.

## 5. Ejecución, revisión y entrega

El implementador desarrolla y prueba dentro del perímetro. Una única revisión
Astra con contexto nuevo y solo lectura evalúa contrato, corrección y evidencia;
añade la lente de seguridad según riesgo. Para IAM, seguridad crítica o
decisiones difíciles de revertir, hace falta criterio técnico humano antes de
ampliar el piloto, que actualmente excluye esas mutaciones.

Tras hallazgos, C1/C2 se registran antes de empezar y la misma revisora verifica
correcciones y efectos directos. Los fallos de arranque se etiquetan para medir
su causa, pero no borran costes ni reinician el contador establecido por
DEC-010. Tras C2 sin conformidad se replantea; no se abre C3 por silencio.

Antes de publicar, el coordinador comprueba el diff completo contra el contrato
fijado, los resultados y la ausencia de datos sensibles. Se aprovecha
`check_scope` cuando su modo de lectura del contrato desde merge-base es
aplicable; si no, se registra la revisión explícita del alcance, sin fingir
que existe un check requerido. El ejecutor no posee la credencial de publicación.
La rama/PR y evidencias privadas permanecen en el repositorio destinatario.

El operador recibe demostración, límites, revisiones, coste y forma de revertir.
La integración es humana y respeta los checks existentes. Probar en aislamiento,
fusionar y poner a disposición de usuarios son hitos distintos; ninguno se da
por completado por el anterior.

## 6. Medición y aprendizaje

Una ficha por entrega: estado, resultado observable, tiempo transcurrido,
minutos humanos, fuentes de coste de autor/revisor, intentos fallidos,
correcciones, defectos e incidentes. Factura adicional, cuota de suscripción y
tiempo humano se informan separadamente. No hay cifra sin fuente.

DEC-001/004 siguen gobernando el coste de las ejecuciones. La excepción
documental de DEC-018 es solo WP-019 y no habilita un piloto con medición de
coste ausente. Las métricas humanas desconocidas se declaran como tales; no se
computan como cero ni permiten afirmar rentabilidad o cumplimiento de metas.

Revisar preparación a los dos días laborables de la fusión de WP-019 y resultados
a los diez, incluso si no hubo entrega. Son puntos de decisión, no autorización
para correr, ampliar gasto o declarar éxito. Un bloqueo persistente debe producir
una propuesta concreta de reducción, no otra plataforma general.

## 7. Primera candidata y siguiente paso

[La preparación de knowledge-base](../../evidence/WP-019/piloto-kb.md) identifica
un defecto pequeño y criterios verificables. Tras aceptar WP-019, el siguiente
trabajo es fijar su contrato, presupuesto y entorno en el repositorio
destinatario. No copiar allí toda la documentación de FDA; enlazar esta versión
e incorporar solo las reglas y controles aplicables.

Después de esa mejora técnica se acuerda un recorrido útil de AI-Comercial-System.
Hasta cinco entregas aportan una muestra exploratoria, sin retrasar el producto
hasta completar la muestra. Agent OS y la infraestructura nueva requieren una
necesidad observada o una garantía indispensable para la siguiente operación.
