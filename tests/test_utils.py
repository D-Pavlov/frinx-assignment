import pytest
import json
from pathlib import Path

import utils


MOCK_DATA_DIR = Path('tests/mock_data/')


def test_loading_nonexistent_file_raises():
    with pytest.raises(FileNotFoundError) as e_info:
        _ = utils.load_json_config(Path(MOCK_DATA_DIR, 'not_here.json'))


def test_loading_invalid_json_raises():
    with pytest.raises(json.decoder.JSONDecodeError) as e_info:
        _ = utils.load_json_config(Path(MOCK_DATA_DIR, 'invalid.json'))


def test_loading_valid_json_produces_dictionary():
    data = {'key': 'value'}

    assert utils.load_json_config(Path(MOCK_DATA_DIR, 'valid.json')) == data
