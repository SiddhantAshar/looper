from enum import Enum
from pathlib import Path

class GlobalConfig:
    HOME_DIR: Path

class ConfigStatus(Enum):
    DOES_NOT_EXIST = 1
    EXISTS_AND_EMPTY = 2
    EXISTS_AND_POPULATED = 3
