<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-c9ef964f-38192u` (sigue a `ccr-62bb64e8-2njnfm`) |
| **Fase / tarea** | 0.1 «Esqueleto, catálogo y detección» ([roadmap](roadmap.md)); H2 hecho, sigue H5 |
| **Último punto estable** | H2 hecho: `catalog/` con 13 modelos, 13 variantes, 2 máquinas y 3 licencias (forma provisional hasta H1; tabla de diferencias revisada, Q-28 a Q-37) |
| **Siguiente paso** | H5: `detect_hardware` en Linux y Windows con `/proc` y `sysfs` simulados en los tests (el catálogo valida al llegar H1, que espera a `gart`) |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1: S1 (hecho), H2 (hecho) y H5

## Hecho (5 últimas)

1. 2026-11-27 — H2: migración a `catalog/` (modelos, máquinas, licencias) con las respuestas Q-28 a Q-37;
   `flux3-image-klein` queda `unconfirmed` (VAE con licencia FLUX no comercial).
2. 2026-11-27 — H2 paso 1: tabla de diferencias (13 modelos, 2 máquinas), revisiones `hf` fijadas y digests de
   Ollama; preguntas Q-28 a Q-37.
3. 2026-11-27 — S1: esqueleto (`pyproject.toml`, `gmod/`, `tests/test_skeleton.py`), tests en el check, reglas del
   proyecto y texto de `branchCheck` en `AGENTS.md`.
4. 2026-11-27 — PR #1 fusionado: workflow, DDD final, roadmap y CHANGELOG en `main`.
5. 2026-11-27 — F0: `docs/roadmap.md` (versiones 0.0 a 0.4) y `CHANGELOG.md`.

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
