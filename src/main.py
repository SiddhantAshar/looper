import typer
# from typing import List
# from typing import Annotated
import time
import os
import json
from json.decoder import JSONDecodeError
from pathlib import Path
from rich.pretty import pprint

from models import Key
from utils import read_config_file, store_config_file


looper = typer.Typer()

@looper.command("show")
def show_config(config_name: str = "current"):

    config_filepath = APP_DIR_PATH/f"{config_name}.json"

    config = read_config_file(config_filepath)
    pprint(config, expand_all=True)


@looper.command("set")
def set_config(key: Key, value: str):

    # Create `current.json` if not present
    current_config_filepath = APP_DIR_PATH/"current.json"
    if not current_config_filepath.exists():
        current_config_filepath.touch()

    current_config = {}
    try:
        current_config = read_config_file(current_config_filepath)
    except JSONDecodeError as e:
        pass

    current_config[key.value] = value

    store_config_file(current_config_filepath, current_config)


@looper.command("load")
def load_config(config_name: str):
    # Create `current.json` if not present
    current_config_filepath = APP_DIR_PATH/"current.json"
    if not current_config_filepath.exists():
        current_config_filepath.touch()
    
    # copy `selected_config.json` to `current.json`
    
    pass

@looper.command("store")
def store_config():
    pass

@looper.command("run")
def run():
    pass

# @looper.command()
# def main(vars: Annotated[List[str], typer.Argument(help="List of values on which the `cmd` should iterate")],
#          cmd: Annotated[str, typer.Argument(help="The command which should be executed")],
#          cooldown: Annotated[float, typer.Argument(help="Gap (in seconds) between each iteration")] = 0):
    
#     for var in vars:
#         print(f"{cmd}".format(var))
#         if var != vars[-1]:
#             time.sleep(cooldown)

# @app.command()
# def not_main(your_name: str):
#     print(f"hello {your_name}")

if __name__=="__main__":
    
    APP_DIR = os.getenv("LOOPER_HOME", "/home/sid/.config/looper")
    APP_DIR_PATH = Path(APP_DIR)

    try:
        APP_DIR_PATH.mkdir()
    except FileExistsError:
        pass
    except PermissionError:
        print(f"Permission denied: Unable to create '{APP_DIR_PATH}'.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while creating the home directory: {e}")
        exit(1)

    os.chdir(APP_DIR)
    
    looper()
