# Diferencias entre los catálogos de los consumidores (2026-11-27)

Tabla de diferencias de H2, en solo lectura (D-18). Complementa `docs/records/inventario-consumidores-2026-11-26.md` (no repite su resumen).

- **Fecha:** 2026-11-27.
- **Commits leídos:** instalador `56f0108` (`/home/user/zeldris/Instalador-WMF-Tarkor`), gimg `bc27219` (`/home/user/zeldris/galivelop-image-generator`), gvoice `8a17618` (`/home/user/zeldris/galivelop-voice-generator`), gvc `014f7ff` (`/home/user/galivelop-developer`).
- **(I) = inferencia; lo demás se leyó.** «—» = el dato no está en la fuente (va a Huecos).
- **Abreviaturas de ruta:** `inst:` = instalador, `gimg:`, `gvoice:`, `gvc:`. Atención: en gimg y gvoice los archivos están dentro del paquete, es decir `gimg:gimg/models.json`, `gvoice:gvoice/engines/qwentts.json`, etc. (el encargo los citaba sin el directorio `gimg/` ni `gvoice/`).
- **Conversiones:** `descargaGb` (instalador) no declara unidad; se toma GB decimal = 10^9 bytes (I, es la unidad de Ollama) y el resultado es aproximado. `sizeMb` de gimg es «megabytes (10^6 bytes), rounded» (`gimg:gimg/schemas/models.schema.json`, l.144): bytes = sizeMb × 10^6, **solo aproximado** (redondeado). gvoice da bytes exactos. Memoria: MiB = GiB × 1024; el instalador usa `MB_POR_GB = 1024` (`inst:app/nucleo/src/perfiles.rs` l.9), así que sus «GB» de memoria son GiB.

## 1. Tabla de modelos

13 modelos, 13 variantes (una por modelo hoy). Los archivos auxiliares (codificadores de texto, VAE, tokenizador) son `VariantFile` con rol (D-12), no modelos. Todas las variantes de Ollama: motor `ollama`, versión mínima del motor no declarada por modelo (el instalador empaqueta Ollama `0.34.3`, `inst:app/catalogo/catalogo.json` `motor.version`; gvc exige `minVersion` `0.34.2`, `gvc:gdev/machine_profiles/steam-deck.json` `engine.minVersion`).

### 1.1 Modelos de Ollama (instalador y gvc)

Para todos: Origen `ollama name:tag` sin digest ni cuantización real en la fuente (D-25; va a Huecos H-4 y H-5); archivos: no hay (Ollama los gestiona); sha256: no; revisión: n/a (digest —). Tarea `text` salvo que se indique.

| Model / Variant propuestos | Tarea | Origen (tag) | Tamaño de descarga | Licencia (tal cual → SPDX propuesto) | Consumidores y ruta | Diferencias / conflictos |
|---|---|---|---|---|---|---|
| `llama3.1-8b-instruct` / `llama3.1-8b-instruct:gguf-q4_k_m` (I: cuantización del tag `llama3.1:8b`, sin confirmar) | text | `ollama llama3.1:8b` | 4,9 GB → ≈4 900 000 000 B (I) | `Llama-3.1-Community` → `unconfirmed` hasta decidir (no es SPDX; ficha propia, ver P-3) | inst: `app/catalogo/catalogo.json` `modelos["llama3.1:8b"]`; perfiles `equilibrado` y `maximo` como `narrador` (`perfiles[2..3].narrador`) | Solo lo usa el instalador. `piensa: false` es ajuste de app. |
| `qwen2.5-1.5b-instruct` / `qwen2.5-1.5b-instruct:gguf-q4_k_m` (I) | text | `ollama qwen2.5:1.5b-instruct` | 1,0 GB → ≈1 000 000 000 B (I) | `Apache-2.0` → `Apache-2.0` | inst: `catalogo.json` `modelos["qwen2.5:1.5b-instruct"]`; perfiles `minimo`, `ligero`, `equilibrado`, `maximo`, `ultra` como `cronista`/`sugerencias` | Solo instalador. |
| `qwen3.5-0.8b` / `qwen3.5-0.8b:gguf-?` | text | `ollama qwen3.5:0.8b` | 1,0 GB → ≈1 000 000 000 B (I) | `Apache-2.0` → `Apache-2.0` | inst: `catalogo.json` `modelos["qwen3.5:0.8b"]` | Ningún perfil de `perfiles` lo cita (el instalador lo descarga solo si se elige a mano, I). Mismo tamaño que `qwen2.5:1.5b-instruct` (1,0 GB) con la mitad de parámetros: dato dudoso, ver H-3. |
| `qwen3.5-2b` / `qwen3.5-2b:gguf-?` | text | `ollama qwen3.5:2b` | 2,7 GB → ≈2 700 000 000 B (I) | `Apache-2.0` | inst: `catalogo.json` `modelos["qwen3.5:2b"]`; perfil `ligero` como `narrador` | Solo instalador. |
| `qwen3.5-4b` / `qwen3.5-4b:gguf-?` | text | `ollama qwen3.5:4b` | 3,4 GB → ≈3 400 000 000 B (I) | `Apache-2.0` | inst: `catalogo.json` `modelos["qwen3.5:4b"]`; perfiles `maximo`, `ultra` como `sugerencias`. gvc: `gdev/catalog.json` `cells[1]` (worker, `steam-deck`); `gdev/machine_profiles/steam-deck.json` `models[1]` | **Dos consumidores.** gvc no declara licencia ni tamaño; lo toma del instalador (`gvc:gdev/catalog.json` `origin`: «Adapted from Instalador…»). Memoria mínima: gvc `minFreeGiB: 5` (catálogo) = `minAvailableGiB: 5` (perfil) = 5120 MiB; el instalador no tiene umbral por modelo (solo `memoriaGb` por perfil). Mismo dato con dos nombres dentro de gvc. |
| `qwen3.5-9b` / `qwen3.5-9b:gguf-?` | text | `ollama qwen3.5:9b` | 6,6 GB → ≈6 600 000 000 B (I) | `Apache-2.0` | inst: `catalogo.json` `modelos["qwen3.5:9b"]`; perfil `ultra` como `narrador` (experimental). gvc: `gdev/catalog.json` `cells[0]`; `gdev/machine_profiles/steam-deck.json` `models[0]` | Igual que 4b. gvc `minFreeGiB: 9` = 9216 MiB, `confirmed: true`, para `steam-deck`; el instalador marca `ultra` como `experimental` y `memoriaGb: 14.0` = 14336 MiB (perfil entero, no solo este modelo). Posible choque: el instalador pide 14 GiB para un perfil con 9b y gvc 9 GiB libres para 9b solo. |
| `nomic-embed-text-v1.5` (I: el tag `nomic-embed-text` apunta a v1.5) / `nomic-embed-text-v1.5:gguf-f16` (I) | embed | `ollama nomic-embed-text` | 0,3 GB → ≈300 000 000 B (I) | `Apache-2.0` | inst: `catalogo.json` `modelos["nomic-embed-text"]`; todos los perfiles como `embeddings` | Solo instalador. Tag sin `:tag` explícito (implica `latest`). |

