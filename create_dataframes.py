import re
import os
import pandas as pd

class CreateDataframes:

    def create_tabular_dataframes(self, sub_files_val:int, data_files:list):
        """
        :param sub_files_val: 1-> Submission File Present, 0-> No Submission File
        :param data_files: Data Files present in the working directory
        :return: Pandas Dataframes in accordance with the number of files present
        """
        global train_f_name, test_f_name, sub_f_name
        for f in data_files:
            if re.findall("train", f, re.IGNORECASE):
                train_f_name = f
            elif re.findall("test", f, re.IGNORECASE):
                test_f_name = f
            elif re.findall("submission", f, re.IGNORECASE):
                sub_f_name = f

        if sub_files_val == 1:
            return pd.read_csv(train_f_name), pd.read_csv(test_f_name), pd.read_csv(sub_f_name)

        elif sub_files_val == 0:
            return pd.read_csv(train_f_name), pd.read_csv(test_f_name)

        else:
            raise Exception("Certain Files are Missing.")

    def determine_submission_file(self):
        """
        Checks for the presence of submission file in the directory
        :return: An integer value; 0-> No Submission File, 1-> Submission File Present
        """
        data_files = []
        for ind, f in enumerate(os.listdir(os.getcwd())):
            csv_files = re.findall("csv", f)
            if len(csv_files) != 0:
                data_files.append(f)

        for f in data_files:
            if re.findall("submission", f, re.IGNORECASE):
                return 1, data_files
            else:
                return 0, data_files