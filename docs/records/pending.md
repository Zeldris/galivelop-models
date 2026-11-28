# Pendiente

Lo que queda abierto; la bitácora solo apunta aquí. Se añade y se quita en este archivo.

## Pendiente
- H5, prueba real (la persona): `python3 -c "import gmod, json; print(json.dumps(gmod.detect_hardware().to_dict()))"` en un Windows con GPU NVIDIA o AMD (la Steam Deck LCD ya pasó el 2026-11-28)
- H5: las APU de AMD se reconocen por id (Deck LCD 163f, OLED 1435) o por VRAM de 2 GiB o menos; una APU con más reserva en la BIOS saldría como discreta (leve, revisar con la prueba real)
- H3: memoria unificada con campo explícito (Q-45: b): la GPU declara `sharedMemory: true` en `gmod.machine/0` y `fit` usa entonces `ramMiB` como bolsa común; sin el campo, `vramMiB: null` sigue dando `unknown` (invariante 6); la steam-deck lo declara (invariante 9)
- Q-42: a: pedir a galivelop-artifacts que el `__init__.py` de `gart` use imports relativos; con eso, la siguiente copia va a `gmod/_vendor/gart` sin editarla
- H7: pedir `registry.ollama.ai` en los hosts del entorno (el proxy lo rechazó en H2; retro 0.1, P5, aplazada)
- La persona: desactivar el conector `Claude_Docs` en el entorno (retro 0.1, P2)
- H1, revisión (leve): `_read` de `gmod/catalog.py` devuelve None ante un error de esquema y da falsos `catalog.missing_machine`/`catalog.unknown_base`; registrar los ids aunque no validen
- H1, revisión (leve): `layers` y `name`/`tag`/`digest` se aceptan en orígenes hf/url; decidir si `layers` es obligatorio en ollama
- H1, revisión (leve): `catalog.variant_id` lleva params `{model,id}` o `{expected}` según la rama; una sola forma o dos códigos
- H1, revisión (leve): los esquemas se leen con `json.loads` (clave duplicada en silencio) y sin caché; usar `gart.canon.loads_strict`
- H1, revisión (leve): gart da por entero `1.0`, así que `"bytes": 4920752841.0` valida; rechazar float en bytes/MiB/layers o escribir en el DDD que se acepta (invariante 10)
- H1, revisión (leve): `AGENTS.md` e invariante 12 dicen «nada fuera de la stdlib»; nombrar ahí la copia vendorizada de `gart`