### 1.2 Modelos de imagen (gimg)

Motor: `stable-diffusion.cpp` release `master-95ff762` con Vulkan (`gimg:instalar.sh` l.20: `sd-master-95ff762-bin-Linux-Ubuntu-24.04-x86_64-vulkan.zip`, sha256 `5af606a8…dad1` del zip; no hay «versión mínima» sino release fija, ver H-6). Tarea `image`. Origen `hf` con URL `…/resolve/main/…` = revisión `main` sin fijar (D-24). Todos: `gimg:gimg/models.json`, entrada `models.<clave>`.

| Model / Variant propuestos | Archivos (rol → nombre, sha256, tamaño) | Origen hf (repo / ruta) | Licencia | Consumidores | Diferencias / conflictos |
|---|---|---|---|---|---|
| `flux2-klein-4b` / `flux2-klein-4b:gguf-q8_0` (clave gimg `flux2-klein-4b-q8`) | `diffusion` → `flux-2-klein-4b-Q8_0.gguf`, sha256 sí (`0bba6951…fa28`), 4301 MB → ≈4 301 000 000 B. `text` → `Qwen3-4B-Q4_K_M.gguf`, sí (`f6f85177…813a`), 2497 MB → ≈2 497 000 000 B. `vae` → `full_encoder_small_decoder.safetensors`, sí (`ea4273f0…ab62`), 250 MB → ≈250 000 000 B. Total ≈7 048 000 000 B (I, suma) | `leejet/FLUX.2-klein-4B-GGUF` (diffusion); `unsloth/Qwen3-4B-GGUF` (text); `black-forest-labs/FLUX.2-small-decoder` (vae); rev `main` | `Apache-2.0` → `Apache-2.0` (una licencia para tres archivos de tres repos; ver P-4) | `gimg:gimg/models.json`; perfil `gimg:gimg/machine_profiles/steam-deck.json` (sin sobrescritura propia) | `installDefault: true` solo aquí. Ajustes de app (`defaults`, `args`) se quedan en gimg. |
| `flux3-image-klein` / `flux3-image-klein:gguf-q8_0` (clave `flux3-klein-q8`) | `diffusion` → `flux3-image-klein-Q8_0.gguf`, sí (`8b71ffd7…9752`), 6152 MB → ≈6 152 000 000 B. `text` → `Qwen3VL-4B-Instruct-Q4_K_M.gguf`, sí (`66358cb1…0a0a`), 2497 MB. `vae` → `flux2-vae.safetensors`, sí (`d64f3a68…c4b5`), 336 MB. Total ≈8 985 000 000 B (I) | `leejet/flux-3-image-klein-GGUF`; `Qwen/Qwen3-VL-4B-Instruct-GGUF`; `Comfy-Org/flux2-dev` (ruta `split_files/vae/flux2-vae.safetensors`); rev `main` | `unconfirmed` (explícita en la fuente) → `unconfirmed` (D-13) | gimg: `models.json`; perfil `steam-deck.json` `engine.models["flux3-klein-q8"]` | El `text` pesa igual que el de Qwen3-4B (2497 MB) pese a ser otro modelo (Qwen3-VL-4B): dato sospechoso, H-3. Id con «flux3»: ver P-1. |
| `z-image-turbo` / `z-image-turbo:gguf-q6_k` (clave `zimage-turbo-q6`) | `diffusion` → `z_image_turbo-Q6_K.gguf`, sí (`319f627b…01af`), 5263 MB → ≈5 263 000 000 B. `text` → `Qwen3-4B-Q4_K_M.gguf` (el mismo archivo que en flux2-klein, sha256 igual `f6f85177…813a`). `vae` → `ae.safetensors`, sí (`afc8e282…9e38`), 335 MB. Total ≈8 095 000 000 B (I) | `leejet/Z-Image-Turbo-GGUF`; `unsloth/Qwen3-4B-GGUF`; `Comfy-Org/Z-Image-Turbo` (ruta `split_files/vae/ae.safetensors`); rev `main` | `Apache-2.0` | gimg: `models.json`; perfil `steam-deck.json` `engine.models["zimage-turbo-q6"]` | Comparte archivo `text` con flux2-klein (mismo sha256 y url): gmod debe permitir el mismo archivo en varias variantes sin descargarlo dos veces (ver P-5). |

