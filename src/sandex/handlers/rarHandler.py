from __future__ import annotations

from pathlib import Path
import shutil

from sandex.handlers.archiveHandlerABS import ArchiveHandler
from sandex.handlers.toolSpec import ToolSpec

class RarHandler(ArchiveHandler):
    _toolName = "unrar"
    _SUFFIXES = (".rar")

    @classmethod
    def tool(cls, archive: Path) -> ToolSpec:
        return ToolSpec(argv=[
            f"{cls._toolName}",
            "x",          # extract with full paths
            "-idq",       # quiet
            "-o-",        # do not overwrite existing files
            "-p-",        # do not prompt for password (fail if encrypted)
            "/in/archive",
            "/out/",
        ])

