<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-62bb64e8-2njnfm` |
| **Fase / tarea** | F-1: versión final del DDD (`docs/ddd.md`) a partir del borrador 1 (2026-11-26), antes de F0 |
| **Último punto estable** | commit de instalación de Galivelop-workflow v0.9.1 |
| **Siguiente paso** | F-1: revisar el borrador 1 del DDD con la persona (preguntas de §8 incluidas) y escribir la versión final en `docs/ddd.md` |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`: verde. Deuda: aún no hay código ni tests; en F0 se añade `python3 -m unittest discover` al check |

## Para la próxima publicación

instalación del workflow + DDD final (F-1), por PR, tras `/code-review` y `reviewed.sh`

## Hecho (5 últimas)

1. 2026-11-26 — Galivelop-workflow v0.9.1 instalado (docs en es, código en en, PR a `main`, sin firmas de agente,
   prefijo `gmod-`, doble licencia MIT / CC BY-NC-SA 4.0).

## Pendiente

Lo pendiente está en el archivo de `pendingFile` (`.claude/gw.json`; por defecto `docs/records/pending.md`): decisiones de la persona que bloquean algo, problemas conocidos, ideas sin planificar. Se añade y se quita allí; `handoff.py move-pending` rehace esta línea y `handoff.py add-pending "texto"` añade sin leer el archivo.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
