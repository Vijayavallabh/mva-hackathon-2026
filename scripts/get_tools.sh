#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TOOLS="$ROOT/tools"
SRC="$TOOLS/src"
PREFIX="$TOOLS/install"
DOWNLOADS="$TOOLS/downloads"
MANIFEST="$TOOLS/versions.tsv"
JOBS=${MVA_BUILD_JOBS:-8}

HTS_VERSION=1.24
BWA_VERSION=2.2.1
PIGZ_VERSION=2.8
VEP_VERSION=116.0
GATK_VERSION=4.7.0.0
NEXTFLOW_VERSION=26.04.6
JAVA_VERSION=17.0.20.1+1
DELLY_VERSION=2.1.0

mkdir -p "$SRC" "$PREFIX/bin" "$DOWNLOADS"

locked() {
  local component=$1 column=$2
  awk -F '\t' -v component="$component" -v column="$column" \
    '$1 == component { print $column; found=1 } END { exit !found }' "$MANIFEST"
}

verify_sha256() {
  local component=$1 path=$2 expected
  expected=$(locked "$component" 4)
  printf '%s  %s\n' "$expected" "$path" | sha256sum --check --status || {
    echo "checksum mismatch: ${path#$ROOT/} ($component)" >&2
    return 1
  }
}

download() {
  local component=$1 url=$2 dest=$3
  local marker="$dest.complete"
  if [[ -s "$dest" ]] && verify_sha256 "$component" "$dest"; then
    touch "$marker"
    return
  fi
  if [[ -f "$marker" ]]; then
    echo "discarding corrupt completed download: ${dest#$ROOT/}" >&2
    rm -f "$marker" "$dest"
  fi
  if [[ ! -f "$marker" ]]; then
    curl --fail --location --retry 5 --continue-at - --output "$dest" "$url"
    if ! verify_sha256 "$component" "$dest"; then
      rm -f "$dest"
      return 1
    fi
    touch "$marker"
  fi
}

extract_once() {
  local archive=$1 dest=$2
  [[ -d "$dest" ]] && return 0
  mkdir -p "$dest"
  case "$archive" in
    *.tar.bz2) tar -xjf "$archive" --strip-components=1 -C "$dest" ;;
    *.tar.gz) tar -xzf "$archive" --strip-components=1 -C "$dest" ;;
    *.zip) unzip -q "$archive" -d "$SRC" ;;
    *) echo "unsupported archive: $archive" >&2; return 1 ;;
  esac
}

