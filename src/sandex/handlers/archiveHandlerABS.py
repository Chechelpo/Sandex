from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar
import shutil

from sandex.extract_policy import ExtractPolicy
from sandex.handlers.toolSpec import ToolSpec

class ArchiveHandler(ABC):
    _toolName: ClassVar[str]  # archive handlers must set
    _SUFFIXES: ClassVar[tuple[str, ...]] = ()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TOOLS:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def tool_name(cls) -> str:
        if not getattr(cls, "_toolName", None):
            raise NotImplementedError(f"{cls.__name__} must define _toolName")
        return cls._toolName

    @classmethod
    def tool_path(cls) -> Path:
        exe = shutil.which(cls.tool_name())
        if exe is None:
            raise FileNotFoundError(f"Required tool not found on PATH: {cls.tool_name()}")
        return Path(exe).resolve()

    @classmethod
    def getExtractorDirectory(cls) -> Path:
        return cls.tool_path().parent

    @abstractmethod
    def tool(self, archive: Path) -> ToolSpec: ...

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SUFFIXES:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @classmethod
    def _match_suffix(cls, filename: str) -> str | None:
        lower = filename.lower()
        for s in sorted(cls._SUFFIXES, key=len, reverse=True):
            if lower.endswith(s):
                return s
        return None

    def supports(self, archive: Path) -> bool:
        """
        Convenience default: suffix-based support check.
        Subclasses can use this directly, or override supports() for signature-based checks.
        """
        return self._match_suffix(archive.name) is not None

    def default_output_name(self, archive: Path) -> str:
        """
        Convenience default: remove the longest matching suffix.
        Falls back to archive.stem if no suffix matches.
        """
        name = archive.name
        s = self._match_suffix(name)
        if s is None:
            raise Exception("Unsupported default name")
        return name[: -len(s)]


    def policy(self) -> ExtractPolicy:
        return ExtractPolicy()
