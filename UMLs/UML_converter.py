import os
from functools import partial

from plantuml import PlantUML, PlantUMLConnectionError, PlantUMLHTTPError

# Changes path to the root directory of the project

ROOTNAME = "Crosslabs"

def get_root_dir(basename = ROOTNAME) -> str:
    while not os.path.basename(os.getcwd()) == basename: os.chdir("..")
    return os.getcwd()


