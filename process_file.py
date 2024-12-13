import datetime
import os
import re
import shutil
from zipfile import ZipFile
import configparser
import dir_paths as dp
import pandas as pd


# Supplement Functions

def check_zip_folders(dir) -> int:
    """
    This function checks whether a directory contains any zip folders.
    :param dir: Directory to be checked for the zip folders
    :return: An integer value depending on the findall object - 0: Folder NOT present, 1: Folder is present
    """
    for ind, f in enumerate(os.listdir(dir)):
        zfs = re.findall("zip", f)
        if len(zfs) != 0:
            return 1
        else:
            return 0

def read_config(sec, ky):
    """
    :param sec: Section of the Config file
    :param ky: Key name in the given section
    :return: Value for the key in the given section of the config file
    """
    parent_path = dp.config_path
    file_name = 'config.ini'

    config = configparser.ConfigParser()
    config.read(os.path.join(parent_path, file_name))
    val = config[sec][ky]
    return val


# Working Class
class MoveDatafold:
    """
    This class moves the data folders from the default download folder to the working directory.
    """

    def __init__(self, targ_dt, download_fold=read_config(sec='Base_Directories', ky='default_download_dir'),
                 targ_dir=os.getcwd()):
        self.download_fold = download_fold
        self.targ_dt = targ_dt
        self.targ_dir = targ_dir

    def __call__(self):
        self.move_data_fold(dir_files=self.src_dir_contents())

        unzip_folder = check_zip_folders(dir=self.targ_dir)
        working_dir_pre = list()
        if unzip_folder == 1:
            working_dir_pre.extend(os.listdir(self.targ_dir))
            self.unzip_data_fold()

        len_working_dir_pre = len(working_dir_pre)

        working_dir_post = os.listdir(self.targ_dir)
        len_working_dir_post = len(working_dir_post)
        unzippd_in_folder = len_working_dir_post - len_working_dir_pre

        # 1 represents that the unzipped contents are inside a unzipped folder
        if unzippd_in_folder == 1:
            self.move_out_unzipped_folders(b4_list=working_dir_pre,
                                           after_list=working_dir_post)
            print("Unzipped Folder contents have been moved out and the redundant folder has been removed.")

    def unzip_data_fold(self):
        """
        Unzips the zipped data folder present in the current working directory

        :return: Unzipped data folder or contents of the data folder
        """
        for ind, f in enumerate(os.listdir(self.targ_dir)):
            zfs = re.findall("zip", f)
            if len(zfs) != 0:
                # Unzip and Display the contents of the zip folder
                z = ZipFile(os.path.join(self.targ_dir,f))
                z.extractall(path=self.targ_dir)
                z.close()

        print(f' Updated Contents of the Working Directory: {os.listdir(self.targ_dir)}')

    def move_out_unzipped_folders(self, b4_list:list, after_list:list):
        """
        Moves out the contents of the unzipped folder to the working directory and then removes the redundant folder

        :param b4_list: List containing the working directories contents before the first unzipping
        :param after_list: List containing the working directory contents after the first unzipping
        :return: A working directory without the redundant unzipped folder
        """

        # Moving Section
        unzp_folder_name = str(set(after_list).difference(set(b4_list)))
        folder_path = os.path.join(self.targ_dir,unzp_folder_name)

        unzp_contents = list(os.listdir(folder_path))
        for content in unzp_contents:
            file_src = os.path.join(folder_path, content)
            file_dst = self.targ_dir
            shutil.move(file_src, file_dst)

        # Deletion Section
        os.rmdir(path=folder_path)


    def src_dir_contents(self):
        """
        Checks the presence of the data files in the downloaded folder for a specific date
        :return: A list containing the files created on the given specific date.
        """
        cr_files = []

        for file in os.listdir(self.download_fold):
            file_path = os.path.join(self.download_fold, file)
            create_time = os.path.getmtime(file_path)
            create_date = datetime.datetime.fromtimestamp(create_time).strftime('%d-%m-%Y')
            if str(create_date) == self.targ_dt:
                cr_files.append(file)

        return cr_files

    def move_data_fold(self, dir_files):
        """
        Moves the data folder into the working directory
        :return: Data folder being moved into the working directory
        """
        try:
            print('Indices of the files in the directory are:\n')
            for ind, f in enumerate(dir_files):
                print(f'{ind} : {f}')

            move_all_files = int(input("Do you want all the files in the directory list to be moved? 1/0: "))
            assert move_all_files == 1 or move_all_files == 0, "Takes only 1/0."

            if move_all_files == 1:
                for file in dir_files:
                    file_src = os.path.join(self.download_fold, file)
                    file_dst = self.targ_dir
                    shutil.move(file_src, file_dst)

            else:
                fil_indxs = input("Please Enter the Indices of the files you want moved.: ")
                fil_indxs_list = fil_indxs.split()

                for i in range(len(fil_indxs_list)):
                    fil_indxs_list[i] = int(fil_indxs_list[i])

                for ind in sorted(fil_indxs_list, reverse=True):
                    file_src = os.path.join(self.download_fold, dir_files[ind])
                    file_dst = self.targ_dir
                    shutil.move(file_src, file_dst)
                    print("Files have been moved Successfully!!")

        except:
            print(f'Data Folder/File have not been moved into the directory.')

class CreateDataframes:

    def create_tabular_dataframes(self):
        data_files = []
        for ind, f in enumerate(os.listdir(os.getcwd())):
            csv_files = re.findall("csv", f)
            if len(csv_files) != 0:
                data_files.append(f)

        file_value = 0
        global train_f_name, test_f_name, sub_f_name
        for f in data_files:
            if re.findall("train", f):
                train_f_name = f
                file_value += 1
            elif re.findall("test", f):
                test_f_name = f
                file_value += 2
            elif re.findall("submission", f):
                sub_f_name = f
                file_value += 3

        if file_value == 3:
            return pd.read_csv(train_f_name), pd.read_csv(test_f_name)

        elif file_value == 6:
            return pd.read_csv(train_f_name), pd.read_csv(test_f_name), pd.read_csv(sub_f_name)

        else:
            raise Exception("Certain Files are Missing.")
