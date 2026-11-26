# DDD: galivelop-models (borrador 1, 2026-11-26)

> Estado: borrador 1, tal como llegó. En F-1 se revisa con la persona (`grill-with-docs`, preguntas en
> `docs/questions.md`) y aquí queda la versión final.

**Uso:** entrada para levantar el repo desde el paso 0, como el DDD de `galivelop-artifacts`. Cuando toque, la persona crea el repo vacío y el proyecto se levanta a partir de este documento. Las preguntas abiertas (§8) se resuelven durante el trabajo y se apunta cómo.

Nombre del repositorio y del proyecto: `galivelop-models` (Model Atlas en el portal). Paquete Python importable: `gmod`. Espacio de artefactos: `gmod`. Visibilidad: repo público, con la misma licencia que los demás repos Galivelop.

**Depende de:** `galivelop-artifacts` (`gart`) con su validador (H2) y su registro (H4). No se empieza antes.

## 1. Propósito

Un **catálogo único, versionado y verificable de modelos de IA local** y de las **máquinas** donde corren, con la respuesta a «¿qué modelo, en qué cuantización y con qué ajustes cabe y rinde en esta máquina?». Hecho solo con stdlib (Python ≥ 3.10).

Sustituye a los catálogos y perfiles que hoy está duplicados:
- el catálogo del instalador (`app/catalogo/catalogo.json` y `perfiles.rs`);
- los perfiles de máquina de gimg (`machine_profiles/steam-deck.json`, …);
- los perfiles de máquina de gvoice (`gvoice/machine_profiles/`);
- los perfiles propios de gvc.

Las medidas de rendimiento y calidad vienen de GVE: el atlas no mide, recoge las medidas y las cita.

**Éxito:**
- el instalador, gimg, gvoice y gvc leen sus modelos y perfiles de una copia de `gmod`, sin cambiar el comportamiento de sus tests;
- el portal publica la página del atlas a partir de ese mismo catálogo.

## 2. Lenguaje del dominio

| Término | Código | Significado |
|---|---|---|
| Modelo | `Model` | Un modelo publicado (familia + tamaño + variante), p. ej. `qwen3-8b-instruct`. Independiente de cómo se empaqueta |
| Variante | `Variant` | Un archivo concreto de un modelo: formato (`gguf`, `safetensors`), cuantización (`Q4_K_M`…), tamaño en bytes, sha256 y origen |
| Tarea | `Task` | Para qué sirve: `chat`, `embed`, `rerank`, `image`, `tts`, `stt`, `judge`… Un modelo declara una o varias |
| Motor | `Runtime` | Lo que ejecuta la variante: `ollama`, `llama.cpp`, `stable-diffusion.cpp`, `qwentts.cpp`… Con su versión mínima |
| Licencia | `License` | Identificador SPDX o ficha propia, con usos permitidos (`commercial`, `redistribute`, `derivatives`) |
| Máquina | `Machine` | Un perfil de hardware: CPU, RAM, GPU/VRAM, API de cómputo (`cuda`, `rocm`, `vulkan`, `metal`, `cpu`) y SO. La Steam Deck es el perfil mínimo de referencia |
| Encaje | `Fit` | Veredicto de una variante en una máquina: `fits`, `tight`, `no`, con la memoria estimada y el motivo |
| Medida | `Measurement` | Un resultado de GVE (velocidad, memoria pico, puntuación de calidad) de una variante en una máquina, con su fecha, la versión del motor y la referencia al informe de GVE |
| Recomendación | `Recommendation` | Para una `Task` y una `Machine`, la lista ordenada de variantes que encajan, con el motivo |
| Catálogo | `Catalog` | Conjunto publicado de modelos, variantes, máquinas y medidas, con versión y manifiesto de huellas |
| Manifiesto | `Manifest` | Lista de archivos del catálogo con su sha256 y la huella global de la versión |

**Notas:**
- Los nombres de código y los campos de los artefactos están en inglés; los textos visibles se dan en es y en.
- La palabra «firmado» del portal quiere decir, en la v1, «con manifiesto de huellas sha256 verificable». La firma criptográfica es la pregunta 1 (§8).

## 3. Contextos acotados