### 1.3 Modelos de voz (gvoice)

Motor: `qwentts.cpp`, repo `https://github.com/ServeurpersoCom/qwentts.cpp`, commit `5916bf7c79dbb4e66fc059cdc507a79a23a28bb4` (`gvoice:gvoice/engines/qwentts.json`); no hay número de versión (H-6). Tarea `tts`. Origen `hf` repo `Serveurperso/Qwen3-TTS-GGUF`, rev `main`. Licencia: **ausente** en la fuente (→ `unconfirmed`, D-13). Cuantización solo en el nombre de archivo (`Q8_0`). Cada variante necesita además el archivo `tokenizer-12hz` (rol `codec` en gvoice; en gmod el rol se llamaría `tokenizer`/`codec`, ver P-6).

| Model / Variant propuestos (id gvoice) | Archivo propio: nombre, bytes, sha256 | Uso (`use`) | Consumidores | Diferencias |
|---|---|---|---|---|
| `qwen3-tts-0.6b-base` / `…:gguf-q8_0` (`0.6b-base`) | `qwen-talker-0.6b-base-Q8_0.gguf`, 992 615 488 B (946 MiB), sí `d54dbaf1…6426` | `base` | `gvoice:gvoice/engines/qwentts.json` `models[0]`; perfil `gvoice:gvoice/machine_profiles/steam-deck.json` `models.produce[0]` | gvoice lo llama «producción». |
| `qwen3-tts-1.7b-base` / `…:gguf-q8_0` (`1.7b-base`) | `qwen-talker-1.7b-base-Q8_0.gguf`, 2 079 448 256 B (1983 MiB), sí `4b9a33a2…4fda` | `base` | `engines/qwentts.json` `models[1]`; perfil `models.produce[1]` | |
| `qwen3-tts-1.7b-voicedesign` / `…:gguf-q8_0` (`1.7b-voicedesign`) | `qwen-talker-1.7b-voicedesign-Q8_0.gguf`, 2 042 833 824 B (1948 MiB), sí `575610ab…2276` | `design` | `engines/qwentts.json` `models[2]`; perfil `models.design` | |
| (archivo compartido `tokenizer-12hz`) | `qwen-tokenizer-12hz-Q8_0.gguf`, 291 150 624 B (277 MiB), sí `1883beee…fbd94` | `codec` | `engines/qwentts.json` `models[3]` | Va en las tres variantes. Suma por variante (propio + tokenizador): 0.6b 1 283 766 112 B; 1.7b-base 2 370 598 880 B; voicedesign 2 333 984 448 B (I, suma). |

Los MiB redondean a la baja el cociente exacto (946,63; 1983,12; 1948,20; 277,66); en gmod el tamaño canónico son los bytes.

### 1.4 Diferencias transversales entre consumidores sobre un mismo modelo

- **Único solape real de modelo:** `qwen3.5:9b` y `qwen3.5:4b` (instalador y gvc). Origen y tag iguales; gvc copia del instalador sin licencia ni tamaño. Los umbrales de memoria solo existen en gvc (`minFreeGiB`/`minAvailableGiB`, duplicados en dos archivos de gvc, ambos 9 y 5).
- **Solape de archivo:** `Qwen3-4B-Q4_K_M.gguf` en dos variantes de gimg. No hay solape entre Ollama y gimg: gimg tiene un `Qwen3-4B` GGUF (text encoder) y el instalador tiene `qwen3.5:*`, familias distintas.
- **Motor de los mismos pesos:** gvc mantiene `llamaServer.apiBase` `http://127.0.0.1:11435` (`gvc:gdev/machine_profiles/steam-deck.json`) como ruta alternativa a Ollama; no declara qué archivos GGUF usaría (—).
- **Ollama como runtime, no como modelo:** instalador `motor` (0.34.3, MIT, sha256 de dos paquetes, `descargaGb` 1,33/1,36 → ≈1 330 000 000 / 1 360 000 000 B (I)) y gvc `minVersion 0.34.2`; no son variantes.

## 2. Tabla de máquinas

2 máquinas: `steam-deck` y `gpu-12gb`. El instalador no guarda máquinas; detecta `Hardware` (D-21) con esta estructura (`inst:app/nucleo/src/equipo.rs` l.60-70): `ram_total_mb`, `ram_libre_mb`, `cpu_modelo`, `nucleos`, `hilos`, `gpus[]` (`nombre`, `fabricante`, `vram_mb`, `integrada`), `disco_libre_mb`, `sistema`. No tiene campo de API de cómputo.

### 2.1 Hardware por máquina y fuente

