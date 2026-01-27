from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence

from sandex.handlers.toolSpec import ToolSpec


@dataclass(frozen=True)
class SandboxSpec:
    """
    bwrap configuration.
    """
    archive_path: Path
    out_dir: Path                     # staging root
    workdir: str = "/out"

    ro_binds: Sequence[tuple[Path, str]] = field(default_factory=tuple)
    extra_args: Sequence[str] = field(default_factory=tuple)
    env: Mapping[str, str] = field(default_factory=dict)


class SandboxBuilder:
    def __init__(self) -> None:
        if shutil.which("bwrap") is None:
            raise RuntimeError("bwrap not found on PATH")

    def build(self, spec: SandboxSpec, tool: ToolSpec) -> list[str]:
        archive = spec.archive_path.resolve()
        out_dir = spec.out_dir.resolve()

        baseline_ro = [
            (Path("/usr"), "/usr"),
            (Path("/lib"), "/lib"),
            (Path("/lib64"), "/lib64"),
            (Path("/bin"), "/bin"),
        ]
        ro = baseline_ro + list(spec.ro_binds)

        env = {
            "HOME": "/nonexistent",
            "TMPDIR": "/tmp",
            "PATH": "/usr/bin:/bin",
            "LANG": "C",
            "LC_ALL": "C",
            **dict(spec.env),
        }

        cmd = [
            "bwrap",
            "--die-with-parent",
            "--new-session",
            "--unshare-user",
            "--unshare-pid",
            "--unshare-net",
            "--unshare-ipc",
            "--unshare-uts",
            "--dev", "/dev",
            "--proc", "/proc",

            "--ro-bind", str(archive), "/in/archive",
            "--bind", str(out_dir), "/out",
            "--tmpfs", "/tmp",
        ]

        for host, guest in ro:
            cmd += ["--ro-bind", str(host), guest]

        cmd += ["--chdir", spec.workdir]

        cmd += ["--clearenv"]
        for k, v in env.items():
            cmd += ["--setenv", k, v]

        cmd += list(spec.extra_args)
        cmd += ["--"] + tool.argv
        return cmd
