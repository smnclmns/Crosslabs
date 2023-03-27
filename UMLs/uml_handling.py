import os
from dataclasses import dataclass, field
from functools import partial

from plantuml import PlantUML, PlantUMLConnectionError, PlantUMLHTTPError

def get_rootdir(basename = "Crosslabs") -> str:
    while not os.path.basename(os.getcwd()) == basename: os.chdir("..")
    return os.getcwd()

def get_txt_files_dir(root_dir: str = get_rootdir()) -> str:
    return os.path.join(root_dir, "UMLs", "txt_files")

def get_uml_dirlist(root_dir: str = get_rootdir()) -> list:
    return [os.path.join(root_dir, "UMLs", "txt_files", file) for file in os.listdir(get_txt_files_dir()) if ".txt" in file]

def get_uml_dict(uml_dirlist: list = get_uml_dirlist()) -> dict:
    return {os.path.basename(path)[:-4]:path for path in uml_dirlist}

def get_ids(uml_dict: dict = get_uml_dict()) -> set:
    return {name for name in uml_dict}


@dataclass(slots=True)
class UML_Handler():

    root_dirname: str = "Crosslabs"
    __root_dir__: str = field(init=False, default_factory=partial(get_rootdir, basename=root_dirname))
    __uml_list__: list = field(init=False, default_factory=get_uml_dirlist)
    __uml_dict__: dict = field(init=False, default_factory=get_uml_dict)

    uml_ids: set = field(init=False, default_factory=get_ids)

    __PlantUML__: PlantUML = field(init=False, default_factory=partial(PlantUML, url="http://www.plantuml.com/plantuml/img/")) # initialises the connection to the open plantuml server

    def __repr__(self) -> str:
        return f"UML_Handler: {self.uml_ids}"


    def get_plantuml_text(self, uml_id: str) -> str:


        if uml_id in self.uml_ids: uml_file = self.__uml_dict__.get(uml_id)

        else: raise FileNotFoundError(f"there is no file with the id '{uml_id}")

            #farbiges markieren der textblöcke
            # #farbe:blocK,
        plantuml_text=""

        with open(uml_file, "r") as f: 
            text = f.read().split()
            text1=[]

            for i,y in enumerate(text):
                
                if text[i][:6] == "while(":
                    text1.append(text[i])

                elif text[i][:10] == "endwhile()":
                    text1.append("endwhile")
                
                elif text[i][:9] == "endwhile(":
                    text1.append(text[i])
                else:
                    s = ":"
                    s1 = ";"
                    x = s + text[i] + s1
                    text1.append(x)
        
        for y in text1: 
                plantuml_text +=  y+"\n"



        plantuml_text = plantuml_text\
        .replace(":motor;", "#green:motor;")\
        .replace(":input;","#green:input;")\
        .replace(":initializing;","#green:initializing;")\
        .replace(":pump;", "#green:pump;")\
        .replace(":Motor;", "#green:Motor;")\
        .replace(":Input;","#green:Input;")\
        .replace(":Initializing;","#green:Initializing;")\
        .replace(":Pump;", "#green:Pump;")

        plantuml_text= "start" +"\n"+ plantuml_text + "\n" +  "end"

        return plantuml_text

    def get_plantuml_url(self, uml_id: str, figtype: str = "any") -> str:

        default_url = self.__PlantUML__.get_url(self.get_plantuml_text(uml_id))
        sections = default_url.split("/")

        if figtype == "any": return default_url

        sections[4] = figtype

        return "/".join(sections)
        

    def get_img_data(self, url: str):

        try:
            response, content = self.__PlantUML__.http.request(url, **self.__PlantUML__.request_opts)
        except self.__PlantUML__.HttpLib2Error as e:
            raise PlantUMLConnectionError(e)
        if response.status != 200:
            raise PlantUMLHTTPError(response, content)
        return content

    def save_png_file(self, uml_id: str) -> bool:

        infile = self.__uml_dict__.get(uml_id)
        outfile = os.path.join(self.__root_dir__, "UMLs", "PNGs", uml_id + ".png")
        errorfile = os.path.join(self.__root_dir__, "UMLs","error_files", uml_id + "_error.html")

        return self.__PlantUML__.processes_file(infile, outfile=outfile, errorfile=errorfile)

    def save_svg_file(self, uml_id: str) -> None:

        url = self.get_plantuml_url(uml_id, "svg")
        content = self.get_img_data(url)

        with open(os.path.join(self.__root_dir__, "UMLs", "SVGs", uml_id + ".svg"), 'wb') as out:
            out.write(content)



    def add_uml_file(self, plant_uml_text: str) -> None:

        with open("UMLs/txt_files/v1.txt", "w") as f: f.write(plant_uml_text)

        self.__uml_list__ = get_uml_dirlist()
        self.__uml_dict__ = get_uml_dict()
        self.uml_ids = get_ids()





if __name__ == "__main__":

    testhandler = UML_Handler()

    testhandler.save_svg_file("v1")