1. **Catálogo (núcleo):** `Model`, `Variant`, `License`, `Runtime` y `Task`, con su validación contra los esquemas `gmod.*` de `gart`. Es puro: sin E/S ni red.
2. **Máquinas:** perfiles de `Machine` y la detección local (lee `/proc`, `lspci`/`sysfs` u otras fuentes del sistema que se definan); la detección es la única parte con E/S de sistema.
3. **Encaje y recomendación:** `fit(variant, machine)` y `recommend(task, machine)`. Funciones puras y deterministas, con la estimación de memoria basada en la tabla de reglas del catálogo.
4. **Medidas:** recoge informes `gve.*` y los convierte en `Measurement`. GVE es el dueño de la medida; el atlas solo la cita y la agrega.
5. **Publicación:** manifiesto, exportación para consumidores (copia vendorizada o JSON plano), página para el portal y CLI.

**Mapa con los demás repos:**

| Repo | Relación con el atlas |
|---|---|
| `galivelop-artifacts` | Proveedor: validador y formato `KindId`. Los esquemas `gmod.*` los publica este repo |
| `galivelop-evaluator` (GVE) | Proveedor de medidas (`gve.*/1`); el atlas nunca mide por su cuenta |
| `Instalador-WMF-Tarkor` | Consumidor: catálogo de descarga y perfiles de máquina |
| `galivelop-image-generator`, `galivelop-voice-generator` | Consumidores: perfiles de máquina y elección de modelo |
| `galivelop-developer` (gvc) | Consumidor: qué modelo usar por tarea en la máquina de la persona |
| `World-Maker-Fantasy` | Consumidor posterior (Ollama del juego); de momento congelado |
| `Portal-Galivelop` | Consumidor: página pública del atlas |

Los consumidores reciben una **copia vendorizada** del catálogo (y de `gmod` si lo necesitan), con su versión y un test que compara la huella del manifiesto, igual que con `gart`. No hay servidor ni descarga en tiempo de ejecución.

## 4. Modelo

- **Raíz del agregado:** `Catalog`. Toda alta o cambio de modelo, variante, máquina o medida pasa por ella y comprueba las invariantes.
- **Entidades:** `Model` (con sus `Variant`), `Machine`.
- **Objetos de valor:** `Variant`, `License`, `Runtime`, `Task`, `Fit`, `Measurement`, `Recommendation`, `Manifest`.
- **Servicios:**
  - `fit(variant, machine) -> Fit`;
  - `recommend(task, machine, *, license_use=None) -> list[Recommendation]`;
  - `detect_machine() -> Machine`;
  - `ingest(gve_report) -> list[Measurement]`;
  - `build_manifest(catalog) -> Manifest`.
- **Eventos:** ninguno en la v1 (biblioteca y datos sin estado).

**Artefactos (`gart`):**
- `gmod.model/0`
- `gmod.machine/0`
- `gmod.measurement/0`
- `gmod.catalog/0`
- `gmod.manifest/0`

Todos son provisionales (`/0`) hasta H6; en H6 pasan a `/1`.

## 5. Invariantes (cada una con su test)

1. Cada `Variant` tiene sha256, tamaño en bytes, origen (URL o repo de Hugging Face) y licencia; sin alguno de ellos, el catálogo no valida.
2. Cada `Model` declara al menos una `Task` y cada `Variant` al menos un `Runtime` con versión mínima.
3. **Un catálogo publicado no cambia:** su manifiesto guarda la huella de cada archivo; un cambio sin subir la versión del catálogo falla.
4. `fit` y `recommend` son **deterministas**: con el mismo catálogo y la misma máquina dan el mismo resultado en el mismo orden. Los empates se deshacen por nombre.
5. `fit` **falla cerrado**: si le falta un dato de la máquina o de la variante (VRAM desconocida, cuantización sin regla), el resultado es `no` con el motivo, nunca `fits`.
6. Una `Measurement` siempre cita su informe de GVE (id y versión del esquema `gve.*`); sin esa cita no entra en el catálogo.
7. `recommend` con `license_use` excluye las variantes cuya licencia no permite ese uso.
8. El perfil `steam-deck` existe siempre, y cada `Task` tiene al menos una variante que encaja en él (el perfil mínimo de Galivelop).
9. Los catálogos es/en de textos tienen las mismas claves y los mismos marcadores.
10. Sin dependencias fuera de stdlib y sin red en `gmod`; los tests no salen a la red.

