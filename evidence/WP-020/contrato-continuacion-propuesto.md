# Borrador de enmienda: C4 excepcional del WP-005 externo

**Estado:** draft, NO EJECUTABLE. No es un WP nuevo ni se registra ahora en el
producto. Instancia: WP-005-acceso-local de `ivanes189/voice-gateway`, no el
WP-005 de alcance en CI de FDA. Autor autorizado condicionalmente: Codex nativo; revisora: misma
GPT-6 Astra Alto que revisó C3, independiente y solo lectura. Configuración
autorizada del autor: GPT-6.1 Sol, gpt-6.1-sol, esfuerzo medium, contexto nuevo
del agente implementer; disponibilidad/configuración se verifican antes de C4.

## Objetivo y origen

Terminar el mismo acceso local sin audio: página en español que explica audio
pendiente y conexión autorizada que responde unavailable y termina. Por defecto
se conserva la aplicación telefónica. Sin micrófono, voz, proveedores o Internet.

Base de producto original: fd516bddc9395ac8c0d44fd3dd1764063ec17fbd.
Contrato técnico: 7e77f82a85d56860d30e09707331fcce184d41f2.
Código parcial C3 revisado: 834a8b5; cierre/evidencia conservados hasta
b173052813c469a77679e3505a811b3cc6216af9. Antes de ejecutar se comprobará la
base vigente del destino y se fijará el origen real; una diferencia material
exige replantear antes de editar. No se adopta automáticamente una base antigua.

C0/C1/C2/C3 consumidos. Estado actual blocked 3/3, C4 autorizada únicamente
tras fusión humana y gates conformes, todavía sin abrir. La enmienda privada
conservará el cierre histórico y añadirá el permiso recibido y la fila C4
abierta antes de editar; 3/4 antes y 4/4 tras consumir. No C0 nuevo ni C5.

## Alcance y archivos

El autor solo podrá editar estos seis archivos:

```text
app/main.py
app/settings.py
app/demo/__init__.py
app/demo/local_voice.py
tests/test_local_access.py
docs/manual/acceso-local.md
```

