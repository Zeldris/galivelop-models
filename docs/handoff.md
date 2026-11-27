<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-c9ef964f-38192u` (sigue a `ccr-62bb64e8-2njnfm`) |
| **Fase / tarea** | 0.1 «Esqueleto, catálogo y detección» ([roadmap](roadmap.md)) |
| **Último punto estable** | S1 hecho: esqueleto `pyproject.toml` + `gmod/` + `tests/`, con los tests en el check |
| **Siguiente paso** | H2: tabla de diferencias entre los catálogos del instalador, gimg, gvoice y gvc (lectura de otros repos con subagente), para revisión de la persona |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1: S1 (hecho), H2 y H5

## Hecho (5 últimas)

1. 2026-11-27 — S1: esqueleto (`pyproject.toml`, `gmod/`, `tests/test_skeleton.py`), tests en el check, reglas del
   proyecto y texto de `branchCheck` en `AGENTS.md`.
2. 2026-11-27 — PR #1 fusionado: workflow, DDD final, roadmap y CHANGELOG en `main`.
3. 2026-11-27 — F0: `docs/roadmap.md` (versiones 0.0 a 0.4) y `CHANGELOG.md`.
4. 2026-11-27 — F-1 cerrada: DDD final (D-1 a D-25).
5. 2026-11-26 — Galivelop-workflow v0.9.1 instalado (docs en es, código en en, PR a `main`, sin firmas de agente,
   prefijo `gmod-`, doble licencia MIT / CC BY-NC-SA 4.0).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
