"""Hardware detection for Embedder (simplified from LocalMind)."""

import logging
import os
import platform
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

logger = logging.getLogger(__name__)


class AcceleratorType(Enum):
    NVIDIA_CUDA = "nvidia_cuda"
    CPU = "cpu"


@dataclass
class CPUInfo:
    name: str = ""
    total_cores: int = 1


@dataclass
class GPUInfo:
    name: str = ""
    accelerator: AcceleratorType = AcceleratorType.CPU
    vram_gb: float = 0.0
    is_available: bool = False
    supports_fp16: bool = False


@dataclass
class HardwareReport:
    cpu: CPUInfo
    primary_gpu: GPUInfo
    device_override: str | None = None


def detect_cpu() -> CPUInfo:
    info = CPUInfo()
    info.total_cores = os.cpu_count() or 1
    info.name = platform.processor() or "Unknown CPU"
    return info


def detect_nvidia_gpu() -> GPUInfo | None:
    try:
        import torch
        if not torch.cuda.is_available():
            return None
            
        device_id = 0
        props = torch.cuda.get_device_properties(device_id)
        
        return GPUInfo(
            name=props.name,
            accelerator=AcceleratorType.NVIDIA_CUDA,
            vram_gb=props.total_memory / (1024**3),
            is_available=True,
            supports_fp16=props.major >= 7,
        )
    except ImportError:
        return None
    except Exception as e:
        logger.debug(f"GPU detection failed: {e}")
        return None


@lru_cache(maxsize=1)
def detect_hardware() -> HardwareReport:
    cpu = detect_cpu()
    gpu = detect_nvidia_gpu()
    
    if gpu:
        return HardwareReport(cpu=cpu, primary_gpu=gpu)
    
    return HardwareReport(
        cpu=cpu, 
        primary_gpu=GPUInfo(is_available=False)
    )
