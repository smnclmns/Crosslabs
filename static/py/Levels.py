import os

def get_rootdir(basename = "Crosslabs") -> str:
    """Changes path to the root directory of the project and returns the path.
    
    Args:
        basename (str, optional): basename of root directory. Defaults to "Crosslabs".
        
    Returns:
        str: path of root directory of the project
        """

    while not os.path.basename(os.getcwd()) == basename: os.chdir("..")
    return os.getcwd()

def get_level_names() -> tuple:
    """Returns a tuple of all template names.
    
    Returns:
        tuple: tuple of all template names
        """

    rootdir = get_rootdir()
    template_dir = os.path.join(rootdir, "templates", "Levels")
    return (name for name in os.listdir(template_dir) if ".html" in name)

class Level():
    """Class for handling levels."""

    def __init__(self, name: str) -> None:

        self.name = name
        self.template_path = os.path.join(get_rootdir(), "templates", "Levels", self.name)

    def __repr__(self) -> str:
        return f"Level: {self.name}"
    
    def __str__(self) -> str:
        return self.name
    
    def get_input_dict(self) -> dict:
        """Returns a dictionary of all input fields of the level.
        
        Returns:
            dict: dictionary of all input fields of the level
            """

        input_dict = {}
        with open(self.template_path, "r") as f:
            for line in f.readlines():
                if "<input" in line:
                    pass
                    
        return input_dict
    


if __name__ == "__main__":
    print(get_level_names())

