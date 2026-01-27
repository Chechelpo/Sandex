from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen = True)
class ResourceSpec:
    max_cpu: int = 100

