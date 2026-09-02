# Local toolchain

`scripts/get_tools.sh` installs the pinned command-line toolchain below this directory.
Only this documentation, `versions.tsv` and `resources.tsv` are tracked; executables and
downloaded archives stay local. Add `tools/install/bin` to `PATH`, or use absolute paths.

```bash
./scripts/get_tools.sh
export PATH="$PWD/tools/install/bin:$PATH"
./scripts/get_tools.sh --check
```

The tracked TSV files are immutable lock manifests: installers verify every downloaded
archive against their pinned SHA-256 and never rewrite the expected value. The `--check`
mode verifies both the archives and installed versions. The installer does not use conda,
pip, or the system package manager.

VEP code is installed locally, while its large cache is managed by
`scripts/get_resources.sh`. The pinned Java runtime is private to this toolchain so GATK
and Nextflow do not depend on the machine's old system Java.
