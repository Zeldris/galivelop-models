# Candidatos `stt` para la `steam-deck` (2026-11-27)

Búsqueda abierta por P-10 y Q-37: ningún consumidor tiene modelo de `stt`, así que la invariante 9 (cada Tarea con
una variante `fits` o `tight` en la `steam-deck`) no se cumple para `stt`. Aquí se apuntan los candidatos con datos
leídos de fuentes primarias; la elección es de la persona (Q-38 y Q-39).

## Requisitos de la Deck

CPU AMD Zen 2 (4 núcleos, 8 hilos), GPU RDNA2 integrada con memoria unificada (16 GiB en total), `vulkan` y `cpu`,
Linux. Los proyectos trabajan en español e inglés, así que el modelo tiene que ser multilingüe (las variantes `.en` no
valen).

## Candidato principal: Whisper con `whisper.cpp`

- **Motor:** `whisper.cpp` (ggml), con backend Vulkan y CPU. Última etiqueta: `v1.9.6`, commit
  `00c1630c14fc8fc187aa4c5ae3975d81ac2e6517` (`git ls-remote --tags https://github.com/ggml-org/whisper.cpp`,
  2026-11-27).
- **Pesos:** repo `ggerganov/whisper.cpp` de Hugging Face, revisión `5359861c739e955e79d9a303bcbc70fb988958b1`
  (último commit, 2024-10-29), licencia `mit` en la ficha (API de Hugging Face, 2026-11-27). Es la licencia de los
  pesos de OpenAI Whisper; el catálogo aún no tiene `mit` en `licenses.json`.
- **Variantes multilingües** (tamaño y sha256 del LFS, API `tree` de esa revisión):

| Archivo | Bytes | sha256 |
|---|---:|---|
| `ggml-large-v3-turbo-q5_0.bin` | 574041195 | `394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2` |
| `ggml-large-v3-turbo-q8_0.bin` | 874188075 | `317eb69c11673c9de1e1f0d459b253999804ec71ac4c23c17ecf5fbe24e259a1` |
| `ggml-medium-q5_0.bin` | 539212467 | `19fea4b380c3a618ec4723c3eef2eb785ffba0d0538cf43f8f235e7b3b34220f` |
| `ggml-small-q8_0.bin` | 264464607 | `49c8fb02b65e6049d5fa6c04f81f53b867b5ec9540406812c643f177317f779f` |
| `ggml-small-q5_1.bin` | 190085487 | `ae85e4a935d7a567bd102fe55afc16bb595bdb618e11b2fc7591bc08120411bb` |
| `ggml-base-q8_0.bin` | 81768585 | `c577b9a86e7e048a0b7eada054f4dd79a56bbfa911fbdacf900ac5b567cbb7d9` |

Por tamaño, todas caben de sobra en la Deck. Lo que no está medido es la velocidad, y en esta CPU puede pesar más que
la memoria: `large-v3-turbo` es la de más calidad multilingüe (decodificador de 4 capas, más rápida que `medium`);
`small` es la opción rápida. La medida real llega con GVE (H6); hasta entonces, `fit` solo mira memoria (H3).

## Descartado por ahora

- **NVIDIA Parakeet TDT 0.6B v3** (`nvidia/parakeet-tdt-0.6b-v3`, revisión `541d1f99c6b0c3cd0b11a95167540bb8edefd82b`):
  25 idiomas europeos, incluido el español, licencia `cc-by-4.0` (pide atribución). Su motor es NeMo o ONNX de
  terceros (`sherpa-onnx`), sin pesos oficiales en un formato que ya use algún consumidor. Se puede volver a mirar si
  un consumidor adopta `sherpa-onnx`.
- **Variantes `.en` de Whisper y Moonshine:** solo inglés.
