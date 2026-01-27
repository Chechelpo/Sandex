# Orchestrator of both extraction and sandboxing.
# For extraction: Pick Handler
#
import os
import secrets
import subprocess
from pathlib import Path
import shutil

from sandex.sandbox import SandboxBuilder,SandboxSpec
from sandex.extract_policy import validate_tree
from sandex.handlers.archiveHandlerABS import ArchiveHandler
from sandex.handlers.pickHandler import Pick_handler
from sandex.extractor import File_dirs,make_staging,commit_staging

def run(file_config: File_dirs) -> Path:
    if not file_config.archive.is_file():
        raise RuntimeError(f"archive not found: {file_config.archive}")

    file_config.out_base.mkdir(parents=True, exist_ok=True)
    if not os.access(file_config.out_base, os.W_OK):
        raise RuntimeError(f"output base not writable: {file_config.out_base}")

    handler = Pick_handler(file_config.archive)

    staging = make_staging(file_config)
    committed = False

    try:
        sb = SandboxBuilder()
        tool = handler.tool(file_config.archive)
        spec = SandboxSpec(
            archive_path=file_config.archive,
            out_dir=staging,
        )
        cmd = sb.build(spec, tool)

        r = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(
                f"extraction failed (rc={r.returncode}):\n{r.stderr}"
            )

        policy = handler.policy()
        validate_tree(staging, policy)

        if file_config.name is None:
            file_config.name = handler.default_output_name(
                file_config.archive
            )

        final_dir = commit_staging(staging, file_config)
        committed = True
        return final_dir

    finally:
        # If we did not commit, staging must die
        if not committed:
            staging_parent = staging.parent
            try:
                shutil.rmtree(staging_parent)
            except FileNotFoundError:
                pass

