<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-c9ef964f-38192u` (sigue a `ccr-62bb64e8-2njnfm`) |
| **Fase / tarea** | Versión `0.1.0` publicada: PR #3 en `main` (`b6fe0e8`) y tag `v0.1.0` sobre ese commit con su release (2026-11-27, confirmado por la persona) |
| **Último punto estable** | `stt` en el catálogo: `whisper-large-v3-turbo` (q5_0) y `whisper-small` (q8_0) con `whisper.cpp` v1.9.6, licencia `mit` (Q-38, Q-39) |
| **Siguiente paso** | Respuesta de la persona a Q-40 (memoria unificada de la steam-deck en `fit`, H3; recomendación b: campo explícito en el esquema de H1). 0.2 sigue esperando al validador de `gart` (H1); lo demás de `records/pending.md` es de la persona |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1: S1, H2 y H5 (hechos)

## Hecho (5 últimas)

1. 2026-11-27 — `stt` para la steam-deck: Whisper large-v3-turbo q5_0 y small q8_0 en `catalog/models/`, licencia `mit` en `licenses.json` (Q-38, Q-39; candidatos en `records/stt-candidatos-2026-11-27.md`).
2. 2026-11-27 — Tag `v0.1.0` sobre `main` (`b6fe0e8`) y release publicados.
3. 2026-11-27 — Invariante 12: el test de esqueleto ve `importlib.import_module`, `import_module` y `__import__`;
   uno sin nombre literal hace fallar el test (pendiente leve de la revisión de bloque H2).
4. 2026-11-27 — PR #3 fusionado (`b6fe0e8`): versión `0.1.0` (pyproject, CHANGELOG con H2, roadmap cerrado con `f53a9b2`).
5. 2026-11-27 — PR #2 fusionado: fase 0.1 (S1, H2, H5) en `main`, con retro aprobada (P3 y P4 aplicadas).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
