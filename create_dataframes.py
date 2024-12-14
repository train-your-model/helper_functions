import re
import os
import pandas as pd

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