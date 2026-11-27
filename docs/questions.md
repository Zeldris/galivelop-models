# Questions

Questions for the user, one entry each; `python3 .claude/gw/scripts/questions.py` reads and rewrites this
file (format: header of scripts/questions.py). Answer by number: `questions.py answer "5. a, 6. ok"`.

## Q-1
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Las fases del workflow son F0 = esqueleto del repo y F1…F8 = H1…H8 del DDD?
- Recommendation: Sí: F0 levanta el esqueleto (pyproject sin dependencias, paquete gmod vacío, copia vendorizada de gart, check con python3 -m unittest); F1…F8 son los hitos H1…H8 del DDD, uno a uno
- Answer: No: F-1 es mejorar, ampliar y cerciorar el DDD; F0 es subir a main todo lo decidido en F-1 y definir su orden en versiones, como el resto de repos
- Answered: 2026-11-26

## Q-2
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: §8.1 Firma del catálogo: ¿sin firma criptográfica en la v1?
- Recommendation: No en la v1: solo manifiesto sha256; se decide cuando el instalador descargue el catálogo por la red
- Answer: ok
- Answered: 2026-11-26

## Q-3
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: §8.2 ¿Los datos del catálogo viven en este repo, en catalog/?
- Recommendation: En este repo, en catalog/, hasta que su tamaño o su ritmo de cambio lo pidan
- Answer: ok
- Answered: 2026-11-26

## Q-4
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: §8.5 ¿Sin máquinas ni medidas de terceros en la v1?
- Recommendation: No en la v1; se reconsidera con el GVE Hub
- Answer: ok
- Answered: 2026-11-26

## Q-5
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: §8.3 ¿Reglas de memoria a mano y, desde H6, informe de desviación contra GVE con umbral configurable?
- Recommendation: A mano en H3; desde H6 un informe que señala dónde lo estimado se aleja de lo medido más que un umbral (clave de configuración)
- Answer: ok
- Answered: 2026-11-26

## Q-6
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Variant con id estable <model-id>:<format>-<quant>?
- Recommendation: Cada Variant tiene un id estable <model-id>:<format>-<quant> en minúsculas (p. ej. qwen3-8b-instruct:gguf-q4_k_m); sigue siendo objeto de valor dentro de su Model, pero el id es lo que citan Measurement, la CLI y los consumidores
- Answer: ok
- Answered: 2026-11-26

## Q-7
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿fit distingue unknown (falta un dato) de no (no cabe)?
- Recommendation: Añadir un cuarto veredicto unknown (falta un dato) distinto de no (no cabe); sigue fallando cerrado: recommend nunca ofrece unknown y el motivo dice qué dato falta
- Answer: ok
- Answered: 2026-11-26

## Q-8
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: §8.4 ¿Datasets fuera y LoRA como Model con modelo base, sin marca especial de derivatives?
- Recommendation: Datasets fuera (no son modelos). Un LoRA entra como Model con Task y referencia a su modelo base; su licencia se describe con los usos normales y el filtro license_use decide. Se quita lo de «marcados como derivatives»
- Answer: ok
- Answered: 2026-11-26

## Q-9
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿El orden de versiones de gmod depende de que gart publique su validador?
- Recommendation: Los hitos de esquema y validación de gmod esperan a la versión de gart con su validador; sin validador provisional propio. Mientras, H1-H2 avanzan en lo que no depende de gart (modelo de dominio, datos en catalog/)
- Answer: ok
- Answered: 2026-11-26

## Q-10
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: §3 ¿Los esquemas gmod.* viven aquí y gart solo los valida?
- Recommendation: Se corrige §3: los esquemas gmod.* viven en este repo; gart solo los carga y valida (ADR 0004 de gart)
- Answer: ok
- Answered: 2026-11-26

## Q-11
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Separar Máquina (hardware) de los ajustes de ejecución de cada app?
- Recommendation: Máquina describe solo hardware (en gmod); los ajustes de ejecución de cada app (minFreeMemoryMb, timeouts, modelo por rol) quedan en el consumidor, con la máquina por id. Se ajusta el criterio de éxito
- Answer: ok
- Answered: 2026-11-26

## Q-12
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Una Variante es un conjunto de archivos con rol, cada uno con su sha256?
- Recommendation: Una Variante es un conjunto de archivos con rol (pesos, texto, vae, tokenizador compartido), cada uno con sha256, bytes y url
- Answer: ok
- Answered: 2026-11-26

## Q-13
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Licencia sin confirmar = unconfirmed, excluida siempre por license_use?
- Recommendation: Licencia unconfirmed explícita, sin usos permitidos: el filtro license_use la excluye siempre
- Answer: ok
- Answered: 2026-11-26

