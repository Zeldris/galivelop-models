"""detect_hardware (H5): Linux and Windows with /proc, sysfs, the registry and nvidia-smi simulated (no real system)."""
import json
import tempfile
import unittest
from pathlib import Path

from gmod.hardware import NVIDIA_SMI_QUERY, WINDOWS_CPU_KEY, WINDOWS_DISPLAY_CLASS, WINDOWS_ENUM_PCI, detect_hardware

ROOT = Path(__file__).resolve().parent.parent
GIB = 1024 ** 3


def cpuinfo(model, cores, threads_per_core=2):
    blocks, n = [], 0
    for core in range(cores):
        for _ in range(threads_per_core):
            blocks.append(f"processor\t: {n}\nmodel name\t: {model}\nphysical id\t: 0\ncore id\t\t: {core}\n")
            n += 1
    return "\n".join(blocks) + "\n"


class LinuxBox:
    """A fake root with only the files a test writes."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def close(self):
        self._tmp.cleanup()

    def write(self, rel, text=""):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def mkdir(self, rel):
        (self.root / rel).mkdir(parents=True, exist_ok=True)

    def base(self, model="AMD Custom APU 0405", cores=4, mem_kb=15_995_464):
        self.write("proc/cpuinfo", cpuinfo(model, cores))
        self.write("proc/meminfo", f"MemTotal:       {mem_kb} kB\nMemFree:         1000 kB\n")

    def card(self, n, pci_id, slot, vram_bytes=None, product=None):
        dev = f"sys/class/drm/card{n}/device"
        self.write(f"{dev}/uevent", f"DRIVER=x\nPCI_ID={pci_id}\nPCI_SLOT_NAME={slot}\n")
        if vram_bytes is not None:
            self.write(f"{dev}/mem_info_vram_total", f"{vram_bytes}\n")
        if product:
            self.write(f"{dev}/product_name", product + "\n")
        # Connector entries share the card's directory and must not count as GPUs.
        self.mkdir(f"sys/class/drm/card{n}-eDP-1")

    def detect(self, smi=None):
        calls = []

        def run(command):
            calls.append(list(command))
            return smi

        hw = detect_hardware(system="Linux", root=self.root, run=run)
        return hw, calls


class LinuxTest(unittest.TestCase):
    def setUp(self):
        self.box = LinuxBox()
        self.addCleanup(self.box.close)

    def test_steam_deck_matches_catalog_machine(self):
        box = self.box
        box.base()
        box.card(0, "1002:163F", "0000:04:00.0", vram_bytes=1 * GIB)
        box.write("usr/share/vulkan/icd.d/radeon_icd.x86_64.json", "{}")
        box.write("dev/kfd")  # SteamOS exposes kfd but ships no ROCm: not a rocm machine
        hw, calls = box.detect()
        self.assertEqual(calls, [], "nvidia-smi runs only with the NVIDIA driver loaded")
        machine = json.loads((ROOT / "catalog/machines/steam-deck.json").read_text(encoding="utf-8"))
        self.assertEqual(hw.os, machine["os"])
        self.assertEqual(hw.compute_apis, tuple(machine["computeApis"]))
        self.assertEqual(hw.cpu.cores, machine["cpu"]["cores"])
        self.assertEqual(hw.cpu.threads, machine["cpu"]["threads"])
        self.assertEqual(hw.cpu.model, "AMD Custom APU 0405")
        self.assertEqual(hw.ram_mib, 15_995_464 // 1024)
        self.assertEqual(len(hw.gpus), 1)
        self.assertEqual(hw.gpus[0].vendor, "AMD")
        self.assertTrue(hw.gpus[0].integrated)
        self.assertIsNone(hw.gpus[0].vram_mib, "the APU carve-out is not dedicated VRAM")
        self.assertEqual(hw.gpus[0].to_dict(), machine["gpus"][0] | {"name": hw.gpus[0].name},
                         "an integrated GPU declares sharedMemory like the catalog machine")

    def test_nvidia_cuda_reads_vram_from_nvidia_smi(self):
        box = self.box
        box.base(model="Intel(R) Core(TM) i7-12700", cores=8, mem_kb=32 * 1024 * 1024)
        box.card(0, "10DE:2504", "0000:01:00.0")
        box.card(1, "8086:4680", "0000:00:02.0")
        box.write("proc/driver/nvidia/version", "NVRM version: 550.54\n")
        box.write("etc/vulkan/icd.d/nvidia_icd.json", "{}")
        hw, calls = box.detect(smi="00000000:01:00.0, NVIDIA GeForce RTX 3060, 12288\n")
        self.assertEqual(calls, [NVIDIA_SMI_QUERY])
        self.assertEqual(hw.compute_apis, ("cuda", "vulkan", "cpu"))
        self.assertEqual(hw.ram_mib, 32768)
        nvidia, intel = hw.gpus
        self.assertEqual((nvidia.name, nvidia.vendor, nvidia.integrated, nvidia.vram_mib),
                         ("NVIDIA GeForce RTX 3060", "NVIDIA", False, 12288))
        self.assertEqual((intel.vendor, intel.integrated, intel.vram_mib), ("Intel", True, None))
        self.assertEqual((nvidia.shared_memory, intel.shared_memory), (False, True))

    def test_nvidia_without_nvidia_smi_keeps_vram_unknown(self):
        box = self.box
        box.base()
        box.card(0, "10de:2504", "0000:01:00.0")
        box.write("proc/driver/nvidia/version", "NVRM\n")
        box.write("proc/driver/nvidia/gpus/0000:01:00.0/information", "Model: \t NVIDIA GeForce RTX 3060\nIRQ: 1\n")
        hw, _ = box.detect(smi=None)
        self.assertEqual(hw.gpus[0].name, "NVIDIA GeForce RTX 3060")
        self.assertIsNone(hw.gpus[0].vram_mib)
        self.assertIn("cuda", hw.compute_apis)

    def test_amd_rocm_discrete(self):
        box = self.box
        box.base(model="AMD Ryzen 7 5800X 8-Core Processor", cores=8)
        box.card(0, "1002:73BF", "0000:03:00.0", vram_bytes=16 * GIB, product="AMD Radeon RX 6800 XT")
        box.write("dev/kfd")
        box.mkdir("opt/rocm")
        box.write("usr/share/vulkan/icd.d/radeon_icd.json", "{}")
        hw, _ = box.detect()
        self.assertEqual(hw.compute_apis, ("rocm", "vulkan", "cpu"))
        gpu = hw.gpus[0]
        self.assertEqual((gpu.name, gpu.integrated, gpu.vram_mib), ("AMD Radeon RX 6800 XT", False, 16384))

    def test_nvidia_without_drm_card_is_still_listed(self):
        box = self.box
        box.base()
        box.write("proc/driver/nvidia/version", "NVRM\n")
        hw, _ = box.detect(smi="00000000:01:00.0, NVIDIA GeForce RTX 3060, 12288\n")
        self.assertEqual(len(hw.gpus), 1)
        self.assertEqual((hw.gpus[0].name, hw.gpus[0].vendor, hw.gpus[0].vram_mib),
                         ("NVIDIA GeForce RTX 3060", "NVIDIA", 12288))
        self.assertIn("cuda", hw.compute_apis)

    def test_nvidia_smi_na_keeps_sysfs_vram(self):
        box = self.box
        box.base()
        box.card(0, "10de:2504", "0000:01:00.0", vram_bytes=8 * GIB)
        box.write("proc/driver/nvidia/version", "NVRM\n")
        hw, _ = box.detect(smi="00000000:01:00.0, NVIDIA GeForce RTX 3060, [N/A]\n")
        self.assertEqual(hw.gpus[0].vram_mib, 8192)

    def test_zero_vram_is_unknown(self):
        box = self.box
        box.base()
        box.card(0, "1002:73bf", "0000:03:00.0", vram_bytes=0)
        self.assertIsNone(box.detect()[0].gpus[0].vram_mib)

    def test_intel_arc_is_discrete(self):
        box = self.box
        box.base()
        box.card(0, "8086:56a0", "0000:03:00.0", vram_bytes=16 * GIB)
        box.card(1, "8086:e20b", "0000:04:00.0")
        arc, bmg = box.detect()[0].gpus
        self.assertEqual((arc.integrated, arc.vram_mib), (False, 16384))
        self.assertEqual((bmg.integrated, bmg.vram_mib), (False, None))

    def test_rocm_with_hip_library_and_no_opt_rocm(self):
        box = self.box
        box.base()
        box.card(0, "1002:73bf", "0000:03:00.0", vram_bytes=16 * GIB)
        box.write("dev/kfd")
        box.write("usr/lib64/libamdhip64.so.6", "")
        self.assertIn("rocm", box.detect()[0].compute_apis)

    def test_software_vulkan_icd_does_not_count(self):
        box = self.box
        box.base()
        box.card(0, "1002:73bf", "0000:03:00.0", vram_bytes=16 * GIB)
        box.write("usr/share/vulkan/icd.d/lvp_icd.x86_64.json", "{}")
        box.write("usr/share/vulkan/icd.d/libvk_swiftshader.json", "{}")
        self.assertNotIn("vulkan", box.detect()[0].compute_apis)

    def test_cpu_only(self):
        self.box.base(model="Intel(R) Xeon(R)", cores=2)
        hw, _ = self.box.detect()
        self.assertEqual(hw.gpus, ())
        self.assertEqual(hw.compute_apis, ("cpu",))
        self.assertEqual((hw.cpu.cores, hw.cpu.threads), (2, 4))

    def test_missing_sources_are_unknown_not_guessed(self):
        hw, _ = self.box.detect()
        self.assertIsNone(hw.cpu)
        self.assertIsNone(hw.ram_mib)
        self.assertEqual(hw.to_dict(), {"cpu": None, "ramMiB": None, "gpus": [], "computeApis": ["cpu"],
                                        "os": "linux"})

    def test_to_dict_has_machine_keys(self):
        self.box.base()
        self.box.card(0, "1002:163f", "0000:04:00.0", vram_bytes=GIB)
        machine = json.loads((ROOT / "catalog/machines/steam-deck.json").read_text(encoding="utf-8"))
        data = self.box.detect()[0].to_dict()
        self.assertEqual(set(data), {"cpu", "ramMiB", "gpus", "computeApis", "os"})
        self.assertLessEqual(set(data), set(machine))
        self.assertEqual(set(data["gpus"][0]), set(machine["gpus"][0]))
        self.assertEqual(set(data["cpu"]), set(machine["cpu"]))


class FakeRegistry:
    def __init__(self, keys):
        self.keys = keys

    def values(self, key):
        return self.keys.get(key, {})

    def subkeys(self, key):
        prefix = key + "\\"
        return sorted({k[len(prefix):].split("\\")[0] for k in self.keys if k.startswith(prefix)})


class WindowsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.system32 = Path(tmp.name)

    def enum(self, keys, sub, slot="0000:01:00.0", hwid="VEN_10DE&DEV_2504", instance=None):
        bus, dev, fn = (int(part, 16) for part in slot.replace(".", ":").split(":")[1:])
        instance = instance or f"4&{sub}"
        keys[f"{WINDOWS_ENUM_PCI}\\{hwid}\\{instance}"] = {
            "Driver": "{4D36E968-E325-11CE-BFC1-08002BE10318}\\" + sub,
            "LocationInformation": f"PCI bus {bus}, device {dev}, function {fn}",
        }
        return f"PCI\\{hwid}\\{instance}"

    def detect(self, keys, dlls=(), env=None, smi=None, ram=16 * GIB, present=lambda _id: True):
        for dll in dlls:
            (self.system32 / dll).write_bytes(b"")
        calls = []

        def run(command):
            calls.append(list(command))
            return smi

        hw = detect_hardware(system="Windows", registry=FakeRegistry(keys), system32=self.system32,
                             env=env or {}, total_ram_bytes=ram, run=run, present=present)
        return hw, calls

    def cpu_keys(self, model, threads):
        return {f"{WINDOWS_CPU_KEY}\\{n}": {"ProcessorNameString": model + "  "} for n in range(threads)}

    def test_nvidia_cuda_with_64bit_vram(self):
        keys = self.cpu_keys("AMD Ryzen 5 5600X 6-Core Processor", 12)
        keys[f"{WINDOWS_DISPLAY_CLASS}\\0000"] = {
            "MatchingDeviceId": r"PCI\VEN_10DE&DEV_2504",
            "DriverDesc": "NVIDIA GeForce RTX 3060",
            "HardwareInformation.qwMemorySize": 12 * GIB,
        }
        keys[f"{WINDOWS_DISPLAY_CLASS}\\Properties"] = {}
        self.enum(keys, "0000")
        hw, calls = self.detect(keys, dlls=("nvcuda.dll", "vulkan-1.dll"), smi="")
        self.assertEqual(calls, [NVIDIA_SMI_QUERY])
        self.assertEqual(hw.os, "windows")
        self.assertEqual(hw.ram_mib, 16384)
        self.assertEqual((hw.cpu.model, hw.cpu.cores, hw.cpu.threads),
                         ("AMD Ryzen 5 5600X 6-Core Processor", None, 12))
        self.assertEqual(hw.compute_apis, ("cuda", "vulkan", "cpu"))
        gpu = hw.gpus[0]
        self.assertEqual((gpu.name, gpu.vendor, gpu.integrated, gpu.vram_mib),
                         ("NVIDIA GeForce RTX 3060", "NVIDIA", False, 12288))

    def test_legacy_32bit_vram_capped_at_4gib_is_unknown(self):
        keys = self.cpu_keys("x", 4)
        keys[f"{WINDOWS_DISPLAY_CLASS}\\0000"] = {
            "MatchingDeviceId": r"PCI\VEN_1002&DEV_73BF",
            "DriverDesc": "AMD Radeon RX 6800 XT",
            "HardwareInformation.MemorySize": (0xFFF00000).to_bytes(4, "little"),
        }
        keys[f"{WINDOWS_DISPLAY_CLASS}\\0001"] = {
            "MatchingDeviceId": r"PCI\VEN_1002&DEV_6FDF",
            "DriverDesc": "AMD Radeon RX 580",
            "HardwareInformation.MemorySize": 3 * GIB,
        }
        self.enum(keys, "0000", "0000:03:00.0", "VEN_1002&DEV_73BF")
        self.enum(keys, "0001", "0000:04:00.0", "VEN_1002&DEV_6FDF")
        hw, calls = self.detect(keys, env={"HIP_PATH": r"C:\AMD\ROCm\6.1"})
        self.assertEqual(calls, [], "nvidia-smi runs only with the NVIDIA driver installed")
        self.assertEqual([g.vram_mib for g in hw.gpus], [None, 3072])
        self.assertEqual(hw.compute_apis, ("rocm", "cpu"))

    def test_basic_display_adapter_is_not_a_gpu(self):
        keys = self.cpu_keys("x", 2)
        keys[f"{WINDOWS_DISPLAY_CLASS}\\0000"] = {
            "MatchingDeviceId": "ROOT\\BasicDisplay",
            "DriverDesc": "Microsoft Basic Display Adapter",
        }
        self.enum(keys, "0000", hwid="ROOT")
        hw, _ = self.detect(keys, dlls=("vulkan-1.dll",))
        self.assertEqual(hw.gpus, ())
        self.assertEqual(hw.compute_apis, ("cpu",))

    def nvidia(self, keys, sub, desc, vram):
        keys[f"{WINDOWS_DISPLAY_CLASS}\\{sub}"] = {
            "MatchingDeviceId": r"PCI\VEN_10DE&DEV_2504",
            "DriverDesc": desc,
            "HardwareInformation.qwMemorySize": vram,
        }

    def test_retired_adapter_is_not_listed_nor_cuda(self):
        keys = self.cpu_keys("x", 2)
        self.nvidia(keys, "0000", "NVIDIA GeForce RTX 3060", 12 * GIB)
        gone = self.enum(keys, "0000")
        hw, _ = self.detect(keys, dlls=("nvcuda.dll",), smi="", present=lambda i: i != gone)
        self.assertEqual(hw.gpus, ())
        self.assertNotIn("cuda", hw.compute_apis)

    def test_adapter_without_enum_instance_is_not_listed(self):
        keys = self.cpu_keys("x", 2)
        self.nvidia(keys, "0000", "NVIDIA GeForce RTX 3060", 12 * GIB)
        hw, _ = self.detect(keys, dlls=("nvcuda.dll",), smi="")
        self.assertEqual(hw.gpus, ())

    def test_same_name_gpus_match_smi_by_slot(self):
        keys = self.cpu_keys("x", 2)
        self.nvidia(keys, "0000", "NVIDIA GeForce RTX 3060", 1 * GIB)
        self.nvidia(keys, "0001", "NVIDIA GeForce RTX 3060", 1 * GIB)
        self.enum(keys, "0000", "0000:01:00.0")
        self.enum(keys, "0001", "0000:02:00.0")
        smi = ("00000000:01:00.0, NVIDIA GeForce RTX 3060, 8192\n"
               "00000000:02:00.0, NVIDIA GeForce RTX 3060, 12288\n")
        hw, _ = self.detect(keys, dlls=("nvcuda.dll",), smi=smi)
        self.assertEqual([g.vram_mib for g in hw.gpus], [8192, 12288])

    def test_smi_na_keeps_registry_vram(self):
        keys = self.cpu_keys("x", 2)
        self.nvidia(keys, "0000", "NVIDIA GeForce RTX 3060", 12 * GIB)
        self.enum(keys, "0000")
        hw, _ = self.detect(keys, dlls=("nvcuda.dll",), smi="00000000:01:00.0, NVIDIA GeForce RTX 3060, [N/A]\n")
        self.assertEqual(hw.gpus[0].vram_mib, 12288)

    def test_zero_vram_is_unknown(self):
        keys = self.cpu_keys("x", 2)
        keys[f"{WINDOWS_DISPLAY_CLASS}\\0000"] = {
            "MatchingDeviceId": r"PCI\VEN_1002&DEV_73BF", "DriverDesc": "AMD",
            "HardwareInformation.qwMemorySize": 0, "HardwareInformation.MemorySize": 0,
        }
        self.enum(keys, "0000", hwid="VEN_1002&DEV_73BF")
        self.assertIsNone(self.detect(keys)[0].gpus[0].vram_mib)

    def test_intel_arc_is_discrete(self):
        keys = self.cpu_keys("x", 2)
        keys[f"{WINDOWS_DISPLAY_CLASS}\\0000"] = {
            "MatchingDeviceId": r"PCI\VEN_8086&DEV_56A0", "DriverDesc": "Intel(R) Arc(TM) A770",
            "HardwareInformation.qwMemorySize": 16 * GIB,
        }
        self.enum(keys, "0000", hwid="VEN_8086&DEV_56A0")
        gpu = self.detect(keys)[0].gpus[0]
        self.assertEqual((gpu.integrated, gpu.vram_mib), (False, 16384))


class OtherSystemTest(unittest.TestCase):
    def test_unsupported_system_is_all_unknown(self):
        hw = detect_hardware(system="Darwin", run=lambda command: self.fail("no program runs"))
        self.assertEqual(hw.to_dict(), {"cpu": None, "ramMiB": None, "gpus": [], "computeApis": [], "os": None})


if __name__ == "__main__":
    unittest.main()
