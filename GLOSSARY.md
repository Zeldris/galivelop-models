<!-- galivelop-workflow v0.9.1 -->
# Glosario

Vocabulario de galivelop-models. Primero van los términos del flujo; el proyecto añade debajo los de su dominio y los
mantiene al día (skill `domain-modeling`). El flujo nunca sobrescribe este archivo una vez creado.

## Términos del flujo

- **Bitácora**: `docs/handoff.md`, el estado del trabajo para la siguiente sesión: rama, tarea en curso, siguiente paso,
  check.
- **Relevo**: una sesión que se acaba y otra que sigue desde la bitácora, sin preguntar por dónde iba.
- **Punto estable**: un estado con el check en verde, con commit y subido.
- **Check**: las órdenes del proyecto que tienen que pasar en cada commit que se sube: `python3 .claude/gw/scripts/md-links.py`, `python3 .claude/gw/scripts/agent-map.py`, `python3 .claude/gw/scripts/tests-after-main.py`.
- **Commit `WIP:`**: un commit subido con algo a medias o en rojo; la bitácora dice qué falla y por qué.
- **Rama protegida**: `main`, lo publicado; solo recibe trabajo revisado, con confirmación
  de la persona.
- **Marca de revisión**: `docs/records/reviewed.txt`, el archivo versionado con el sha del último commit revisado; los ganchos
  aceptan código hasta él.
- **Contenido frente a código**: el contenido (lo que casa con `content` de `.claude/gw.json`) no necesita revisión
  de código; todo lo demás es código.
- **Encargo a un subagente**: lo que recibe un subagente: objetivo, rutas, restricciones, el check que debe pasar y
  qué tiene que devolver.
- **Retro**: la retrospectiva de la sesión antes de ir a la rama protegida; sus propuestas se presentan a la persona y
  lo que confirme se aplica en la rama.
- **Propuesta (`.gw-new`)**: un archivo del flujo que la actualización no pudo aplicar sin perder cambios locales;
  se fusiona a mano y luego se borra.

## Términos del proyecto

<!-- **Término**: definición, y dónde vive en el código. -->

- **Regla de memoria (`MemoryRule`)**: por motor (`runtime`), los formatos y cuantizaciones que cubre, las APIs de
  cómputo que admite, el factor sobre los bytes de la variante (en milésimas), la sobrecarga y el margen en MiB;
  mantenida a mano (D-5). Vive en `catalog/memory-rules.json` (`gmod.memory_rules/0`) y la usa `gmod.fit.fit`.
- **Memoria compartida (`sharedMemory`)**: marca de una GPU de `gmod.machine/0` que usa la RAM del sistema; `fit` usa
  entonces `ramMiB` como bolsa. `Gpu.shared_memory` en `gmod/hardware.py` (verdadero en toda GPU integrada).

- **Variante** (*Variant*): una forma concreta de descargar y ejecutar un Modelo (formato y cuantización). Su id es
  `<model-id>:<formato>-<cuant>` en minúsculas, p. ej. `qwen3-8b-instruct:gguf-q4_k_m`.
- **Encaje** (*Fit*): el veredicto de si una Variante cabe en una Máquina: `fits`, `tight`, `no` o `unknown` (falta un
  dato; el motivo dice cuál). Da la memoria estimada de la variante; la reserva de cada app la pone la app. Una
  recomendación nunca ofrece `unknown`.
- **Máquina** (*Machine*): un perfil de hardware (CPU, RAM, GPU/VRAM, API de cómputo, SO), sin ajustes de ninguna app.
  `steam-deck` es la de referencia. El **hardware detectado** tiene los mismos campos, leídos en ejecución.
- **Origen** (*Source*): de dónde sale una Variante: `hf` (repo + commit), `url` u `ollama` (tag + digest). El tag de
  Ollama es un origen, no un id.
