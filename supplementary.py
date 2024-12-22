import json
import os


class ApproachExport:
    """
    This class performs the following tasks:
        1. Makes a new Directory for the data files to be stored.
    """
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    def __call__(self):
        self.create_dir()

    def create_dir(self):
        """
        :return: A new directory with the user given name
        """
        if os.path.exists(os.path.join(os.path.join(os.getcwd(), self.dir_path))):
            print('Directory with the same name already exists.')
            dir_new_name = str(input("Please Enter a new name for the Directory: "))
            self.dir_path = dir_new_name
            return os.mkdir(os.path.join(os.getcwd(), self.dir_path))

        else:
            return os.mkdir(os.path.join(os.getcwd(), self.dir_path))

    def dict_export(self, map_dict, f_name):
        """
        :map_dict: Dictionary to be exported
        :param f_name: File name to be given
        :return: A json file containing the dictionary
        """
        with open(f_name, "w") as outfile:
            json.dump(map_dict, outfile)