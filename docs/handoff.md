<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `claude/release-v0.1.0` (sigue a `ccr-c9ef964f-38192u`) |
| **Fase / tarea** | `v0.1.0` publicada (2026-11-27): tag anotado sobre `b6fe0e8` y release en GitHub con sus notas |
| **Último punto estable** | Release `v0.1.0` publicada; bitácora y pendientes al día |
| **Siguiente paso** | 0.2 espera al validador de `gart` (H1); mientras, lo de `records/pending.md` que no dependa de él |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

Nada todavía (la `0.1.0` ya está publicada).

## Hecho (5 últimas)

1. 2026-11-27 — `v0.1.0` publicada: tag sobre `b6fe0e8` y release en GitHub (sección `[0.1.0]` del CHANGELOG y
   limitaciones conocidas).
2. 2026-11-27 — Invariante 12: el test de esqueleto ve `importlib.import_module`, `import_module` y `__import__`;
   uno sin nombre literal hace fallar el test (pendiente leve de la revisión de bloque H2).
3. 2026-11-27 — PR #3 fusionado (`b6fe0e8`): versión `0.1.0` (pyproject, CHANGELOG con H2, roadmap cerrado con `f53a9b2`).
4. 2026-11-27 — PR #2 fusionado: fase 0.1 (S1, H2, H5) en `main`, con retro aprobada (P3 y P4 aplicadas).
5. 2026-11-27 — H5: `detect_hardware` en Linux (`/proc`, `sysfs`, `nvidia-smi`) y Windows (registro,
   `System32`), con todas las fuentes simuladas en los tests; prueba real pendiente de la persona.

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
