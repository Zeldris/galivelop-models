"""The vendored `gart` validator: its copy matches VENDOR.json (no import of the copied code) and it validates."""
import hashlib
import json
import os
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("GMOD_VENDOR_ROOT") or Path(__file__).resolve().parent.parent)
PACKAGE = ROOT / "gart"


class VendorTableTest(unittest.TestCase):
    def setUp(self):
        self.table = json.loads((PACKAGE / "VENDOR.json").read_text(encoding="utf-8"))

    def test_pin(self):
        self.assertEqual(self.table["source"]["commit"], "7d26869")
        self.assertEqual(self.table["version"], "0.0.0+7d26869")

    def test_files_match_the_table(self):
        actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in PACKAGE.glob("*.py")}
        self.assertEqual(sorted(actual), sorted(self.table["files"]), "set of vendored files differs")
        for name, digest in sorted(actual.items()):
            with self.subTest(file=name):
                self.assertEqual(digest, self.table["files"][name], f"{name} was edited")

    def test_no_extra_entries(self):
        extra = sorted(p.name for p in PACKAGE.iterdir() if p.suffix == ".py" or p.is_dir())
        self.assertEqual([n for n in extra if n != "__pycache__"], sorted(self.table["files"]))


class SmokeTest(unittest.TestCase):
    SCHEMA = {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}

    def test_valid_and_invalid_instance(self):
        from gart import validate

        self.assertEqual(list(validate({"name": "x"}, self.SCHEMA)), [])
        errors = list(validate({"name": 3}, self.SCHEMA))
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, "type")
