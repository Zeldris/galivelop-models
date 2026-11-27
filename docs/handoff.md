<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-c9ef964f-38192u` (sigue a `ccr-62bb64e8-2njnfm`) |
| **Fase / tarea** | Versión `0.1.0` fusionada en `main` (PR #3, `b6fe0e8`, 2026-11-27, confirmada por la persona; retro omitida con su confirmación) |
| **Último punto estable** | PR #3 fusionado con el CI en verde y la marca de revisión de `4fcd4db` |
| **Siguiente paso** | Tag `v0.1.0` sobre `main` (`b6fe0e8`): lo sube un agente desde local (en `records/pending.md`). Luego 0.2 espera al validador de `gart` (H1); mientras, lo de `records/pending.md` que no dependa de él |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1: S1, H2 y H5 (hechos)

## Hecho (5 últimas)

1. 2026-11-27 — PR #3 fusionado (`b6fe0e8`): versión `0.1.0` (pyproject, CHANGELOG con H2, roadmap cerrado con `f53a9b2`).
2. 2026-11-27 — PR #2 fusionado: fase 0.1 (S1, H2, H5) en `main`, con retro aprobada (P3 y P4 aplicadas).
3. 2026-11-27 — H5: `detect_hardware` en Linux (`/proc`, `sysfs`, `nvidia-smi`) y Windows (registro,
   `System32`), con todas las fuentes simuladas en los tests; prueba real pendiente de la persona.
4. 2026-11-27 — H2: migración a `catalog/` (modelos, máquinas, licencias) con las respuestas Q-28 a Q-37;
   `flux3-image-klein` queda `unconfirmed` (VAE con licencia FLUX no comercial).
5. 2026-11-27 — H2 paso 1: tabla de diferencias (13 modelos, 2 máquinas), revisiones `hf` fijadas y digests de
   Ollama; preguntas Q-28 a Q-37.

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
