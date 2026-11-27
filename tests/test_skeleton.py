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


def imported_roots(path):
    """The top-level names of the absolute imports of one source file."""
    roots = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
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


if __name__ == "__main__":
    unittest.main()
