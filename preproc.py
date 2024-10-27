# Imports
import numpy as np


class TabularClean:
    """
    This class performs the following operations:
        1. Categorizes predictors based on their dtypes
        2. Sorts the variables into variables with and without Missing Values.
        3. Threshold the Missing Variables on the basis of given threshold value.
    """
    # Parameters
    miss_var_list = list()  # List containing variable names with missing values
    non_miss_var_list = list()  # List containing the variables names without the missing values
    miss_var_dict = dict()  # Dictionary containing the variable names and their missing value proportion

    obj_pred_lst = []  # List containing variables of object dtype
    int_pred_lst = []  # List containing variables of int dtype
    flt_pred_lst = []  # List containing variables of float dtype
    dt_pred_lst = []  # List containing variables of datetime dtype

    outlier_indices = []  # List containing the indices of the predictors with outliers

    # Methods
    def dtype_categorize(self):
        """
        Function to categorize predictors on the basis of their dtypes
        :return: Lists of grouped predictors
        """
        int_types = ['int8', 'int32', 'int64']
        flt_types = ['float32', 'float64']
        obj_types = ['object']

        cols = self.df.columns

        for col in cols:
            if self.df[col].dtypes in int_types:
                TabularClean.int_pred_lst.append(col)

            elif self.df[col].dtypes in obj_types:
                TabularClean.obj_pred_lst.append(col)

            elif self.df[col].dtypes in flt_types:
                TabularClean.flt_pred_lst.append(col)

    def dtype_sanity_check(self):
        """
        Checks if the total of lengths of the dtype lists equal to the number of dataframe columns
        :return: An interger 1 - Successful Categorization, 0 - Failed Categorization
        """
        list_len = (len(TabularClean.obj_pred_lst) + len(TabularClean.int_pred_lst) + len(TabularClean.flt_pred_lst)
                    + len(TabularClean.dt_pred_lst))

        if list_len == self.df.shape[1]:
            return 1
        else:
            return 0

    def sort_miss_vars(self):
        for ind, row in enumerate(self.df.isnull().sum()):
            if row != 0:
                TabularClean.miss_var_list.append(self.df.columns[ind])
                TabularClean.miss_var_dict.update({self.df.columns[ind]: np.round((row / len(self.df)) * 100, 2)})

            else:
                TabularClean.non_miss_var_list.append(self.df.columns[ind])

    def miss_var_prop(self):
        sorted_dict = dict(sorted(TabularClean.miss_var_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
        return sorted_dict

    def miss_nonmiss_list(self):
        return TabularClean.miss_var_list, TabularClean.non_miss_var_list

    def threshold_miss_vars(self, threshold_val: float):
        """
        Thresholding missing variables based on the missing variable proportion
        :param threshold_val: maximum proportion of missing value allowed for each variable
        :return: A tuple of lists containing filtered and rejected missing variables
        """
        thr_miss_vars = []  # List of predictors meeting the criteria
        miss_vars_thr_rej = []  # List of predictors not meeting the criteria

        for k in TabularClean.miss_var_dict.keys():
            if TabularClean.miss_var_dict[k] <= threshold_val:
                thr_miss_vars.append(k)
            else:
                miss_vars_thr_rej.append(k)

        return thr_miss_vars, miss_vars_thr_rej

    def check_outlier(self):
        """
        Checks the presence of outliers in numeric predictors.
        Outliers will be determined using the IQR technique

        :return: An integer 0 - Outlier Not Present, 1 - Outlier Present
        """
        ...

    # Initialization
    def __init__(self, df, target_variable):
        self.df = df
        self.target_variable = target_variable

    def __call__(self):

        # Lower the column Names
        self.df.columns = self.df.columns.str.lower()
        print("Dataframe Column Names have been lowered.")
        print('\n')

        # Dtype Grouping
        self.dtype_categorize()
        if self.dtype_sanity_check() != 1:
            print("Dtype Categorization did not process accurately")
