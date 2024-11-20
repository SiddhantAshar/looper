import typer

from typing import Annotated
import time

from rich.pretty import pprint
from rich import print

from utils import get_config_list, read_config_file, store_config_file, init_looper, execute_command

looper = typer.Typer()

@looper.command("list")
def list_configs():
    # TODO: Stylist list using single column table?
    config_list = get_config_list()
    print(config_list)


@looper.command("show")
def show_config(config_name: Annotated[str, typer.Argument(help='Name of the config to view. Use "list" command to view available configs.')]):
    # TODO: proper error stating how to get config_name
    config = read_config_file(config_name)
    pprint(config, expand_all=True)


@looper.command("set")
def set_config(
    command: Annotated[str, typer.Option(help="The command which should be executed")] = None,
    variable: Annotated[str, typer.Option(help="List of values on which the `cmd` should iterate")] = None,
    separator: Annotated[str, typer.Option(help="Separator to split list of variables")] = None,
    cooldown: Annotated[float, typer.Option(help="Gap (in seconds) between each iteration")] = None):

    # Read current config
    current_config = read_config_file("current")

    # Update values
    if variable:
        current_config["variable"] = variable
    
    if command:
        current_config["command"] = command
    
    if separator:
        current_config["separator"] = separator
    
    if cooldown:
        current_config["cooldown"] = cooldown

    store_config_file("current", current_config)


@looper.command("load")
def load_config(config_name: Annotated[str, typer.Argument(help='Name of the config to load. Use "list" command to view available configs.')]):
    # copy `selected_config.json` to `current.json`
    # current_config_file_path = APP_DIR_PATH/"current.json"
    # config_file_path = APP_DIR_PATH/f"{config_name}.json"
    
    # TODO: check if config_file_path exists
    # TODO: current config will be lost, prompt overwrite/abort

    pass

@looper.command("store")
def store_config(config_file_name: Annotated[str, typer.Argument(help='Name of the target config.')]):

    # Read current config
    current_config = read_config_file("current")

    # TODO: check if new config file exists, prompt overwrite/abort
    store_config_file(config_file_name, current_config)


@looper.command("run")
def run():

    # Read current config
    current_config = read_config_file("current")

    # TODO: check if empty
    # TODO: verify all the required key-value are present in config
    
    for variable in current_config["variable"].split(current_config["separator"]):

        print("====================================")
        print(f"Variable= {variable}")
        # TODO: check if variable is empty (e.g. trailing separator)
        execute_command(f"{current_config['command']}".format(variable))
        
        # print(f"{current_config['command']}".format(variable))
        print("====================================")
        time.sleep(float(current_config["cooldown"]))
        
        # if var != vars[-1]:
        #     time.sleep(cooldown)


if __name__ == "__main__":
    init_looper()

    looper()