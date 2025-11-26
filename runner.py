"""Runner for simstream package.

This script ensures `noVNC` is present inside the package folder and then
launches the bundled `start_server.sh`. If `noVNC` is missing it will
attempt to download the upstream `noVNC` master branch zip and extract it.

Installed as a console script `simstream-start`.
"""
import os
import sys
import stat
import shutil
import subprocess
from pathlib import Path


def ensure_novnc(pkg_dir: Path):
    """Ensure noVNC exists inside the package.

    The package now vendors the current `noVNC/` copy. If it's missing,
    instruct the user to reinstall or copy it into the package.
    """
    novnc_dir = pkg_dir / "noVNC"
    if not novnc_dir.exists():
        print("noVNC not found inside the packaged `simstream` directory.")
        print("Ensure you installed the package correctly or copy a local noVNC into:", novnc_dir)
        raise FileNotFoundError("vendored noVNC missing")


def main(argv=None):
    argv = argv or sys.argv[1:]
    pkg_dir = Path(__file__).resolve().parent

    # If there's a .fluxbox in the current working directory (dev mode), copy it into package
    cwd_fluxbox = Path.cwd() / ".fluxbox"
    if cwd_fluxbox.exists() and not (pkg_dir / ".fluxbox").exists():
        try:
            shutil.copytree(cwd_fluxbox, pkg_dir / ".fluxbox")
            print("Copied .fluxbox into package folder.")
        except Exception:
            pass

    ensure_novnc(pkg_dir)

    script = pkg_dir / "start_server.sh"
    if not script.exists():
        print("start_server.sh not found in package. Aborting.")
        sys.exit(1)

    # Ensure executable bit
    st = script.stat().st_mode
    script.chmod(st | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    env = os.environ.copy()
    env["SIMSTREAM_ROOT"] = str(pkg_dir)

    # Execute the script using bash so that the same behavior is preserved
    try:
        subprocess.check_call(["/bin/bash", str(script)], env=env)
    except subprocess.CalledProcessError as e:
        print("start_server.sh failed with exit code", e.returncode)
        raise


if __name__ == "__main__":
    main()
