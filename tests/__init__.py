import json
from pathlib import Path

import yaml

TEST_DATA = Path(__file__).parent / 'data'


def load_yaml(file: str):
    with (TEST_DATA / file).open() as f:
        return yaml.load(f)


def assert_dict_equal(expected: dict, actual: dict):
    # dict_a_str = json.dumps(expected, sort_keys=True, indent=2)
    # dict_b_str = json.dumps(actual, sort_keys=True, indent=2)
    # assert dict_a_str == dict_b_str
    assert expected == actual

