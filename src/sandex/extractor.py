from __future__ import annotations

import secrets
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class File_dirs:
    archive: Path
    name: str | None
    out_base: Path
    # out_path = base output directory (NOT including final folder name)


# ---------- staging lifecycle ----------

def make_staging(config: File_dirs) -> Path:
    """
    Create and return a unique staging root directory:
        <out_path>/.sandex-staging-<token>/root
    """
    if config.out_base is None:
        raise ValueError("out_path must be set before creating staging")

    token = secrets.token_hex(8)
    base = config.out_base / f".sandex-staging-{token}"
    root = base / "root"

    base.mkdir(parents=True, exist_ok=False)
    root.mkdir(parents=True, exist_ok=False)

    return root


def commit_staging(staging_root: Path, config: File_dirs) -> Path:
    """
    Atomically move staging_root to its final location:
        <out_path>/<name>

    Assumes:
    - staging_root exists
    - config.name is resolved
    """
    if config.out_base is None:
        raise ValueError("out_path must be set before committing")

    if config.name is None:
        raise ValueError("name must be set before committing")

    final_dir = (config.out_base / config.name).resolve()

    if final_dir.exists():
        raise RuntimeError(f"final directory already exists: {final_dir}")

    # Atomic rename (same filesystem)
    staging_root.rename(final_dir)

    # Best-effort cleanup of .sandex-staging-<token>
    staging_parent = staging_root.parent
    try:
        staging_parent.rmdir()
    except OSError:
        pass

    return final_dir
