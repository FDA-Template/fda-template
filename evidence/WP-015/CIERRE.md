# WP-015 — Cierre `done`

## Identidad del resultado

```text
wp_id: WP-015
estado_final: done
fecha_cierre: 2026-09-27
base_candidato_cierre: 99e5f82e08a22ac11dd20c08a778e5389a26b337
head_pr_revisado: eccae059c31daa569254f7096a30ca0bd094171a
pr: https://github.com/ivanes189/fda-template/pull/53
merged_at_utc: 2026-09-27T09:55:05Z
merge_commit: 99e5f82e08a22ac11dd20c08a778e5389a26b337
tested_head_c3: 333eb072e62f3298f465c32c9d47a69b043cb8c1
candidato_revalidado_c3: 1c14c797814ef98dd0b48721557c92a267add2f7
ciclos_correccion: 3 / 3
coste_eur: 22.97
estado_coste: estimado
presupuesto_eur: 40
techo_excepcional_eur: 28.29
```

El cierre se materializa como diff de operador sobre
`base_candidato_cierre`. Su identidad comprobable antes de crear un commit es
esa base más la composición cerrada de seis rutas enumerada en DEC-003 §4.

## Resultado entregado

- La PR #53 fusionó exclusivamente los 28 archivos permitidos por el contrato.
- `scripts/check_scope.py` y `scripts/scope_rules.py` proporcionan el
  ejecutable local determinista y la biblioteca única previstos por DEC-011.
- La revalidación enfocada final de la misma Astra cerró `WP015-F2` y emitió
  `APTO`; no quedan hallazgos pendientes.
- El contador final es `3 / 3`; C3 fue la excepción única de DEC-013 y no
  existe C4.
- El coste queda `estimado` en 22,97 EUR, dentro del presupuesto de 40 EUR y
  del techo excepcional acumulado de 28,29 EUR.

## Verificación remota de la fusión

La consulta de GitHub en solo lectura confirmó para la PR #53:

| Campo | Resultado |
|---|---|
| Estado | `MERGED` |
| Base | `7d1b26afcb3285e29ee17dee7548b34351948330` |
| Cabeza | `eccae059c31daa569254f7096a30ca0bd094171a` |
| Merge commit | `99e5f82e08a22ac11dd20c08a778e5389a26b337` |
| Rutas | 28, todas dentro de los cinco patrones permitidos |
| `Gobierno FDA` | `SUCCESS` |
| `Lint · Shell · Tests · Manual` | `SUCCESS` |
| `Escaneo de secretos` | `SUCCESS` |

La evidencia de implementación versionada registra además 152/152 pruebas,
14/14 controles de seguridad estática, 12/12 comandos contractuales y la
identidad de los bytes probados en `TESTED_HEAD` C3.

## Composición del cierre

La transición atómica cambia exactamente seis rutas:

```text
docs/03-hoja-de-ruta.md
docs/manual/05-bloqueos-y-parada.md
evidence/WP-015/CIERRE.md
specs/decisions/DEC-003-pausa-migracion-y-contencion.md
work-packages/ACTIVE
work-packages/WP-015-check-scope-local.md
```

El contrato cambia únicamente `estado: ready` por `estado: done`. `ACTIVE`
elimina su único identificador ejecutable y conserva solo comentarios, por lo
que la fábrica vuelve a reposo. Los otros tres documentos registran el estado
real, la composición cerrada y el límite de lo demostrado.

## Límites

Este cierre acredita solo el ejecutable local y la biblioteca única. No
acredita job de CI, check requerido, bloqueo de fusión, convergencia del guard,
runtime fail-closed, humo seguro, E2, cierre de la pausa ni instalación en
`AI-Comercial-System`. No modifica código, pruebas, workflows, ruleset,
DEC-011, DEC-012, DEC-013, ramas, worktrees o candidatas. No ejecuta C4 ni
crea, aprueba, admite, activa o implementa otro WP.
