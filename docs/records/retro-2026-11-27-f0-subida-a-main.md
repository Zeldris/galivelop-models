# Retro: F0, subida a `main` (2026-11-27)

Sesión `c8fcc8e5`, rama `ccr-c9ef964f-38192u`: respuestas a Q-26 y Q-27, fase 1 (revisión) y fase 2 (esta retro y
`gw-opt-tokens`).

**Estado:** pendiente de la persona: P1 a P4 presentados, sin decidir.

## Medida (`gw-opt-tokens`)

21 llamadas, contexto medio 103.8k (suelo 47k, techo 124k), sin compactaciones; 96 % lectura de caché. Arranque fijo
~40k por llamada (39 %). Lo más arrastrado: la lectura junta de `AGENTS.md` + `REVIEW.md` + ayudas de scripts (6.3k,
88k arrastrados) y el `git diff --stat` de los 244 archivos de la rama (4.8k, 81k arrastrados). El contexto medio no
pasa de 150k: no hace falta repartir más a subagentes ni adelantar la compactación.

## Propuestas, de más a menos importante

### P1 — La bitácora de una sesión nueva en la nube puede estar en otra rama (general, para el flujo)

La rama de la sesión salía de `main`, que solo tenía el README: la bitácora, las preguntas abiertas y todo F-1 estaban
en `ccr-62bb64e8-2njnfm`. Encontrarlo costó tres llamadas a ciegas (log, GitHub, ramas). Una sesión que no mirase las
ramas habría empezado de cero.

**Cambio:** `session-start.sh` (o `recover.py --state`), cuando la rama actual no tiene `docs/handoff.md` o es igual
a `main`, lista las ramas remotas por delante de `main` que sí la tienen, con su último commit y su `Siguiente:`, y
dice la orden para traerla (`git merge --ff-only origin/<rama>`). **Riesgo:** ninguno; solo informa.

### P2 — `review-scope.py` necesita un clon del flujo que en la nube no existe (general, para el flujo)

Sin `../Galivelop-workflow`, `review-scope.py` no sabe qué está vendorizado y manda revisar las 26k líneas. Lo resolví
clonando la v0.9.1 en el scratchpad a mano. **Cambio:** que `review-scope.py` (y `doctor.py`) clonen la versión
marcada con `--depth 1` en una caché por usuario (`$XDG_CACHE_HOME/galivelop-workflow/<versión>`) cuando falte, o que
digan la orden exacta con esa ruta. **Riesgo:** una red cerrada; entonces sigue el aviso de ahora.

### P3 — `git diff --stat` de una rama con el flujo vendorizado (proyecto)

Lista los 244 archivos. **Cambio:** apuntar en `.claude/gw/gw-opt-tokens.md`, «Costes conocidos»: para ver qué trae
una rama, `git diff --shortstat` y `review-scope.py --workflow <clon>` en vez de `--stat`. **Riesgo:** ninguno.

### P4 — Barrido de leves (proyecto)

En `docs/records/pending.md` hay un solo leve (el texto de `branchCheck` en `AGENTS.md`); ningún script tiene dos o
más: no se propone barrido. Sí se puede arreglar el leve en S1 (0.1), cuando se rellenen las reglas del proyecto en
`AGENTS.md`.

## For Galivelop-workflow

- P1: aviso de bitácora en otra rama al empezar una sesión en una rama nueva.
- P2: clon en caché de la versión del flujo para `review-scope.py` y `doctor.py`.
