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

## Q-40
- Refs: H1
- Status: answered
- Asked: 2026-11-28
- Question: El validador de gart ya está en su main (gart-H1, H2, H9; commit 7d26869), sin tag y sin el kit de vendorizado (gart-H11, aún lejos). Solo stdlib; no admite anyOf/oneOf/allOf ni $ref fuera del archivo. ¿Empezamos H1 vendorizándolo a mano (a) o esperamos a un tag o a gart-H11 (b)?
- Recommendation: a) Empezar H1 ya: copiar gart/ fijado a 7d26869 en gmod/_vendor/gart con un VENDOR.json escrito a mano y un test que rehace los sha256 con hashlib (invariante 11 de gart); al salir gart-H11, se cambia por su kit. Es la copia vendorizada de su ADR 0002, no un validador provisional, así que D-9 se cumple
- Answer: a
- Answered: 2026-11-28

## Q-41
- Refs: H1
- Status: answered
- Asked: 2026-11-28
- Question: GVE no registra aún variante, máquina ni versión del motor (D-19), y su repo no menciona nuestra petición. ¿Se la haces llegar tú (a) o la abro yo como issue en galivelop-evaluator (b)?
- Recommendation: a) Pasarle tú la petición docs/records/peticion-gve-2026-11-27.md a GVE (allí no consta en ningún sitio); H6 sigue esperando
- Answer: b
- Answered: 2026-11-28

## Q-42
- Refs: H1
- Status: answered
- Asked: 2026-11-28
- Question: La copia de gart se instala como paquete de primer nivel `gart`. Si otro consumidor (grun, gforge) o el propio galivelop-artifacts se instalan en el mismo entorno con su `gart`, uno pisa al otro y el commit fijado deja de regir. ¿Lo dejamos en la raíz y pedimos a gart imports relativos (a), o lo metemos ya en gmod/_vendor/gart editando sus 3 imports, con la nota en VENDOR.json y el sha256 del archivo editado (b)?
- Recommendation: a) Dejarlo en la raíz y pedir a gart que su __init__.py use imports relativos; con eso, la siguiente copia va a gmod/_vendor/gart sin editarla. Hoy gart no es instalable (no tiene pyproject), así que el choque no puede darse aún
- Answer: a
- Answered: 2026-11-28

## Q-43
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Qué Whisper entra en el catálogo como stt (docs/records/stt-candidatos-2026-11-27.md)? a) large-v3-turbo q5_0 + small q8_0; b) solo large-v3-turbo q5_0; c) solo small q8_0
- Recommendation: a: whisper-large-v3-turbo q5_0 (574 MB, más calidad) y whisper-small q8_0 (264 MB, la rápida), los dos con whisper.cpp v1.9.6; así la Deck tiene calidad y una salida si turbo va lenta
- Answer: a
- Answered: 2026-11-27

## Q-44
- Refs: H2
- Status: answered
- Asked: 2026-11-27
- Question: ¿Se añade la licencia mit a catalog/licenses.json para los pesos de Whisper?
- Recommendation: Sí: añadir la licencia mit (SPDX MIT, usos commercial, redistribute, derivatives) a catalog/licenses.json
- Answer: ok
- Answered: 2026-11-27

## Q-45
- Refs: H3
- Status: answered
- Asked: 2026-11-27
- Question: ¿Cómo trata `fit` (H3) una GPU integrada con memoria unificada y `vramMiB: null`, como la steam-deck? a) Regla implícita: GPU `integrated: true` + `vramMiB: null` ⇒ la memoria es `ramMiB`; b) campo explícito de memoria compartida en el esquema de `Machine` (H1) y `fit` usa `ramMiB` solo con él; c) la Deck solo encaja por `cpu` contra `ramMiB` y la GPU queda `unknown`
- Recommendation: b) Campo explícito en el esquema (H1): la GPU declara memoria compartida (p. ej. `sharedMemory: true`); con él, `fit` usa `ramMiB` como bolsa común de CPU y GPU, y `vramMiB: null` sin ese campo sigue dando `unknown` (invariante 6 intacta). La reserva del sistema y del juego la sigue poniendo el consumidor (D-22). Así la invariante 9 se cumple con datos, no con un caso especial de `steam-deck`
- Answer: b
- Answered: 2026-11-28

