#!/usr/bin/env python3
"""Stage an authorized native ARC-AGI-3 research experiment without publishing game assets.

Only copies owner-held archives and repo-authored scripts; no SDK calls are made.
Run the staged prepare_runtime.py separately after reviewing permissions.
"""
from __future__ import annotations
import argparse
import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N100_SHA256 = "b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888"
FROZEN_SHA256 = "cfcb4c5c82a17d860aa8affe06f6a6611496f5aad856a16a062ed48f20c484bc"
SOURCE_SHA256 = "e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d"
NOTEBOOK_SHA256 = "1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify(path, expected):
    if not path.is_file():
        raise SystemExit(f"Missing archive: {path}")
    actual = sha256(path)
    if actual != expected:
        raise SystemExit(f"Archive checksum mismatch: {path}: {actual}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--experiment", choices=("N114", "N117"), default="N114")
    p.add_argument("--n100-runtime", required=True, type=Path)
    p.add_argument("--frozen-release", required=True, type=Path)
    p.add_argument("--destination", required=True, type=Path)
    args = p.parse_args()

    verify(args.n100_runtime, N100_SHA256)
    verify(args.frozen_release, FROZEN_SHA256)
    source_py = ROOT / "src/baselines/frozen_n093.py"
    source_nb = ROOT / "notebooks/frozen_n093_submission.ipynb"
    verify(source_py, SOURCE_SHA256)
    verify(source_nb, NOTEBOOK_SHA256)
    with zipfile.ZipFile(args.frozen_release) as z:
        for name, local in (("submission.py", source_py), ("submission.ipynb", source_nb)):
            if z.read(name) != local.read_bytes():
                raise SystemExit(f"Frozen release differs from original {name}")

    dest = args.destination.resolve()
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"Destination is not empty: {dest}")
    shutil.copytree(ROOT / "experiments" / args.experiment, dest, dirs_exist_ok=True)
    inputs = dest / "inputs"
    inputs.mkdir(exist_ok=True)
    shutil.copyfile(args.n100_runtime, inputs / "N100_ACTIVE_FSM_20261025.zip")
    shutil.copyfile(args.frozen_release, inputs / "FROZEN_B1_PRETRAINED_PUCT_KAGGLE_20261025.zip")
    shutil.copyfile(source_py, inputs / "submission.py")
    shutil.copyfile(source_nb, inputs / "submission.ipynb")
    print("Staged", args.experiment, "at", dest)
    print("This has NOT run any SDK actions or reproduced original results.")
    print("Next commands:")
    print("cd", dest)
    print("python3 prepare_runtime.py")
    if args.experiment == "N114":
        print("python3 run_public_games.py --families vc33 --output-dir reproduction/smoke")
        print("python3 run_all_isolated.py --output-dir results --timeout-seconds 90")
        print("python3 verify_release.py")
    else:
        print("python3 run_native.py --arm baseline --families vc33")
        print("python3 run_native.py --arm local --families vc33")
        print("python3 verify_replay.py results/local/vc33.json")
    print("All SDK calls are charged; public layouts have been historically exposed.")


if __name__ == "__main__":
    main()
