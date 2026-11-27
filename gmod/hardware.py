"""Detection of the running machine's hardware (DDD: `detect_hardware() -> Hardware`, D-21).

The only part of `gmod` with system I/O. Every source is injectable so the tests simulate it: `root` prefixes the
Linux paths (`/proc`, `/sys`, `/dev`, `/opt`, `/usr`, `/etc`), `run` stands for running a local program
(`nvidia-smi`) and `registry` / `system32` / `env` stand for the Windows registry, `System32` and the environment.

Detection fails closed like `fit` (invariant 6): a value it cannot read is `None`, never a guess.
"""
from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Optional, Protocol, Sequence

__all__ = ["Cpu", "Gpu", "Hardware", "Registry", "detect_hardware"]

MIB = 1024 * 1024
# Canonical order of `computeApis`, the same list the `gmod.machine/0` field uses.
COMPUTE_API_ORDER = ("cuda", "rocm", "vulkan", "metal", "cpu")
VENDORS = {"1002": "AMD", "10de": "NVIDIA", "8086": "Intel"}
# AMD APUs by PCI device id (unified memory, no dedicated VRAM): Steam Deck LCD (Van Gogh) and OLED (Sephiroth).
AMD_APU_DEVICE_IDS = {"163f", "1435"}
# An AMD GPU with at most this much "VRAM" is an APU carve-out, not dedicated memory.
APU_CARVEOUT_MAX_MIB = 2048
LEGACY_VRAM_CAP_MIB = 4095
NVIDIA_SMI_QUERY = ["nvidia-smi", "--query-gpu=pci.bus_id,name,memory.total", "--format=csv,noheader,nounits"]
# Display adapters class in the Windows registry.
WINDOWS_DISPLAY_CLASS = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
WINDOWS_ENUM_PCI = r"SYSTEM\CurrentControlSet\Enum\PCI"
WINDOWS_DISPLAY_GUID = "{4d36e968-e325-11ce-bfc1-08002be10318}"
# Intel discrete GPUs by PCI device id prefix: Arc (DG2) and Battlemage.
INTEL_DISCRETE_PREFIXES = ("56", "e2")
LINUX_HIP_LIB_DIRS = ("usr/lib", "usr/lib64", "usr/lib/x86_64-linux-gnu")
WINDOWS_CPU_KEY = r"HARDWARE\DESCRIPTION\System\CentralProcessor"

Runner = Callable[[Sequence[str]], Optional[str]]


@dataclass(frozen=True)
class Cpu:
    model: Optional[str]
    cores: Optional[int]
    threads: Optional[int]

    def to_dict(self) -> dict:
        return {"model": self.model, "cores": self.cores, "threads": self.threads}


@dataclass(frozen=True)
class Gpu:
    name: Optional[str]
    vendor: Optional[str]
    integrated: bool
    vram_mib: Optional[int]

    def to_dict(self) -> dict:
        return {"name": self.name, "vendor": self.vendor, "integrated": self.integrated, "vramMiB": self.vram_mib}


@dataclass(frozen=True)
class Hardware:
    """The fields of a `Machine` read from the running computer, never stored in the catalog (D-21)."""

    cpu: Optional[Cpu]
    ram_mib: Optional[int]
    gpus: tuple
    compute_apis: tuple
    os: Optional[str]

    def to_dict(self) -> dict:
        """The same keys and units as a `gmod.machine/0` document (MiB integers, invariant 10)."""
        return {
            "cpu": self.cpu.to_dict() if self.cpu else None,
            "ramMiB": self.ram_mib,
            "gpus": [gpu.to_dict() for gpu in self.gpus],
            "computeApis": list(self.compute_apis),
            "os": self.os,
        }


class Registry(Protocol):
    """Read-only view of `HKEY_LOCAL_MACHINE`: the values and the subkey names of one key (empty if it is missing)."""

    def values(self, key: str) -> Mapping[str, object]: ...

    def subkeys(self, key: str) -> Sequence[str]: ...