## Q-46
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Dónde vive la tabla de reglas de memoria de H3? a) archivo de datos del catálogo con su propio esquema; b) constante en Python dentro de gmod/fit.py
- Recommendation: Un archivo de datos catalog/memory-rules.json con su esquema gmod.memory_rules/0 (gart no admite guiones en el nombre del KindId), validado por validate_catalog. El DDD dice que la estimación «sale de la tabla de reglas del catálogo», y así la tabla entra en el manifiesto (H7) y el informe de desviación de H6 la compara con lo medido
- Answer: a
- Answered: 2026-11-28

## Q-47
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Con qué clave y qué forma tienen las reglas? a) por cuantización solamente; b) por motor, con los formatos y las cuantizaciones que cubre; c) por motor y tarea
- Recommendation: b) Una regla por motor (ollama, llama.cpp, stable-diffusion.cpp, qwentts.cpp, whisper.cpp), con: los formatos y las cuantizaciones que cubre, las APIs de cómputo con las que corre, overheadMiB fijo (contexto, activaciones, búferes) y weightsFactor (un multiplicador de los bytes de la variante, en milésimas enteras para no usar floats). Estimación = ceil(bytes/MiB × factor) + overheadMiB. Una variante cuyo motor, formato o cuantización no tiene regla da unknown (invariante 6). Sin regla por tarea: hoy cada motor sirve a una sola tarea, salvo ollama (text, embed, vision)
- Answer: b
- Answered: 2026-11-28

## Q-48
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Qué bytes cuenta la estimación? a) el total de la variante (bytes); b) solo los pesos principales, sin proyector de visión ni draft
- Recommendation: a) Se cuentan todos los bytes de la variante (pesos, texto, vae, proyector, draft). Es lo más conservador: si un consumidor no carga el proyector le sobra memoria, y nunca al revés. Afinarlo por capa espera a las medidas de GVE (H6)
- Answer: a
- Answered: 2026-11-28

## Q-49
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Cómo se separan fits, tight y no? a) con un margen absoluto en MiB por motor; b) con un porcentaje fijo global (p. ej., tight si queda menos del 10 %)
- Recommendation: Con la reserva del margen en la propia regla (marginMiB por motor): fits si estimación + margen ≤ memoria disponible; tight si estimación ≤ memoria < estimación + margen; no si la memoria es menor que la estimación. El margen es el de «pesos + contexto + margen por motor» del DDD; la reserva del sistema y de la app sigue siendo del consumidor (D-22)
- Answer: a
- Answered: 2026-11-28

## Q-50
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Qué memoria compara fit? a) la mejor bolsa entera (una GPU, o la RAM), sin reparto; b) suma de VRAM de todas las GPUs y descarga parcial a RAM
- Recommendation: a) Bolsas sin reparto: si la máquina tiene una API de cómputo de GPU que el motor admite y una GPU con vramMiB (o sharedMemory), se prueba la GPU más grande; si no cabe y el motor corre en cpu, se prueba ramMiB; el veredicto es el mejor de los dos y el Fit dice qué bolsa usó (gpu, shared o ram). Con sharedMemory hay una sola bolsa, ramMiB. Ni reparto entre varias GPUs ni descarga parcial a CPU (ollama lo hace, pero estimarlo sin medidas sería optimista). computeApis vacío o sin una API que el motor admita ⇒ unknown (gpu-12gb hoy)
- Answer: a
- Answered: 2026-11-28

## Q-51
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Cómo entra sharedMemory (Q-45 b)? a) obligatorio en el esquema y detect_hardware lo rellena para GPUs integradas; b) opcional (false por defecto) y la detección no lo toca
- Recommendation: a) sharedMemory obligatorio (boolean) en cada GPU de gmod.machine/0, para que nadie lo olvide: la steam-deck true, gpu-12gb false. detect_hardware lo pone a true en toda GPU integrada (AMD, Intel), con lo que fit funciona también con el hardware detectado en la Deck; Hardware.to_dict lo saca con la misma clave
- Answer: a
- Answered: 2026-11-28

