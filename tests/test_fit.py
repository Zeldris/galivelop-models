"""H3: `fit` with the memory rules (invariants 5, 6, 9, 10; docs/tasks/H3.md)."""
import json
import unittest
from pathlib import Path

from gmod.catalog import validate_catalog
from gmod.fit import MIB, Fit, estimate_mib, fit, load_memory_rules
from tests.test_hardware import GIB, LinuxBox

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
TASKS = ("text", "embed", "image", "stt", "tts", "vision")


def rule(runtime="eng", **over):
    base = {"runtime": runtime, "formats": ["gguf"], "quantizations": ["q4_k_m"], "computeApis": ["cuda", "vulkan", "cpu"],
            "weightsFactorPermille": 1000, "overheadMiB": 100, "marginMiB": 50, "notes": ""}
    base.update(over)
    return base


def rules_doc(*rules):
    return {"kind": "gmod.memory_rules/0", "rules": list(rules) or [rule()]}


def variant(mib=1000, runtimes=("eng",), **over):
    # estimate with rule(): mib + 100 overhead (factor 1000)
    base = {"id": "m:gguf-q4_k_m", "format": "gguf", "quantization": "q4_k_m", "bytes": mib * MIB,
            "runtimes": [{"id": r, "minVersion": "1"} for r in runtimes]}
    base.update(over)
    return base


def gpu(vram, shared=False, integrated=False):
    return {"name": "g", "vendor": None, "integrated": integrated, "vramMiB": vram, "sharedMemory": shared}


def machine(gpus=(), ram=8000, apis=("cuda", "vulkan", "cpu")):
    return {"kind": "gmod.machine/0", "id": "t", "cpu": None, "ramMiB": ram, "gpus": list(gpus), "computeApis": list(apis), "os": None}


def real_machine(name):
    return json.loads((CATALOG / "machines" / f"{name}.json").read_text(encoding="utf-8"))


class EstimateTest(unittest.TestCase):
    def test_integer_ceiling(self):
        r = rule(weightsFactorPermille=1100, overheadMiB=1024)
        self.assertEqual(estimate_mib(MIB, r), 1 + 1024 + 1)  # 1.1 MiB rounds up to 2
        self.assertEqual(estimate_mib(10 * MIB, r), 11 + 1024)
        self.assertEqual(estimate_mib(1, rule(overheadMiB=0)), 1)
        self.assertIsInstance(estimate_mib(4920752841, r), int)


class VerdictTest(unittest.TestCase):
    def check(self, available, expected):
        got = fit(variant(1000), machine([gpu(available)], apis=("cuda",)), rules_doc())
        self.assertEqual((got.verdict, got.reason, got.estimate_mib, got.available_mib, got.pool),
                         (expected[0], expected[1], 1100, available, "gpu"))
        return got

    def test_exact_limits(self):
        self.check(1150, ("fits", "fit.ok"))  # estimate + margin == available
        self.check(1149, ("tight", "fit.tight"))
        self.check(1100, ("tight", "fit.tight"))  # estimate == available
        self.check(1099, ("no", "fit.too_big"))

    def test_params_and_to_dict(self):
        got = self.check(2000, ("fits", "fit.ok"))
        self.assertEqual(got.params, {"estimateMiB": 1100, "availableMiB": 2000, "marginMiB": 50, "pool": "gpu"})
        self.assertEqual(got.to_dict(), {"verdict": "fits", "variant": "m:gguf-q4_k_m", "runtime": "eng", "estimateMiB": 1100,
                                         "availableMiB": 2000, "pool": "gpu", "reason": {"code": "fit.ok", "params": got.params}})
        self.assertIsInstance(got, Fit)
        with self.assertRaises(Exception):
            got.verdict = "no"


