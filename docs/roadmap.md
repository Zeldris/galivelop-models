# Roadmap

Todo el desarrollo de galivelop-models (`gmod`), separado por versiones, con la misma forma que el roadmap de los
demás repos Galivelop (D-1). El diseño está en el [DDD](ddd.md); aquí, el orden en que se entrega. Lo que salga al
trabajar entra aquí como tarea `pendiente` en la versión que le toca; la bitácora ([handoff.md](handoff.md)) solo
enlaza la tarea en curso.

## Identificadores

Cada tarea tiene un id con la **letra de su bloque** y un número. Los ids **nunca se reutilizan**: una tarea
descartada se queda con su id y estado `descartada`.

| Letra | Bloque |
|---|---|
| `D` | Diseño: el DDD y sus decisiones (fase F-1) |
| `S` | Esqueleto del repo: paquete, check, CI |
| `H` | Los hitos del DDD ([§7](ddd.md#7-escalera-de-hitos)), con el mismo número |

**Estados**, en texto: `pendiente`, `en curso`, `esperando <qué>`, `hecho`, `descartada`. Al cerrar:
`hecho (\`0.1.0\`, \`<sha>\`)`; antes de la primera versión publicada, `hecho (<fecha>)`.

## Regla de versiones

- **Semver** (`MAYOR.MENOR.PARCHE`): mayor, lo que obliga a cambiar cómo se usa (esquemas `gmod.*`, órdenes de la
  CLI, formato de la exportación); menor, una capacidad compatible; parche, un arreglo. Mientras la versión sea `0.x`,
  lo que rompe sube la **menor**.
- Cada versión tiene su sección aquí, con el nombre de lo que entrega, y su entrada en [CHANGELOG.md](../CHANGELOG.md)
  (Keep a Changelog): cada viñeta con la ruta, los ids y qué cambia.
- La versión vive en **un único sitio** cuando haya código (`pyproject.toml`); hasta entonces, aquí y en el CHANGELOG.
- Se publica con un tag `vX.Y.Z` sobre `main`.
- Una versión se cierra cuando todas sus tareas están `hecho` o `descartada`, o se mueven a otra versión diciéndolo.
- **Orden por dependencias:** lo que espera a otro repo (el validador de `gart`, D-9; los informes de GVE, D-19) no
  bloquea una versión entera; lo que no depende de nadie va antes.

## `0.0` «Diseño»

Fase F-1. No lleva código ni se publica.

| Id | Tarea | Estado |
|---|---|---|
| D1 | DDD final, D-1 a D-25 ([DDD](ddd.md), [preguntas](questions.md)) | hecho (2026-11-27) |
| D2 | Inventario de los consumidores, en solo lectura ([inventario](records/inventario-consumidores-2026-11-26.md)) | hecho (2026-11-26) |
| D3 | Petición a GVE: variante, máquina y motor en sus informes ([petición](records/peticion-gve-2026-11-27.md)) | hecho (2026-11-27) |
| D4 | Roadmap por versiones y CHANGELOG (F0, este archivo); reparto aprobado (Q-26) | hecho (2026-11-27) |

## `0.1` «Esqueleto, catálogo y detección»

Lo que no depende del validador de `gart`: el esqueleto, los datos del catálogo y la detección de hardware.

| Id | Tarea | Estado |
|---|---|---|
| S1 | Esqueleto: `pyproject.toml` sin dependencias, paquete `gmod` vacío, `python3 -m unittest discover` en el check y en el CI; en `AGENTS.md`, las reglas del proyecto y el texto de `branchCheck` como lo fija `.claude/gw.json` (leve de la fase 1, retro P4) | hecho (`0.1.0`, `f53a9b2`) |
| H2 | Catálogo inicial: tabla de diferencias entre los catálogos del instalador, gimg, gvoice y gvc, con revisiones `hf` fijadas a un commit (D-24); revisión de la persona; migración a `catalog/` (valida al llegar H1) | hecho (`0.1.0`, `f53a9b2`); valida al llegar H1 |
| H5 | `detect_hardware` en Linux y Windows, con `/proc` y `sysfs` simulados en los tests; prueba real en la Deck, pendiente de la persona | hecho (`0.1.0`, `f53a9b2`); prueba real en la Deck y en Windows, pendiente de la persona |

## `0.2` «Esquemas y encaje»

| Id | Tarea | Estado |
|---|---|---|
| H1 | Esquemas `gmod.model/0` y `gmod.machine/0`, con ejemplos válidos e inválidos; valida el catálogo de H2 | esperando el validador de `gart` |
| H3 | `fit` con la tabla de reglas de memoria a mano (D-5, D-21, D-22) | pendiente (tras H1) |
| H4 | `recommend` con filtro por tarea y por licencia (D-13) | pendiente (tras H3) |

## `0.3` «Exportación, CLI y portal»

La primera versión que puede vendorizar un consumidor.

| Id | Tarea | Estado |
|---|---|---|
| H7 | Manifiesto sha256 y exportación vendorizada (D-2) | pendiente (tras H1) |
| H8 | Textos es/en, CLI `gmod` y página para el portal (D-15) | pendiente (tras H4 y H7) |

## `0.4` «Medidas de GVE»

Rompe los esquemas (paso a `/1`), así que sube la menor.

| Id | Tarea | Estado |
|---|---|---|
| H6 | Ingesta de `gmod.measurement`, informe de desviación con umbral (D-5) y paso de todos los tipos a `/1` | esperando la versión de GVE con variante, máquina y motor (D-19) |

## Después

`1.0` se decide al cerrar `0.4`, con al menos un consumidor usando la copia vendorizada. La migración de cada
consumidor es tarea de su repo, no de este (DDD, §7).
