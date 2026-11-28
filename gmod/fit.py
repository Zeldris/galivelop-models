"""`fit` (H3): does a variant fit a machine? A verdict from the hand-kept memory rules (D-5), integer MiB (invariant 10).

Pure and without I/O except `load_memory_rules`. Docs: docs/tasks/H3.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from gart.canon import loads_strict
from gmod.hardware import Hardware

MIB = 1024 * 1024
VERDICT_ORDER = {"fits": 0, "tight": 1, "no": 2, "unknown": 3}
POOL_ORDER = {"gpu": 0, "shared": 1, "ram": 2}
GPU_APIS = ("cuda", "rocm", "vulkan", "metal")


@dataclass(frozen=True)
class Fit:
    verdict: str  # fits | tight | no | unknown
    variant: str
    runtime: Optional[str] = None
    estimate_mib: Optional[int] = None
    available_mib: Optional[int] = None
    pool: Optional[str] = None  # gpu | shared | ram
    reason: str = ""
    params: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"verdict": self.verdict, "variant": self.variant, "runtime": self.runtime,
                "estimateMiB": self.estimate_mib, "availableMiB": self.available_mib, "pool": self.pool,
                "reason": {"code": self.reason, "params": dict(self.params)}}


def load_memory_rules(root: Union[str, Path]) -> dict:
    """Read `root/memory-rules.json` (a `gmod.memory_rules/0` document)."""
    return loads_strict((Path(root) / "memory-rules.json").read_text(encoding="utf-8"))


def estimate_mib(variant_bytes: int, rule: dict) -> int:
    """`ceil(bytes * factor / 1000 / MiB) + overhead`, all integers."""
    scaled = variant_bytes * rule["weightsFactorPermille"]
    return -(-scaled // (1000 * MIB)) + rule["overheadMiB"]


def _pools(machine: dict, rule: dict) -> tuple[list[tuple[str, int]], Optional[tuple[str, dict]]]:
    """The memory pools of `machine` this rule can use, in order gpu/shared/ram, and the first missing-data reason."""
    apis = set(machine.get("computeApis") or [])
    allowed = set(rule["computeApis"])
    pools: list[tuple[str, int]] = []
    missing: Optional[tuple[str, dict]] = None
    gpus = machine.get("gpus") or []
    if apis & allowed & set(GPU_APIS) and gpus:
        # Integrated + discrete (a laptop): both pools are tried and the best verdict wins.
        shared = [g for g in gpus if g.get("sharedMemory")]
        dedicated = [g for g in gpus if not g.get("sharedMemory")]
        if shared:
            if machine.get("ramMiB") is None:
                missing = missing or ("fit.missing", {"field": "ramMiB"})
            else:
                pools.append(("shared", machine["ramMiB"]))
        if dedicated:
            best = max(dedicated, key=lambda g: -1 if g.get("vramMiB") is None else g["vramMiB"])
            if best.get("vramMiB") is None:
                missing = missing or ("fit.missing", {"field": "vramMiB"})
            else:
                pools.append(("gpu", best["vramMiB"]))
    if "cpu" in apis and "cpu" in allowed:
        if machine.get("ramMiB") is None:
            missing = missing or ("fit.missing", {"field": "ramMiB"})
        else:
            pools.append(("ram", machine["ramMiB"]))
    pools.sort(key=lambda p: POOL_ORDER[p[0]])
    return pools, missing


def _verdict(estimate: int, available: int, margin: int) -> tuple[str, str]:
    if estimate + margin <= available:
        return "fits", "fit.ok"
    if estimate <= available:
        return "tight", "fit.tight"
    return "no", "fit.too_big"


def fit(variant: dict, machine: Union[dict, Hardware], rules: dict) -> Fit:
    """Verdict of `variant` on `machine` (a `gmod.machine/0` document or a detected `Hardware`)."""
    if isinstance(machine, Hardware):
        machine = machine.to_dict()
    by_runtime = {r["runtime"]: r for r in rules["rules"]}
    candidates: list[tuple[tuple, Fit]] = []
    unknowns: list[Fit] = []
    for runtime in sorted(r["id"] for r in variant["runtimes"]):
        base = {"variant": variant["id"], "runtime": runtime}
        rule = by_runtime.get(runtime)
        if rule is None:
            unknowns.append(Fit("unknown", reason="fit.no_rule", params={"missing": "runtime", "runtime": runtime}, **base))
            continue
        gap = next(((k, variant[k]) for k, plural in (("format", "formats"), ("quantization", "quantizations"))
                    if variant[k] not in rule[plural]), None)
        if gap:
            unknowns.append(Fit("unknown", reason="fit.no_rule", params={"missing": gap[0], "value": gap[1], "runtime": runtime}, **base))
            continue
        est = estimate_mib(variant["bytes"], rule)
        pools, missing = _pools(machine, rule)
        for pool, available in pools:
            verdict, code = _verdict(est, available, rule["marginMiB"])
            params = {"estimateMiB": est, "availableMiB": available, "marginMiB": rule["marginMiB"], "pool": pool}
            candidates.append(((VERDICT_ORDER[verdict], POOL_ORDER[pool], runtime),
                               Fit(verdict, variant["id"], runtime, est, available, pool, code, params)))
        if not pools:
            if missing:
                unknowns.append(Fit("unknown", reason=missing[0], params=missing[1], estimate_mib=est, **base))
            else:
                unknowns.append(Fit("unknown", reason="fit.no_compute_api",
                                    params={"machine": sorted(machine.get("computeApis") or []), "rule": rule["computeApis"]},
                                    estimate_mib=est, **base))
    if candidates:
        return min(candidates, key=lambda c: c[0])[1]
    if unknowns:
        return unknowns[0]
    return Fit("unknown", variant["id"], reason="fit.no_rule", params={"missing": "runtime"})
