<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `claude/release-v0.1.0` (sesión local; reúne `ccr-c9ef964f-38192u` y `ccr-99b59083-p3cl8m`) |
| **Fase / tarea** | 0.2: H1 y H3 hechos (`gart/` vendorizado en `7d26869`, esquemas `gmod.*/0` y `validate_catalog`) y `stt` en el catálogo (Whisper, Q-43, Q-44) |
| **Último punto estable** | H3 hecho: `gmod/fit.py`, `catalog/memory-rules.json` y `sharedMemory` en las máquinas; check en verde (commit `feat(H3)`) |
| **Siguiente paso** | Revisión del bloque H1 + stt + H3 hecha (base `2dcd7cc`): 1 medio a la espera de Q-53 (bolsas atadas a la API de cada GPU), 4 leves en `pending.md`. Con la respuesta, arreglo (commit con `Findings: 1`) y luego H4 (`recommend`). Pedir a gart imports relativos (Q-42: a). D-19 pedida a GVE en Zeldris/galivelop-evaluator#17 |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

Desde la 0.1.0: esquemas y `validate_catalog` (H1) y `stt` con Whisper, los dos en `[Unreleased]` del CHANGELOG

## Hecho (5 últimas)

1. 2026-11-28 — H3: `fit` con reglas de memoria, `sharedMemory` en `gmod.machine/0` y `Gpu`.
2. 2026-11-28 — H5 probado en la Steam Deck LCD: 4 núcleos, 8 hilos, GPU AMD `163f` integrada sin VRAM, `vulkan` y `cpu`.
3. 2026-11-28 — Fusionadas aquí `ccr-c9ef964f-38192u` (stt) y `ccr-99b59083-p3cl8m` (H1); preguntas de stt renumeradas a Q-43 a Q-45.
4. 2026-11-28 — H1, revisión del bloque: esquemas como datos del paquete (`gmod/schemas/`), params de gart en los códigos reutilizados y base de LoRA sin ciclos.
5. 2026-11-28 — H1: esquemas, `validate_catalog` y tests; `gart/` vendorizado en la raíz con `VENDOR.json`.

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