class UnknownTest(unittest.TestCase):
    def one(self, v, m, rules=None):
        got = fit(v, m, rules or rules_doc())
        self.assertEqual(got.verdict, "unknown")
        return got

    def test_no_rule_for_runtime(self):
        got = self.one(variant(runtimes=("other",)), machine([gpu(9999)]))
        self.assertEqual((got.reason, got.params), ("fit.no_rule", {"missing": "runtime", "runtime": "other"}))
        self.assertEqual((got.runtime, got.pool, got.estimate_mib), ("other", None, None))

    def test_no_rule_for_format_and_quantization(self):
        got = self.one(variant(format="ggml"), machine([gpu(9999)]))
        self.assertEqual((got.reason, got.params), ("fit.no_rule", {"missing": "format", "value": "ggml", "runtime": "eng"}))
        got = self.one(variant(quantization="q2_k"), machine([gpu(9999)]))
        self.assertEqual((got.reason, got.params), ("fit.no_rule", {"missing": "quantization", "value": "q2_k", "runtime": "eng"}))

    def test_missing_vram_without_shared_memory(self):
        got = self.one(variant(), machine([gpu(None)], apis=("cuda",)))
        self.assertEqual((got.reason, got.params), ("fit.missing", {"field": "vramMiB"}))

    def test_missing_ram(self):
        got = self.one(variant(), machine([], ram=None, apis=("cpu",)))
        self.assertEqual((got.reason, got.params), ("fit.missing", {"field": "ramMiB"}))
        got = self.one(variant(), machine([gpu(0, shared=True, integrated=True)], ram=None, apis=("vulkan",)))
        self.assertEqual((got.reason, got.params), ("fit.missing", {"field": "ramMiB"}))

    def test_empty_compute_apis_is_the_real_gpu_12gb(self):
        v = json.loads((CATALOG / "models" / "qwen3.5-4b.json").read_text(encoding="utf-8"))["variants"][0]
        got = self.one(v, real_machine("gpu-12gb"), load_memory_rules(CATALOG))
        self.assertEqual(got.reason, "fit.no_compute_api")
        self.assertEqual(got.params, {"machine": [], "rule": ["cuda", "rocm", "vulkan", "metal", "cpu"]})

    def test_no_api_in_common(self):
        got = self.one(variant(), machine([gpu(9999)], apis=("metal",)))
        self.assertEqual(got.reason, "fit.no_compute_api")


class PoolTest(unittest.TestCase):
    def test_discrete_gpu_beats_ram(self):
        got = fit(variant(1000), machine([gpu(4000)], ram=64000), rules_doc())
        self.assertEqual((got.verdict, got.pool, got.available_mib), ("fits", "gpu", 4000))

    def test_falls_back_to_ram_with_cpu(self):
        got = fit(variant(1000), machine([gpu(512)], ram=4000), rules_doc())
        self.assertEqual((got.verdict, got.pool, got.available_mib), ("fits", "ram", 4000))

    def test_no_fallback_to_ram_without_cpu_api(self):
        got = fit(variant(1000), machine([gpu(512)], ram=64000, apis=("cuda",)), rules_doc())
        self.assertEqual((got.verdict, got.pool), ("no", "gpu"))

    def test_rule_without_cpu_ignores_ram(self):
        got = fit(variant(1000), machine([gpu(512)], ram=64000), rules_doc(rule(computeApis=["cuda"])))
        self.assertEqual((got.verdict, got.pool), ("no", "gpu"))

    def test_shared_memory_uses_ram(self):
        got = fit(variant(1000), machine([gpu(None, shared=True, integrated=True)], ram=4000, apis=("vulkan",)), rules_doc())
        self.assertEqual((got.verdict, got.pool, got.available_mib), ("fits", "shared", 4000))

    def test_shared_beats_ram_on_a_tie(self):
        got = fit(variant(1000), machine([gpu(None, shared=True, integrated=True)], ram=4000), rules_doc())
        self.assertEqual(got.pool, "shared")

    def test_largest_gpu_alone(self):
        got = fit(variant(1000), machine([gpu(600), gpu(1200)], ram=1, apis=("cuda",)), rules_doc())
        self.assertEqual((got.pool, got.available_mib), ("gpu", 1200))  # no split across GPUs

    def test_usable_pool_beats_missing_data(self):
        got = fit(variant(1000), machine([gpu(None)], ram=4000), rules_doc())
        self.assertEqual((got.verdict, got.pool), ("fits", "ram"))