check_tools() {
  local failed=0 cmd output delly_output
  export PATH="$PREFIX/bin:$PATH"
  export JAVA_CMD="$PREFIX/bin/java"
  for cmd in bcftools samtools bgzip tabix bwa-mem2 pigz vep gatk nextflow java delly; do
    if [[ ! -x "$PREFIX/bin/$cmd" ]]; then
      echo "missing: tools/install/bin/$cmd" >&2
      failed=1
    fi
  done
  (( failed == 0 )) || return 1
  verify_sha256 samtools+htslib "$DOWNLOADS/samtools-$HTS_VERSION.tar.bz2"
  verify_sha256 bcftools "$DOWNLOADS/bcftools-$HTS_VERSION.tar.bz2"
  verify_sha256 bwa-mem2 "$DOWNLOADS/bwa-mem2-$BWA_VERSION.tar.bz2"
  verify_sha256 pigz "$DOWNLOADS/pigz-$PIGZ_VERSION.tar.gz"
  verify_sha256 Temurin-JRE "$DOWNLOADS/OpenJDK17U-jre_x64_linux_hotspot_17.0.20.1_1.tar.gz"
  verify_sha256 GATK "$DOWNLOADS/gatk-$GATK_VERSION.zip"
  verify_sha256 Nextflow "$DOWNLOADS/nextflow-$NEXTFLOW_VERSION-dist"
  verify_sha256 Ensembl-VEP "$DOWNLOADS/ensembl-vep-$VEP_VERSION.tar.gz"
  verify_sha256 cpanminus "$DOWNLOADS/App-cpanminus-1.7048.tar.gz"
  verify_sha256 Exporter-Tiny "$DOWNLOADS/Exporter-Tiny-1.006003.tar.gz"
  verify_sha256 List-MoreUtils "$DOWNLOADS/List-MoreUtils-0.430.tar.gz"
  verify_sha256 VEP-HTSlib "$DOWNLOADS/htslib-1.9.tar.bz2"
  verify_sha256 Bio-DB-HTS "$DOWNLOADS/Bio-DB-HTS-2.11.tar.gz"
  verify_sha256 DELLY "$DOWNLOADS/delly-v$DELLY_VERSION-linux-amd64"
  [[ $("$PREFIX/bin/bcftools" --version | head -1) == "bcftools $HTS_VERSION" ]]
  [[ $("$PREFIX/bin/samtools" --version | head -1) == "samtools $HTS_VERSION" ]]
  "$PREFIX/bin/tabix" --version 2>&1 | head -1 | rg -q "htslib\) $HTS_VERSION$"
  [[ $("$PREFIX/bin/bwa-mem2" version 2>&1 | tail -1) == "$BWA_VERSION" ]]
  [[ $("$PREFIX/bin/pigz" --version 2>&1) == "pigz $PIGZ_VERSION" ]]
  "$PREFIX/bin/vep" --help 2>&1 | rg -q "ensembl-vep[[:space:]]+: $VEP_VERSION$"
  "$PREFIX/bin/gatk" --version 2>&1 | rg -q "GATK\) v$GATK_VERSION$"
  NXF_HOME="$TOOLS/nextflow-home" "$PREFIX/bin/nextflow" -version | rg -q "version $NEXTFLOW_VERSION build"
  "$PREFIX/bin/java" -version 2>&1 | head -1 | rg -q "\"${JAVA_VERSION%%+*}\""
  delly_output=$("$PREFIX/bin/delly" --version 2>&1)
  rg -q "^Delly version: v$DELLY_VERSION$" <<<"$delly_output"
  "$PREFIX/bin/bcftools" --version | head -1
  "$PREFIX/bin/samtools" --version | head -1
  "$PREFIX/bin/tabix" --version 2>&1 | head -1
  "$PREFIX/bin/bwa-mem2" version 2>&1 | tail -1
  "$PREFIX/bin/pigz" --version 2>&1
  "$PREFIX/bin/vep" --help >/dev/null
  "$PREFIX/bin/gatk" --version 2>&1 | tail -1
  NXF_HOME="$TOOLS/nextflow-home" "$PREFIX/bin/nextflow" -version | rg 'version' | head -1
  "$PREFIX/bin/java" -version 2>&1 | head -1
  printf 'Delly %s\n' "$DELLY_VERSION"
}

if [[ ${1:-} == "--check" ]]; then
  check_tools
  exit
