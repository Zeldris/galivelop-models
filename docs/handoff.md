<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `ccr-99b59083-p3cl8m` (desde `main` tras el PR #3) |
| **Fase / tarea** | 0.2, H1 en curso (Q-40: a): `gart/` vendorizado a mano en la raíz, fijado a `7d26869` (hecho) |
| **Último punto estable** | H1 primer trozo: `gart/` (copia sin editar de `7d26869`, `gart/VENDOR.json` escrito a mano: sin tag ni kit gart-H11) con test de sha256 y smoke test; el invariante 12 cubre también `gart/` |
| **Siguiente paso** | H1: esquemas `gmod.model/0` y `gmod.machine/0` con ejemplos, y validar `catalog/`. D-19 pedida a GVE en Zeldris/galivelop-evaluator#17 |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

0.1.0 publicada en `main`; desde entonces, solo un test (sin entrada en el CHANGELOG)

## Hecho (5 últimas)

0. 2026-11-28 — H1: `gart/` vendorizado en la raíz (sibling de `gmod/`, imports absolutos intactos), `VENDOR.json` y tests.
1. 2026-11-27 — Tag `v0.1.0` comprobado en el remoto, sobre `b6fe0e8`.
2. 2026-11-27 — Invariante 12: el test del esqueleto rechaza importaciones dinámicas en `gmod`.
3. 2026-11-27 — PR #3 fusionado: versión `0.1.0` en `main`.
4. 2026-11-27 — Commit de versión `0.1.0` (pyproject, CHANGELOG con H2, roadmap cerrado con `f53a9b2`).
5. 2026-11-27 — PR #2 fusionado: fase 0.1 (S1, H2, H5) en `main`, con retro aprobada (P3 y P4 aplicadas).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
