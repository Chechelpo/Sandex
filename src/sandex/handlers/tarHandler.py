from __future__ import annotations

from pathlib import Path

from sandex.handlers.archiveHandlerABS import ArchiveHandler
from sandex.handlers.toolSpec import ToolSpec


class TarHandler(ArchiveHandler):
    """
    TAR-family handler using bsdtar.
    Supports: .tar, .tar.gz, .tgz, .tar.bz2, .tbz2, .tar.xz, .txz, .tar.zst, .tzst
    """
    _toolName = "bsdtar"
    _SUFFIXES = (
        ".tar",
        ".tar.gz", ".tgz",
        ".tar.bz2", ".tbz2",
        ".tar.xz", ".txz",
        ".tar.zst", ".tzst",
    )
    @classmethod
    def tool(cls, archive: Path) -> ToolSpec:
        # The sandbox will bind the real archive to /in/archive
        return ToolSpec(argv=[f"{cls._toolName}", "-xf", "/in/archive"])
