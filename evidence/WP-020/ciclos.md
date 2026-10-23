# Ciclos documentales — WP-020

| Pasada | Origen | Objetivo | Apertura | Estado |
|---|---|---|---|---|
| C0 documental | Contrato 839877355aeb3556a3de5434bf27e178f458978e; autorización de preparación | Propuesta, avisos, borrador y evidencia | 2026-10-23, antes de la composición | RECHAZA a8949e0: WP020-F1, espacios finales en log; comandos 2/0/0/0 en revisión |
| C1 documental | a8949e09bd9372efcdde7c314c9804d51a662fec; revisión-astra-C0.md; apertura 9a8180c | WP020-F1: conservar salida mediante formato reversible y validar composición completa | 2026-10-23, versionada antes de corregir | consumida 1/2; Astra APRUEBA preparación en 23bd55c, F1 cerrado y cuatro comandos 0 sobre candidata final |
| C2 documental | 2c7e5bf913e2b5203c990e0da278c0cf03b3f8b7; autorizacion-adopcion.md; apertura 35f8e1a | Registrar adopción humana posterior, vigencia tras fusión y permiso de publicación; sin nuevo hallazgo técnico | 2026-10-23, versionada antes de actualizar normas | consumida 2/2; Astra APRUEBA publicación sobre 26a3fdd, cuatro comandos 0, sin hallazgos |
| C3 documental excepcional | PR #88, diagnóstico independiente y autorizacion-C3.md; enmienda congelada antes de .gitleaksignore | Una sola excepción exacta del falso positivo histórico, sin tocar CI/permisos o producto | 2026-10-23, apertura a4b6b08998ba75c1978e1970bd77dd16b1eda650 antes del archivo; SHA en C3_CONTRACT_BASE | CONSUMIDA 3/3; Astra APRUEBA local sobre 6ec62c1; seis comandos 0 y CI 3/3 success sobre 66717b0. Integración humana pendiente, comprobar HEAD vigente. Sin C4 documental automática |

Pasadas de WP-020: C1 y C2 consumidas, 2/2 histórico; el nuevo recibo autoriza
solo C3 y eleva el máximo a 3 sin reiniciar la cuenta. C3 abierta antes de
crear el archivo y consumida al preparar candidata, 3/3. PR FDA publicada,
con C3 local conforme y primer CI corregido verde; antes de retirar el borrador
confirmar todos los checks del HEAD vigente tras incorporar esa evidencia.
La integración sigue pendiente de fusión humana. Este contador nunca
reinicia el WP-005 externo: sigue blocked 3/3, con una C4 autorizada solo tras
fusión humana y gates conformes, todavía sin abrir. No se ha llamado a Claude.
