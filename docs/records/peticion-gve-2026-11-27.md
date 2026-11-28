# Petición a GVE (galivelop-evaluator), 2026-11-27

**De:** galivelop-models (gmod). **Decisión:** D-19 de [`docs/ddd.md`](../ddd.md).
**Estado:** abierta como issue en GVE el 2026-11-28 (Zeldris/galivelop-evaluator#17, Q-41: b).

gmod recoge las medidas de GVE y las cita (`gmod.measurement`, hito H6). Para eso, cada informe `gve.*` que mida un
modelo tiene que decir, además de lo que ya trae (`run.id`, `gve_version`, el esquema):

1. **La variante medida**, por su id de gmod (`<model-id>:<formato>-<cuant>`, p. ej. `qwen3-8b-instruct:gguf-q4_k_m`)
   o, mientras no lo conozca, por su origen: tag de Ollama + digest (ya está en `config.embedding_model` y
   `embedding_model_digest` de `gve.evidence/1`), o repo de Hugging Face + commit + sha256 del archivo.
2. **La máquina**: el id de una máquina de gmod (p. ej. `steam-deck`) o el hardware detectado (CPU, RAM en MiB, GPU,
   VRAM en MiB, API de cómputo, SO).
3. **El motor y su versión** (p. ej. `ollama` 0.34.3).
4. **Las medidas** con unidades fijas: memoria pico en MiB, velocidad en tokens/s (o la unidad de la tarea) y la
   puntuación de calidad con el nombre de la métrica.

Hoy `gve.evidence/1` (`gve/evidence.py`) y `gve.comparison/1` (`gve/compare.py`) no traen 2 ni 3. Hasta que una versión
de GVE los traiga, H6 de gmod espera.
