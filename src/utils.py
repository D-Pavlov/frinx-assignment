import json
from pathlib import Path


def load_json_config(path: Path):
    if not path.exists():
        raise FileNotFoundError(f'Config file {path} not found.')

    with open(path, 'r') as config_file:
       config_data = json.loads(config_file.read())

    return config_data
