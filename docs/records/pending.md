# Pendiente

Lo que queda abierto; la bitácora solo apunta aquí. Se añade y se quita en este archivo.

## Pendiente
- Tag `v0.1.0` sobre `main` (`b6fe0e8`, PR #3 fusionado): lo sube un agente desde el equipo local de la persona (`git fetch origin main && git tag -a v0.1.0 origin/main -m "0.1.0" && git push origin v0.1.0`)
- H5, prueba real (la persona): `python3 -c "import gmod, json; print(json.dumps(gmod.detect_hardware().to_dict()))"` en la Steam Deck (debe dar 4 núcleos, 8 hilos, GPU AMD integrada sin VRAM, `vulkan` y `cpu`) y en un Windows con GPU NVIDIA o AMD
- H5: las APU de AMD se reconocen por id (Deck LCD 163f, OLED 1435) o por VRAM de 2 GiB o menos; una APU con más reserva en la BIOS saldría como discreta (leve, revisar con la prueba real)
- stt sin variante en el catálogo: invariante 9 de la steam-deck incumplida hasta encontrar un modelo stt (H2, Q-37)
- steam-deck con vramMiB null: con la invariante 6, fit puede dar unknown en la Deck para imagen y voz; decidir en H3 cómo se trata la memoria unificada (afecta a la invariante 9)
- H7: pedir `registry.ollama.ai` en los hosts del entorno (el proxy lo rechazó en H2; retro 0.1, P5, aplazada)
- La persona: desactivar el conector `Claude_Docs` en el entorno (retro 0.1, P2)
