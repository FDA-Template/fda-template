# Lectura y procedencia de las evidencias de WP-020

Los cuatro logs C0 y verificacion.json son históricos: miden el commit
0c10418, anterior a incorporarlos. No acreditan por sí solos la composición
posterior. Astra rechazó a8949e0 porque el log del manual añadió espacios finales.

C1 representa 03-manual.log como JSON con los bytes originales íntegros en
base64, tamaño y SHA-256. No recorta, normaliza o oculta salida; los otros tres
logs C0 conservan su formato. La preimagen sigue también en Git a8949e0.
Decodificar a stdout, sin crear otro archivo versionado con espacios finales:

```bash
python3 -c 'import base64,json,sys; d=json.load(open("evidence/WP-020/03-manual.log")); sys.stdout.buffer.write(base64.b64decode(d["original_bytes_base64"],validate=True))'
```

Los nuevos archivos C1-01 a C1-04 son JSON: command, executed_head, fecha,
stdout y stderr completos como cadenas con saltos escapados, y exit_code.
json.load(...)["stdout"] recupera exactamente esa salida. No se repasa la
salida para quitar espacios. Los códigos de salida proceden de subprocess.

C1-verificacion.json identifica el HEAD donde se ejecutó la batería, no un
SHA futuro imposible de insertar en su propio commit. La incorporación de
los resultados no modifica el contenido normativo. La revisora contrasta la
composición final, incluidos esos archivos, identifica su SHA y repite las
cuatro comprobaciones. Su dictamen vincula la aptitud a ese candidato exacto;
no se deduce de la medición del commit padre.