## Q-14
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Orígenes v1: hf, url y ollama?
- Recommendation: Tipos de origen v1: hf (repo + revisión), url (directa) y ollama (name:tag + digest)
- Answer: ok
- Answered: 2026-11-26

## Q-15
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Portal sin «firmado» y páginas en src/data/proyectos/?
- Recommendation: En el portal no se dice «firmado» (D-2); las páginas van en src/data/proyectos/. Se corrigen la nota y H8
- Answer: ok
- Answered: 2026-11-26

## Q-16
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Lista cerrada de Tareas en v1 y el invariante 8 limitado a ella?
- Recommendation: Lista cerrada de Tareas en v1 (texto, embeddings, imagen, voz-a-texto, texto-a-voz, visión); añadir una es cambio de esquema. El invariante 8 se limita a esa lista
- Answer: ok
- Answered: 2026-11-26

## Q-17
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Con qué autor (nombre y correo) firmo los commits?
- Recommendation: Los commits de este repo salen con el autor que me digas (nombre y correo, p. ej. tu usuario noreply de GitHub); hasta entonces sigo con el actual
- Answer: ok
- Answered: 2026-11-26
- Correction: 2026-11-27, la persona aclara que el autor es su cuenta (la del commit inicial), no el agente

## Q-18
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Añado GVE, gvc e Instalador-WMF-Tarkor en solo lectura para H2?
- Recommendation: Para la tabla de diferencias de H2 añado con add_repo GVE, gvc e Instalador-WMF-Tarkor (solo lectura, resumen con un subagente)
- Answer: ok
- Answered: 2026-11-26

## Q-19
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿H6 depende de que GVE añada variante, máquina y motor a sus informes?
- Recommendation: Sí: la Medición (H6) depende de que GVE añada a sus informes la variante, la máquina y la versión del motor. Se deja una petición escrita a GVE en docs/records/ (como hizo gvc) y H6 espera a esa versión de GVE
- Answer: ok
- Answered: 2026-11-27

## Q-20
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Los paquetes de modelos por rol se quedan en los consumidores?
- Recommendation: Las asignaciones de modelo por rol (perfiles minimo…ultra del instalador, celdas rol × nivel de gvc, models.design de gvoice) se quedan en cada consumidor, como D-11; gmod da modelos, variantes, máquinas y encaje, y el consumidor cita las variantes por id
- Answer: ok
- Answered: 2026-11-27

## Q-21
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿fit acepta hardware detectado en ejecución, no solo máquinas del catálogo?
- Recommendation: fit acepta tanto una Máquina del catálogo por id como una descripción de hardware detectada en ejecución (mismos campos); el instalador detecta y pregunta sin guardar su máquina
- Answer: ok
- Answered: 2026-11-27

## Q-22
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿fit estima la memoria de la variante y la reserva la pone cada app?
- Recommendation: fit devuelve la memoria estimada de la variante; la reserva de cada app (sistema, juego, margen) la pone el consumidor. La fórmula del instalador se convierte en regla de su lado, no de gmod
- Answer: ok
- Answered: 2026-11-27

## Q-23
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿Tamaños en bytes y memoria en MiB en todo gmod?
- Recommendation: Todos los tamaños en bytes y la memoria en MiB enteros; nada de GB/MB/GiB mezclados
- Answer: ok
- Answered: 2026-11-27

## Q-24
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿La revisión de hf se fija siempre a un commit, nunca main?
- Recommendation: Un origen hf fija la revisión a un commit (sha de 40 caracteres), nunca main; H2 resuelve las urls actuales de gimg y gvoice al commit de hoy
- Answer: ok
- Answered: 2026-11-27

## Q-25
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-26
- Question: ¿El tag de Ollama es solo un origen y la cuantización se apunta explícita?
- Recommendation: Un origen ollama guarda el tag y el digest del manifiesto; la cuantización real se apunta en la variante (no se deja implícita). El tag de Ollama no es el id: qwen3.5:9b pasa a una variante gmod con ese origen
- Answer: ok
- Answered: 2026-11-27

## Q-26
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-27
- Question: ¿Vale el reparto en versiones de docs/roadmap.md?
- Recommendation: Sí, tal cual: 0.1 esqueleto + catálogo (H2) + detección (H5), que no esperan a gart; 0.2 esquemas/fit/recommend (H1, H3, H4); 0.3 exportación y CLI (H7, H8); 0.4 GVE (H6)
- Answer: Sí, tal cual
- Answered: 2026-11-27

