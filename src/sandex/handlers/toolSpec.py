from dataclasses import dataclass

@dataclass(frozen=True)
class ToolSpec:
    argv: list[str]              # command executed inside sandbox
