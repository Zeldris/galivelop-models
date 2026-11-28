"""Validation of the catalog against the `gmod.*` JSON Schemas (H1; stdlib plus the vendored `gart`, no network).

`validate_catalog(root)` returns a list of `Problem(file, pointer, code, params)`; empty means the catalog is valid.
Schema errors keep the `gart` code (`required`, `pattern`, `type`...). What a schema without `if`/`anyOf` cannot say
is checked here, with codes prefixed `catalog.` (docs/ddd.md section 5, invariants 1 and 3).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NamedTuple

from gart.canon import CanonError, loads_strict
from gart.kind_id import KindId, KindIdError
from gart.schema import check_schema, validate

SCHEMAS_DIR = Path(__file__).resolve().parent / "schemas"  # package data (pyproject: gmod = ["schemas/*.json"])
SCHEMA_FILES = {
    "gmod.model/0": "gmod.model.0.json",
    "gmod.machine/0": "gmod.machine.0.json",
    "gmod.licenses/0": "gmod.licenses.0.json",
    "gmod.memory_rules/0": "gmod.memory_rules.0.json",
}


class Problem(NamedTuple):
    file: str  # path relative to the catalog root, "/" separated
    pointer: str  # JSON Pointer inside the file ("" is the root)
    code: str
    params: dict


def load_schema(kind: str, schemas_dir: Path | None = None) -> dict:
    """Load and check the schema of `kind` (`gmod.model/0`...)."""
    schema = json.loads((Path(schemas_dir or SCHEMAS_DIR) / SCHEMA_FILES[kind]).read_text(encoding="utf-8"))
    check_schema(schema)
    return schema


def validate_document(doc: Any, expected_kind: str, schemas_dir: Path | None = None) -> list[tuple[str, str, dict]]:
    """Schema errors of `doc` as `(pointer, code, params)`; the `kind` must be `expected_kind`."""
    kind = doc.get("kind") if isinstance(doc, dict) else None
    try:
        KindId.parse(kind)
    except KindIdError as exc:
        return [("/kind", exc.code, {"text": kind})]
    if kind != expected_kind:
        return [("/kind", "catalog.kind", {"expected": expected_kind, "found": kind})]
    return [(e.path, e.code, e.params) for e in validate(doc, load_schema(kind, schemas_dir))]


def _model_checks(doc: dict) -> list[tuple[str, str, dict]]:
    """Checks of a schema-valid model that the schema cannot express (invariant 1, origin-dependent fields)."""
    out: list[tuple[str, str, dict]] = []
    for i, var in enumerate(doc["variants"]):
        vp = f"/variants/{i}"
        if not var["id"].startswith(f"{doc['id']}:"):
            out.append((f"{vp}/id", "catalog.variant_id", {"model": doc["id"], "id": var["id"]}))
        elif var["id"] != f"{doc['id']}:{var['format']}-{var['quantization']}":
            out.append((f"{vp}/id", "catalog.variant_id", {"expected": f"{doc['id']}:{var['format']}-{var['quantization']}"}))
        src = var["source"]
        files = var["files"]
        if src["type"] == "ollama":
            for key in ("name", "tag", "digest"):
                if key not in src:
                    out.append((f"{vp}/source", "required", {"name": key}))
            if files:
                out.append((f"{vp}/files", "catalog.files_not_allowed", {"source": "ollama"}))
            layers = var.get("layers")
            if layers is not None and sum(layers.values()) != var["bytes"]:
                out.append((f"{vp}/bytes", "catalog.bytes_sum", {"expected": sum(layers.values()), "found": var["bytes"]}))
        else:
            if not files:
                out.append((f"{vp}/files", "minItems", {"limit": 1}))
            elif sum(f["bytes"] for f in files) != var["bytes"]:
                out.append((f"{vp}/bytes", "catalog.bytes_sum", {"expected": sum(f["bytes"] for f in files), "found": var["bytes"]}))
            for j, f in enumerate(files):
                fp = f"{vp}/files/{j}"
                if src["type"] == "hf":
                    if "hf" not in f:
                        out.append((fp, "required", {"name": "hf"}))
                    else:
                        h = f["hf"]
                        want = f"https://huggingface.co/{h['repo']}/resolve/{h['revision']}/{h['path']}"
                        if f["url"] != want:
                            out.append((f"{fp}/url", "catalog.url_mismatch", {"expected": want}))
                elif "hf" in f:
                    out.append((f"{fp}/hf", "additionalProperties", {"name": "hf"}))
    return out


def _read(path: Path, rel: str, kind: str, problems: list[Problem], schemas_dir: Path | None) -> Any:
    try:
        doc = loads_strict(path.read_text(encoding="utf-8"))
    except (CanonError, UnicodeDecodeError, OSError) as exc:
        problems.append(Problem(rel, "", getattr(exc, "code", "catalog.read"), {"reason": str(exc)}))
        return None
    errors = validate_document(doc, kind, schemas_dir)
    problems.extend(Problem(rel, p, c, d) for p, c, d in errors)
    return None if errors else doc


def validate_file(path: str | Path, schemas_dir: str | Path | None = None) -> list[Problem]:
    """Validate one model or machine document alone (no cross-file checks: licenses, base, unique ids)."""
    path = Path(path)
    problems: list[Problem] = []
    try:
        doc = loads_strict(path.read_text(encoding="utf-8"))
    except (CanonError, UnicodeDecodeError, OSError) as exc:
        return [Problem(path.name, "", getattr(exc, "code", "catalog.read"), {"reason": str(exc)})]
    kind = doc.get("kind") if isinstance(doc, dict) else None
    errors = validate_document(doc, kind if kind in SCHEMA_FILES else "gmod.model/0", Path(schemas_dir) if schemas_dir else None)
    if not errors and kind == "gmod.model/0":
        errors = _model_checks(doc)
    problems.extend(Problem(path.name, p, c, d) for p, c, d in errors)
    return problems


def validate_catalog(root: str | Path, schemas_dir: str | Path | None = None) -> list[Problem]:
    """Validate `root/{models,machines}/*.json` and `root/licenses.json`; return every problem found."""
    root = Path(root)
    sdir = Path(schemas_dir) if schemas_dir else None
    problems: list[Problem] = []
    licenses = _read(root / "licenses.json", "licenses.json", "gmod.licenses/0", problems, sdir) if (root / "licenses.json").exists() else None
    if licenses is None and not (root / "licenses.json").exists():
        problems.append(Problem("licenses.json", "", "catalog.missing", {}))
    license_ids: set[str] = set()
    if licenses:
        for i, lic in enumerate(licenses["licenses"]):
            if lic["id"] in license_ids:
                problems.append(Problem("licenses.json", f"/licenses/{i}/id", "catalog.duplicate", {"id": lic["id"]}))
            license_ids.add(lic["id"])
            if lic["id"] == "unconfirmed" and lic["uses"]:
                problems.append(Problem("licenses.json", f"/licenses/{i}/uses", "catalog.unconfirmed_uses", {}))
    rules_path = root / "memory-rules.json"
    if not rules_path.exists():
        problems.append(Problem("memory-rules.json", "", "catalog.missing", {}))
    else:
        rules = _read(rules_path, "memory-rules.json", "gmod.memory_rules/0", problems, sdir)
        if rules:
            seen: set[str] = set()
            for i, rule in enumerate(rules["rules"]):
                if rule["runtime"] in seen:
                    problems.append(Problem("memory-rules.json", f"/rules/{i}/runtime", "catalog.duplicate", {"id": rule["runtime"]}))
                seen.add(rule["runtime"])
                for key in ("formats", "quantizations", "computeApis"):
                    for j, item in enumerate(rule[key]):
                        if item in rule[key][:j]:
                            problems.append(Problem("memory-rules.json", f"/rules/{i}/{key}/{j}", "catalog.duplicate", {"id": item}))
    models: dict[str, tuple[str, dict]] = {}
    variant_ids: dict[str, str] = {}
    for path in sorted((root / "models").glob("*.json")):
        rel = f"models/{path.name}"
        doc = _read(path, rel, "gmod.model/0", problems, sdir)
        if doc is None:
            continue
        found = [(p, c, d) for p, c, d in _model_checks(doc)]
        if path.stem != doc["id"]:
            found.append(("/id", "catalog.file_name", {"expected": path.stem}))
        if doc["id"] in models:
            found.append(("/id", "catalog.duplicate", {"id": doc["id"]}))
        models.setdefault(doc["id"], (rel, doc))
        for i, var in enumerate(doc["variants"]):
            if licenses is not None and var["license"] not in license_ids:
                found.append((f"/variants/{i}/license", "catalog.unknown_license", {"license": var["license"]}))
            if var["id"] in variant_ids:
                found.append((f"/variants/{i}/id", "catalog.duplicate", {"id": var["id"], "other": variant_ids[var["id"]]}))
            variant_ids.setdefault(var["id"], rel)
        problems.extend(Problem(rel, p, c, d) for p, c, d in found)
    for rel, doc in models.values():
        if "base" not in doc:
            continue
        if doc["base"] == doc["id"]:
            problems.append(Problem(rel, "/base", "catalog.base_self", {"base": doc["base"]}))
        elif doc["base"] not in models:
            problems.append(Problem(rel, "/base", "catalog.unknown_base", {"base": doc["base"]}))
        elif "base" in models[doc["base"]][1]:
            problems.append(Problem(rel, "/base", "catalog.base_chain", {"base": doc["base"]}))
    machine_ids: set[str] = set()
    for path in sorted((root / "machines").glob("*.json")):
        rel = f"machines/{path.name}"
        doc = _read(path, rel, "gmod.machine/0", problems, sdir)
        if doc is None:
            continue
        if path.stem != doc["id"]:
            problems.append(Problem(rel, "/id", "catalog.file_name", {"expected": path.stem}))
        if doc["id"] in machine_ids:
            problems.append(Problem(rel, "/id", "catalog.duplicate", {"id": doc["id"]}))
        machine_ids.add(doc["id"])
    if "steam-deck" not in machine_ids:
        problems.append(Problem("machines", "", "catalog.missing_machine", {"id": "steam-deck"}))
    return problems