| Campo | `steam-deck` | `gpu-12gb` |
|---|---|---|
| CPU | — en todas las fuentes de catálogo (gvc docs: «iGPU», sin modelo de CPU) | — |
| RAM MiB | gvc: «16 GiB» → 16384 MiB (`gvc:gdev/machine_levels/steam-deck.json` `description`); gvc docs: «16 GB compartidos» (`gvc:docs/investigacion/2026-11-21-mejorar-modelos-locales.md` l.32; `gvc:docs/records/peticion-gve-2026-11-21.md` l.15); instalador, solo en un test: 16 (GB) → 16384 MiB (`inst:app/nucleo/src/perfiles.rs` l.187-190, `ev(16, None, 200)`, memoria para IA 11,0 GiB = 11264 MiB) | gvc: `minTotalGiB: 14` → 14336 MiB (umbral, no valor nominal; nominal 16 GB, `gvc:gdev/machine_levels/gpu-12gb.json` `description`) |
| GPU | gvc: «iGPU», memoria unificada (`steam-deck.json` `description`); instalador (test): AMD integrada sin VRAM (`perfiles.rs` l.139); gvc investigación cita «Radeon 680M … (también RDNA2)» (`gvc:docs/investigacion/2026-11-21-motor-de-inferencia.md` l.38), (I) cita de una issue, no medida | gvc: «discrete GPU with 12 GiB of memory» (`gpu-12gb.json`) |
| VRAM MiB | — dedicada (memoria unificada); gimg limita el uso: `maxVram: "vulkan0=2"` (`gimg:gimg/machine_profiles/steam-deck.json` `engine.maxVram`, unidad sin declarar: ajuste de app) | `minVramGiB: 11.5` → 11776 MiB (umbral); nominal 12 GiB = 12288 MiB (descripción). Dato leído de `mem_info_vram_total` solo en amdgpu (descripción) |
| API de cómputo | Vulkan: gimg `maxVram: vulkan0=…` y `sd-…-vulkan.zip`; gvoice `device: "Vulkan0"`, `fallbackDevice: "cpu"` (`gvoice:gvoice/machine_profiles/steam-deck.json` `engine`) | — (el instalador deja ROCm fuera: «Vulkan ya cubre las gráficas AMD», `inst:catalogo.json` `motor.notas`; NVIDIA vía `nvidia-smi`) |
| SO | — (el instalador lee `System::long_os_version`; gimg solo publica binarios Linux/Ubuntu 24.04) | — |

**Otros perfiles en el instalador:** los tests usan equipos sintéticos (4 GB, 6 GB, portátil 8 GB, PC 16 GB + GPU 8 GiB = 8192 MiB, `perfiles.rs` l.162-222) que **no** son máquinas de catálogo; no se proponen como tales.

### 2.2 Conflictos entre fuentes

1. **RAM de la Deck:** «GiB» (`machine_levels`) frente a «GB» (docs de gvc); mismo valor 16 en ambos, unidad ambigua. Propuesta: 16384 MiB (la RAM real de la Deck es 16 GB LPDDR5 entregados como ≈15 GiB utilizables, I; ver P-7).
2. **Umbral frente a nominal:** gvc `minTotalGiB: 14` y `minVramGiB: 11.5` son umbrales de clasificación («below the nominal 16 GB and 12 GB because the kernel reports less»), no la ficha de hardware. La máquina `gpu-12gb` del catálogo necesita valores nominales; los umbrales son de la detección.
3. **`steam-deck` con VRAM dedicada:** gvc no la declara; el instalador trata una AMD con ≤ `VRAM_MINIMA_DEDICADA_MB` como integrada sin VRAM (`equipo.rs` `clasificar_gpu`, test `reserva_pequena_de_apu_cuenta_como_integrada`: 1024 MB). Un `Hardware` detectado en la Deck y la `Machine` `steam-deck` no coincidirán en `vram`.
4. **Rango:** gvc `rank` (0, 1) ordena niveles; en gmod no hay rango (se deduciría de RAM/VRAM).

### 2.3 Hardware frente a ajuste de app (D-11)

No pasan a `Machine`; se quedan en el consumidor, que cita la máquina por id (D-11, D-20, D-22):

- **instalador** (`inst:app/catalogo/catalogo.json` `reglas`): `reservaMinimaGb` 3,0, `reservaProporcion` 0,25, `memoriaJuegoGb` 1,0, `proporcionVramUtil` 0,9, `margenComodoGb` 1,5, `margenDisco` 1,1, `contextoNarrador` 8192; los `perfiles` (`memoriaGb`, `calidad`, `velocidad`, `maxModelosCargados`, `keepAlive`, roles `narrador`/`cronista`/`sugerencias`/`embeddings`, `experimental`) y `piensa` por modelo. Nota: `proporcionVramUtil` y la fórmula `RAM − max(3 GB, 25 %) − 1 GB` son reserva (D-22), no hardware.
- **gimg** (`gimg:gimg/machine_profiles/steam-deck.json`): `minFreeMemoryMb` 7000, `watchMemoryMb` 1500, `maxReferences` 1, `timeoutS` 900, `maxSteps` 50, `maxPixels` 1048576, `engine.maxVram`, `paramsBackend` `disk`, `ollama` `abort`, y `engine.models` por modelo (`args`, `timeoutS`, `minFreeMemoryMb` 5000 para flux3). Y de `models.json`: `installDefault`, `defaults`, `args`, `initImageArgs`.
- **gvoice** (`gvoice:gvoice/machine_profiles/steam-deck.json`): `minFreeMemoryMb` 4096, `watchMemoryMb` 1536, `timeoutS` 900, `engine.device`/`fallbackDevice`, y la asignación por rol `models.design`/`models.produce` (D-20).
- **gvc** (`gvc:gdev/machine_profiles/steam-deck.json`): `engine` (`kind`, `binary`, `apiBase`, `minVersion`), `llamaServer`, `models[].think`, `models[].minAvailableGiB`, `proposal.*`, `loop.*` (`numCtx` 16384, `numPredict` 4096…); y de `gdev/catalog.json`: `role`, `toolMode`, `minFreeGiB`, `reservedGiB`, `evidence`, `confirmed`. `minFreeGiB` (9, 5) es una exigencia de memoria de variante: candidato a salir de la reserva de la app y pasar a la regla de memoria de gmod (P-8).
- **Nombres de «memoria libre mínima»**: `minFreeMemoryMb` (gimg, gvoice), `minAvailableGiB` y `minFreeGiB` (gvc), `memoriaGb` (instalador). Valores en MiB: gimg 7000 (5000 para flux3), gvoice 4096, gvc 9216 y 5120 (9 y 5 GiB), instalador de 2048 a 14336 (2,0 a 14,0 GiB, por perfil entero). Los de gimg y gvoice ya vienen en MiB (D-23), sin conversión.

