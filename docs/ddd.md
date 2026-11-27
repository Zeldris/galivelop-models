# DDD: galivelop-models

> **Estado:** versión final de F-1 (2026-11-27), revisada con la persona en tres rondas (Q-1 a Q-25 en
> [`docs/questions.md`](questions.md)); las decisiones están al final, D-1 a D-25. Parte del borrador 1 del 2026-11-26.
> El orden en versiones se fija en F0.

Nombre del repositorio y del proyecto: `galivelop-models` (Model Atlas en el portal). Paquete Python importable: `gmod`.
Espacio de artefactos: `gmod`. Repo público, con la misma licencia que los demás repos Galivelop.

**Depende de:**
- `galivelop-artifacts` (`gart`): su validador publicado para los hitos de esquema (H1 y siguientes). Sin validador
  provisional propio (D-9).
- `galivelop-evaluator` (GVE): una versión de sus informes que diga qué variante, en qué máquina y con qué motor se
  midió, para la ingesta de medidas (H6, D-19).

Mientras no estén, se avanza en lo que no depende de ellos: el modelo de dominio, los datos de `catalog/` y la tabla de
diferencias de H2.

## 1. Propósito

Un **catálogo único, versionado y verificable de modelos de IA local** y de las **máquinas** donde corren, con la
respuesta a «¿qué variante de qué modelo cabe en esta máquina?». Hecho solo con stdlib (Python ≥ 3.10).

Sustituye a los datos de modelos y de hardware que hoy están duplicados (inventario en
[`docs/records/inventario-consumidores-2026-11-26.md`](records/inventario-consumidores-2026-11-26.md)):
- el catálogo de modelos del instalador (`app/catalogo/catalogo.json`, sección `modelos`);
- los catálogos de modelos de gimg (`models.json`) y gvoice (`engines/*.json`);
- los niveles de máquina de gvc (`gdev/machine_levels/`) y la parte de hardware de los perfiles `steam-deck` de gimg,
  gvoice y gvc.

**No sustituye** lo que es de cada app (D-11, D-20): los ajustes de ejecución (`minFreeMemoryMb`, timeouts,
`maxSteps`, el bucle de gvc), la reserva de memoria (la fórmula del instalador) ni la elección de modelo por rol (los
perfiles `minimo`…`ultra` del instalador, la tabla rol × nivel de gvc, `models.design` de gvoice). Esos datos siguen en
cada consumidor y citan las variantes y las máquinas de gmod por su id.

Las medidas de rendimiento y calidad vienen de GVE: el atlas no mide, recoge las medidas y las cita.

**Éxito:**
- el instalador, gimg, gvoice y gvc leen sus modelos, variantes y máquinas de una copia de `gmod`, con sus ajustes de
  ejecución y sus asignaciones por rol en su propio repo apuntando a ids de gmod, sin cambiar el comportamiento de sus
  tests;
- el portal publica la página del atlas a partir de ese mismo catálogo.

## 2. Lenguaje del dominio

