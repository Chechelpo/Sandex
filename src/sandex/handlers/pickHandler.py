from __future__ import annotations

from pathlib import Path

from sandex.handlers.archiveHandlerABS import ArchiveHandler
from sandex.handlers.tarHandler import TarHandler
from sandex.handlers.zipHandler import ZipHandler
from sandex.handlers.rarHandler import RarHandler

_HANDLERS: list[ArchiveHandler] = [
    ZipHandler(),
    TarHandler(),
    RarHandler()
]

def Pick_handler(archive:Path) -> ArchiveHandler:
    for handler in _HANDLERS:
        if (handler.supports(archive)):
            return handler

    raise RuntimeError(f"Unsupported file: {archive}")