## 3. Huecos

Por variante (invariantes de `docs/ddd.md` sección 5):

- **H-1 (cerrado en 5.4) Licencia ausente o sin SPDX:** gvoice (tres variantes, ninguna licencia); gimg `flux3-klein-q8` (`unconfirmed`); instalador `llama3.1:8b` (`Llama-3.1-Community`, sin SPDX ni usos). Los demás tienen SPDX pero sin comprobar contra el repo de origen (una licencia por variante, no por archivo).
- **H-2 (cerrado en 5.2)** Origen `ollama` sin digest del manifiesto (invariante 1): los siete tags del instalador (`llama3.1:8b`, `qwen2.5:1.5b-instruct`, `qwen3.5:0.8b`, `qwen3.5:2b`, `qwen3.5:4b`, `qwen3.5:9b`, `nomic-embed-text`). GVE sí los registra para sus evidencias (inventario), pero no está en este alcance.
- **H-3 (cerrado en 5.1 y 5.2)** Tamaño total en bytes: instalador, solo GB decimales redondeados a 0,1 GB (error hasta ±50 000 000 B); gimg, solo MB redondeados (error hasta ±500 000 B por archivo). Falta bytes exactos de los siete tags de Ollama (el tamaño real de capas está en el manifiesto de Ollama, sin red no se lee) y de los 8 archivos de gimg. Sospechas por duplicidad: `qwen3.5:0.8b` = 1,0 GB igual que `qwen2.5:1.5b-instruct`; `Qwen3-4B` y `Qwen3VL-4B` ambos 2497 MB.
- **H-4 (cerrado en 5.2)** Cuantización real tras cada tag de Ollama (D-25): los siete. Sin dato; solo (I) para `llama3.1:8b` y `qwen2.5:1.5b-instruct` (Q4_K_M).
- **H-5 (cerrado en 5.3)** Variante sin formato/cuantización en el id propuesto: los cuatro `qwen3.5:*` (id `:gguf-?`) hasta resolver H-4.
- **H-6 Runtime con versión mínima (invariante 3):** gimg, solo release `master-95ff762` (fija, no mínima); gvoice, solo commit `5916bf7…` de `qwentts.cpp` sin versión; instalador/gvc, Ollama 0.34.3 / 0.34.2 sin relación por modelo; no hay dato de versión mínima por variante en ninguno. El motor `llama.cpp` (`llamaServer` de gvc) sin versión.
- **H-7 sha256 por archivo:** presente en todos los de gimg y gvoice; **no aplica** a Ollama (digest, H-2). Falta el sha256 del tokenizador por variante solo si gmod duplica el archivo (no).
- **H-8 CPU y SO de las máquinas:** ninguna fuente da CPU ni SO de `steam-deck` ni de `gpu-12gb`; `gpu-12gb` no tiene API de cómputo declarada.
- **H-9 Tarea del archivo auxiliar:** `Qwen3-4B` y `Qwen3-VL-4B` son codificadores de texto, no tienen Tarea propia (D-16).
- **H-10 (en parte, 5.3: `vision` con `qwen3.5:*`; `stt` sigue abierto)** Invariante 9 de gmod (`steam-deck` con variante `fits`/`tight` para cada Tarea): no hay candidato para `vision` ni `stt` en ningún consumidor leído (solo `text`, `embed`, `image`, `tts`). Falta fuente para esas dos Tareas.

**Urls/repos `hf` que hay que fijar a un commit (40 hex, D-24).** Todas apuntan hoy a `resolve/main`; fijadas en 5.1:

| # | Repo `hf` | Ruta de archivo | Fuente |
|---|---|---|---|
| 1 | `leejet/FLUX.2-klein-4B-GGUF` | `flux-2-klein-4b-Q8_0.gguf` | `gimg:gimg/models.json` flux2-klein-4b-q8 `files.diffusion.url` |
| 2 | `unsloth/Qwen3-4B-GGUF` | `Qwen3-4B-Q4_K_M.gguf` | `gimg:gimg/models.json` flux2-klein-4b-q8 y zimage-turbo-q6 `files.text.url` (mismo repo, dos entradas) |
| 3 | `black-forest-labs/FLUX.2-small-decoder` | `full_encoder_small_decoder.safetensors` | `gimg:gimg/models.json` flux2-klein-4b-q8 `files.vae.url` |
| 4 | `leejet/flux-3-image-klein-GGUF` | `flux3-image-klein-Q8_0.gguf` | `gimg:gimg/models.json` flux3-klein-q8 `files.diffusion.url` |
| 5 | `Qwen/Qwen3-VL-4B-Instruct-GGUF` | `Qwen3VL-4B-Instruct-Q4_K_M.gguf` | `gimg:gimg/models.json` flux3-klein-q8 `files.text.url` |
| 6 | `Comfy-Org/flux2-dev` | `split_files/vae/flux2-vae.safetensors` | `gimg:gimg/models.json` flux3-klein-q8 `files.vae.url` |
| 7 | `leejet/Z-Image-Turbo-GGUF` | `z_image_turbo-Q6_K.gguf` | `gimg:gimg/models.json` zimage-turbo-q6 `files.diffusion.url` |
| 8 | `Comfy-Org/Z-Image-Turbo` | `split_files/vae/ae.safetensors` | `gimg:gimg/models.json` zimage-turbo-q6 `files.vae.url` |
| 9 | `Serveurperso/Qwen3-TTS-GGUF` | `qwen-talker-0.6b-base-Q8_0.gguf` | `gvoice:gvoice/engines/qwentts.json` `models[0].url` |
| 10 | `Serveurperso/Qwen3-TTS-GGUF` | `qwen-talker-1.7b-base-Q8_0.gguf` | `models[1].url` |
| 11 | `Serveurperso/Qwen3-TTS-GGUF` | `qwen-talker-1.7b-voicedesign-Q8_0.gguf` | `models[2].url` |
| 12 | `Serveurperso/Qwen3-TTS-GGUF` | `qwen-tokenizer-12hz-Q8_0.gguf` | `models[3].url` |

