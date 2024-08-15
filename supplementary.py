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