def detect_hardware(
    *,
    system: Optional[str] = None,
    root: os.PathLike | str = "/",
    run: Optional[Runner] = None,
    registry: Optional[Registry] = None,
    system32: Optional[os.PathLike | str] = None,
    env: Optional[Mapping[str, str]] = None,
    total_ram_bytes: Optional[int] = None,
    present: Optional[Callable[[str], bool]] = None,
) -> Hardware:
    """Read the hardware of this computer (Linux or Windows); with no arguments, the real one.

    Any other system gives a `Hardware` with every field unknown, so `fit` answers `unknown` (invariant 6).
    """
    system = (system or platform.system()).lower()
    run = run if run is not None else _run_local
    if system == "linux":
        return _detect_linux(Path(root), run)
    if system == "windows":
        env = os.environ if env is None else env
        if registry is None:
            registry = _WinRegistry()
        if system32 is None:
            system32 = Path(env.get("SystemRoot", r"C:\Windows")) / "System32"
        if total_ram_bytes is None:
            total_ram_bytes = _windows_total_ram()
        if present is None:
            present = _windows_present
        return _detect_windows(registry, Path(system32), env, total_ram_bytes, run, present)
    return Hardware(cpu=None, ram_mib=None, gpus=(), compute_apis=(), os=None)


# --- shared ---------------------------------------------------------------------------------------------------------


