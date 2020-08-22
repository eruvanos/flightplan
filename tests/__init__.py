from pathlib import Path

import pytest
import yaml

TEST_DATA = Path(__file__).parent / "data"


def T(name, *args):
    return pytest.param(*args, id=name)


def load_yaml(file: str):
    with (TEST_DATA / file).open() as f:
        return yaml.safe_load(f)


def get_resource(file_name: str) -> Path:
    return TEST_DATA / file_name
