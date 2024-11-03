import os
import json
from json import JSONDecodeError
from pathlib import Path
import subprocess
import shlex

from models import GlobalConfig

global_config = GlobalConfig()


def get_config_list():
    return [file.stem for file in list(global_config.HOME_DIR.glob('*.json'))]


def get_config_status(config_name: str):
    # create Path object
    # return status according to models.ConfigStatus
    pass


def read_config_file(config_file: str):
    config_file_path = get_path(config_file)
    
    # TODO: handle invalid config name and filedoesnotexist error
    config = {}
    with open(config_file_path, 'r') as fd_config:
        try:
            config = json.load(fd_config)
        except JSONDecodeError as e:
            # file is empty, ignore
            pass

    return config


def store_config_file(config_file:str, config: dict):
    config_file_path = get_path(config_file)

    with open(config_file_path, 'w') as fd_config:
        json.dump(config, fd_config)


def get_path(config_file: str) -> Path:
    # create path object
    # verify if exists
    return Path(global_config.HOME_DIR)/f'{config_file}.json'

def init_looper():
    # Get home directory from env
    HOME_DIR = os.getenv("LOOPER_HOME", "/home/sid/.config/looper")
    HOME_DIR_PATH = Path(HOME_DIR)

    # Attempt to create home directory
    try:
        HOME_DIR_PATH.mkdir()
    except FileExistsError:
        pass
    except PermissionError:
        print(f"Permission denied: Unable to create '{HOME_DIR_PATH}'.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while creating the home directory: {e}")
        exit(1)

    # Home directory set successfully
    global_config.HOME_DIR = HOME_DIR_PATH

    # Create `current.json` if it does not exist
    current_config_file_path = HOME_DIR_PATH/"current.json"
    if not current_config_file_path.exists():
        current_config_file_path.touch()

    # Home directory initialized successfully, navigate there
    os.chdir(HOME_DIR)

def execute_command(command):

    # calls the command and sends the output of the subprocess to parent's stdout and stderr
    rc = subprocess.call(shlex.split(command))

    # Popen is a lower level function, need to handle r/w of the stdout manually
    # process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    # while True:
    #     print("here")
    #     output = process.stdout.readline()
    #     if process.poll() is not None:
    #         break
    #     if output:
    #         print(output.strip())
    # rc = process.poll()
    return rc