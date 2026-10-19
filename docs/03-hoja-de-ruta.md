# Hoja de ruta — FDA mediante entregas supervisadas

**Revisión:** 2026-10-19 · **Decisión:** [DEC-018](../specs/decisions/DEC-018-entregas-supervisadas.md).
**Vigencia:** el operador ha autorizado materializar y revisar esta composición.
El nuevo modo entra en vigor con la fusión humana de WP-019; antes de ella,
esta candidata no habilita ejecutar el piloto. La pausa ordinaria se conserva.
**Objetivo:** convertir necesidades del operador en mejoras utilizables,
demostrando calidad, coste e intervención humana antes de ampliar la fábrica.

## 1. Estado y siguiente entrega

| Elemento | Estado acreditado / siguiente acción |
|---|---|
| WP-015, comprobación local de alcance | Entregado; reutilizar. No es un check requerido de GitHub. |
| WP-014, diez acciones fijadas por SHA | Entregado. No demuestra aislamiento ni operación autónoma. |
| Pausa de DEC-003 | Continúa para operación ordinaria/autónoma. DEC-018 permite preparar el piloto supervisado con gates propios. |
| WP-016, WP-018 y OF1 | Fuera de la prioridad inmediata; no se reabren, ejecutan ni declaran resueltos. Mantienen contratos, costes e historia. |
| WP-019 | Composición documental de operador en revisión. `ACTIVE` de FDA permanece en reposo. |
| Primera entrega propuesta | Corregir descubrimiento de documentos anidados en `knowledge-base`; preparación en [expediente](../evidence/WP-019/piloto-kb.md). Aún no ejecutada. |
| Agent OS | Evolución prevista de AI-Comercial-System; no se crea ahora otro repositorio ni un núcleo general. |
| Hostelería / otros productos | No se abren como frentes paralelos de este piloto. No se declara validación comercial. |

La foto de recursos de WP-018 es la documentada en su expediente, no una
observación viva del proveedor. Posponer trabajo no apaga recursos ni acredita
coste de infraestructura cero. Cualquier revisión de recursos será de lectura;
su modificación exige alcance y autorización propios.

## 2. Qué se conserva

Contrato por entrega, estado versionado, alcance comprobable, pruebas,
separación autor/revisor, permisos mínimos, límites de gasto y fusión humana.
El aislamiento debe comprobarse antes de ejecutar código; un worktree solo
separa archivos. Ninguna candidata histórica no conforme se ejecuta o importa.
No se cambia CI, hooks, `CODEOWNERS`, permisos ni ADR-001 con esta reforma.

## 3. Qué cambia y por qué

La preparación de la operación autónoma deja de ser prerrequisito de toda
experiencia sobre producto. El piloto tendrá un perímetro menor, sin acceso a
producción ni capacidad de fusión o despliegue. No obtiene las garantías de una
plataforma autónoma por denominarse FDA.

La autorización de un encargo cerrado puede incluir preparación, rama,
implementación, verificación, C1/C2, publicación en el repositorio destinatario
y apertura de PR. Se registra una vez su alcance; no se pide permiso por cada
paso reversible incluido. Fusión, despliegue, gasto nuevo, permisos y cambios
de alcance siguen siendo decisiones separadas.

Se lee primero el estado actual y el contrato. Las decisiones históricas se
consultan por relevancia, conservando sus restricciones aplicables; no se
reconstruye todo el expediente en cada tarea. Se distinguen hechos, propuestas,
supuestos y capacidades todavía no verificadas.

## 4. Elección de tecnología

Antes de proponer un lenguaje o servicio, inspeccionar el proyecto y reutilizar
sus componentes adecuados. Para una decisión material comparar pocas opciones
viables: necesidad, coste de construcción y operación, mantenimiento, seguridad,
capacidad esperada y dificultad de cambiar después. Consultar documentación
vigente si la decisión depende de versiones, soporte, precios o compatibilidad.

Registrar brevemente recomendación, motivo, alternativa descartada, incertidumbre
y señal concreta que justificaría revisarla. Una duda decisiva puede resolverse
con una prueba pequeña presupuestada. No prometer una solución universalmente
óptima ni añadir infraestructura por un crecimiento hipotético. El operador
decide utilidad, prioridades y gasto; no sustituye una revisión técnica experta.

## 5. Secuencia de trabajo

1. **WP-019: concretar el cambio de rumbo.** Una PR documental con revisión
   independiente. Integración humana; no activa por sí sola un piloto.
2. **Primera entrega externa pequeña.** Preparar el WP de `knowledge-base`,
   fijar revisión de origen, criterios, presupuesto, runtime y controles del
   entorno. Ejecutar solo cuando los gates del [manual 09](manual/09-piloto-supervisado.md)
   estén aprobados y acreditados. Obtener un cambio probado y revisable; después integración
   humana en el repositorio destinatario. No migrar toda la FDA a ese repositorio.
3. **Una función útil en el proyecto comercial.** Tras esa primera experiencia,
   acordar con el operador un recorrido observable de AI-Comercial-System.
   Evitar una limpieza general, una migración de arquitectura o Agent OS como
   requisitos previos si no son necesarios para ese recorrido.
