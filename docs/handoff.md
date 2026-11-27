<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-c9ef964f-38192u` (sigue a `ccr-62bb64e8-2njnfm`) |
| **Fase / tarea** | 0.1 «Esqueleto, catálogo y detección» ([roadmap](roadmap.md)); S1, H2 y H5 hechos; fase cerrada (CI en verde sobre `cb7621c`) |
| **Último punto estable** | H5 hecho: `gmod/hardware.py` (`detect_hardware`, `Hardware`) y `tests/test_hardware.py` (26 tests), con la revisión de bloque hecha (7 hallazgos arreglados) |
| **Siguiente paso** | La persona confirmó llevar 0.1 a `main` y fusionar con el CI en verde (2026-11-27): fases 1 y 2 hechas, retro aprobada; `reviewed.sh`, PR, fusión y tag `v0.1.0`. Luego 0.2 espera al validador de `gart` (H1) |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1: S1, H2 y H5 (hechos)

## Hecho (5 últimas)

1. 2026-11-27 — H5: `detect_hardware` en Linux (`/proc`, `sysfs`, `nvidia-smi`) y Windows (registro,
   `System32`), con todas las fuentes simuladas en los tests; prueba real pendiente de la persona.
2. 2026-11-27 — H2: migración a `catalog/` (modelos, máquinas, licencias) con las respuestas Q-28 a Q-37;
   `flux3-image-klein` queda `unconfirmed` (VAE con licencia FLUX no comercial).
3. 2026-11-27 — H2 paso 1: tabla de diferencias (13 modelos, 2 máquinas), revisiones `hf` fijadas y digests de
   Ollama; preguntas Q-28 a Q-37.
4. 2026-11-27 — S1: esqueleto (`pyproject.toml`, `gmod/`, `tests/test_skeleton.py`), tests en el check, reglas del
   proyecto y texto de `branchCheck` en `AGENTS.md`.
5. 2026-11-27 — PR #1 fusionado: workflow, DDD final, roadmap y CHANGELOG en `main`.

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
