from __future__ import annotations

from pathlib import Path

from sandex.handlers.archiveHandlerABS import ArchiveHandler
from sandex.handlers.toolSpec import ToolSpec


class ZipHandler(ArchiveHandler):
    """ZIP handler using bsdtar."""
    _toolName = "bsdtar"
    _SUFFIXES = (".zip")

    @classmethod
    def tool(cls, archive: Path) -> ToolSpec:
        return ToolSpec(argv=[f"{cls._toolName}", "-xf", "/in/archive"])