Nota: al fijar commit, el sha256 de cada archivo debe seguir casando con el que ya tienen las fuentes; si el commit fijado cambia el contenido, es un archivo distinto.

## 4. Preguntas para la persona

1. **P-1 Id de modelo de gimg «flux3».** `flux3-klein-q8` usa el repo `flux-3-image-klein-GGUF` y archivo `flux3-image-klein`, pero su VAE es `flux2-vae`. Propongo `flux3-image-klein` (el nombre del archivo) porque `flux3-klein` no es el nombre publicado. Recomendación: `flux3-image-klein`; confirmar el nombre público.
2. **P-2 Ids de familia Qwen3.5.** El tag `qwen3.5:9b` no dice si es instruct, base o híbrido de razonamiento. Recomendación: `qwen3.5-9b` sin sufijo (el tag de Ollama no lo dice) y añadir el sufijo solo si la ficha de Ollama lo confirma; no inventar `-instruct`. Para `llama3.1:8b` y `qwen2.5:1.5b-instruct` sí se conservan `instruct`.
3. **P-3 Licencia de Llama 3.1.** No es SPDX. Recomendación: ficha propia `llama-3.1-community` con usos `redistribute` y `derivatives` y `commercial` sujeto a el umbral de 700 M usuarios (a confirmar leyendo la ficha); hasta entonces `unconfirmed`, lo que la excluye de `recommend` con `license_use` (D-13).
4. **P-4 Licencia por archivo.** Una variante de gimg junta archivos de tres repos con licencias que pueden diferir (p. ej. el VAE de `black-forest-labs` y los Qwen). gimg declara una licencia por modelo. Recomendación: licencia de la variante = la más restrictiva de sus archivos; tomar la de gimg como provisional y verificar cada repo antes de publicar `Apache-2.0`.
5. **P-5 Archivo compartido entre variantes.** `Qwen3-4B-Q4_K_M.gguf` está en dos variantes de gimg. Recomendación: repetirlo en cada variante (mismo sha256, misma url) y dejar al consumidor deduplicar por sha256; evita añadir referencias entre variantes al esquema.
6. **P-6 Roles de archivo.** gimg usa `diffusion`/`text`/`vae`; gvoice usa `use` con `base`/`design`/`codec` (que describe el uso del modelo, no el rol del archivo). Recomendación: roles de archivo `weights`, `text`, `vae`, `tokenizer`; el `use` de gvoice (`base`, `design`) se queda en el consumidor y `codec` pasa a `tokenizer`.
7. **P-7 RAM de la `steam-deck`.** Escribir 16384 MiB (nominal, 16 GiB) o la RAM visible tras reservar para la GPU. Recomendación: 16384 MiB nominal; la reserva la aplica `fit` desde el `Hardware` detectado (D-21, D-22) y el instalador ya descuenta con su fórmula.
8. **P-8 Exigencia de memoria de variante (`minFreeGiB`).** gvc tiene 9 y 5 GiB medidos o fijados a mano por persona (`confirmed: true`). Recomendación: guardarlos como medida de gvc hasta H3 (reglas de memoria de gmod, D-5) y no meterlos en `Machine`; son datos de variante.
9. **P-9 `gpu-12gb` solo existe en gvc y sin evidencia.** Recomendación: incluirla como máquina del catálogo con RAM nominal 16384 MiB y VRAM 12288 MiB; los umbrales 14336/11776 MiB quedan como reglas de detección de gvc (la máquina más cercana a un `Hardware` se elige en el consumidor).
10. **P-10 Tareas `stt` y `vision` sin datos.** Ningún consumidor tiene candidato de `stt`; para `vision`, ver 5.3 punto 4. Recomendación: abrir la búsqueda en H2 aparte (no inventarlas) y avisar de que el invariante 9 no se podrá cumplir hasta entonces.
11. **P-11 (resuelta en 5.2: el catálogo guarda bytes exactos)** Unidad de `descargaGb` del instalador. Recomendación: tratar como GB decimal (10^9) y marcar «aproximado» hasta que se lea el tamaño real de capas del manifiesto de Ollama (H-3).

## 5. Resuelto con red (2026-11-27)

Leído de `huggingface.co` (API `revision` y `tree`) y de `registry.ollama.ai` (manifiesto v2 y blob de configuración) el 2026-11-27, con la red del entorno `galivelop-models`. Cierra H-2, H-3 (bytes exactos), H-4, H-5 y las 12 urls de la sección 3.

### 5.1 Orígenes `hf` fijados a commit (D-24)

Los 12 sha256 de las fuentes **casan** con el `lfs.oid` de Hugging Face en el commit fijado, así que fijar la revisión no cambia ningún archivo.