## 6. Alcance

**Dentro:**
- esquemas `gmod.*` y el catálogo inicial, migrado de los catálogos y perfiles actuales, con una tabla de diferencias primero;
- detección de máquina en Linux (incluida la Steam Deck) y Windows;
- `fit` y `recommend`;
- ingesta de informes de GVE;
- manifiesto de huellas;
- exportación para consumidores y una página estática (JSON + HTML) para el portal;
- la CLI:
  - `gmod detect`
  - `gmod fit <variant> [--machine <id>]`
  - `gmod recommend <task> [--machine <id>] [--license-use <uso>]`
  - `gmod ingest <informe-gve>`
  - `gmod manifest`
  - `gmod list`
  - `gmod show <id>`

**Fuera:**
- descargar modelos: lo sigue haciendo cada consumidor, y el atlas solo da URL y huella;
- medir: lo hace GVE;
- ejecutar modelos;
- un servidor o una API en línea;
- macOS en la v1;
- precios de modelos en la nube.

## 7. Escalera de hitos

| Hito | Nivel | Qué | Lo decide |
|---|---|---|---|
| H1 | un archivo | Esquemas `gmod.model/0` y `gmod.machine/0` sobre `gart`, con ejemplos válidos e inválidos | tests de validación |
| H2 | varios pasos | Catálogo inicial: tabla de diferencias entre los catálogos y perfiles del instalador, gimg, gvoice y gvc; después, la migración | cada modelo y perfil actual está en el catálogo; la tabla de diferencias, revisada por la persona |
| H3 | varios pasos | `fit` con la tabla de reglas de memoria (pesos + contexto + margen por motor) | tests de encaje, incluidos los casos de falta de datos (invariante 5) y el perfil `steam-deck` (invariante 8) |
| H4 | un archivo | `recommend` con filtro por tarea y por licencia | tests de orden y de empates (invariantes 4 y 7) |
| H5 | varios pasos | `detect_machine` en Linux y Windows, con la lectura de `/proc` y `sysfs` simulada en los tests | tests con muestras de la Deck, CUDA, ROCm y solo CPU; la prueba real en la Deck queda como pendiente de la persona |
| H6 | partir un hito | Ingesta de GVE (`gmod.measurement`) y paso de todos los tipos a `/1` | tests con informes `gve.*/1` reales del repo de GVE |
| H7 | varios pasos | Manifiesto y exportación vendorizada | test de huella en un consumidor de ejemplo (invariante 3) |
| H8 | varios pasos | Textos es/en, CLI y página para el portal | tests de `main([...])` en los dos idiomas; ficha en `docs/projects/Portal-Galivelop.md` |

**Después de H8, en cada repo consumidor** (es una tarea de ese repo, no de este): sustituir su catálogo o sus perfiles por la copia vendorizada. Lo que tenga que hacer cada repo se apunta en `docs/projects/<repo>.md`.

## 8. Preguntas abiertas

1. **Firma del catálogo.** La v1 lleva solo un manifiesto sha256. ¿Hace falta una firma criptográfica (minisign, sigstore) fuera de stdlib, como extra opcional? Recomendación: no en la v1; se decide cuando el instalador descargue el catálogo por la red.
2. **Dónde viven los datos.** ¿El catálogo va en este repo o en un repo de datos aparte? Recomendación: en este repo, en `catalog/`, hasta que su tamaño o su ritmo de cambio lo pidan.
3. **Reglas de memoria.** ¿Las reglas de `fit` se ajustan a mano o se recalibran con las medidas de GVE? Recomendación: a mano en H3 y, desde H6, un informe que señale dónde la estimación se aleja más de un umbral de lo medido. El umbral es una clave de configuración.
4. **Licencias de los datasets y LoRA propios** (p. ej. los de Tarkor, con CC BY-NC-SA). ¿Entran en el atlas? Recomendación: sí, con su licencia, pero marcados como `derivatives`. El filtro de licencia de `recommend` decide si se ofrecen.
5. **Máquinas de la comunidad.** ¿Se aceptan perfiles y medidas de terceros? Recomendación: no en la v1; se reconsidera con el GVE Hub.

## Decisiones

_(vacío: se rellena al resolver las preguntas de §8)_
