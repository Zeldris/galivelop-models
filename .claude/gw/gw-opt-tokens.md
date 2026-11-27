<!-- galivelop-workflow v0.9.1 -->
# gw-opt-tokens — notas del proyecto

Las lee la skill `gw-opt-tokens` antes de proponer nada, y se actualizan cuando la persona aprueba un cambio. El flujo
las crea una vez; desde entonces son del proyecto.

## Herramientas que ya ahorran

<!-- Una línea cada una, con cómo se corre. -->
- `python3 .claude/gw/scripts/recover.py --state` y `--search "<texto>"`: recuperar lo que se llevó una
  compactación.
- `gw-orchestrate-dealer`: el trabajo de más de un paso, repartido a subagentes de contexto limpio.

## Costes conocidos

<!-- Lo que se ha visto que cuesta mucho en este proyecto (archivos grandes leídos enteros, salidas largas...). -->
- `git diff --stat` de una rama que trae el flujo vendorizado lista cientos de archivos (4.8k tokens con 244): para
  ver qué trae, `git diff --shortstat` y `python3 .claude/gw/scripts/review-scope.py --workflow <clon>`. (Retro
  2026-11-27, P3.)

- `docs/roadmap.md` y `docs/ddd.md` leídos enteros una y otra vez (8 veces cada uno en 0.1, ~690k arrastrados): el
  roadmap con `python3 .claude/gw/scripts/roadmap.py show <id>` o `list <versión>`; el DDD con
  `grep -n -A8 'D-<n>' docs/ddd.md` sobre la decisión que toca. (Retro 0.1, P3.)
- La salida de un push o check en segundo plano se lee con `tail -5` (la última línea de `push.sh` lo resume); si
  falló, `ci-status.py --failed` o un `grep` de la causa. Un `tail -c 6000` costó 361k arrastrados. (Retro 0.1, P4.)

## Ajustes en vigor

- Ventana de compactación automática: `CLAUDE_CODE_AUTO_COMPACT_WINDOW` en `.claude/settings.json`.

## Referencias medidas

<!-- Cifras medidas con las que comparar: fecha, sesión, contexto medio, llamadas, total. -->
- 2026-11-27, fase 0.1 (sesión `c8fcc8e5`): 95 llamadas, contexto medio 131.6k, arranque fijo ~84k/llamada (64 %),
  1 compactación; subagentes 9 % de la entrada.
