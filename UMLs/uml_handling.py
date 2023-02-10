import os
from dataclasses import dataclass, field
from functools import partial

from plantuml import PlantUML

def get_rootdir(basename = "Crosslabs") -> str:
    while not os.path.basename(os.getcwd()) == basename: os.chdir("..")
    return os.getcwd()

def get_uml_dirlist(root_dir: str = get_rootdir()) -> list:
    return [os.path.join(root_dir, "UMLs", file) for file in os.listdir("UMLs") if ".txt" in file]

def get_uml_dict(uml_dirlist: list = get_uml_dirlist()) -> dict:
    return {os.path.basename(path)[:-4]:path for path in uml_dirlist}

def get_ids(uml_dict: dict = get_uml_dict()) -> set:
    return {name for name in uml_dict}


@dataclass(slots=True, frozen=True)
class UML_Handler():

    root_dirname: str = "Crosslabs"
    __root_dir__: str = field(init=False, default_factory=partial(get_rootdir, basename=root_dirname))
    __uml_list__: list = field(init=False, default_factory=get_uml_dirlist)
    __uml_dict__: dict = field(init=False, default_factory=get_uml_dict)

    uml_ids: set = field(init=False, default_factory=get_ids)

    __PlantUML__: PlantUML = field(init=False, default_factory=PlantUML) # initialises the connection to the open plantuml server

    def __repr__(self) -> str:
        return f"UML_Handler: {self.uml_ids}"


    def get_plantuml_text(self, uml_id: str) -> str:

        if uml_id in self.uml_ids: uml_file = self.__uml_dict__.get(uml_id)

        else: raise FileNotFoundError(f"there is no file with the id '{uml_id}")

        with open(uml_file, 'r') as f: plantuml_text: str = "".join(f.readlines())

        return plantuml_text

    def get_plantuml_url(self, uml_id: str) -> str:

        return self.__PlantUML__.get_url(self.get_plantuml_text(uml_id))

    def get_img_data(self, uml_id: str):

        return self.__PlantUML__.processes(self.get_plantuml_text(uml_id))

    def add_Block(self, uml_id: str) -> None:
        pass



if __name__ == "__main__":

    testhandler = UML_Handler()

    print(testhandler)