| # | Archivo (fuente) | Repo `hf` | Commit | Bytes exactos | sha256 casa |
|---|---|---|---|---|---|
| 1 | `gimg:flux2-klein-4b-q8:diffusion` `flux-2-klein-4b-Q8_0.gguf` | `leejet/FLUX.2-klein-4B-GGUF` | `3b1f5a9dc3abb32238b053aeb3d823c30afdacbd` | 4 300 629 440 | sí |
| 2 | `gimg:flux2-klein-4b-q8:text` `Qwen3-4B-Q4_K_M.gguf` | `unsloth/Qwen3-4B-GGUF` | `22c9fc8a8c7700b76a1789366280a6a5a1ad1120` | 2 497 281 312 | sí |
| 3 | `gimg:flux2-klein-4b-q8:vae` `full_encoder_small_decoder.safetensors` | `black-forest-labs/FLUX.2-small-decoder` | `a3efc24f613ef42d9428af62fdbd6f5fd8856c4a` | 249 519 092 | sí |
| 4 | `gimg:flux3-klein-q8:diffusion` `flux3-image-klein-Q8_0.gguf` | `leejet/flux-3-image-klein-GGUF` | `57dfa91df2284f4985a4107c399d05d12e0f9b63` | 6 151 716 032 | sí |
| 5 | `gimg:flux3-klein-q8:text` `Qwen3VL-4B-Instruct-Q4_K_M.gguf` | `Qwen/Qwen3-VL-4B-Instruct-GGUF` | `1cd86afb9a95c410a6038ab3b40d8b578c892266` | 2 497 281 664 | sí |
| 6 | `gimg:flux3-klein-q8:vae` `split_files/vae/flux2-vae.safetensors` | `Comfy-Org/Flux-2-Dev` (la fuente dice `Comfy-Org/flux2-dev`, que redirige) | `9630c1b4b6e690497ae0c19bb6b1b35d4ebedcb7` | 336 213 556 | sí |
| 7 | `gimg:zimage-turbo-q6:diffusion` `z_image_turbo-Q6_K.gguf` | `leejet/Z-Image-Turbo-GGUF` | `c61c0e422dc8b541b7548cf33a4ef8302b0f8085` | 5 263 239 104 | sí |
| 8 | `gimg:zimage-turbo-q6:text` `Qwen3-4B-Q4_K_M.gguf` | `unsloth/Qwen3-4B-GGUF` | `22c9fc8a8c7700b76a1789366280a6a5a1ad1120` | 2 497 281 312 | sí |
| 9 | `gimg:zimage-turbo-q6:vae` `split_files/vae/ae.safetensors` | `Comfy-Org/Z-Image-Turbo` | `6fc90a3b1b653e935a0d175e260736de25b84df5` | 335 304 388 | sí |
| 10 | `gvoice:0.6b-base` `qwen-talker-0.6b-base-Q8_0.gguf` | `Serveurperso/Qwen3-TTS-GGUF` | `b7ee2e8c7459c3bea99da23e3d178125a7d1713c` | 992 615 488 | sí |
| 11 | `gvoice:1.7b-base` `qwen-talker-1.7b-base-Q8_0.gguf` | `Serveurperso/Qwen3-TTS-GGUF` | `b7ee2e8c7459c3bea99da23e3d178125a7d1713c` | 2 079 448 256 | sí |
| 12 | `gvoice:1.7b-voicedesign` `qwen-talker-1.7b-voicedesign-Q8_0.gguf` | `Serveurperso/Qwen3-TTS-GGUF` | `b7ee2e8c7459c3bea99da23e3d178125a7d1713c` | 2 042 833 824 | sí |
| 13 | `gvoice:tokenizer-12hz` `qwen-tokenizer-12hz-Q8_0.gguf` | `Serveurperso/Qwen3-TTS-GGUF` | `b7ee2e8c7459c3bea99da23e3d178125a7d1713c` | 291 150 624 | sí |

Totales por variante (bytes exactos):

- `flux2-klein-4b-q8`: 7 047 429 844 B
- `flux3-klein-q8`: 8 985 211 252 B
- `zimage-turbo-q6`: 8 095 824 804 B
- `0.6b-base` (con el tokenizador): 1 283 766 112 B
- `1.7b-base` (con el tokenizador): 2 370 598 880 B
- `1.7b-voicedesign` (con el tokenizador): 2 333 984 448 B

### 5.2 Orígenes `ollama`: digest, bytes y cuantización real (D-25)

Digest = sha256 del manifiesto v2 en bruto. Cuantización = `file_type` del blob de configuración. Capas: `model` (pesos), `projector` (codificador de visión), `draft` (modelo de borrador para decodificación especulativa).

| Tag | Digest del manifiesto | Cuantización real | Parámetros | Bytes de `model` | Otras capas grandes | Total (bytes) | `descargaGb` del instalador |
|---|---|---|---|---|---|---|---|
| `llama3.1:8b` | `sha256:46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e` | `Q4_K_M` | 8.0B | 4 920 738 944 | — | 4 920 752 841 | 4.9 |
| `qwen2.5:1.5b-instruct` | `sha256:65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` | `Q4_K_M` | 1.5B | 986 048 512 | — | 986 061 405 | 1.0 |
| `qwen3.5:0.8b` | `sha256:de63045f29755d4721c09d54c9b45c2dadb644f4fd7d604d4cac90d96049971c` | `Q8_0` | 752.39M | 811 843 520 | `projector` 207 346 304; `draft` 302 867 776 | 1 322 069 043 | 1.0 |
| `qwen3.5:2b` | `sha256:0689d44085e06d165161a8a9a1731344278cfb5aade63a3c3dbdb48ab54b130a` | `Q8_0` | 1.9B | 2 012 012 448 | `projector` 671 372 768 | 2 683 396 637 | 2.7 |
| `qwen3.5:4b` | `sha256:d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04` | `Q4_K_M` | 4.2B | 2 648 593 216 | `projector` 675 569 120 | 3 324 173 757 | 3.4 |
| `qwen3.5:9b` | `sha256:56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90` | `Q4_K_M` | 9.0B | 5 629 109 120 | `projector` 921 704 832 | 6 550 825 373 | 6.6 |
| `nomic-embed-text:latest` | `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` | `F16` | 137M | 274 290 656 | — | 274 302 030 | 0.3 |

