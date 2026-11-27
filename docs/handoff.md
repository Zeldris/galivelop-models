<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-c9ef964f-38192u` (sigue a `ccr-62bb64e8-2njnfm`) |
| **Fase / tarea** | 0.1 «Esqueleto, catálogo y detección» ([roadmap](roadmap.md)); H2 en curso |
| **Último punto estable** | H2, paso 1: tabla de diferencias en [`docs/records/diferencias-catalogos-2026-11-27.md`](records/diferencias-catalogos-2026-11-27.md), con las 13 urls `hf` fijadas a commit (sha256 comprobados) y los 7 tags de Ollama con digest, bytes y cuantización real |
| **Siguiente paso** | H2, paso 2: la persona revisa la tabla y contesta Q-28 a Q-37; después, migración a `catalog/` con esas respuestas. Red: entorno personal `galivelop-models` (permite `huggingface.co` y `registry.ollama.ai`); clones de solo lectura en `/home/user/zeldris/` y `/home/user/galivelop-developer` (se rehacen con `git clone --depth 1`) |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1: S1 (hecho), H2 y H5

## Hecho (5 últimas)

1. 2026-11-27 — H2 paso 1: tabla de diferencias (13 modelos, 2 máquinas), revisiones `hf` fijadas y digests de
   Ollama; preguntas Q-28 a Q-37.
2. 2026-11-27 — S1: esqueleto (`pyproject.toml`, `gmod/`, `tests/test_skeleton.py`), tests en el check, reglas del
   proyecto y texto de `branchCheck` en `AGENTS.md`.
3. 2026-11-27 — PR #1 fusionado: workflow, DDD final, roadmap y CHANGELOG en `main`.
4. 2026-11-27 — F0: `docs/roadmap.md` (versiones 0.0 a 0.4) y `CHANGELOG.md`.
5. 2026-11-27 — F-1 cerrada: DDD final (D-1 a D-25).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
