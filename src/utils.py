from pathlib import Path
import json

def read_config_file(config_file_path: Path):
    with open(config_file_path, 'r') as fd_config:
        config = json.load(fd_config)

    return config

def store_config_file(config_file_path: Path, config: dict):
    with open(config_file_path, 'w') as fd_config:
        json.dump(config, fd_config)