| Término | Código | Significado |
|---|---|---|
| Modelo | `Model` | Un modelo publicado (familia + tamaño + ajuste), p. ej. `qwen3-8b-instruct`, independiente de cómo se empaqueta. Un LoRA es un Modelo con referencia a su modelo base (D-8) |
| Variante | `Variant` | Una forma concreta de obtener y ejecutar un Modelo: formato, cuantización, origen y archivos. Id `<model-id>:<formato>-<cuant>` en minúsculas, p. ej. `qwen3-8b-instruct:gguf-q4_k_m` (D-6) |
| Archivo | `VariantFile` | Uno de los archivos de una variante, con su rol (`weights`, `text`, `vae`, `tokenizer`…), sha256, bytes y url (D-12) |
| Origen | `Source` | De dónde sale la variante: `hf` (repo + revisión fijada a un commit), `url` (enlace directo) u `ollama` (`name:tag` + digest del manifiesto) (D-14, D-24, D-25) |
| Tarea | `Task` | Para qué sirve, de una lista cerrada en la v1: `text`, `embed`, `image`, `stt`, `tts`, `vision` (D-16) |
| Motor | `Runtime` | Lo que ejecuta la variante: `ollama`, `llama.cpp`, `stable-diffusion.cpp`, `qwentts.cpp`…, con su versión mínima |
| Licencia | `License` | Identificador SPDX o ficha propia, con sus usos permitidos (`commercial`, `redistribute`, `derivatives`). `unconfirmed` es una licencia explícita sin ningún uso permitido (D-13) |
| Máquina | `Machine` | Un perfil de **hardware**: CPU, RAM, GPU/VRAM, API de cómputo (`cuda`, `rocm`, `vulkan`, `metal`, `cpu`) y SO. Nada de ajustes de apps (D-11). La Steam Deck (`steam-deck`) es el perfil mínimo de referencia |
| Hardware detectado | `Hardware` | Los mismos campos de una Máquina, leídos del equipo en ejecución y sin guardar en el catálogo (D-21) |
| Encaje | `Fit` | Veredicto de una variante en una máquina: `fits`, `tight`, `no` o `unknown` (falta un dato), con la memoria estimada de la variante y el motivo (D-7, D-22) |
| Medida | `Measurement` | Un resultado de GVE (velocidad, memoria pico, puntuación de calidad) de una variante en una máquina, con su fecha, la versión del motor y la referencia al informe de GVE |
| Recomendación | `Recommendation` | Para una Tarea y una Máquina, la lista ordenada de variantes con veredicto `fits` o `tight`, con el motivo |
| Catálogo | `Catalog` | Conjunto publicado de modelos, variantes, máquinas y medidas, con versión y manifiesto |
| Manifiesto | `Manifest` | Lista de archivos del catálogo con su sha256 y la huella global de la versión (D-2) |

**Notas:**
- Los nombres de código y los campos de los artefactos están en inglés; los textos visibles se dan en es y en.
- Unidades: los tamaños, en bytes; la memoria, en MiB enteros (D-23). Ningún campo en GB, MB ni GiB.
- El tag de Ollama (`qwen3.5:9b`) no es un id de gmod: es el origen de una variante, y la cuantización real que hay
  detrás se apunta en la variante, no se deja implícita (D-25).

## 3. Contextos acotados

1. **Catálogo (núcleo):** `Model`, `Variant`, `VariantFile`, `Source`, `License`, `Runtime` y `Task`, con su validación
   contra los esquemas `gmod.*`. Los esquemas viven en este repo; `gart` solo da el validador que los carga y el formato
   `KindId` (D-10). Es puro: sin E/S ni red.
2. **Máquinas:** perfiles de `Machine` y la detección local de `Hardware` (lee `/proc`, `sysfs` u otras fuentes del
   sistema); la detección es la única parte con E/S de sistema.
3. **Encaje y recomendación:** `fit` y `recommend`. Funciones puras y deterministas; la estimación de memoria de la
   variante sale de la tabla de reglas del catálogo. La reserva de memoria (sistema, juego, margen) no es de gmod: la pone
   cada consumidor sobre la estimación (D-22).
4. **Medidas:** recoge informes `gve.*` y los convierte en `Measurement`. GVE es el dueño de la medida; el atlas solo la
   cita y la agrega.
5. **Publicación:** manifiesto, exportación para consumidores (copia vendorizada), página para el portal y CLI.

**Mapa con los demás repos:**

| Repo | Relación con el atlas |
|---|---|
| `galivelop-artifacts` (`gart`) | Proveedor: validador y formato `KindId`. Los esquemas `gmod.*` son de este repo |
| `galivelop-evaluator` (GVE) | Proveedor de medidas (`gve.*`); el atlas nunca mide por su cuenta. Hoy sus informes no dicen variante, máquina ni motor: se le hace una petición (D-19) |
| `Instalador-WMF-Tarkor` | Consumidor: modelos y variantes para descargar; detecta el hardware en ejecución y llama a `fit` con él |
| `galivelop-image-generator` (gimg), `galivelop-voice-generator` (gvoice) | Consumidores: variantes multiarchivo y la máquina `steam-deck` |
| `galivelop-developer` (gvc) | Consumidor: variantes por tarea y las máquinas de sus niveles (`steam-deck`, `gpu-12gb`) |
| `World-Maker-Fantasy` | Consumidor posterior (Ollama del juego); de momento congelado |
| `Portal-Galivelop` | Consumidor: página pública del atlas, en `src/data/proyectos/` (D-15) |

