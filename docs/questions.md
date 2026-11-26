# Questions

Questions for the user, one entry each; `python3 .claude/gw/scripts/questions.py` reads and rewrites this
file (format: header of scripts/questions.py). Answer by number: `questions.py answer "5. a, 6. ok"`.

## Q-1
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: ¿Las fases del workflow son F0 = esqueleto del repo y F1…F8 = H1…H8 del DDD?
- Recommendation: Sí: F0 levanta el esqueleto (pyproject sin dependencias, paquete gmod vacío, copia vendorizada de gart, check con python3 -m unittest); F1…F8 son los hitos H1…H8 del DDD, uno a uno

## Q-2
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: §8.1 Firma del catálogo: ¿sin firma criptográfica en la v1?
- Recommendation: No en la v1: solo manifiesto sha256; se decide cuando el instalador descargue el catálogo por la red

## Q-3
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: §8.2 ¿Los datos del catálogo viven en este repo, en catalog/?
- Recommendation: En este repo, en catalog/, hasta que su tamaño o su ritmo de cambio lo pidan

## Q-4
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: §8.5 ¿Sin máquinas ni medidas de terceros en la v1?
- Recommendation: No en la v1; se reconsidera con el GVE Hub

## Q-5
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: §8.3 ¿Reglas de memoria a mano y, desde H6, informe de desviación contra GVE con umbral configurable?
- Recommendation: A mano en H3; desde H6 un informe que señala dónde lo estimado se aleja de lo medido más que un umbral (clave de configuración)

## Q-6
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: ¿Variant con id estable <model-id>:<format>-<quant>?
- Recommendation: Cada Variant tiene un id estable <model-id>:<format>-<quant> en minúsculas (p. ej. qwen3-8b-instruct:gguf-q4_k_m); sigue siendo objeto de valor dentro de su Model, pero el id es lo que citan Measurement, la CLI y los consumidores

## Q-7
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: ¿fit distingue unknown (falta un dato) de no (no cabe)?
- Recommendation: Añadir un cuarto veredicto unknown (falta un dato) distinto de no (no cabe); sigue fallando cerrado: recommend nunca ofrece unknown y el motivo dice qué dato falta

## Q-8
- Refs: DDD-1
- Status: open
- Asked: 2026-11-26
- Question: §8.4 ¿Datasets fuera y LoRA como Model con modelo base, sin marca especial de derivatives?
- Recommendation: Datasets fuera (no son modelos). Un LoRA entra como Model con Task y referencia a su modelo base; su licencia se describe con los usos normales y el filtro license_use decide. Se quita lo de «marcados como derivatives»