fi
if [[ $# -ne 0 ]]; then
  echo "usage: $0 [--check]" >&2
  exit 2
fi

SAMTOOLS_ARCHIVE="$DOWNLOADS/samtools-$HTS_VERSION.tar.bz2"
BCFTOOLS_ARCHIVE="$DOWNLOADS/bcftools-$HTS_VERSION.tar.bz2"
download samtools+htslib "https://github.com/samtools/samtools/releases/download/$HTS_VERSION/samtools-$HTS_VERSION.tar.bz2" "$SAMTOOLS_ARCHIVE"
download bcftools "https://github.com/samtools/bcftools/releases/download/$HTS_VERSION/bcftools-$HTS_VERSION.tar.bz2" "$BCFTOOLS_ARCHIVE"
extract_once "$SAMTOOLS_ARCHIVE" "$SRC/samtools-$HTS_VERSION"
extract_once "$BCFTOOLS_ARCHIVE" "$SRC/bcftools-$HTS_VERSION"
if [[ ! -x "$PREFIX/bin/samtools" ]]; then
  if [[ ! -f "$SRC/samtools-$HTS_VERSION/config.status" ]]; then
    (cd "$SRC/samtools-$HTS_VERSION/htslib-$HTS_VERSION" && ./configure --prefix="$PREFIX" --disable-bz2 --disable-lzma)
    (cd "$SRC/samtools-$HTS_VERSION" && ./configure --prefix="$PREFIX" --without-curses --with-htslib="htslib-$HTS_VERSION")
  fi
  make -C "$SRC/samtools-$HTS_VERSION" -j"$JOBS"
  make -C "$SRC/samtools-$HTS_VERSION" install prefix="$PREFIX"
fi
if [[ ! -x "$PREFIX/bin/bcftools" ]]; then
  if [[ ! -f "$SRC/bcftools-$HTS_VERSION/config.status" ]]; then
    (cd "$SRC/bcftools-$HTS_VERSION/htslib-$HTS_VERSION" && ./configure --prefix="$PREFIX" --disable-bz2 --disable-lzma)
    (cd "$SRC/bcftools-$HTS_VERSION" && ./configure --prefix="$PREFIX" --with-htslib="htslib-$HTS_VERSION")
  fi
  make -C "$SRC/bcftools-$HTS_VERSION" -j"$JOBS"
  make -C "$SRC/bcftools-$HTS_VERSION" install prefix="$PREFIX"
fi
if [[ ! -x "$PREFIX/bin/bgzip" || ! -x "$PREFIX/bin/tabix" ]]; then
  make -C "$SRC/samtools-$HTS_VERSION/htslib-$HTS_VERSION" -j"$JOBS" bgzip tabix
  install -m 0755 "$SRC/samtools-$HTS_VERSION/htslib-$HTS_VERSION/bgzip" "$PREFIX/bin/bgzip"
  install -m 0755 "$SRC/samtools-$HTS_VERSION/htslib-$HTS_VERSION/tabix" "$PREFIX/bin/tabix"
fi

BWA_ARCHIVE="$DOWNLOADS/bwa-mem2-$BWA_VERSION.tar.bz2"
download bwa-mem2 "https://github.com/bwa-mem2/bwa-mem2/releases/download/v$BWA_VERSION/bwa-mem2-${BWA_VERSION}_x64-linux.tar.bz2" "$BWA_ARCHIVE"
extract_once "$BWA_ARCHIVE" "$SRC/bwa-mem2-$BWA_VERSION"
if [[ ! -x "$PREFIX/bin/bwa-mem2" ]]; then
  for executable in "$SRC/bwa-mem2-$BWA_VERSION"/bwa-mem2*; do
    [[ -f "$executable" && -x "$executable" ]] || continue
    install -m 0755 "$executable" "$PREFIX/bin/$(basename "$executable")"
  done
fi

PIGZ_ARCHIVE="$DOWNLOADS/pigz-$PIGZ_VERSION.tar.gz"
download pigz "https://github.com/madler/pigz/archive/refs/tags/v$PIGZ_VERSION.tar.gz" "$PIGZ_ARCHIVE"
extract_once "$PIGZ_ARCHIVE" "$SRC/pigz-$PIGZ_VERSION"
if [[ ! -x "$PREFIX/bin/pigz" ]]; then
  make -C "$SRC/pigz-$PIGZ_VERSION" -j"$JOBS"
  install -m 0755 "$SRC/pigz-$PIGZ_VERSION/pigz" "$PREFIX/bin/pigz"
  ln -sfn pigz "$PREFIX/bin/unpigz"
fi

JAVA_ARCHIVE="$DOWNLOADS/OpenJDK17U-jre_x64_linux_hotspot_17.0.20.1_1.tar.gz"
download Temurin-JRE "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.20.1%2B1/OpenJDK17U-jre_x64_linux_hotspot_17.0.20.1_1.tar.gz" "$JAVA_ARCHIVE"
extract_once "$JAVA_ARCHIVE" "$TOOLS/java"
ln -sfn "$TOOLS/java/bin/java" "$PREFIX/bin/java"

GATK_ARCHIVE="$DOWNLOADS/gatk-$GATK_VERSION.zip"
download GATK "https://github.com/broadinstitute/gatk/releases/download/$GATK_VERSION/gatk-$GATK_VERSION.zip" "$GATK_ARCHIVE"
if [[ ! -d "$SRC/gatk-$GATK_VERSION" ]]; then
  unzip -q "$GATK_ARCHIVE" -d "$SRC"
fi
cat > "$PREFIX/bin/gatk" <<EOF
#!/usr/bin/env bash
export PATH="$PREFIX/bin:\$PATH"
exec "$SRC/gatk-$GATK_VERSION/gatk" "\$@"
EOF
chmod 0755 "$PREFIX/bin/gatk"

DELLY_ASSET="$DOWNLOADS/delly-v$DELLY_VERSION-linux-amd64"
download DELLY \
  "https://github.com/dellytools/delly/releases/download/v$DELLY_VERSION/delly-v$DELLY_VERSION-linux-amd64" \
  "$DELLY_ASSET"
install -m 0755 "$DELLY_ASSET" "$PREFIX/bin/delly"

NEXTFLOW_ASSET="$DOWNLOADS/nextflow-$NEXTFLOW_VERSION-dist"
download Nextflow "https://github.com/nextflow-io/nextflow/releases/download/v$NEXTFLOW_VERSION/nextflow-$NEXTFLOW_VERSION-dist" "$NEXTFLOW_ASSET"
install -m 0755 "$NEXTFLOW_ASSET" "$TOOLS/nextflow"
cat > "$PREFIX/bin/nextflow" <<EOF
#!/usr/bin/env bash
export JAVA_CMD="$PREFIX/bin/java"
export NXF_HOME="$TOOLS/nextflow-home"
exec "$TOOLS/nextflow" "\$@"
EOF
chmod 0755 "$PREFIX/bin/nextflow"

VEP_ARCHIVE="$DOWNLOADS/ensembl-vep-$VEP_VERSION.tar.gz"
download Ensembl-VEP "https://github.com/Ensembl/ensembl-vep/archive/refs/tags/release/$VEP_VERSION.tar.gz" "$VEP_ARCHIVE"
extract_once "$VEP_ARCHIVE" "$TOOLS/vep"
CPANM_ARCHIVE="$DOWNLOADS/App-cpanminus-1.7048.tar.gz"
download cpanminus "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.7048.tar.gz" "$CPANM_ARCHIVE"
extract_once "$CPANM_ARCHIVE" "$SRC/App-cpanminus-1.7048"
EXPORTER_ARCHIVE="$DOWNLOADS/Exporter-Tiny-1.006003.tar.gz"
MOREUTILS_ARCHIVE="$DOWNLOADS/List-MoreUtils-0.430.tar.gz"
download Exporter-Tiny "https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.006003.tar.gz" "$EXPORTER_ARCHIVE"
download List-MoreUtils "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-0.430.tar.gz" "$MOREUTILS_ARCHIVE"
if [[ ! -f "$TOOLS/perl5/lib/perl5/List/MoreUtils.pm" ]]; then
  PERL5LIB="$TOOLS/perl5/lib/perl5${PERL5LIB:+:$PERL5LIB}" perl "$SRC/App-cpanminus-1.7048/bin/cpanm" \
    --notest --local-lib-contained "$TOOLS/perl5" \
    "$EXPORTER_ARCHIVE" "$MOREUTILS_ARCHIVE"
fi
if [[ ! -f "$TOOLS/vep/Bio/EnsEMBL/Registry.pm" ]]; then
  (cd "$TOOLS/vep" && \
    PERL5LIB="$TOOLS/perl5/lib/perl5${PERL5LIB:+:$PERL5LIB}" \
    perl INSTALL.pl --AUTO a --NO_UPDATE --NO_HTSLIB --DESTDIR "$TOOLS/vep")
fi
VEP_HTSLIB_ARCHIVE="$DOWNLOADS/htslib-1.9.tar.bz2"
download VEP-HTSlib "https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2" "$VEP_HTSLIB_ARCHIVE"
extract_once "$VEP_HTSLIB_ARCHIVE" "$SRC/htslib-1.9"
if [[ ! -f "$SRC/htslib-1.9/libhts.a" ]]; then
  (cd "$SRC/htslib-1.9" && CFLAGS='-O2 -fPIC' ./configure --disable-bz2 --disable-lzma --without-libdeflate)
  make -C "$SRC/htslib-1.9" -j"$JOBS" lib-static
fi
BIO_DB_HTS_ARCHIVE="$DOWNLOADS/Bio-DB-HTS-2.11.tar.gz"
download Bio-DB-HTS "https://github.com/Ensembl/Bio-DB-HTS/archive/refs/tags/2.11.tar.gz" "$BIO_DB_HTS_ARCHIVE"
if [[ ! -f "$TOOLS/perl5/lib/perl5/x86_64-linux-gnu-thread-multi/Bio/DB/HTS/Tabix.pm" ]]; then
  HTSLIB_DIR="$SRC/htslib-1.9" \
    PERL5LIB="$TOOLS/perl5/lib/perl5:$TOOLS/vep:$TOOLS/vep/Bio" \
    perl "$SRC/App-cpanminus-1.7048/bin/cpanm" --notest --local-lib "$TOOLS/perl5" \
    "$BIO_DB_HTS_ARCHIVE"
fi
if ! head -1 "$TOOLS/vep/vep" | grep -q 'perl'; then
  tar -xzf "$VEP_ARCHIVE" --strip-components=1 -C "$TOOLS/vep" "ensembl-vep-release-$VEP_VERSION/vep"
fi
if [[ -L "$PREFIX/bin/vep" ]]; then
  unlink "$PREFIX/bin/vep"
fi
cat > "$PREFIX/bin/vep" <<EOF
#!/usr/bin/env bash
export PERL5LIB="$TOOLS/perl5/lib/perl5:$TOOLS/vep:$TOOLS/vep/Bio${PERL5LIB:+:$PERL5LIB}"
exec perl "$TOOLS/vep/vep" "\$@"
EOF
chmod 0755 "$PREFIX/bin/vep"

check_tools
echo "toolchain ready: $PREFIX/bin"
