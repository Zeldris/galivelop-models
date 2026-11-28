<!-- galivelop-workflow v0.9.1 -->
# Bitácora (traspaso)

> Léela entera al empezar cualquier sesión. Lo que no está subido no existe: commit + push en cada punto estable,
> con esta bitácora actualizada en el mismo commit. El flujo nunca la sobrescribe una vez creada.

## Estado actual

| Campo | Valor |
|---|---|
| **Rama** | `claude/release-v0.1.0` (sesión local; reúne `ccr-c9ef964f-38192u` y `ccr-99b59083-p3cl8m`) |
| **Fase / tarea** | 0.2: H1 hecho (`gart/` vendorizado en `7d26869`, esquemas `gmod.*/0` y `validate_catalog`) y `stt` en el catálogo (Whisper, Q-43, Q-44) |
| **Último punto estable** | Las dos ramas remotas fusionadas aquí; Q-38 a Q-40 de la rama stt pasan a Q-43 a Q-45. H5 probado de verdad en la Steam Deck LCD (2026-11-28) |
| **Siguiente paso** | H3 (`fit`): esperar respuesta a Q-46 a Q-52 (diseño de la tabla de reglas, veredictos, bolsas de memoria, `sharedMemory`, motivo del Fit; cada una con recomendación) y luego spec en `docs/tasks/H3.md`, test en rojo e implementación. Presupuesto de compactaciones: 1; pedir a gart imports relativos (Q-42: a). Revisión de H1, stt y H3 antes de `main`. D-19 pedida a GVE en Zeldris/galivelop-evaluator#17 |
| **Check** | `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`, `python3 -m unittest discover -s tests -t .`: verde |

## Para la próxima publicación

Desde la 0.1.0: esquemas y `validate_catalog` (H1) y `stt` con Whisper, los dos en `[Unreleased]` del CHANGELOG

## Hecho (5 últimas)

1. 2026-11-28 — H5 probado en la Steam Deck LCD: 4 núcleos, 8 hilos, GPU AMD `163f` integrada sin VRAM, `vulkan` y `cpu`.
2. 2026-11-28 — Fusionadas aquí `ccr-c9ef964f-38192u` (stt) y `ccr-99b59083-p3cl8m` (H1); preguntas de stt renumeradas a Q-43 a Q-45.
3. 2026-11-28 — H1, revisión del bloque: esquemas como datos del paquete (`gmod/schemas/`), params de gart en los códigos reutilizados y base de LoRA sin ciclos.
4. 2026-11-28 — H1: esquemas, `validate_catalog` y tests; `gart/` vendorizado en la raíz con `VENDOR.json`.
5. 2026-11-27 — `stt` para la steam-deck: Whisper large-v3-turbo q5_0 y small q8_0, licencia `mit` (Q-43, Q-44).

## Pendiente

Lo pendiente está en [`docs/records/pending.md`](records/pending.md); se añade y se quita allí.

## Comprobar el estado

- Últimos commits: `git fetch origin <rama> && git log --oneline -5 origin/<rama>`.
- El check: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/ci-local.py --validate`, `python3 .claude/gw/scripts/tests-after-main.py`.
- Flujo bien montado: `python3 .claude/gw/scripts/doctor.py`.
- Estado de la bitácora tal como lo recibe una sesión nueva: `python3 .claude/gw/scripts/recover.py --state`.
