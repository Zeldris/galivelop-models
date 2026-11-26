<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-62bb64e8-2njnfm` |
| **Fase / tarea** | F-1: mejorar, ampliar y cerciorar el DDD (`docs/ddd.md`) a partir del borrador 1. Después, F0: subir a `main` lo decidido en F-1 y ordenarlo en versiones, como el resto de repos |
| **Último punto estable** | respuestas a Q-1 a Q-18 subidas |
| **Siguiente paso** | F-1 (refs `DDD-1`): ronda 3 (Q-19 a Q-25, del inventario `docs/records/inventario-consumidores-2026-11-26.md`) presentada; apuntar respuestas y escribir la versión final de `docs/ddd.md` |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`: verde. Deuda: aún no hay código ni tests; en F0 se añade `python3 -m unittest discover` al check |

## Para la próxima publicación

instalación del workflow + DDD final (F-1), por PR, tras `/code-review` y `reviewed.sh`

## Hecho (5 últimas)

1. 2026-11-26 — Galivelop-workflow v0.9.1 instalado (docs en es, código en en, PR a `main`, sin firmas de agente,
   prefijo `gmod-`, doble licencia MIT / CC BY-NC-SA 4.0).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
