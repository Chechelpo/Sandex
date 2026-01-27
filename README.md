## Sandex

CLI tool for extracting files in a sandbox.  
Only available for Linux.

---

### Dependencies

- **bubblewrap (`bwrap`)** — sandboxing  
  https://github.com/containers/bubblewrap

- **bsdtar** — ZIP and TAR extraction  
  https://github.com/libarchive/libarchive

- **unrar** — RAR extraction  
  https://github.com/aawc/unrar

---

### Sandbox configuration

For details on how the sandbox is configured, see `sandbox.py`.

Future versions will support:

- Sandboxing overrides
- Profile creation

---
## Usage

Basic extraction:

    sandex archive_path

Extracts the given archive into its parent directory.  
The extracted folder name defaults to the archive filename without its suffix.

Example:

    sandex samples.zip

---

Specify output directory:

    sandex archive_path --out output_directory

Example:

    sandex samples.tar.gz --out /tmp

---

Specify extracted folder name:

    sandex archive_path --name folder_name

Example:

    sandex samples.zip --name extracted_samples

---

Combine options:

    sandex archive_path --out output_directory --name folder_name

Example:

    sandex samples.rar --out /tmp --name test_run

---

Show version:

    sandex --version

---

Output

On success, sandex prints the full path of the final extraction directory to stdout.

On failure, a Python traceback is printed and the process exits with status code 1.

---

Exit codes

- 0 — success
- 1 — failure

---

Synopsis

    sandex [--version] ARCHIVE [--out DIR] [--name NAME]

Arguments

- ARCHIVE — path to archive file (required)
- --out — output directory (default: archive parent directory)
- --name — extracted folder name (default: archive name without suffix)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N01T3UQQ)
