import datetime
import os
import re
import shutil
from zipfile import ZipFile
import configparser
import dir_paths as dp
import pandas as pd


# Supplement Functions
def unzip_data_fold():
    """
    Unzips the zipped data folder present in the current working directory

    :return: Unzipped data folder or contents of the data folder
    """
    for ind, f in enumerate(os.listdir(os.getcwd())):
        zfs = re.findall("zip", f)
        if len(zfs) != 0:
            fold_ind = ind
            # Unzip and Display the contents of the zip folder
            z = ZipFile(os.listdir(os.getcwd())[fold_ind], 'r')
            z.extractall()
            z.close()

    print(f' Updated Contents of the Working Directory: {os.listdir(os.getcwd())}')


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

        unzip_folder = int(input("Do you wish to unzip the data folder? 1/0: "))
        assert unzip_folder == 1 or unzip_folder == 0, "Takes only 1/0"
        if unzip_folder == 1:
            unzip_data_fold()

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