## Q-27
- Refs: DDD-1
- Status: answered
- Asked: 2026-11-27
- Question: ¿Subo a main por PR lo de F-1 y F0 (DDD final, roadmap, CHANGELOG, workflow v0.9.1)?
- Recommendation: Sí: tras la revisión de código (fase 1) y la retro (fase 2) presentadas, PR a main con reviewed.sh
- Answer: Sí, con revisión y PR
- Answered: 2026-11-27

## Q-28
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Id del modelo flux3-klein-q8 de gimg (P-1 de docs/records/diferencias-catalogos-2026-11-27.md)?
- Recommendation: flux3-image-klein, el nombre publicado del repo y del archivo
- Answer: ok
- Answered: 2026-11-27

## Q-29
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Ids de la familia Qwen3.5: con o sin sufijo -instruct (P-2)?
- Recommendation: qwen3.5-<tamaño> sin sufijo (Ollama no dice instruct/base); llama3.1-8b-instruct y qwen2.5-1.5b-instruct conservan instruct
- Answer: ok
- Answered: 2026-11-27

## Q-30
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Licencia de llama3.1:8b, que no es SPDX (P-3)?
- Recommendation: Ficha propia llama-3.1-community leída de la capa license del manifiesto de Ollama; unconfirmed hasta escribirla
- Answer: ok
- Answered: 2026-11-27

## Q-31
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Licencia de una variante que junta archivos de varios repos hf (P-4)?
- Recommendation: Licencia de la variante = la más restrictiva de sus archivos; verificar cada repo hf antes de publicar Apache-2.0
- Answer: ok
- Answered: 2026-11-27

## Q-32
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Cómo se guarda un archivo compartido por dos variantes, Qwen3-4B-Q4_K_M.gguf en gimg (P-5)?
- Recommendation: Repetir el archivo en cada variante (mismo sha256 y url) y que el consumidor deduplique por sha256
- Answer: ok
- Answered: 2026-11-27

## Q-33
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Qué roles de archivo usa gmod frente a diffusion/text/vae de gimg y base/design/codec de gvoice (P-6)?
- Recommendation: Roles de archivo weights, text, vae, tokenizer; el use de gvoice (base, design) se queda en gvoice y codec pasa a tokenizer
- Answer: ok
- Answered: 2026-11-27

## Q-34
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿RAM de la máquina steam-deck: nominal o la visible (P-7)?
- Recommendation: 16384 MiB nominal; la reserva la pone cada consumidor sobre fit (D-22)
- Answer: ok
- Answered: 2026-11-27

## Q-35
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Dónde van los minFreeGiB 9 y 5 de gvc (P-8)?
- Recommendation: No van a Machine: se guardan como dato de memoria de la variante para H3 (D-5), citando a gvc como fuente
- Answer: ok
- Answered: 2026-11-27

## Q-36
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Entra gpu-12gb en el catálogo, solo existe en gvc (P-9)?
- Recommendation: Sí: gpu-12gb con 16384 MiB de RAM y 12288 MiB de VRAM nominales; los umbrales 14336/11776 se quedan en la detección de gvc
- Answer: ok
- Answered: 2026-11-27

## Q-37
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Tareas de qwen3.5-* y qué se hace con stt sin candidato (P-10)?
- Recommendation: vision: qwen3.5-* declaran text y vision (capa projector); stt queda sin candidato y el invariante 9 se aplaza para stt
- Answer: ok
- Answered: 2026-11-27

## Q-38
- Refs:
- Status: answered
- Asked: 2026-11-27
- Question: ¿Cómo se sube el tag v0.1.0? (a) lo subes tú a mano; (b) conectas tu equipo por Remote Control a esta sesión; (c) en una sesión local
- Recommendation: c: abrir una sesión de Claude Code en tu equipo con el repo y pedir el tag; aquí no hay equipo conectado
- Answer: ya estaba subido (v0.1.0 sobre b6fe0e8)
- Answered: 2026-11-27

## Q-39
- Refs:
- Status: answered
- Asked: 2026-11-27
- Question: 0.2 (H1, H3, H4, H7) depende del validador de gart (D-9). ¿Qué hago mientras? (a) esperar; (b) adelantar H3 (memoria unificada de la Deck, sin validador); (c) otra cosa
- Recommendation: a: esperar al validador de gart; si ya está publicado, dime dónde y empiezo H1
- Answer: a (la persona delega; el agente elige esperar): gart sigue en DDD (8d7489c, sin tags ni código del validador) y H3 depende de H1 según el DDD, así que (b) no era viable
- Answered: 2026-11-27
