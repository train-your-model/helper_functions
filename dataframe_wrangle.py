# Imports
import numpy as np

class Tabular:
    """
    This class performs the following tasks:
        1. Lowers the column names.
        2. Checks the presence of duplicated rows and drop them if present.
        3. [OPTIONALLY!!] Sorts the variables into variables with and without Missing Values.
        4. [OPTIONALLY!!] Threshold the Missing Variables on the basis of given threshold value.
    """
    def __init__(self, train_df):
        self.df = train_df

    def __call__(self):
        self.stand_col_names()
        self.check_remove_dupl_val()
        if na_val != 0:
            self.sort_miss_vars()
        else:
            print('Dataset has NO Variables with Missing Values')

    def stand_col_names(self):
        self.df.columns = self.df.columns.str.lower()

    def check_remove_dupl_val(self):
        dupl_val = self.df.duplicated().sum()

        if dupl_val != 0:
            before_drop_shape = self.df.shape()[0]
            print('There is  presence of duplicated rows in the dataset')
            self.df = self.df.drop_duplicates(inplace=True)
            after_drop_shape = self.df.shape()[0]
            print(f'Number of duplicated rows dropped: {before_drop_shape-after_drop_shape}')

        else:
            print('Dataset is free of Duplicated rows.')

    def check_na(self):
        global na_val
        na_val = len(self.df.columns[self.df.isnull().any()].tolist())
        return na_val

    def sort_miss_vars(self):
        global miss_var_list_df, non_miss_var_list_df, mv_dict_sorted_df
        miss_var_list_df = []
        non_miss_var_list_df = []
        mv_dict_df = dict()

        for ind, row in enumerate(self.df.isnull().sum()):
            if row != 0:
                miss_var_list_df.append(self.df.columns[ind])
                mv_dict_df.update({self.df.columns[ind]: np.round((row / len(self.df)) * 100, 2)})
            else:
                non_miss_var_list_df.append(self.df.columns[ind])

            ## Sorting the predictors on the basis of Missing value proportions
        mv_dict_sorted_df = sorted(mv_dict_df.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    def miss_vars_prop(self):
        return dict(mv_dict_sorted_df)

    def missvars_non_missvars(self):
        return miss_var_list_df, non_miss_var_list_df

    def miss_vars_thresholding(self, miss_var_prop_dict, thr_val:float):
        # List of predictors meeting the criteria
        thr_miss_vars = []
        # List of predictors not meeting the criteria
        miss_vars_thr_rej = []

        for k in miss_var_prop_dict.keys():
            if miss_var_prop_dict[k] <= thr_val:
                thr_miss_vars.append(k)
            else:
                miss_vars_thr_rej.append(k)

        return thr_miss_vars, miss_vars_thr_rej

class Time_Series(Tabular):
    """
    This class performs the following tasks:
        1. Lowers the column names.
        2. Checks for the presence of missing values.
    """
    def __init__(self, train_df):
        super().__init__(train_df)

    def __call__(self):
        super().stand_col_names()
        na_present = super().check_na()
        if na_present == 0:
            print("Dataset has NO Variables with Missing Values.")
        else:
            print("Dataset contains Variables with Missing Values.")
            super().sort_miss_vars()
