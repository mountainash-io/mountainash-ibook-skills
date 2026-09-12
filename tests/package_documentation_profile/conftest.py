import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def skill_root() -> Path:
    return Path(__file__).parents[2] / "skills" / "package-documentation-profile"


@pytest.fixture
def protocol_root(skill_root: Path) -> Path:
    return skill_root / "references" / "protocol"


@pytest.fixture
def profile_fixture() -> Path:
    return Path(__file__).parent / "fixtures" / "valid-profile"


@pytest.fixture
def load_json():
    def _load(path: Path):
        return json.loads(path.read_text())

    return _load


@pytest.fixture
def write_json():
    def _write(path: Path, value):
        path.write_text(json.dumps(value, indent=2) + "\n")

    return _write


@pytest.fixture
def sha256():
    def _sha(path: Path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    return _sha


@pytest.fixture
def copy_fixture(tmp_path: Path):
    def _copy(source: Path) -> Path:
        destination = tmp_path / source.name
        shutil.copytree(source, destination)
        return destination

    return _copy


@pytest.fixture
def run_validator():

    def _run(profile_root: Path, *args: str):
        return subprocess.run(
            [sys.executable, "-m", "ibook_tools", "profile", "validate", str(profile_root), *args],
            text=True,
            capture_output=True,
        )

    return _run
