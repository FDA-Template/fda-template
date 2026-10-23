**Estado de publicación:** borrador, pendiente de CI de la cabeza publicada.
La misma Astra aprueba localmente C3 sobre 6ec62c1, seis comandos 0 y sin
hallazgos abiertos. El único hallazgo inicial era un SHA-256 de integridad,
confirmado como falso positivo por Astra. La autorización humana posterior
permite una única C3 documental y una entrada exacta en .gitleaksignore.
Se conservan escáner e historial, sin cambios de CI o permisos. Ver
`evidence/WP-020/autorizacion-C3.md` y `diagnostico-escaneo.md`.
No fusionar con el escaneo en rojo ni inferir verde antes de comprobarlo.

**WP:** WP-020 — Excepción acotada de autoría Codex supervisada
**Rama:** `wp/WP-020-excepcion-autoria-codex`
**Requisitos / ADR:** REQ-FDA-001, REQ-FDA-002, SEC-001 / ADR-001, ADR-002

## Qué y por qué

El circuito de autoría del piloto dejó incompleto el acceso local tras C3.
Esta PR habilita una única continuación C4 con Codex (GPT-6.1 Sol medium) y
revisión Astra separada, únicamente después de fusión humana y gates conformes.
Conserva los intentos/costes y el régimen general Claude Code; no implementa
producto. El operador ha aceptado explícitamente la excepción y su publicación.

## Alcance

- [x] Alcance original conservado hasta la enmienda previa de C3; después solo una ruta nueva autorizada, .gitleaksignore.
- [x] CLAUDE y ADR autorizados; sin cambios en CI, hooks, permisos o CODEOWNERS.
- [x] ACTIVE en reposo; producto y expediente privado intactos.

## Verificación

```bash
git diff --check 0205556be8ad9cd7993feeddd0b4347694cf37f8
bash tests/governance/check-active.sh
python3 evidence/WP-000/checks/check-manual.py
python3 scripts/check_scope.py WP-020 "${WP020_CONTRACT_BASE:?}...${WP020_C3_CONTRACT_BASE:?}"
python3 scripts/check_scope.py WP-020 "${WP020_C3_CONTRACT_BASE:?}...HEAD"
python3 -c 'from pathlib import Path; assert Path(".gitleaksignore").read_bytes() == b"0c104189cb04faa570cf001487c8776ffc11be75:evidence/WP-020/origen-y-preservacion.json:generic-api-key:9\n"'
```

Las variables se leen de `evidence/WP-020/CONTRACT_BASE` y `C3_CONTRACT_BASE`.
La segunda fija a4b6b08998ba75c1978e1970bd77dd16b1eda650, enmienda/apertura
previas a .gitleaksignore. Se revisan ambas etapas, diff completo, primer commit
solo contractual y ausencia de .gitleaksignore en la apertura. El control de
alcance es local; no se presenta como check requerido en CI.

- [x] C2 local revisada conforme; el fallo remoto posterior permanece en el historial.
- [x] Seis comandos C3 verdes, repetidos por la misma Astra sobre 6ec62c1.
- [x] Revalidación local C3 conforme, incluida seguridad y alcance de ambas etapas.
- [ ] Criterio 7 final: todos los checks remotos de la cabeza publicada verdes.
- [x] Sin funciones/código de producto nuevos; validación documental y gobierno.

## Evidencias

- `evidence/WP-020/autorizacion-adopcion.md`: aceptación humana y permiso condicionado.
- `evidence/WP-020/autorizacion-C3.md`, `C3_CONTRACT_BASE`: decisión puntual y apertura previa a la excepción del escáner.
- `evidence/WP-020/C3-verificacion.json`, `C3-01` a `C3-06`, `C3-comprobaciones-complementarias.json` y `revision-astra-C3.md`: comandos, salidas, preservación y revalidación C3.
- `evidence/WP-020/C2-verificacion.json` y `C2-01` a `C2-04`: comandos, salidas íntegras y códigos.
- `evidence/WP-020/revision-astra-C2.md`: revalidación independiente de autoridad y seguridad, sin hallazgos.
- `evidence/WP-020/origen-y-preservacion.json`: expediente externo, doce hashes y ACTIVE intactos.
- `evidence/WP-020/aceptacion.md`, `cost.md` y `ciclos.md`: criterios, desconocidos e intentos conservados.
- [x] Salidas conservadas reversiblemente; rechazo C0 y corrección C1 no borrados.
- [x] Coste registrado, sin importe inventado.

## Riesgos

El editor nativo tiene acceso más amplio que seis archivos: reglas, hashes y
revisión detectan incumplimientos, pero no son confinamiento físico ni separación
técnica de credenciales. El operador aceptó esa diferencia. El código seguirá
en Docker sin red/home/claves/socket y su perímetro se comprobará antes de C4.
La cuota Codex es desconocida. No se acredita seguridad de producción o eficiencia.

## Deuda introducida

No se resuelven aislamiento físico del editor, medición de cuota ni controles
de operación autónoma. La excepción es de una instancia, sin nueva plataforma,
otra llamada Claude, audio, proveedores, compras o C5 automática.

## Rollback

Antes de fusionar, rechazar deja el producto intacto. Después, detener cualquier
continuación antes de retirar conjuntamente ADR-002 y avisos. Conservar historial,
candidatos y costes; no restaurar autoridad o intentos automáticamente.

## Coste

| Concepto | Valor |
|---|---|
| Coste atribuible de cuota Codex | no_disponible; no gratuito ni cierre económico |
| Nueva facturación autorizada de WP-020 | 0 EUR |
| Pasadas documentales consumidas | 3/3, incluida única C3 excepcional; sin más continuación automática |
| Producto | Cierre 3/3 preservado; C4 condicionada, todavía no abierta |

## Documentación y revisión

- [x] Manual actualizado en la misma PR.
- [x] Una GPT-6 Astra Alto independiente revisó contrato y seguridad; C1/C2 revalidadas por la misma revisora.
- [x] Decisión humana sobre propuesta y riesgo registrada; fusión humana pendiente.

La fusión de esta PR es necesaria, pero no sustituye los gates privados previos
a C4. Su permiso ya está registrado: no requiere otra confirmación si se mantienen
los límites. Ningún agente fusionará esta PR.
