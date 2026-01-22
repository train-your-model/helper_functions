# ------------------
# IMPORTS
# ------------------
import os
import platform
from pathlib import Path
import yaml
import dir_paths as dp


class NewUser:
    """
    This function does the following actions:
        1. Extracts the path for the Desktop, for the Directories to be moved.
        2. Extracts the path for the Download Directory, for the downloaded data folders to be moved.
        3. Creates the Root Directory.

    :param def_path: 1 - Use Default Paths. 0 - Use Custom Destination
    """

    def __init__(self, def_path=1):
        self.os_type = platform.system()
        self.def_path = def_path
        self.root_dir_path = ""

    def get_desktop_path(self):
        """
        :return: The path for Desktop for different OS versions
        """
        if self.def_path == 1:
            if self.os_type == "Windows":
                full_path = os.path.join(Path(os.environ["USERPROFILE"]), "Desktop")
                return full_path

        else:
            dest_dir = str(input("Enter the Destination Directory: "))
            if self.os_type == "Windows":
                full_path = os.path.join(Path(os.environ["USERPROFILE"]), dest_dir)
                return full_path

    def get_download_path(self):
        """
        :return: The path for the Default Download Directory
        """
        if self.def_path == 1:
            if self.os_type == "Windows":
                full_path = os.path.join(Path(os.environ["USERPROFILE"]), "Downloads")
                return full_path

        else:
            dest_dir = str(input("Enter the Destination Directory: "))
            if self.os_type == "Windows":
                full_path = os.path.join(Path(os.environ["USERPROFILE"]), dest_dir)
                return full_path

    def get_site_names_file_path(self):
        """
        :return: The path for the saved json file for site names
        """
        if self.os_type == "Windows":
            func_dir = Path(__file__).resolve().parents[1]
            full_path = os.path.join(func_dir, "files", "site_names.json")
            return full_path

    def get_templates_names_file_path(self):
        """
        :return: The path for the saved json file for templates names
        """
        if self.os_type == "Windows":
            func_dir = Path(__file__).resolve().parents[1]
            full_path = os.path.join(func_dir, "files", "templates_names.json")
            return full_path

    def get_templates_path(self):
        """
        :return: The path for the ipynb templates
        """
        if self.os_type == "Windows":
            func_dir = Path(__file__).resolve().parents[1]
            full_path = os.path.join(func_dir, "templates")
            return full_path

    def paths_dump(self):
        config = {
            "defaults":{
                "download_dir":self.get_download_path(),
                "parent_dir":self.get_desktop_path(),
                "templates_dir":self.get_templates_path()
            },
            "json_files":{
                "site_names":self.get_site_names_file_path(),
                "templates_names":self.get_templates_names_file_path()
            }
        }
        func_dir = Path(__file__).resolve().parents[1]
        config_file_path = os.path.join(func_dir, "files", "config.yaml")
        with open(config_file_path, "w") as f:
            yaml.safe_dump(config, f)
            f.close()

        # Updating the File Path in the dir_paths file
        dp.config_path = config_file_path

    def create_root_dir(self,dir_name):
        """
        :param dir_name: Name of the Root Directory containing all the project directories
        """
        yaml_path = dp.config_path
        with yaml_path.open("r") as f:
            path = yaml.safe_load(f)["defaults"]["parent_dir"]
            par_dir = os.path.join(path, dir_name)
            self.root_dir_path = par_dir
            os.mkdir(par_dir)
            f.close()

    def append_root_dir_path(self):
        """
        :return: Appends the default YAML file with the root directory
        """
        yaml_path = dp.config_path
        with yaml_path.open("r") as f:
            y_f = yaml.safe_load(f)

        y_f.setdefault("defaults",{})["root_dir_path"] = self.root_dir_path
        with yaml_path.open("w") as f:
            yaml.safe_dump(y_f, f, sort_keys=False)
            f.close()

    def run(self):
        self.paths_dump()
        root_name = str(input("Enter the Name of the Root Folder for the Projects: "))
        self.create_root_dir(dir_name=root_name)
        self.append_root_dir_path()
        return self
