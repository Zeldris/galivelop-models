# Inventario de catálogos y perfiles de los consumidores (2026-11-26)

Lectura en solo lectura (D-18) para la tabla de diferencias de H2. Commits leídos: instalador `56f0108`, gimg
`bc27219`, gvoice `8a17618`, gvc `014f7ff`, GVE `6cc80cc`. Lo marcado (I) es inferencia; el resto se leyó.

| Repo | Catálogo de modelos | Perfil de máquina | Encaje |
|---|---|---|---|
| Instalador-WMF-Tarkor | `app/catalogo/catalogo.json`: 7 modelos por tag de Ollama (`llama3.1:8b`, `qwen3.5:9b`…), con `descargaGb`, `licencia`, `piensa`; sin sha256 ni url por modelo (el digest lo da Ollama) | No hay dato: se detecta en ejecución (`app/nucleo/src/equipo.rs`). Sus `perfiles` (`minimo`…`ultra`) son paquetes de modelos por rol, no máquinas | `app/nucleo/src/perfiles.rs`: memoria para IA = RAM − max(3 GB, 25 %) − 1 GB (+ 0,9·VRAM dedicada); `memoriaGb` de cada perfil escrito a mano |
| gimg | `models.json` + `schemas/models.schema.json`: 3 modelos multiarchivo (`diffusion`, `text`, `vae`), cada archivo con `url`, `sha256`, `sizeMb`; `license` admite `unconfirmed`; urls a `resolve/main` sin revisión fijada | `machine_profiles/steam-deck.json`: casi todo ajustes de la app (`minFreeMemoryMb`, `timeoutS`, `maxSteps`, sobrescrituras por modelo) | Solo `MemAvailable >= minFreeMemoryMb`; aviso si `maxVram` > 2 GB |
| gvoice | `engines/qwentts.json`: 4 archivos con `url`, `bytes`, `sha256`, `use`; sin licencia; cuantización solo en el nombre de archivo | `machine_profiles/steam-deck.json`: ajustes de la app y modelo por rol | Solo `minFreeMemoryMb` |
| gvc | `gdev/catalog.json` (`gdev.catalog/0`): tabla rol × nivel de máquina, 2 celdas (`qwen3.5:9b`, `qwen3.5:4b`) | `gdev/machine_levels/` (`steam-deck`, `gpu-12gb`): hardware puro; `machine_profiles/steam-deck.json`: ajustes | Primera celda confirmada con `minFreeGiB + reservedGiB <= libre` |
| GVE | — | — | Solo `gve.evidence/1` y `gve.comparison/1`, como cadenas en el código (`gve/evidence.py`, `gve/compare.py`); el modelo se identifica por tag de Ollama + digest; **no hay campos de máquina, variante ni motor**. Ejemplo real: `docs/evidence/tarkor/2026-11-14/` |

Diferencias principales:

1. Ids: tag de Ollama (instalador, gvc), cuantización dentro del id (gimg), tamaño sin cuantización (gvoice).
2. Tamaños en GB, MB, bytes y GiB; licencia como `licencia`, `license` o ausente.
3. Revisión de Hugging Face sin fijar (`main`) en gimg y gvoice.
4. Lo mismo («memoria libre mínima») con cinco nombres: `minFreeMemoryMb`, `minAvailableGiB`, `minFreeGiB`, `memoriaGb`.
5. El único perfil compartido es `steam-deck` (gimg, gvoice, gvc); el instalador no tiene perfiles de máquina guardados.