class DeterminismTest(unittest.TestCase):
    def test_same_call_same_result(self):
        args = (variant(1000, runtimes=("b", "a")), machine([gpu(4000)]), rules_doc(rule("a"), rule("b")))
        self.assertEqual(fit(*args), fit(*args))

    def test_best_verdict_across_runtimes(self):
        rules = rules_doc(rule("a", overheadMiB=5000), rule("b"))
        got = fit(variant(1000, runtimes=("a", "b")), machine([gpu(4000)]), rules)
        self.assertEqual((got.runtime, got.verdict), ("b", "fits"))

    def test_tie_goes_to_runtime_id(self):
        rules = rules_doc(rule("b"), rule("a"))
        for order in (("a", "b"), ("b", "a")):
            got = fit(variant(1000, runtimes=order), machine([gpu(4000)]), rules)
            self.assertEqual(got.runtime, "a")

    def test_unknown_reason_is_the_first_runtime(self):
        got = fit(variant(runtimes=("z", "y")), machine([gpu(100)]), rules_doc())
        self.assertEqual(got.params["runtime"], "y")

    def test_known_runtime_beats_unknown_one(self):
        got = fit(variant(1000, runtimes=("zzz", "eng")), machine([gpu(4000)]), rules_doc())
        self.assertEqual((got.runtime, got.verdict), ("eng", "fits"))


class DeckTest(unittest.TestCase):
    def test_detected_deck_equals_catalog_deck(self):
        box = LinuxBox()
        self.addCleanup(box.close)
        box.base()
        box.card(0, "1002:163F", "0000:04:00.0", vram_bytes=1 * GIB)
        box.write("usr/share/vulkan/icd.d/radeon_icd.x86_64.json", "{}")
        hw, _ = box.detect()
        self.assertTrue(hw.gpus[0].shared_memory)
        self.assertEqual(hw.to_dict()["gpus"][0]["sharedMemory"], True)
        rules, deck = load_memory_rules(CATALOG), real_machine("steam-deck")
        for path in sorted((CATALOG / "models").glob("*.json")):
            for var in json.loads(path.read_text(encoding="utf-8"))["variants"]:
                with self.subTest(variant=var["id"]):
                    a, b = fit(var, hw, rules), fit(var, deck, rules)
                    self.assertEqual((a.verdict, a.runtime, a.pool, a.estimate_mib), (b.verdict, b.runtime, b.pool, b.estimate_mib))
                    self.assertEqual(b.pool, "shared")

    def test_rules_stay_under_the_gvc_memory_hints_on_the_deck(self):
        rules, deck = load_memory_rules(CATALOG), real_machine("steam-deck")
        for path in sorted((CATALOG / "models").glob("*.json")):
            for var in json.loads(path.read_text(encoding="utf-8"))["variants"]:
                for hint in var.get("memoryHints", []):
                    if hint["machine"] == "steam-deck":
                        with self.subTest(variant=var["id"]):
                            got = fit(var, deck, rules)
                            self.assertLess(got.estimate_mib + 512, hint["minFreeMiB"])

    def test_invariant_9_every_task_fits_the_deck(self):
        rules, deck = load_memory_rules(CATALOG), real_machine("steam-deck")
        best = {task: None for task in TASKS}
        for path in sorted((CATALOG / "models").glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            for var in doc["variants"]:
                if fit(var, deck, rules).verdict in ("fits", "tight"):
                    for task in doc["tasks"]:
                        best[task] = var["id"]
        self.assertEqual([t for t, v in best.items() if v is None], [])


class RulesFileTest(unittest.TestCase):
    def test_real_rules_validate_and_cover_the_catalog_runtimes(self):
        self.assertEqual(validate_catalog(CATALOG), [])
        rules = load_memory_rules(CATALOG)
        used = {r["id"] for p in (CATALOG / "models").glob("*.json")
                for v in json.loads(p.read_text(encoding="utf-8"))["variants"] for r in v["runtimes"]}
        self.assertEqual(used, {r["runtime"] for r in rules["rules"]})


if __name__ == "__main__":
    unittest.main()
