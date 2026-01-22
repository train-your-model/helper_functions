# ------------------
# IMPORTS
# ------------------
import dir_paths as dp
import yaml
import json
import os

class ReturnUser:
    """
    For a returning user, this class performs the following tasks:
        1. Checks for the presence of the site name in the site json file. Depending on the outcome,
        two possible scenarios are dealt with.
        Scenario 1: New Site Name
            1. Adds the site abbreviation and full site name into the site json file.
            2. Extracts and Creates the Site Specific Directory
            3. Extracts and Creates Project Specific Directory
    """
    def __init__(self, site_abv):
        self.site_abv = site_abv
        self.site_name = ""
        self.json_f_path = ""
        self.new_site: int = 1
        self.site_path: str = ""
        self.proj_dirpath: str = ""

    def get_json_file_path(self):
        """
        :return: Extracts the file path for the json file containing the site names key:value pair
        """
        with open(dp.config_path, 'r') as f:
            path = yaml.safe_load(f)["json_files"]["site_names"]
            self.json_f_path = path
            f.close()

    def check_site_names(self):
        """
        Checks for the presence of user_input for the site name in the already stored site names json files
        :return: 0 - To Represent the absence of the site_abv in the json file
        """
        with open(self.json_f_path, "r") as f:
            f_dict = json.load(f)
            if str(self.site_abv).upper() not in f_dict.keys():
                self.new_site = 0

    def add_site_name(self, site_fullname):
        """
        :return: Appends the json file with site_abv: site_full_name
        """
        self.site_name = site_fullname
        with open(self.json_f_path, "r") as f:
            f_dict = json.load(f)
            f_dict.update({str(self.site_abv).upper(): self.site_name})
            f.close()
        print("JSON File has been updated with the New Site Name", end="\n")

    def create_site_dir(self):
        """
        :return: Site Specific Directory is created. Path to that directory is also returned.
        """
        with open(self.json_f_path, 'r') as f:
            f_dict = json.load(f)
            self.site_name = f_dict.get(self.site_abv)
            path = yaml.safe_load(f)["defaults"]["root_dir_path"]
            self.site_path = os.path.join(path, self.site_name)
            os.mkdir(self.site_path)

    def create_proj_dir(self, proj_name):
        """
        :param proj_name: Project Based Directory
        :return: A project Based Directory
        """
        self.proj_dirpath = os.path.join(self.site_path, proj_name)
        os.mkdir(self.proj_dirpath)

    def extract_site_path(self):
        """
        This function deals with the directory path extraction when previous directories exist from the yaml file
        """
        with open(self.json_f_path, 'r') as f:
            j_path = yaml.safe_load(f)["json_files"]["site_names"]
            with open(j_path, 'r') as f:
                site_dict = json.load(f)
                self.site_name = site_dict[self.site_abv]
                f.close()
            path = yaml.safe_load(f)["defaults"]["root_dir_path"]
            self.site_path = os.path.join(path, self.site_name)
            f.close()

    def run(self):
        self.get_json_file_path()
        self.check_site_names()

        if self.new_site == 0:
            fullname = str(input("Please Enter the Full Name of the Abbreviated Site: "))
            self.add_site_name(site_fullname=fullname)
            self.create_site_dir()
            proj_name = str(input("Please Enter the Name of the Project Specific Directory: "))
            self.create_proj_dir(proj_name=proj_name)

        else:
            self.extract_site_path()
            proj_name = str(input("Please Enter the Name of the Project Specific Directory: "))
            self.create_proj_dir(proj_name=proj_name)

        return self