Los consumidores reciben una **copia vendorizada** del catálogo (y de `gmod` si lo necesitan), con su versión y un test
que compara la huella del manifiesto, igual que con `gart`. No hay servidor ni descarga en tiempo de ejecución.

## 4. Modelo

- **Raíz del agregado:** `Catalog`. Toda alta o cambio de modelo, variante, máquina o medida pasa por ella y comprueba
  las invariantes.
- **Entidades:** `Model` (con sus `Variant`), `Machine`.
- **Objetos de valor:** `Variant` (con sus `VariantFile` y su `Source`), `License`, `Runtime`, `Task`, `Hardware`,
  `Fit`, `Measurement`, `Recommendation`, `Manifest`. Una `Variant` es objeto de valor dentro de su `Model`, pero su id
  es estable y es lo que citan las medidas, la CLI y los consumidores (D-6).
- **Servicios:**
  - `fit(variant, machine_or_hardware) -> Fit`: acepta una `Machine` del catálogo o un `Hardware` detectado (D-21);
  - `recommend(task, machine_or_hardware, *, license_use=None) -> list[Recommendation]`;
  - `detect_hardware() -> Hardware`;
  - `ingest(gve_report) -> list[Measurement]`;
  - `build_manifest(catalog) -> Manifest`.
- **Eventos:** ninguno en la v1 (biblioteca y datos sin estado).

**Artefactos** (esquemas en este repo, validados con `gart`):
- `gmod.model/0` (modelo con sus variantes, archivos y orígenes)
- `gmod.machine/0`
- `gmod.measurement/0`
- `gmod.catalog/0`
- `gmod.manifest/0`

Todos son provisionales (`/0`) hasta H6; en H6 pasan a `/1`.

## 5. Invariantes (cada una con su test)

1. Cada `Variant` tiene origen, licencia y tamaño total en bytes. Con origen `hf` o `url`, cada `VariantFile` tiene rol,
   sha256, bytes y url; con origen `ollama`, la variante tiene `name:tag` y digest del manifiesto. Sin alguno de ellos,
   el catálogo no valida.
2. Un origen `hf` fija la revisión a un commit (40 caracteres hexadecimales); `main` o cualquier rama no validan (D-24).
3. Cada `Model` declara al menos una `Task` de la lista cerrada, y cada `Variant` al menos un `Runtime` con versión
   mínima. Un LoRA cita un modelo base que existe en el catálogo.
4. **Un catálogo publicado no cambia:** su manifiesto guarda la huella de cada archivo; un cambio sin subir la versión
   del catálogo falla.
5. `fit` y `recommend` son **deterministas**: con el mismo catálogo y la misma máquina dan el mismo resultado en el mismo
   orden. Los empates se deshacen por id de variante.
6. `fit` **falla cerrado**: si le falta un dato de la máquina o de la variante (VRAM desconocida, cuantización sin
   regla), el veredicto es `unknown` y el motivo nombra el dato que falta; nunca `fits` ni `tight`. `recommend` no
   ofrece nunca una variante `unknown` ni `no` (D-7).
7. Una `Measurement` siempre cita su informe de GVE (id y versión del esquema `gve.*`) y la variante, la máquina y la
   versión del motor medidas; sin esa cita no entra en el catálogo.
8. `recommend` con `license_use` excluye las variantes cuya licencia no permite ese uso; una licencia `unconfirmed` se
   excluye siempre que se pase `license_use` (D-13).
9. La máquina `steam-deck` existe siempre, y cada `Task` de la lista cerrada tiene al menos una variante con veredicto
   `fits` o `tight` en ella (D-16).