4. **Medición sobre hasta cinco tareas reales.** Las tareas aportan valor desde
   la primera; cinco no es un gate previo al producto ni una prueba estadística
   de rentabilidad. Comparar tareas de dificultad semejante con un flujo mínimo
   seguro, registrando diferencias de modelo, alcance y riesgo.
5. **Mejorar el cuello de botella demostrado.** Recuperar trabajo de plataforma
   solo si un fallo observado o la siguiente capacidad autorizada lo exige.
   Antes de retomar WP-016/018, comparar de forma acotada su coste y sus garantías
   con alternativas para el nivel de autonomía requerido. No rebajar su contrato
   por conveniencia ni presentar una revisión humana como control automático.
6. **Agent OS y escala.** Extraer componentes comunes cuando dos agentes de
   negocio diferentes los utilicen realmente. La orquestación propia conserva
   los gates M1/M2/M3 y el veto de ADR-001; no se prescribe aquí una nueva pila.

**Límites desde la fusión de WP-019, sin esperar al fin de la pausa:** a los dos
días laborables revisar si el primer WP está listo. Si solo crece preparación,
reducir el alcance o elegir una tarea más sencilla; no abrir infraestructura
automáticamente. A los diez días laborables realizar el balance aunque no haya
entregas, contando también los bloqueos. Son puntos de decisión, no promesas de
plazo ni autorizaciones por silencio. No se programa una automatización aquí.

Como límite inicial de prioridad, no abrir dos WPs consecutivos sobre la FDA
sin una entrega externa entre ellos. Una necesidad de seguridad puede justificar
una excepción concreta registrada, con trabajo mínimo y criterio de salida.

## 6. Riesgo y revisión proporcional

Cambios reversibles y aislados: contrato breve, pruebas pertinentes y una
revisión independiente. Cambios de auth, red, secretos, entrada no confiable,
datos persistentes, dependencias o controles: lente de seguridad obligatoria y
especialista humano cuando la decisión exceda una aprobación de negocio.

Se registra la clasificación y su razón en el WP; construir un clasificador
automático no es condición del piloto. No se ejecutan migraciones destructivas,
cambios de permisos o despliegues dentro del piloto. La revisión bloquea por
incumplimiento de aceptación, seguridad o evidencia inválida; mejoras laterales
se registran sin ampliar el encargo. C1/C2 mantienen la regla de DEC-010.

## 7. Métricas y criterio para continuar

Por tarea: resultado demostrado, estado (preparado/probado/integrado/disponible),
tiempo transcurrido, minutos humanos, consumo de todos los autores y revisores,
intentos fallidos, correcciones, defectos posteriores y violaciones de alcance.
Separar factura adicional, consumo de cuota y tiempo humano. Desconocido no es
cero; sin datos comparables no se afirma ahorro ni rentabilidad.

La continuación exige entregas correctas y un coste/intervención compatibles
con el presupuesto acordado. Si las tareas pequeñas siguen exigiendo días de
preparación o dirección constante, simplificar el mecanismo responsable antes
de ampliarlo. No extrapolar autonomía profesional desde una sola entrega.

## 8. Riesgos y decisiones de parada

| Señal | Respuesta |
|---|---|
| Entorno sin aislamiento demostrado, acceso indebido o pruebas inválidas | No ejecutar/integrar; corregir el perímetro o reducir la tarea. |
| Gasto sin autorización o sin medición exigida | Detener llamadas facturables; no inventar cifras. |
| Tercer ciclo, cambio de alcance o ADR necesario | Replanificación humana; no reiniciar contadores. |
| Dos días de preparación sin WP listo | Decidir reducción; no convertir un plazo en otra ampliación. |
| Diez días sin resultado útil | Registrar el fracaso del experimento y revisar el método. |
| Riesgo de perder trabajo previo | Preservar candidatas y ramas; ninguna limpieza queda autorizada. |

## 9. Procedencia e historial

La autorización de cambio es el encargo del operador de 2026-10-19 registrado
en [WP-019](../work-packages/WP-019-ruta-piloto-supervisado.md), ampliado por la
[autorización precisa](../evidence/WP-019/autorizacion.md) para pausa y coste.
[DEC-018](../specs/decisions/DEC-018-entregas-supervisadas.md) define precedencia
y vigencia; el [manual 09](manual/09-piloto-supervisado.md) explica la operación.

La v2 completa, sus revisiones y anexos permanecen en
[Git, base 91d4a7c](https://github.com/FDA-Template/fda-template/blob/91d4a7c8af855ebac146c59310e44a20a8e160e4/docs/03-hoja-de-ruta.md).
Las decisiones DEC-001 a DEC-017 y evidencias históricas se conservan. Las
referencias antiguas a etapas de v2 se interpretan contra esa versión, no como
órdenes actuales que bloqueen el piloto. Fuera de DEC-018 conservan su efecto.

La investigación anterior vive en [04](04-analisis-conversaciones-ia.md) y
[05](05-analisis-investigacion-leandro-y-revalidacion.md). No se actualizan esas
fotos fijas ni se reutilizan sus porcentajes o plazos como mediciones presentes.