### 5.3 Qué cambia respecto a las secciones 1 a 4

1. **Cuantización (H-4, H-5 cerrados):** `qwen3.5:0.8b` y `qwen3.5:2b` son `Q8_0`, no Q4; `qwen3.5:4b` y `:9b`, `Q4_K_M`; `llama3.1:8b` y `qwen2.5:1.5b-instruct`, `Q4_K_M` (se confirma la inferencia); `nomic-embed-text`, `F16`. Ids de variante: `qwen3.5-0.8b:gguf-q8_0`, `qwen3.5-2b:gguf-q8_0`, `qwen3.5-4b:gguf-q4_k_m`, `qwen3.5-9b:gguf-q4_k_m`, `nomic-embed-text-v1.5:gguf-f16`.
2. **Digest (H-2 cerrado):** los siete tags tienen digest; es lo que el catálogo fija (D-25). Si Ollama mueve el tag, el digest deja de casar y la variante se revisa.
3. **Tamaños (H-3 cerrado):** bytes exactos para todo. El instalador se queda corto en `qwen3.5:0.8b` (dice 1,0 GB; son 1 322 069 043 B, porque cuenta solo los pesos y no el proyector ni el borrador). La sospecha de H-3 sobre `Qwen3-4B` y `Qwen3VL-4B` era falsa: pesan casi lo mismo (2 497 281 312 y 2 497 281 664 B) pero son archivos distintos.
4. **Visión (H-10, P-10):** los cuatro `qwen3.5:*` traen capa `projector`: son modelos con entrada de imagen (I: por la capa; la ficha de Ollama lo confirmaría). Son candidatos a la Tarea `vision` además de `text`, y `qwen3.5-0.8b` o `-2b` podrían cubrir `vision` en la `steam-deck` (invariante 9). `stt` sigue sin candidato.
5. **Borrador:** `qwen3.5:0.8b` trae una capa `draft` (302 867 776 B). Es parte de la variante (cuenta en sus bytes y en su memoria), no un modelo aparte.
6. **Repo renombrado:** `Comfy-Org/flux2-dev` es hoy `Comfy-Org/Flux-2-Dev`; el catálogo usa el nombre canónico. gimg sigue funcionando por la redirección, pero conviene que use el nuevo al pasar a gmod.
7. **Licencia en Ollama:** los siete manifiestos traen capa `license`; sirve para resolver P-3 (Llama 3.1) sin buscar fuera.

### 5.4 Licencias comprobadas (Q-31)

Comprobado el 2026-11-27 con `cardData.license` de la API de Hugging Face (`https://huggingface.co/api/models/<repo>`).

| Repo | Licencia |
|---|---|
| `leejet/FLUX.2-klein-4B-GGUF` | apache-2.0 |
| `unsloth/Qwen3-4B-GGUF` | apache-2.0 |
| `black-forest-labs/FLUX.2-small-decoder` | apache-2.0 |
| `Qwen/Qwen3-VL-4B-Instruct-GGUF` | apache-2.0 |
| `leejet/Z-Image-Turbo-GGUF` | apache-2.0 |
| `Comfy-Org/Z-Image-Turbo` | apache-2.0 |
| `Serveurperso/Qwen3-TTS-GGUF` | apache-2.0 |
| `black-forest-labs/FLUX.2-klein-4B` | apache-2.0 |
| `Tongyi-MAI/Z-Image-Turbo` | apache-2.0 |
| `Qwen/Qwen3-4B` | apache-2.0 |
| `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | apache-2.0 |
| `nomic-ai/nomic-embed-text-v1.5` | apache-2.0 |
| `Comfy-Org/Flux-2-Dev` | other (flux-1-dev-non-commercial-license) |
| `leejet/flux-3-image-klein-GGUF` | no declara ninguna |
| `black-forest-labs/flux-3-image-klein` | other (flux-kommunity-license) |

Conclusión: flux2-klein-4b, z-image-turbo y las tres de voz quedan `apache-2.0`; flux3-image-klein queda `unconfirmed`.

## 6. Migración a catalog/ (2026-11-27)

H2 paso 2: 13 modelos, 13 variantes y 2 máquinas pasan a `catalog/` (JSON y README, sin código).

1. **Forma usada (provisional, la fija H1):** `gmod.model/0`, `gmod.machine/0`, `gmod.licenses/0`; claves camelCase, bytes enteros, MiB enteros, `provenance` por modelo y máquina.
2. **Origen `hf` por archivo:** una variante de imagen o de voz junta archivos de varios repos, así que cada archivo lleva su `hf` (repo canónico, commit de 40 hex, ruta) y su `url`. H1 tiene que decidir si el origen vive en la variante o en el archivo.
3. **`layers` de Ollama:** las variantes de Ollama llevan `files` vacío y `layers` (`model`, `projector`, `draft`, más `other` = `bytes` menos la suma de las demás capas, así que la suma de `layers` es igual a `bytes`). H1 decide si `layers` entra en el esquema.
4. **`memoryHints`:** solo en `qwen3.5-9b` (9216 MiB) y `qwen3.5-4b` (5120 MiB), de gvc (`gdev/catalog.json@014f7ff`, `confirmed: true`); H1 y H3 deciden si son dato de variante (P-8).
5. **`stt` sin variante:** ningún modelo cubre `stt`; el invariante 9 de la `steam-deck` queda incumplido (pendiente, Q-37). El tokenizador de voz se repite en las tres variantes (Q-32), con el mismo sha256.
