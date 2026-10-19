# Preparación de la primera entrega — knowledge-base

**Estado:** inspección de lectura y propuesta de aceptación; no ejecutada ni
implementada. Fecha: 2026-10-19. No es un WP aprobado del repositorio destino.

## Origen comprobado

Repositorio destinatario: `ivanes189/knowledge-base`, rama `master`.
Commit observado: `ddcd6f6b47d43a2ab7ceef84d36d1f74962d310f`.
Archivo: `scripts/validate_docs.py`.
Blob Git observado: `a79d3a9caa25d2cf9993c03b98103340368b12c2`.
Fuentes de lectura: rama, contenido del archivo y árbol recursivo mediante
conector GitHub. Antes de abrir el WP comprobar que la base sigue vigente.

No se copian aquí código privado, documentos comerciales ni sus contenidos.
La implementación, las pruebas y sus resultados pertenecerán al repositorio
destinatario con su misma visibilidad.

## Problema y utilidad

La búsqueda actual es no recursiva, tanto al validar como al contar documentos.
En el árbol observado, `documentos/` solo contiene subdirectorios. Por
inspección estática, la búsqueda no descubre sus Markdown y devuelve ausencia
de documentos. No se afirma haber ejecutado el programa contra los datos reales.

Resultado útil: que el control encuentre los documentos organizados en carpetas
y comunique sus errores reales. Es una mejora técnica del ecosistema comercial;
no demuestra por sí sola utilidad para un cliente ni viabilidad de Agent OS.

## Solución candidata

Conservar Python y su biblioteca estándar. Alinear descubrimiento y contador,
mantener las reglas actuales de validación y mostrar rutas relativas inequívocas.
No hacen falta otro lenguaje, servicio externo, dependencia o arquitectura.
La forma concreta se decide tras revisar CONTRIBUTING y el contrato del destino.

Archivos de producto candidatos: `scripts/validate_docs.py` y una prueba nueva
`tests/test_validate_docs.py`; el árbol consultado no contiene aún esa prueba.
El contrato final debe incluir sus propias rutas documentales y de evidencia.
No se cambia CI ni se corrigen masivamente documentos existentes para obtener
un resultado verde.

## Aceptación propuesta

1. Descubre Markdown en raíz y subdirectorios, incluido más de un nivel.
2. Usa el mismo conjunto para contar y validar; orden determinista y rutas
   relativas distinguibles cuando dos carpetas contienen el mismo nombre.
3. Mantiene detección de vacío, longitud insuficiente y sufijo de versión
   inválido; no relaja las reglas para que los documentos existentes pasen.
4. Árbol sin documentos: error y salida no cero. Todos válidos: salida cero.
   Un documento inválido: error identificable y salida no cero.
5. No sigue enlaces hacia fuera del árbol de documentos; comportamiento ante
   enlaces explícito y probado para no ampliar lecturas accidentalmente.
6. Pruebas con datos sintéticos: el caso anidado reproduce el defecto antes y
   pasa después. No se toca contenido comercial ni se realizan llamadas de red.

Comando candidato, sujeto al contrato final:
`python3 -m unittest discover -s tests -p 'test_validate_docs.py'`.
La prueba debe cubrir la salida del programa y los casos de error, no solo
invocar una función sin comprobar sus resultados.

## Condiciones aún no acreditadas

Integración humana del nuevo marco; contrato y autorización del destinatario;
presupuesto y captura de coste del autor/revisor; runtime y perímetro aislado
con pruebas de denegación; aceptación fijada fuera de la autoridad del autor.
Ninguna se presume satisfecha por esta inspección. Mientras falten no se ejecuta
el piloto. No se ha creado una rama ni una PR en knowledge-base.

Siguiente entrega tras esta mejora: concretar con el operador un recorrido útil
de AI-Comercial-System, usando lo que ya existe. No esperar a cinco ejercicios
internos ni construir Agent OS para poder demostrar ese recorrido.
