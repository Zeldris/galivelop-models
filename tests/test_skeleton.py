"""Skeleton invariants: the package imports, and it uses only the stdlib and no network (DDD invariant 12)."""
import ast
import sys
import unittest
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ImportError:  # Python 3.10: the package supports it, this one test does not
    tomllib = None

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "gmod"
# Modules that reach the network; `gmod` never imports them (DDD invariant 12).
NETWORK_MODULES = {"socket", "ssl", "http", "urllib", "ftplib", "smtplib", "imaplib", "poplib", "xmlrpc", "asyncio"}
# Calls that import a module by name at run time: `importlib.import_module`, `import_module`, `__import__`.
DYNAMIC_IMPORTS = {"import_module", "__import__"}


def _call_name(func):
    """The bare name a call goes to: `import_module` for both `import_module(...)` and `importlib.import_module(...)`."""
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def imported_roots(path):
    """The top-level names one source file imports, static or dynamic.

    A dynamic import whose module name is not a string literal cannot be checked, so it comes back as
    `<dynamic>`, which is never in the stdlib and makes the invariant test fail.
    """
    roots = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and _call_name(node.func) in DYNAMIC_IMPORTS:
            arg = node.args[0] if node.args else None
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and not arg.value.startswith("."):
                roots.add(arg.value.split(".")[0])
            else:
                roots.add("<dynamic>")
    return roots


class SkeletonTest(unittest.TestCase):
    def test_package_imports(self):
        import gmod

        self.assertEqual(Path(gmod.__file__).resolve().parent, PACKAGE)

    @unittest.skipIf(tomllib is None, "tomllib needs Python 3.11+")
    def test_pyproject_has_no_dependencies(self):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        self.assertEqual(project["dependencies"], [])
        self.assertEqual(project["requires-python"], ">=3.10")

    def test_only_stdlib_and_no_network(self):
        sources = sorted(PACKAGE.rglob("*.py"))
        self.assertTrue(sources, "gmod has no source files")
        for path in sources:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                roots = imported_roots(path) - {"gmod"}
                self.assertEqual(roots - set(sys.stdlib_module_names), set(), "imports outside the stdlib")
                self.assertEqual(roots & NETWORK_MODULES, set(), "imports a network module")

    def test_dynamic_imports_are_seen(self):
        cases = {
            'import importlib\nimportlib.import_module("socket")\n': {"importlib", "socket"},
            'from importlib import import_module\nimport_module("http.client")\n': {"importlib", "http"},
            '__import__("ssl")\n': {"ssl"},
            'import importlib\nname = "socket"\nimportlib.import_module(name)\n': {"importlib", "<dynamic>"},
        }
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            for source, expected in cases.items():
                with self.subTest(source=source):
                    path = Path(tmp) / "mod.py"
                    path.write_text(source, encoding="utf-8")
                    self.assertEqual(imported_roots(path), expected)


if __name__ == "__main__":
    unittest.main()
