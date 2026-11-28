# Changelog

Formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versiones [semver](https://semver.org/lang/es/);
la regla y las tareas de cada versión, en el [roadmap](docs/roadmap.md).

## [Unreleased]

### Added

- Esquemas `gmod.model/0`, `gmod.machine/0` y `gmod.licenses/0` en `gmod/schemas/` (datos del paquete), y `gmod.validate_catalog(root)` (valida `catalog/` con `gart`; devuelve `Problem(file, pointer, code, params)`).

## [0.1.0] - 2026-11-27

### Added

- Catálogo inicial en `catalog/`: 13 modelos (`models/<model-id>.json`, una variante cada uno, revisiones `hf` fijadas
  a commit y digests de Ollama), 2 máquinas (`steam-deck`, `gpu-12gb`) y `licenses.json`, migrados desde el
  instalador, gimg, gvoice y gvc según `docs/records/diferencias-catalogos-2026-11-27.md`; forma provisional hasta H1
  y `flux3-image-klein` con licencia `unconfirmed` (H2).
- `gmod.detect_hardware()` y `Hardware` (mismos campos que una `Machine`): Linux con `/proc`, `sysfs` y
  `nvidia-smi`; Windows con el registro, `GlobalMemoryStatusEx` y `System32`. Lo que no lee queda `None` (H5).
- Esqueleto: `pyproject.toml` sin dependencias (Python ≥ 3.10), paquete `gmod` vacío y `tests/test_skeleton.py`
  (solo stdlib y sin red, invariante 12); `python3 -m unittest discover` entra en el check y el CI (S1).
- Roadmap por versiones `0.0` a `0.4` en `docs/roadmap.md` y este CHANGELOG (D4, F0).
- DDD final en `docs/ddd.md`, decisiones D-1 a D-25 (D1, F-1).
- Inventario de los consumidores en `docs/records/inventario-consumidores-2026-11-26.md` (D2).
- Petición a GVE en `docs/records/peticion-gve-2026-11-27.md` (D3).
- Galivelop-workflow v0.9.1 instalado: scripts, skills, ganchos y CI.
