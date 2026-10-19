"""Verify the public Automação release archive before publishing it."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


REQUIRED = {
    "automacao/__init__.py", "automacao/icone_motor.svg",
    "automacao/icone_cadeado_aberto.svg", "automacao/icone_cadeado_fechado.svg",
    "automacao/icone_passo_atras.svg", "automacao/icone_passo_frente.svg",
    "automacao/icone_pause.svg", "automacao/icone_play_reverso.svg",
    "automacao/icone_play.svg", "automacao/icone_stop.svg",
}

FORBIDDEN_PARTS = ("__pycache__", ".backup_", "automacao-debug.log")


def main() -> int:
    archive = Path(sys.argv[1] if len(sys.argv) > 1 else "ingetrazo-automacao-v1.0.0.zip")
    if not archive.is_file():
        print(f"MISSING_ARCHIVE: {archive}")
        return 2
    with zipfile.ZipFile(archive) as package:
        files = {name for name in package.namelist() if not name.endswith("/")}
        bad = sorted(name for name in files if any(part in name for part in FORBIDDEN_PARTS))
        missing = sorted(REQUIRED - files)
        extra = sorted(files - REQUIRED)
        source = package.read("automacao/__init__.py").decode("utf-8")
    compile(source, "automacao/__init__.py", "exec")
    if missing or bad or extra:
        print("PACKAGE_INVALID")
        if missing:
            print("MISSING:", *missing, sep="\n  ")
        if bad:
            print("FORBIDDEN:", *bad, sep="\n  ")
        if extra:
            print("EXTRA:", *extra, sep="\n  ")
        return 1
    print("PACKAGE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
