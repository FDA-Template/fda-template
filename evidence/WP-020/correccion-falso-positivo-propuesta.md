# Propuesta de corrección puntual del falso positivo — sin aplicar

Única excepción solicitada: registrar como no secreta esta huella histórica,
que coincide con el SHA-256 de un archivo de pruebas, confirmado por Astra.
No es una exclusión genérica de claves, reglas, rutas o futuros commits.

Archivo nuevo propuesto: .gitleaksignore, con exactamente una línea:

```text
0c104189cb04faa570cf001487c8776ffc11be75:evidence/WP-020/origen-y-preservacion.json:generic-api-key:9
```

La propuesta no se ha aplicado. Para ello se solicita una única C3 documental
de WP-020, con estas condiciones:

1. Registrar decisión humana nueva y apertura previa; elevar solo el máximo
   documental de 2 a 3, conservando C0/C1/C2. Sin C4 documental automática.
2. Añadir únicamente .gitleaksignore como nueva ruta. Enmendar contrato,
   DEC-019 y manual 09 dentro de sus rutas existentes para documentar causa,
   límites y verificación; evidencias bajo evidence/WP-020/.
3. Versionar esa enmienda antes de crear .gitleaksignore y fijar su SHA en
   C3_CONTRACT_BASE, conservando CONTRACT_BASE original intacto.
4. Comprobar alcance de ambas etapas con el evaluador existente: desde el
   contrato original hasta la nueva base contractual bajo la lista antigua,
   y desde la nueva base hasta HEAD bajo la lista ampliada. Contrastar también
   el diff completo, primer commit solo contractual y única entrada literal.
5. Repetir diff, reposo, manual, alcance y escaneo remoto; misma Astra revisa
   solo esta excepción y efectos directos. No retirar borrador hasta CI verde.

Nueva facturación: 0 EUR. Cuota Codex desconocida, nunca gratuita. Sin Claude,
proveedores, producto, nuevas herramientas, CI, permisos, dependencias o compras.
No force-push, squash que borre intentos, borrado de historia o relajación del
escáner. El presupuesto original no aumenta. Mantener todas sus otras detecciones.

La eficacia se juzga sobre la cabeza publicada, no por anticipar que pasará.
Si queda un hallazgo o la excepción exacta no basta, detenerse; no ampliarla.
No se abren ahora C3 documental o C4 de producto. La segunda sigue dependiendo
de fusión humana y gates técnicos, bajo el permiso ya registrado.
