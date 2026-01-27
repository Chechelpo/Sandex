from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExtractPolicy:
    deny_symlinks: bool = True
    deny_hardlinks: bool = True
    deny_special: bool = True
    deny_setid: bool = True


def validate_tree(root: Path, policy: ExtractPolicy) -> None:
    """
    Post-extraction validation (v1):
    - Reject symlinks (files and directories)
    - Reject hardlinks (nlink > 1) on regular files
    - Reject special files (fifo/socket/block/char)
    - Reject setuid/setgid bits
    - Optional caps (v2 knobs): max_files, max_total_bytes, max_file_bytes
    """
    files = 0
    total_bytes = 0

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dp = Path(dirpath)

        # Reject symlinked directories explicitly
        if policy.deny_symlinks:
            for d in list(dirnames):
                p = dp / d
                st = os.lstat(p)
                if stat.S_ISLNK(st.st_mode):
                    raise RuntimeError(f"Symlinked directory not allowed: {p}")

        for f in filenames:
            p = dp / f
            st = os.lstat(p)
            mode = st.st_mode

            if policy.deny_symlinks and stat.S_ISLNK(mode):
                raise RuntimeError(f"Symlink not allowed: {p}")

            if policy.deny_special and (
                stat.S_ISCHR(mode)
                or stat.S_ISBLK(mode)
                or stat.S_ISFIFO(mode)
                or stat.S_ISSOCK(mode)
            ):
                raise RuntimeError(f"Special file not allowed: {p}")

            if policy.deny_setid and ((mode & stat.S_ISUID) or (mode & stat.S_ISGID)):
                raise RuntimeError(f"setuid/setgid not allowed: {p}")

            if policy.deny_hardlinks and stat.S_ISREG(mode) and st.st_nlink > 1:
                raise RuntimeError(f"Hardlink not allowed: {p} (nlink={st.st_nlink})")
