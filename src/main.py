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
from rich.panel import Panel
from rich.pretty import Pretty
from rich import print


looper = typer.Typer()

@looper.command("list")
def list_configs():
    # TODO: does looper provide any tool to display list?
    pprint([file.stem for file in list(APP_DIR_PATH.glob('*.json'))])
    # for file in list(APP_DIR_PATH.glob('*.json')):
    #     # print(f"- {file.stem}")
    #     pprint(file.stem)


@looper.command("show")
def show_config(config_name: str):
    # TODO: proper error stating how to get confif_name
    config_file_path = APP_DIR_PATH/f"{config_name}.json"
    # TODO: check if config_file_path exists
    config = read_config_file(config_file_path)
    pprint(config, expand_all=True)


@looper.command("set")
def set_config(key: Key, value: str):

    # Create `current.json` if not present
    current_config_file_path = APP_DIR_PATH/"current.json"
    if not current_config_file_path.exists():
        current_config_file_path.touch()

    current_config = {}
    try:
        current_config = read_config_file(current_config_file_path)
    except JSONDecodeError as e:
        # File is empty, ignore
        pass

    current_config[key.value] = value

    store_config_file(current_config_file_path, current_config)


@looper.command("load")
def load_config(config_name: str):
    # copy `selected_config.json` to `current.json`
    current_config_file_path = APP_DIR_PATH/"current.json"
    config_file_path = APP_DIR_PATH/f"{config_name}.json"
    
    # TODO: check if config_file_path exists
    # TODO: current config will be lost, prompt overwrite/abort

    pass

@looper.command("store")
def store_config(config_file_name:str):

    current_config_file_path = APP_DIR_PATH/"current.json"
    new_config_file_path = APP_DIR_PATH/f"{config_file_name}.json"
    
    # TODO: check if current config exists
    # TODO: check if new config file exists, prompt overwrite/abort

    current_config = read_config_file(current_config_file_path)

    store_config_file(new_config_file_path, current_config)


@looper.command("run")
def run():
    current_config_file_path = APP_DIR_PATH/"current.json"

    # TODO: check if current config exists
    # print(f"{command}".format)
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
