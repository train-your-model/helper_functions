# ------------------
# IMPORTS
# ------------------
from setup_update import ReturnUser
import dir_paths as dp

import datetime
import yaml
import os
from zipfile import ZipFile
import shutil

class DataFoldDeal(ReturnUser):
    """
    This class performs the following tasks:
    1. Checks for the presence of zipped data folders in the download folder
    """
    def __init__(self, site_abv):
        super().__init__(site_abv)
        self.download_dir_path = ""
        self.contents = [] # List of Data Files in the Download Directory
        self.zp_fold_in_dir = [] # List of Zipped Data Folders in the Working Directory

        self.b4_unzip_cont = [] # List of Project Directory Contents before unzipping
        self.af8_unzip_cont = [] # List of Project Directory Contents after unzipping

        self.unzip_folder_path = []

    def get_download_dir_path(self):
        """
        :return: Extracted file path for the default download directory
        """
        with open(dp.config_path, 'r') as f:
            data_path = yaml.safe_load(f)["defaults"]["download_dir"]
            self.download_dir_path = data_path

    def get_dir_contents(self,
                         targ_date = datetime.date.today().strftime('%d-%m-%Y')):
        """
        :return: Returns a list with the contents of the Directory containing the data files.
        """
        for f in os.listdir(self.download_dir_path):
            f_path = os.path.join(self.download_dir_path, f)
            create_time = os.path.getmtime(f_path)
            create_date = datetime.datetime.fromtimestamp(create_time).strftime('%d-%m-%Y')
            if str(create_date) == targ_date:
                self.contents.append(f_path)

    def move_data_folders(self):
        """
        :return: Moves data folders into the project working directory
        """
        print('Indices of the files in the directory are:\n')
        for ind, f in enumerate(self.contents):
            print(f'{ind} : {f}')

        move_all_files = int(input("Do you want all the files in the directory list to be moved? 1/0: "))
        assert move_all_files == 1 or move_all_files == 0, "Takes only 1/0."

        if move_all_files == 1:
            for f_path in self.contents:
                shutil.move(f_path, self.proj_dirpath)

        else:
            try:
                file_index = input("Please Enter the indices of the files you want moved (space separated): ")
                indices = sorted(map(int, file_index.split()), reverse=True)

            except ValueError:
                print("All Indices must be integers")

            else:
                for ind in indices:
                    file_src = self.contents[ind]
                    shutil.move(file_src, self.proj_dirpath)

    def check_for_zip_files(self):
        """
        Checks for the presence of zip file in the data contents list
        :return: The file path of the zip file
        """
        for f in self.contents:
            if f.endswith(".zip"):
                self.zp_fold_in_dir.append(f)

        if len(self.zp_fold_in_dir) != 0:
            self.b4_unzip_cont.extend(os.listdir(self.proj_dirpath))

    def unzip_folder(self):
        """
        :return: Unzips the zipped data folder in the working directory
        """
        if len(self.zp_fold_in_dir) == 1:
            for f in self.zp_fold_in_dir:
                z = ZipFile(f)
                z.extractall()
                z.close()

            self.af8_unzip_cont.extend(os.listdir(self.proj_dirpath))

        elif len(self.zp_fold_in_dir) > 1:
            print('Indices of the files in the directory are:\n')
            for ind, f in enumerate(self.zp_fold_in_dir):
                print(f'{ind} : {f}')

            file_index = input("Please Enter the indices of the files you want moved (space separated): ")
            indices = sorted(map(int, file_index.split()), reverse=True)

            for ind in indices:
                z = ZipFile(self.zp_fold_in_dir[ind])
                z.extractall()
                z.close()

            self.af8_unzip_cont.extend(os.listdir(self.proj_dirpath))

        # Dealing with Unzipped Folder
        unzip_folder_name = list(map(str,set(self.af8_unzip_cont).difference(set(self.b4_unzip_cont))))
        folder_path = [os.path.join(self.proj_dirpath,x) for x in unzip_folder_name]
        self.unzip_folder_path.extend(folder_path)

    def extract_from_unzip(self):
        """
        Extracts out the contents from the unzipped folder into the project directory.
        Once the extraction is carried out, the folder is removed / deleted.
        """
        # Extraction
        for d in self.unzip_folder_path:
            for f in os.listdir(d):
                f_path = os.path.join(self.proj_dirpath, d, f)
                shutil.move(f_path, self.proj_dirpath)

        # Empty Folder Removal
        for d in self.unzip_folder_path:
            os.rmdir(path=d)

    def run(self):
        super().run()

        self.get_download_dir_path()
        data_filter_date = input("Enter the date to be used as filter for getting downloaded data folder/files "
                                 "'%d-%m-%Y': ")
        self.get_dir_contents(targ_date=data_filter_date)
        self.move_data_folders()
        self.check_for_zip_files()

        if len(self.zp_fold_in_dir) == 0:
            print("Data Files have been successfully moved into the Project Directory")
            return self

        else:
            self.unzip_folder()
            self.extract_from_unzip()
            return self
