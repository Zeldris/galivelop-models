"""H1: the gmod.model/0 and gmod.machine/0 schemas, their examples and the catalog (docs/ddd.md invariants 1, 2, 3, 10)."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from gart.schema import check_schema
from gmod.catalog import SCHEMA_FILES, SCHEMAS_DIR, validate_catalog, validate_file

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"

# fixture -> the single expected (pointer, code); the test asserts exactly these problems and no others.
INVALID = {
    # invariant 1: origin, license, size, and per-origin fields
    "model-no-license": [("/variants/0", "required")],
    "model-no-bytes": [("/variants/0", "required")],
    "model-no-source": [("/variants/0", "required")],
    "model-file-no-sha256": [("/variants/0/files/0", "required")],
    "model-file-no-role": [("/variants/0/files/1", "required")],
    "model-hf-file-without-hf": [("/variants/0/files/0", "required")],
    "model-hf-no-files": [("/variants/0/files", "minItems")],
    "model-hf-bytes-sum": [("/variants/0/bytes", "catalog.bytes_sum")],
    "model-ollama-no-digest": [("/variants/0/source", "required")],
    "model-ollama-no-tag": [("/variants/0/source", "required")],
    # invariant 2: hf revision is a 40-hex commit
    "model-hf-revision-branch": [("/variants/0/files/0/hf/revision", "pattern")],
    "model-hf-revision-short": [("/variants/0/files/0/hf/revision", "pattern")],
    # invariant 3: tasks from the closed list, runtime with minimum version
    "model-tasks-empty": [("/tasks", "minItems")],
    "model-task-unknown": [("/tasks/0", "enum")],
    "model-no-runtimes": [("/variants/0/runtimes", "minItems")],
    "model-runtime-no-version": [("/variants/0/runtimes/0", "required")],
    # invariant 10: integer bytes and MiB, no GB fields
    "model-bytes-float": [("/variants/0/bytes", "type")],
    "model-extra-gb-field": [("/variants/0/sizeGB", "additionalProperties")],
    "machine-vram-float": [("/gpus/0/vramMiB", "type")],
    "machine-ram-in-gb": [("", "required"), ("/ramGB", "additionalProperties")],
    "machine-api-unknown": [("/computeApis/2", "enum")],
    "model-wrong-kind": [("/kind", "catalog.kind")],
}


class SchemaTest(unittest.TestCase):
    def test_schemas_are_valid_for_gart(self):
        for kind, name in SCHEMA_FILES.items():
            with self.subTest(kind=kind):
                schema = json.loads((SCHEMAS_DIR / name).read_text(encoding="utf-8"))
                check_schema(schema)
                self.assertEqual(schema["title"], kind)


class ExamplesTest(unittest.TestCase):
    def test_valid_examples(self):
        paths = sorted((FIXTURES / "valid").glob("*.json"))
        self.assertGreaterEqual(len(paths), 4)
        for path in paths:
            with self.subTest(example=path.name):
                self.assertEqual(validate_file(path), [])

    def test_every_invalid_example_is_listed_and_exists(self):
        on_disk = sorted(p.stem for p in (FIXTURES / "invalid").glob("*.json") if p.stem != "model-lora-base-missing")
        self.assertEqual(on_disk, sorted(INVALID))

    def test_invalid_examples_fail_with_their_code_and_path(self):
        for name, expected in INVALID.items():
            with self.subTest(example=name):
                got = sorted((p.pointer, p.code) for p in validate_file(FIXTURES / "invalid" / f"{name}.json"))
                self.assertEqual(got, sorted(expected))

    def test_nullable_vram_is_valid(self):
        # the steam-deck gap of docs/records/pending.md: vramMiB null stays legal
        doc = json.loads((FIXTURES / "valid" / "machine-steam-deck.json").read_text(encoding="utf-8"))
        self.assertIsNone(doc["gpus"][0]["vramMiB"])
        self.assertEqual(validate_file(FIXTURES / "valid" / "machine-steam-deck.json"), [])


class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for sub in ("models", "machines"):
            (self.tmp / sub).mkdir()
        shutil.copy(ROOT / "catalog" / "licenses.json", self.tmp / "licenses.json")
        shutil.copy(ROOT / "catalog" / "machines" / "steam-deck.json", self.tmp / "machines")
        shutil.copy(FIXTURES / "valid" / "model-ollama.json", self.tmp / "models" / "llama3.1-8b-instruct.json")
        shutil.copy(FIXTURES / "valid" / "model-lora.json", self.tmp / "models" / "llama3.1-8b-lora.json")

    def test_the_real_catalog_validates(self):
        self.assertEqual(validate_catalog(ROOT / "catalog"), [])

    def test_small_valid_catalog(self):
        self.assertEqual(validate_catalog(self.tmp), [])

    def test_lora_base_must_exist(self):
        shutil.copy(FIXTURES / "invalid" / "model-lora-base-missing.json", self.tmp / "models" / "llama3.1-8b-lora.json")
        got = [(p.file, p.pointer, p.code) for p in validate_catalog(self.tmp)]
        self.assertEqual(got, [("models/llama3.1-8b-lora.json", "/base", "catalog.unknown_base")])

    def test_unknown_license(self):
        path = self.tmp / "models" / "llama3.1-8b-instruct.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["variants"][0]["license"] = "mit"
        path.write_text(json.dumps(doc), encoding="utf-8")
        got = [(p.file, p.pointer, p.code) for p in validate_catalog(self.tmp)]
        self.assertIn(("models/llama3.1-8b-instruct.json", "/variants/0/license", "catalog.unknown_license"), got)

    def test_duplicate_variant_id(self):
        shutil.copy(FIXTURES / "valid" / "model-ollama.json", self.tmp / "models" / "llama3.1-8b-lora.json")
        codes = [(p.file, p.code) for p in validate_catalog(self.tmp)]
        self.assertIn(("models/llama3.1-8b-lora.json", "catalog.duplicate"), codes)

    def test_steam_deck_must_exist(self):
        (self.tmp / "machines" / "steam-deck.json").unlink()
        self.assertEqual([(p.file, p.code) for p in validate_catalog(self.tmp)], [("machines", "catalog.missing_machine")])

    def test_duplicate_keys_are_rejected(self):
        (self.tmp / "machines" / "steam-deck.json").write_text('{"kind": "a.b/0", "kind": "a.b/0"}', encoding="utf-8")
        got = validate_catalog(self.tmp)
        self.assertEqual(got[0].file, "machines/steam-deck.json")
        self.assertTrue(got[0].code.startswith("canon."), got[0])


if __name__ == "__main__":
    unittest.main()
