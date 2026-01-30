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
### Installation
1. Ensure that you have the dependencies listed earlier
2. Download a wheel from releases.
3. Run
`python -m installer --prefix="$HOME/.local" <path to wheel>`
  to install as user (no need for SUDO)
4. Follow the usage guide below to start extracting files

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

---

### Sandbox configuration
All of the following points apply to the sandbox defaults
  1. `unshare-net` : Creates a new network namespace, isolating the process from the host's one. Because no other network is provided the process cannot access the internet.
  2. `unshare-pid` : Creates a new process namespace, preventing the sandbox from seeing host processes.
  3. `die-with-parent` : Ensures process tree is killed if parent dies. Prevents orphaned sandbox processes.
  4. `ro-bind` : Both the archive to extract and needed binaries (/usr, /bin, /lib, ... ) are mounted as read only, preventing writes to those paths while allowing execution of tools.
  5. `bind` : Allows only writes to the extraction directory.
These are some of the flags, for more details on how the sandbox is configured, see `sandbox.py`.
#### Why?
Extracting untrusted files is always unsafe, sandex is a way to limit the blast radius.
Here are some examples of relevant security vulnerabilities of extractors:
  1. CVE-2025-45582 GNU Tar 1.35: Attackers were able to write to critical system files via symlinks, after the user extracts a tar.
     https://nvd.nist.gov/vuln/detail/CVE-2025-45582
  2. CVE-2025-55188 7Zip : Same symlink things.
     https://nvd.nist.gov/vuln/detail/CVE-2025-55188
<p>Issues with extractors usually involve Zip slips, which should (in theory) be prevented with sandex's sandboxing.</p>

Future versions will support:

- Sandboxing overrides
- Profile creation


[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N01T3UQQ)