Coordinación podrá registrar únicamente la enmienda, decisión y evidencias
en el contrato privado existente, specs/decisions/DEC-002-preparar-acceso-local.md,
docs/manual/plan-entregas-voz.md y evidence/WP-005/**, según el permiso condicionado recibido, después de la fusión.
No modifica aceptación independiente, regresiones, CI, dependencias, permisos,
secretos, pipeline, observabilidad, motor telefónico o expediente FDA.

Dentro: integración de factory, pruebas propias y guía, corrección de Ruff y
cierre de hallazgos C3 en las seis rutas. Se acepta depurar tokens vencidos
al emitir una nueva sesión, conservando tokens válidos y semántica de un uso;
prueba propia con reloj sintético, sin nuevas tareas en segundo plano.
Este tratamiento adicional está aceptado con el contrato revisado; no se
modifica ahora producto o aceptación congelada. Fuera: audio,
APIs, cuotas de voz, persistencia, runners o cambios de arquitectura.

## Interfaces y aceptación conservadas

Rigen íntegros los siete contratos técnicos del snapshot original; este resumen
no los sustituye:

- Dos flags desactivados por defecto; factory con reloj/TTL inyectables, TTL
  finito mayor que cero y hasta 60, sin bool. Selección de app según flag;
  modo local excluye rutas telefónicas y live no activa motor.
- Rutas /demo, /demo/session y /demo/ws; Host literal 127.0.0.1:8765 y Origin
  literal http://127.0.0.1:8765 donde corresponde; no confiar en forwarded.
- POST solo JSON objeto vacío, máximo real 1024 bytes; errores 400/403/413.
- Tokens criptográficos compatibles con subprotocolo, mínimo 32 caracteres,
  únicos, efímeros y de un uso; frontera TTL exclusiva y consumo atómico.
- WebSocket sin query no vacía, protocolo exacto y validación antes de consumir;
  rechazo 1008, éxito fda-demo, único mensaje unavailable y cierre 1000.
- HTML sin botón/audio/micrófono; ninguna llamada o instancia de proveedor.
- Pruebas propias, aceptación independiente y 45 regresiones en la misma
  ejecución; Ruff limpio, guía fiel, alcance y revisión sin hallazgos abiertos.

Hallazgos C3: integración ausente, tests/guía ausentes, importación sin uso y
retención de tokens vencidos. El diagnóstico 96 aprobadas/2 fallidas de C3 no
sustituye la batería obligatoria ni acredita una entrega casi terminada.

## Gates antes de empezar

1. Aceptación humana específica de ADR-002/DEC-019 ya registrada en
   autorizacion-adopcion.md: C4, cuota Codex desconocida y diferencia de confianza
   del editor. Sigue pendiente la fusión humana de la composición FDA.
2. Contrato/autorización privados fijados: base, seis rutas, tratamiento
   de retención aceptado y límite de una pasada. Fila C4 versionada antes de editar.
3. Perfil/herramientas reales y modelo/configuración con procedencia verificable,
   sin leer secretos. Si no se establece un modelo exacto obligatorio, no
   inventarlo ni ejecutar con ese gate incumplido. Versión del CLI no es modelo.
4. Editor nativo de confianza supervisada, sin ampliar permisos. Prohibidos
   conectores, credenciales, publicación y escalaciones para acceso extra.
   El perfil tiene capacidades más amplias: rutas/hashes se controlan por
   política y detección, no por confinamiento físico de seis archivos.
5. Producto, imports, pytest y Ruff exclusivamente en Docker endurecido:
   imagen sha256:e08cf9993dcd8d5382f38c5224f2f730eabd9b0b96b699c6938e5fac8f520be8,
   no root, red none, raíz RO, cap-drop ALL, no-new-privileges, límites
   2 CPU/1 GiB/128 procesos; sin home, secretos ni socket Docker montados.
   Registrar montajes y pruebas inocuas negativas del código antes de ejecutar;
   no inferir aislamiento del editor a partir de pruebas del contenedor.
6. Oráculo, regresiones y origen parcial fijados por hash antes/después.
   El código validado y el candidato revisado por Astra deben coincidir.

Un gate pendiente mantiene el borrador sin ejecución. No se construirá otra
plataforma ni se hará una calibración de modelos para abrirlo.

## Presupuesto, duración y ciclos propuestos

Sin nueva facturación de Claude, APIs o servicios. Cuota Codex de programación
y revisión admitida como no_disponible por aceptación humana expresa; no coste
cero ni F1 ficticio. Claude histórico de WP-005: 0,275969906178 EUR estimados;
agregado de autoría del recorrido de voz: 3,255144804390 EUR estimados. Codex y
tiempo humano desconocidos. No es factura o coste total; techo original 5 EUR
intacto. No se deduce una nueva autorización del remanente.

Una pasada C4, máximo operativo 45 minutos desde apertura hasta entrega del
candidato del autor, controlado por coordinación, no corte técnico ni garantía
económica. Incluye trabajo/pruebas antes del nuevo veredicto; no una corrección
posterior C5. Registrar hora/resultado incluso sin cambios o con interrupción.

## Verificación, en este orden

En el contenedor, mismos comandos del contrato original:

```bash
python -m pytest -q tests/test_local_access.py tests/acceptance/test_local_access_contract.py tests/test_rag_processor.py tests/test_turn_detector.py tests/test_resilience.py tests/test_settings.py
python -m ruff check app/main.py app/settings.py app/demo tests/test_local_access.py tests/acceptance/test_local_access_contract.py
```

Coordinación comprueba diff completo desde la base de producto, seis rutas,
hashes inmutables y ausencia de secretos/supresiones; repite verificación Docker
independiente con logs y códigos. Misma Astra revalida hallazgos y efectos
directos, incluida seguridad. No sustituir comandos por diagnósticos parciales.

Oráculo conservado, sin copiar su código a FDA:
078bf4e6c5fe4c660b8e02b7716160c72d33012c08e6d5156f3dffaa7b52965a.

APTO exige toda la batería, guía, límites y revisión conformes. Fallo o hallazgo
abierto tras la pasada: blocked sin C5. Publicar PR privada solo después de
APTO, bajo el permiso condicionado ya recibido; fusión humana.

## Evidencia y reversión

Guardar autorización, perfil, origen/modelo, apertura/cierre C4, coste, hashes,
diff, salidas terminales, revisión y explicación para Iván en el expediente
privado. C3 e intentos previos no se reescriben. Sin migraciones o servicios.
Detener contenedores propios y revertir solo la continuación si se rechaza;
conservar candidatos, costes y evidencias. Preparar esto no satisface sus gates.
