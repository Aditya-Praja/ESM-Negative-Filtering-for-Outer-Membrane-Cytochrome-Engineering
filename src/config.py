"""Load the pre-registered config and refuse to run if it has drifted from its commit."""
from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "config" / "filter_v1.yaml"


def load(path: str | Path = DEFAULT) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def assert_config_committed(path: str | Path = DEFAULT) -> None:
    out = subprocess.run(["git", "status", "--porcelain", str(path)],
                         capture_output=True, text=True, cwd=ROOT).stdout.strip()
    if out:
        raise RuntimeError(f"{path} has uncommitted changes. Commit + tag before running.")