10. Tamaños en bytes y memoria en MiB enteros en todos los artefactos (D-23).
11. Los catálogos es/en de textos tienen las mismas claves y los mismos marcadores.
12. Sin dependencias fuera de stdlib y sin red en `gmod`; los tests no salen a la red.

## 6. Alcance

**Dentro:**
- esquemas `gmod.*` y el catálogo inicial en `catalog/` (D-3), migrado de los catálogos de los consumidores, con una
  tabla de diferencias primero;
- detección de hardware en Linux (incluida la Steam Deck) y Windows;
- `fit` (estimación de memoria de la variante) y `recommend`;
- ingesta de informes de GVE;
- manifiesto de huellas sha256;
- exportación para consumidores y una página estática (JSON + HTML) para el portal;
- la CLI:
  - `gmod detect`
  - `gmod fit <variant> [--machine <id>]` (sin `--machine`, con el hardware detectado)
  - `gmod recommend <task> [--machine <id>] [--license-use <uso>]`
  - `gmod ingest <informe-gve>`
  - `gmod manifest`
  - `gmod list`
  - `gmod show <id>`

**Fuera:**
- descargar modelos: lo sigue haciendo cada consumidor, y el atlas solo da el origen y las huellas;
- medir: lo hace GVE;
- ejecutar modelos;
- ajustes de ejecución, reservas de memoria y asignación de modelos por rol: son de cada consumidor (D-11, D-20, D-22);
- datasets (D-8);
- máquinas y medidas de terceros (D-4); se reconsidera con el GVE Hub;
- firma criptográfica del catálogo (D-2); se decide cuando el instalador descargue el catálogo por la red;
- un servidor o una API en línea;
- macOS en la v1;
- precios de modelos en la nube.

## 7. Escalera de hitos

| Hito | Nivel | Qué | Espera a | Lo decide |
|---|---|---|---|---|
| H1 | un archivo | Esquemas `gmod.model/0` y `gmod.machine/0`, con ejemplos válidos e inválidos | validador de `gart` | tests de validación, incluidas las invariantes 1, 2, 3 y 10 |
| H2 | varios pasos | Catálogo inicial: tabla de diferencias entre los catálogos del instalador, gimg, gvoice y gvc (parte del inventario), con las revisiones de `hf` fijadas a un commit; después, la migración a `catalog/` | — (los datos se preparan antes que H1; validan al llegar H1) | cada modelo y máquina actual está en el catálogo; la tabla de diferencias, revisada por la persona |
| H3 | varios pasos | `fit` con la tabla de reglas de memoria (pesos + contexto + margen por motor), mantenida a mano (D-5) | H1 | tests de encaje, incluidos los casos `unknown` (invariante 6) y la máquina `steam-deck` (invariante 9) |
| H4 | un archivo | `recommend` con filtro por tarea y por licencia | H3 | tests de orden, empates y licencias (invariantes 5 y 8) |
| H5 | varios pasos | `detect_hardware` en Linux y Windows, con la lectura de `/proc` y `sysfs` simulada en los tests | — | tests con muestras de la Deck, CUDA, ROCm y solo CPU; la prueba real en la Deck queda como pendiente de la persona |
| H6 | partir un hito | Ingesta de GVE (`gmod.measurement`), informe de desviación entre estimación y medida con umbral configurable (D-5), y paso de todos los tipos a `/1` | versión de GVE con variante, máquina y motor (D-19) | tests con informes `gve.*` reales del repo de GVE |
| H7 | varios pasos | Manifiesto y exportación vendorizada | H1 | test de huella en un consumidor de ejemplo (invariante 4) |
| H8 | varios pasos | Textos es/en, CLI y página para el portal | H4, H7 | tests de `main([...])` en los dos idiomas; ficha en `docs/projects/Portal-Galivelop.md` con la página en `src/data/proyectos/` |

**Después de H8, en cada repo consumidor** (es una tarea de ese repo, no de este): sustituir su catálogo por la copia
vendorizada y hacer que sus ajustes y asignaciones por rol citen ids de gmod. Lo que tenga que hacer cada repo se apunta
en `docs/projects/<repo>.md`.

## 8. Preguntas abiertas

