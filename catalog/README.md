# Catálogo de gmod

Datos del catálogo, migrados en H2 desde los cuatro consumidores. Solo JSON; el código y el validador llegan con H1 (D-9).

## Qué hay

- `licenses.json`: licencias (`apache-2.0`, `llama-3.1-community`, `mit`, `unconfirmed`).
- `models/<model-id>.json`: 15 modelos, una variante cada uno (formato, cuantización, origen, archivos, licencia, runtimes).
- `machines/<id>.json`: 2 máquinas, `steam-deck` y `gpu-12gb`.

## Forma provisional

La forma (claves en inglés, camelCase, bytes enteros, memoria en MiB, listas ordenadas por id) es **provisional hasta H1**, que la fija. Las variantes de Ollama llevan `layers` (su suma es igual a `bytes`; `other` recoge lo que no es modelo, proyector ni borrador) y digest del manifiesto; las de Hugging Face, un origen por archivo, fijado a commit de 40 hex.

## De dónde sale cada dato

Todo sale de `docs/records/diferencias-catalogos-2026-11-27.md`: la tabla de modelos y máquinas (secciones 1 y 2) y lo resuelto con red (sección 5, que manda sobre la 1). La sección 6 de ese archivo resume la migración. Cada modelo y máquina cita en `provenance` el consumidor, la ruta y el commit leídos.

Los dos Whisper (`stt`, Q-38) no vienen de un consumidor: salen de la búsqueda de `docs/records/stt-candidatos-2026-11-27.md`, que citan en `provenance`.

## Qué no está aquí

Lo propio de cada app (ajustes, reservas de memoria, roles, asignación por rol) se queda en su consumidor (D-11, D-20, D-22).