## Q-52
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: ¿Cómo es el motivo de un Fit? a) un código estable con parámetros, y los textos llegan en H8; b) una frase en español ya ahora
- Recommendation: Fit como dataclass congelada: verdict, estimateMiB (None si falta la regla o el tamaño), availableMiB, pool (gpu | shared | ram | None) y reason como código estable más parámetros (p. ej. ('missing', {'field': 'vramMiB'}), ('no-rule', {'runtime': 'x'})). Los textos es/en de los motivos llegan con H8; hasta entonces, los tests comprueban el código
- Answer: a
- Answered: 2026-11-28

## Q-53
- Refs: H3
- Status: answered
- Asked: 2026-11-28
- Question: Revisión del bloque H3 (medio): fit da la bolsa shared a una GPU integrada aunque la API común solo corra en la discreta (iGPU Intel + dGPU NVIDIA con computeApis [cuda] y regla [cuda] ⇒ fits en shared, cuando CUDA no corre en la Intel). ¿Cómo se ata cada bolsa a las API de su GPU?
- Recommendation: a) en fit, un mapa vendor→API (nvidia: cuda, vulkan; amd: rocm, vulkan; intel: vulkan; apple: metal); una GPU solo da su bolsa si la API común está en las de su vendor; vendor null ⇒ se aceptan todas las de la máquina (lo de hoy). Sin cambiar el esquema de máquina. b) computeApis por GPU en gmod.machine/1 (más exacto, cambia esquema y hardware.py). c) dejarlo como está y apuntarlo en la spec.
- Answer: a
- Answered: 2026-11-28

## Q-54
- Refs: H4
- Status: open
- Asked: 2026-11-28
- Question: ¿Cómo recibe recommend el catálogo? a) un Catalog cargado con load_catalog(root); b) los documentos sueltos (models, licenses, rules) como argumentos
- Recommendation: a) load_catalog(root) -> Catalog: dataclass congelada con models, licenses (por id), machines (por id) y rules; corre validate_catalog y lanza CatalogError con los problemas si no valida. recommend(task, machine, catalog, *, license_use=None), con machine = id de máquina del catálogo, documento gmod.machine/0 o Hardware (D-21). Es la raíz del agregado del DDD y la usarán la CLI (H8) y la exportación (H7)

## Q-55
- Refs: H4
- Status: open
- Asked: 2026-11-28
- Question: ¿En qué orden van las recomendaciones? a) fits antes que tight y, dentro, la estimación mayor primero; b) la más ligera primero; c) solo por id de variante
- Recommendation: a) fits antes que tight; dentro de cada veredicto, la estimación de memoria mayor primero (sin medidas, el modelo más grande que cabe es el mejor indicio de calidad; GVE lo afinará en H6); empates por id de variante (invariante 5). b) la más ligera primero. c) solo por id

## Q-56
- Refs: H4
- Status: open
- Asked: 2026-11-28
- Question: ¿Se devuelven todas las variantes que encajan o una por modelo? a) todas; b) la mejor de cada modelo
- Recommendation: a) todas las variantes que encajan, sin agrupar por modelo: el consumidor elige y aplica su reserva (D-22) sobre estimate_mib. b) solo la mejor variante de cada modelo

## Q-57
- Refs: H4
- Status: open
- Asked: 2026-11-28
- Question: ¿Qué lleva una Recommendation y qué pasa con los LoRA? a) model, variant, license y el Fit entero; LoRA fuera en v1; b) otra forma
- Recommendation: a) Recommendation dataclass congelada: model, variant, license (id) y fit (el Fit entero, que lleva motor, bolsa, estimación y motivo), con to_dict() camelCase. Los LoRA (modelos con base) quedan fuera de recommend en v1: no corren solos

## Q-58
- Refs: H4
- Status: open
- Asked: 2026-11-28
- Question: ¿Cómo falla recommend ante una llamada mal hecha (tarea, uso de licencia o máquina que no existen)? a) ValueError con código estable; b) lista vacía
- Recommendation: a) errores de llamada con ValueError y código estable en args: tarea fuera de la lista cerrada (recommend.unknown_task), license_use fuera de commercial/redistribute/derivatives (recommend.unknown_use), id de máquina que no existe (recommend.unknown_machine). license_use es un solo uso, como en el DDD y la CLI; una licencia que no está en licenses.json cuenta como unconfirmed
