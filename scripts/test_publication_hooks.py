"""Exercise actual startup hook installation in isolated, subject-free repositories."""

from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main():
    startup = (ROOT / "init.sh").read_text()
    hook_section = startup.split('echo "=== 2. no subject data in git ==="', 1)[1]
    hook_section = hook_section.split('echo "=== 3. verify_data self-check ==="', 1)[0]
    for kind in ("absent", "unrelated", "dangling", "nonexecutable"):
        with tempfile.TemporaryDirectory(prefix="publication-hook-") as name:
            repo = Path(name)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            (repo / "scripts").mkdir()
            gate = repo / "scripts/no_data_in_git.sh"
            shutil.copy2(ROOT / "scripts/no_data_in_git.sh", gate)
            gate.chmod(0o755)
            hook = repo / ".git/hooks/pre-commit"
            if kind == "unrelated":
                hook.write_text("#!/bin/sh\nexit 0\n")
                hook.chmod(0o755)
            elif kind == "dangling":
                hook.symlink_to(repo / "missing-hook")
            elif kind == "nonexecutable":
                gate.chmod(0o644)
                hook.symlink_to(gate)
            result = subprocess.run(["bash", "-c", "set -euo pipefail\n" + hook_section],
                                    cwd=repo, capture_output=True)
            assert (result.returncode == 0) == (kind == "absent"), kind
            if kind == "absent":
                assert hook.resolve() == gate
                assert subprocess.run([str(hook)], cwd=repo, capture_output=True).returncode == 0
            elif kind == "unrelated":
                assert hook.read_text() == "#!/bin/sh\nexit 0\n"
            elif kind == "dangling":
                assert hook.is_symlink() and not hook.exists()
    print("publication hooks: installation, invocation and incompatible-hook rejection pass")


if __name__ == "__main__":
    main()
