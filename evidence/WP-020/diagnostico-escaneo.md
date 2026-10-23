# Bloqueo remoto: un falso positivo de integridad

PR: https://github.com/FDA-Template/fda-template/pull/88, ahora en borrador.
Head publicado inicialmente: 58ac9a8330024ea59c18245c367bc54b2745bd23.
Run: https://github.com/FDA-Template/fda-template/actions/runs/39973340592.
Gobierno y calidad: success. Escaneo: failure, gitleaks exit 2 y un hallazgo.

## Causa comprobada

Regla generic-api-key, huella exacta:

```text
0c104189cb04faa570cf001487c8776ffc11be75:evidence/WP-020/origen-y-preservacion.json:generic-api-key:9
```

En ese commit, la línea 9 es una propiedad de external_hashes que asocia la
ruta del evaluador de aceptación a su SHA-256. Se recalculó la huella del archivo
privado congelado y coincide. Es un dato de integridad, no una credencial.
El valor no se reproduce aquí; no se consultaron claves o autenticación.

El log se consultó mediante extracción de indicadores, reglas y fingerprints,
sin imprimir Secret, Match, cabeceras o log bruto. El escáner sí se ejecutó.
La advertencia Resource not accessible by integration corresponde al intento
opcional posterior de escribir un comentario sobre el hallazgo; no es la causa
de la detección y ampliar permisos no resuelve este falso positivo.

La [acción fijada](https://github.com/gitleaks/gitleaks-action/blob/ff98106e4c7b2bc287b24eaf42907196329070c7/src/gitleaks.js)
ejecuta --redact, interpreta exit 2 como detección y captura como advertencia
el fallo al comentar. También describe .gitleaksignore para fingerprints de
falsos positivos. Su rango de escaneo incluye commits históricos; cambiar
el JSON en un commit nuevo no elimina la detección del anterior.

## Comprobación independiente

La misma Astra /root/review_wp020, GPT-6 Astra Alto y solo lectura, confirmó
independientemente el blob, línea y coincidencia con el evaluador preservado.
Expediente externo limpio en b173052813c469a77679e3505a811b3cc6216af9.
Diagnóstico CONFORME: una entrada de esa huella sería excepción puntual
justificada, sin excluir reglas o archivos completos, manteniendo escáner e
historial. No acredita CI verde futuro ni autoriza aplicarla.

## Parada y decisión pendiente

.gitleaksignore no existe en esta candidata y está fuera de la allowlist del
WP-020. Sus dos pasadas documentales están consumidas. No se crea el archivo,
no se abre C3 ni se modifica CI, permisos o historia. La PR permanece borrador.
La publicación y su diagnóstico no se presentan como una corrección adicional.

La [propuesta concreta](correccion-falso-positivo-propuesta.md) requiere decisión
humana nueva antes de modificar el alcance y abrir una C3 documental. Es distinta
de la C4 del producto ya autorizada tras fusión humana y gates conformes.