Ninguna: las cinco del borrador 1 y las que salieron en F-1 están resueltas abajo. Las que aparezcan al trabajar se
apuntan en `docs/questions.md`.

## Decisiones

Resueltas en F-1 (`docs/questions.md`, rondas 1 a 3) e integradas en el texto de arriba.

- **D-1 (Q-1):** F-1 mejora, amplía y cerciora este DDD; F0 sube a `main` lo decidido en F-1 y lo ordena en versiones.
- **D-2 (Q-2):** sin firma criptográfica en v1: el catálogo publicado lleva un manifiesto con sha256 de cada archivo.
- **D-3 (Q-3):** los datos del catálogo viven en este repo, en `catalog/`.
- **D-4 (Q-4):** en v1 no se aceptan máquinas ni medidas de terceros.
- **D-5 (Q-5):** las reglas de memoria se mantienen a mano en H3; desde H6, un informe de desviación frente a GVE con umbral configurable.
- **D-6 (Q-6):** id de Variante `<model-id>:<formato>-<cuant>` en minúsculas (p. ej. `qwen3-8b-instruct:gguf-q4_k_m`); sigue siendo objeto de valor dentro de Modelo.
- **D-7 (Q-7):** Encaje con cuatro veredictos: el cuarto, `unknown`, cuando falta un dato; `recommend` nunca lo ofrece y el motivo dice qué dato falta.
- **D-8 (Q-8):** datasets fuera; un LoRA es un Modelo con su Tarea y referencia al modelo base; su licencia, por los usos normales.
- **D-9 (Q-9):** los hitos de esquema y validación esperan al validador publicado de gart, sin validador provisional; mientras, se avanza en lo que no depende de gart.
- **D-10 (Q-10):** los esquemas `gmod.*` viven en este repo; gart solo los carga y valida.
- **D-11 (Q-11):** Máquina describe solo hardware; los ajustes de ejecución de cada app quedan en el consumidor, que cita la máquina por id.
- **D-12 (Q-12):** una Variante es un conjunto de archivos con rol (pesos, texto, vae, tokenizador compartido), cada uno con sha256, bytes y url.
- **D-13 (Q-13):** licencia `unconfirmed` explícita, sin usos permitidos; `license_use` la excluye siempre.
- **D-14 (Q-14):** orígenes v1: `hf` (repo + revisión), `url` y `ollama` (`name:tag` + digest).
- **D-15 (Q-15):** el portal no dice «firmado»; las páginas van en `src/data/proyectos/`.
- **D-16 (Q-16):** lista cerrada de Tareas en v1 (texto, embeddings, imagen, voz a texto, texto a voz, visión); añadir una es cambio de esquema. El invariante de `steam-deck` se limita a ella.
- **D-17 (Q-17):** los commits salen con la cuenta de la persona, la del commit inicial (`git log --format='%an <%ae>' --reverse | head -1`), nunca con `noreply@anthropic.com`. Corregido el 2026-11-27: la respuesta «ok» se había leído como «seguir con el autor actual».
- **D-18 (Q-18):** GVE, gvc, el instalador, gimg y gvoice se leen en solo lectura para la tabla de diferencias de H2 (inventario en `docs/records/`).
- **D-19 (Q-19):** H6 depende de que GVE añada a sus informes la variante, la máquina y la versión del motor; se le deja una petición escrita en `docs/records/`.
- **D-20 (Q-20):** las asignaciones de modelo por rol se quedan en cada consumidor; gmod da modelos, variantes, máquinas y encaje.
- **D-21 (Q-21):** `fit` acepta una Máquina del catálogo por id o un hardware detectado en ejecución, con los mismos campos.
- **D-22 (Q-22):** `fit` estima la memoria de la variante; la reserva de cada app la pone el consumidor.
- **D-23 (Q-23):** tamaños en bytes y memoria en MiB enteros en todo gmod.
- **D-24 (Q-24):** un origen `hf` fija la revisión a un commit, nunca `main`.
- **D-25 (Q-25):** el tag de Ollama es solo un origen (con su digest); la cuantización real se apunta en la variante.
