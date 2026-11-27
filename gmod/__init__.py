"""Model Atlas: the catalog of local AI models, hardware detection and fit (stdlib only, no network)."""
from gmod.hardware import Cpu, Gpu, Hardware, detect_hardware

__all__ = ["Cpu", "Gpu", "Hardware", "detect_hardware"]
