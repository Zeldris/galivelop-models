<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-62bb64e8-2njnfm` |
| **Fase / tarea** | F-1: mejorar, ampliar y cerciorar el DDD (`docs/ddd.md`) a partir del borrador 1. Después, F0: subir a `main` lo decidido en F-1 y ordenarlo en versiones, como el resto de repos |
| **Último punto estable** | F0: roadmap por versiones (`docs/roadmap.md`) y `CHANGELOG.md` escritos |
| **Siguiente paso** | Esperar las respuestas Q-26 (reparto en versiones) y Q-27 (subir a `main`). Con Q-27 sí: fase 1 (revisión del bloque, el `commit-msg` avisa de 25998 líneas, casi todo el flujo vendorizado), fase 2 (`gw-opt-tokens` + `retro`, presentadas), fase 3 (`reviewed.sh`) y PR |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`: verde. Deuda: aún no hay código ni tests; en F0 se añade `python3 -m unittest discover` al check |

## Para la próxima publicación

instalación del workflow + DDD final (F-1), por PR, tras `/code-review` y `reviewed.sh`

## Hecho (5 últimas)

1. 2026-11-27 — F0: `docs/roadmap.md` (versiones 0.0 a 0.4) y `CHANGELOG.md`.
2. 2026-11-27 — F-1 cerrada: DDD final (D-1 a D-25).
3. 2026-11-26 — Galivelop-workflow v0.9.1 instalado (docs en es, código en en, PR a `main`, sin firmas de agente,
   prefijo `gmod-`, doble licencia MIT / CC BY-NC-SA 4.0).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