def _run_local(command: Sequence[str]) -> Optional[str]:
    """Run a local program and return its output, or None if it is missing or fails. Never reaches the network."""
    if shutil.which(command[0]) is None:
        return None
    try:
        done = subprocess.run(list(command), capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if done.returncode == 0 else None


def _is_integrated(vendor: Optional[str], device_id: Optional[str], vram_mib: Optional[int]) -> bool:
    if vendor == "Intel":
        if device_id and device_id.lower().startswith(INTEL_DISCRETE_PREFIXES):
            return False
        return vram_mib is None or vram_mib <= APU_CARVEOUT_MAX_MIB
    if vendor == "AMD":
        if device_id in AMD_APU_DEVICE_IDS:
            return True
        return vram_mib is not None and vram_mib <= APU_CARVEOUT_MAX_MIB
    return False


def _gpu(name, vendor, device_id, vram_mib) -> Gpu:
    integrated = _is_integrated(vendor, device_id, vram_mib)
    # An integrated GPU shares system RAM: its carve-out is not dedicated VRAM (catalog `steam-deck`).
    return Gpu(name=name, vendor=vendor, integrated=integrated, vram_mib=None if integrated else vram_mib)


def _ordered(apis) -> tuple:
    return tuple(api for api in COMPUTE_API_ORDER if api in apis)


def _nvidia_smi(run: Runner) -> dict:
    """`{pci slot: (name, vram MiB)}` from nvidia-smi, keyed like sysfs (`0000:01:00.0`)."""
    found = {}
    for line in (run(NVIDIA_SMI_QUERY) or "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
            continue
        bus, name, memory = parts
        found[bus.lower()[-12:]] = (name or None, int(memory) if memory.isdigit() else None)
    return found


# --- Linux ----------------------------------------------------------------------------------------------------------


def _read(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _linux_cpu(root: Path) -> Optional[Cpu]:
    text = _read(root / "proc/cpuinfo")
    if text is None:
        return None
    model, threads, cores = None, 0, set()
    for block in text.split("\n\n"):
        fields = {}
        for line in block.splitlines():
            key, sep, value = line.partition(":")
            if sep:
                fields[key.strip()] = value.strip()
        if "processor" not in fields:
            continue
        threads += 1
        model = model or fields.get("model name")
        if "physical id" in fields and "core id" in fields:
            cores.add((fields["physical id"], fields["core id"]))
    if threads == 0:
        return None
    return Cpu(model=model, cores=len(cores) or None, threads=threads)


def _linux_ram_mib(root: Path) -> Optional[int]:
    match = re.search(r"^MemTotal:\s+(\d+)\s*kB", _read(root / "proc/meminfo") or "", re.MULTILINE)
    return int(match.group(1)) // 1024 if match else None


def _linux_gpus(root: Path, smi: dict) -> list:
    drm = root / "sys/class/drm"
    cards = sorted(
        (entry for entry in (drm.iterdir() if drm.is_dir() else []) if re.fullmatch(r"card\d+", entry.name)),
        key=lambda entry: int(entry.name[4:]),
    )
    gpus, seen = [], set()
    for card in cards:
        uevent = dict(
            line.split("=", 1) for line in (_read(card / "device/uevent") or "").splitlines() if "=" in line
        )
        vendor_id, _, device_id = uevent.get("PCI_ID", "").lower().partition(":")
        slot = uevent.get("PCI_SLOT_NAME", "").lower()
        if not vendor_id or slot in seen:
            continue
        seen.add(slot)
        vendor = VENDORS.get(vendor_id)
        name = (_read(card / "device/product_name") or "").strip() or None
        vram_mib = None
        vram_bytes = (_read(card / "device/mem_info_vram_total") or "").strip()
        if vram_bytes.isdigit() and int(vram_bytes) > 0:
            vram_mib = int(vram_bytes) // MIB
        if vendor == "NVIDIA":
            smi_name, smi_vram = smi.get(slot, (None, None))
            if smi_vram is not None:
                vram_mib = smi_vram
            name = smi_name or _nvidia_proc_model(root, slot) or name
        gpus.append(_gpu(name or f"{vendor or vendor_id} {device_id}", vendor, device_id, vram_mib))
    # NVIDIA GPUs the driver lists but sysfs has no DRM card for (no modesetting).
    proc_gpus = root / "proc/driver/nvidia/gpus"
    proc_slots = [e.name.lower() for e in proc_gpus.iterdir() if e.is_dir()] if proc_gpus.is_dir() else []
    for slot in sorted(set(smi) | set(proc_slots)):
        if slot in seen:
            continue
        seen.add(slot)
        smi_name, smi_vram = smi.get(slot, (None, None))
        name = smi_name or _nvidia_proc_model(root, slot) or "NVIDIA"
        gpus.append(_gpu(name, "NVIDIA", None, smi_vram))
    return gpus


def _nvidia_proc_model(root: Path, slot: str) -> Optional[str]:
    match = re.search(r"^Model:\s*(.+)$", _read(root / "proc/driver/nvidia/gpus" / slot / "information") or "", re.M)
    return match.group(1).strip() if match else None


def _linux_compute_apis(root: Path, gpus: list, smi: dict) -> tuple:
    apis = {"cpu"}
    vendors = {gpu.vendor for gpu in gpus}
    if "NVIDIA" in vendors and (smi or (root / "proc/driver/nvidia/version").exists()):
        apis.add("cuda")
    if "AMD" in vendors and (root / "dev/kfd").exists():
        hip_lib = any(
            (root / d).is_dir() and any((root / d).glob("libamdhip64.so*")) for d in LINUX_HIP_LIB_DIRS
        )
        if (root / "opt/rocm").is_dir() or hip_lib:
            apis.add("rocm")
    icd_dirs = [root / "usr/share/vulkan/icd.d", root / "etc/vulkan/icd.d"]

    def hardware_icd(path: Path) -> bool:
        name = path.name.lower()
        return not (name.startswith("lvp_") or "swiftshader" in name)

    if gpus and any(d.is_dir() and any(hardware_icd(f) for f in d.glob("*.json")) for d in icd_dirs):
        apis.add("vulkan")
    return _ordered(apis)


def _detect_linux(root: Path, run: Runner) -> Hardware:
    has_nvidia = (root / "proc/driver/nvidia").is_dir()
    smi = _nvidia_smi(run) if has_nvidia else {}
    gpus = _linux_gpus(root, smi)
    return Hardware(
        cpu=_linux_cpu(root),
        ram_mib=_linux_ram_mib(root),
        gpus=tuple(gpus),
        compute_apis=_linux_compute_apis(root, gpus, smi),
        os="linux",
    )


# --- Windows --------------------------------------------------------------------------------------------------------


class _WinRegistry:
    """`Registry` over the real `winreg` (only importable on Windows)."""

    def __init__(self):
        import winreg

        self._winreg = winreg

    def values(self, key):
        winreg = self._winreg
        found = {}
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as handle:
                index = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(handle, index)
                    except OSError:
                        break
                    found[name] = value
                    index += 1
        except OSError:
            pass
        return found

    def subkeys(self, key):
        winreg = self._winreg
        names = []
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as handle:
                index = 0
                while True:
                    try:
                        names.append(winreg.EnumKey(handle, index))
                    except OSError:
                        break
                    index += 1
        except OSError:
            pass
        return names


def _windows_total_ram() -> Optional[int]:
    import ctypes

    class MemoryStatusEx(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    status = MemoryStatusEx()
    status.dwLength = ctypes.sizeof(MemoryStatusEx)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):  # type: ignore[attr-defined]
        return None
    return int(status.ullTotalPhys)


def _windows_cpu(registry: Registry) -> Optional[Cpu]:
    threads = [name for name in registry.subkeys(WINDOWS_CPU_KEY) if name.isdigit()]
    if not threads:
        return None
    model = registry.values(WINDOWS_CPU_KEY + "\\" + threads[0]).get("ProcessorNameString")
    # The registry lists logical processors only; physical cores stay unknown.
    return Cpu(model=str(model).strip() if model else None, cores=None, threads=len(threads))


def _registry_int(value) -> Optional[int]:
    if isinstance(value, int):
        return value
    if isinstance(value, (bytes, bytearray)) and value:
        return int.from_bytes(value, "little")
    return None


def _windows_present(instance_id: str) -> bool:
    """True if the device node exists now (a retired adapter keeps its registry entries but has no node)."""
    import ctypes

    node = ctypes.c_ulong()
    cfgmgr32 = ctypes.windll.cfgmgr32  # type: ignore[attr-defined]
    return cfgmgr32.CM_Locate_DevNodeW(ctypes.byref(node), instance_id, 0) == 0


def _windows_present_adapters(registry: Registry, present: Callable[[str], bool]) -> dict:
    """`{Class subkey NNNN: pci slot or None}` of the display adapters whose device node is present."""
    prefix = (WINDOWS_DISPLAY_GUID + "\\").lower()
    found = {}
    for hwid in registry.subkeys(WINDOWS_ENUM_PCI):
        for instance in registry.subkeys(WINDOWS_ENUM_PCI + "\\" + hwid):
            values = registry.values(WINDOWS_ENUM_PCI + "\\" + hwid + "\\" + instance)
            driver = str(values.get("Driver") or "")
            if not driver.lower().startswith(prefix):
                continue
            if not present("PCI\\" + hwid + "\\" + instance):
                continue
            location = re.search(
                r"bus (\d+), device (\d+), function (\d+)", str(values.get("LocationInformation") or ""), re.I
            )
            slot = "%04x:%02x:%02x.%x" % (0, *map(int, location.groups())) if location else None
            found[driver[len(prefix):]] = slot
    return found


def _windows_gpus(registry: Registry, smi: dict, present: Callable[[str], bool]) -> list:
    gpus = []
    adapters = _windows_present_adapters(registry, present)
    for sub in sorted(name for name in registry.subkeys(WINDOWS_DISPLAY_CLASS) if name.isdigit()):
        if sub not in adapters:
            continue
        values = registry.values(WINDOWS_DISPLAY_CLASS + "\\" + sub)
        match = re.search(r"VEN_([0-9A-Fa-f]{4})&DEV_([0-9A-Fa-f]{4})", str(values.get("MatchingDeviceId", "")))
        if not match:  # Basic display adapters, remote and virtual displays: no PCI GPU behind them
            continue
        vendor_id, device_id = match.group(1).lower(), match.group(2).lower()
        vendor = VENDORS.get(vendor_id)
        name = str(values.get("DriverDesc") or "").strip() or None
        vram_bytes = _registry_int(values.get("HardwareInformation.qwMemorySize")) or None
        if vram_bytes is None:
            # The 32-bit value saturates just under 4 GiB (0xFFFFFFFF, 0xFFF00000): from 4095 MiB up it is only a
            # lower bound, so unknown (fails closed).
            legacy = _registry_int(values.get("HardwareInformation.MemorySize"))
            vram_bytes = legacy if legacy and legacy < LEGACY_VRAM_CAP_MIB * MIB else None
        vram_mib = vram_bytes // MIB if vram_bytes is not None else None
        slot = adapters[sub]
        if vendor == "NVIDIA" and slot in smi:
            smi_name, smi_vram = smi[slot]
            if smi_vram is not None:
                vram_mib = smi_vram
        gpus.append(_gpu(name or f"{vendor or vendor_id} {device_id}", vendor, device_id, vram_mib))
    return gpus


def _detect_windows(registry, system32: Path, env, total_ram_bytes, run: Runner, present) -> Hardware:
    smi = _nvidia_smi(run) if (system32 / "nvcuda.dll").exists() else {}
    gpus = _windows_gpus(registry, smi, present)
    vendors = {gpu.vendor for gpu in gpus}
    apis = {"cpu"}
    if "NVIDIA" in vendors and (system32 / "nvcuda.dll").exists():
        apis.add("cuda")
    if "AMD" in vendors and env.get("HIP_PATH"):
        apis.add("rocm")
    if gpus and (system32 / "vulkan-1.dll").exists():
        apis.add("vulkan")
    return Hardware(
        cpu=_windows_cpu(registry),
        ram_mib=total_ram_bytes // MIB if total_ram_bytes else None,
        gpus=tuple(gpus),
        compute_apis=_ordered(apis),
        os="windows",
    )
