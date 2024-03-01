"""
pytest for utils.py
"""

import pytest

from src import utils

from .utils import get_test_file_path


@pytest.fixture()
def set_config():
    """load test_config.yaml"""
    with open(get_test_file_path("test_config.yaml")) as fh:
        return utils.yaml_load(fh)


def test_get_typed_value():
    """test get_typed_value.py"""
    value = utils.get_typed_value("2")
    assert isinstance(value, int)

    value = utils.get_typed_value("1.2")
    assert isinstance(value, float)

    value = utils.get_typed_value("1.c2")
    assert isinstance(value, str)


def test_yaml_load(set_config):
    """test yaml_load.py"""
    assert isinstance(set_config, dict)
    with pytest.raises(FileNotFoundError):
        with open(get_test_file_path("404.yml")) as fh:
            utils.yaml_load(fh)
