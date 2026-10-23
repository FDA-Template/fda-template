# ADR-002 — Excepción propuesta de autoría Codex supervisada

**Estado:** proposed, sin vigencia operativa. **Fecha:** 2026-10-23.
**Ámbito:** una única C4 propuesta del WP-005 externo de acceso local sin audio
de `ivanes189/voice-gateway`; no afecta al WP-005 de FDA ni a otros proyectos.
**Relación:** sustitución parcial de la elección Claude Code de ADR-001 solo
si se acepta e integra esta excepción; invariantes I1-I4 intactos.

## Contexto

El método usado para esta entrega no ha producido una entrega válida. C0/C1
se detuvieron antes de usar herramientas; C2 solo leyó; C3 produjo tres archivos
parciales y terminó por límite de interacciones. Siguen pendientes integración,
pruebas propias, guía y hallazgos de revisión. El expediente y el presupuesto
se conservan. Esto acredita un fallo del circuito concreto, no que Claude sea
incapaz ni que cambiar de modelo garantice mejores resultados.

Se autoriza preparar esta alternativa, no ejecutarla. Adoptarla requiere
aceptar las diferencias de confianza de la edición nativa y la cuota desconocida.

## Alternativas y recomendación

| Alternativa | Consecuencia |
|---|---|
| Mantener blocked | Sin nuevo intento; preserva límites y deja la funcionalidad incompleta. |
| Otra llamada Claude con el circuito actual | Repite la vía que falló; no se autoriza ni se propone calibración adicional. |
| Una continuación Codex nativa, supervisada | Elimina el puente MCP y su corte de interacciones; exige aceptar capacidades de host más amplias y coste de cuota no atribuible. |

Se recomienda presentar la tercera al operador como excepción de una sola
entrega. No construir un runtime, runner, interfaz de gobierno o aislamiento
nuevo para probarla. La recomendación no equivale a elegir por él el riesgo.

## Decisión propuesta y condiciones de entrada

Codex podría editar y corregir durante una sola pasada C4, con las seis rutas
de producto del contrato externo. Configuración propuesta del autor:
GPT-6.1 Sol, `gpt-6.1-sol`, esfuerzo `medium`, en un contexto nuevo del agente
implementer. Es una elección propuesta explícita, no la identidad supuesta
del coordinador actual. Se comprobará disponibilidad sin una calibración
facturable y se registrará la configuración al abrir C4; si no está disponible,
no sustituirlo por otro modelo por silencio. La misma Astra que revisó C3 comprobaría
hallazgos y efectos directos sin modificar el candidato. La autoría y revisión
documentales de WP-020 son un encargo distinto, con su propio contador.

Antes de ejecutar deben existir: aceptación humana específica de los cuatro
puntos de DEC-019 §3; fusión humana de esta composición; contrato y autorización
privados fijados; apertura C4 versionada; perfil real del autor, procedencia del
modelo/configuración y origen parcial registrados sin leer secretos; imagen y
pruebas de perímetro del código acreditadas. Falta de un dato obligatorio:
no ejecutar ni inventarlo. “Codex” identifica el producto, no un modelo exacto;
la versión del CLI instalado tampoco identifica el modelo que escribe.

La pasada conserva criterios y comandos del contrato fijado; no habilita voz,
micrófono, red de producto o proveedores. Se registra un límite operativo de
45 minutos desde la apertura hasta la entrega del candidato por el autor,
comprobado por el coordinador; no es un corte técnico del runtime ni una
garantía de coste. Interrupción o incumplimiento: C4 consumida, blocked.
Después de la revisión no hay C5 implícita, aunque sobren euros o cuota.

## Dos perímetros, con garantías diferentes

**Edición nativa:** el perfil disponible permite lecturas del sistema y
escrituras en raíces más amplias; hay conectores privilegiados disponibles.
Se prohíbe al autor usar secretos, conectores, publicación, escalaciones para
ampliar acceso o escrituras fuera de seis rutas. Son límites de autoridad y
comprobación posterior, no una barrera física por archivo o una separación
técnica acreditada de credenciales. El agente que edita debe considerarse de
confianza dentro de ese perfil; una copia Git separada no cambia ese hecho.
La revisión no puede eliminar el riesgo de una lectura indebida ya realizada.

**Código ejecutado:** toda importación de producto, pruebas y Ruff continúa en
Docker desechable, usuario no root, red none, raíz de solo lectura, sin home,
secretos o socket Docker montados. La coordinación controla el lanzamiento
limitado a la imagen y montajes fijados. No se ejecuta producto en el host.
Pruebas inocuas de perímetro y hashes antes/después siguen siendo necesarias;
un Docker correcto no demuestra confinamiento del editor nativo.

El evaluador y las regresiones permanecen fuera de la lista autorizada del
autor, fijados por hash y contrastados contra el origen. No se afirma que el
host impida modificarlos: cualquier diferencia invalida la candidata. Se
repite la verificación de forma independiente sobre el código final.

No se cambian perfiles, permisos, hooks o CI. Si solo se acepta autoría con
confinamiento físico de seis archivos, esta opción queda bloqueada: no se
promete instalarlo como resultado de aceptar ADR-002.

## Coste, utilidad y revisión de la decisión

Se propone declarar no_disponible la cuota de autoría y revisión Codex, sin
equivalencia monetaria inventada ni F1 de Claude. No se autorizan llamadas
Claude, APIs facturables, compras o servicios. La propuesta económica solo
valdría para C4 tras aceptación humana, nunca como excepción general de coste.
Los consumos anteriores y el techo original del piloto permanecen registrados.
No se calcula rentabilidad ni se afirma gratuidad.

La señal de utilidad es una entrega integrada y aceptada del acceso local,
con pruebas y guía, no la existencia de este ADR. No se extiende a otro encargo
por éxito o por vencimiento del plazo. Tras el resultado se decide con datos;
si no hay entrega, conservar el bloqueo sin otra excepción automática.

## Consecuencias y reversión

Ventaja esperada: herramientas directas y menos pasos de transporte. Riesgos:
acceso nativo más amplio, coste de cuota desconocido y nueva parada sin entrega.
Ninguna ventaja está demostrada todavía por una ejecución Codex de producto.

Descartar antes de adoptar no altera el producto. Después de adoptar, detener
primero cualquier ejecución y retirar conjuntamente la excepción y sus avisos.
El régimen general sigue siendo ADR-001; retirar ADR-002 no reabre Claude ni
concede presupuesto. Historial y ciclos permanecen en archivos versionados.
