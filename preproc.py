# Imports
import numpy as np


class TabularClean:
    """
    This class performs the following operations:
        1. Categorizes predictors based on their dtypes
        2. Sorts the variables into variables with and without Missing Values.
        3. Threshold the Missing Variables on the basis of given threshold value.
        4. Checks for the presence of outliers in the predictors of the dataframe.
    """
    # Parameters
    miss_var_list = list()  # List containing variable names with missing values
    non_miss_var_list = list()  # List containing the variables names without the missing values
    miss_var_dict = dict()  # Dictionary containing the variable names and their missing value proportion

    obj_pred_lst = []  # List containing variables of object dtype
    int_pred_lst = []  # List containing variables of int dtype
    flt_pred_lst = []  # List containing variables of float dtype
    dt_pred_lst = []  # List containing variables of datetime dtype

    predictors_with_outliers = []  # List containing the names of the predictors with outliers

    # Methods
    def dtype_categorize(self):
        """
        Function to categorize predictors on the basis of their dtypes
        :return: Lists of grouped predictors - int, float, object
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

        return (TabularClean.int_pred_lst, TabularClean.flt_pred_lst, TabularClean.obj_pred_lst,
                TabularClean.dt_pred_lst)

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

        :return: A class list containing the names of the predictors with outliers
        """
        for col in TabularClean.int_pred_lst:
            q1, q3 = np.percentile(np.array(self.df[col]), [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - (iqr * 1.5)
            upper_bound = q3 + (iqr * 1.5)
            outlier_sum = sum(np.where((np.array(self.df[col]) > upper_bound) | (np.array(self.df[col]) < lower_bound),
                                       1, 0))
            if outlier_sum != 0:
                TabularClean.predictors_with_outliers.append(col)

    # Initialization
    def __init__(self, df, target_variable):
        self.df = df
        self.target_variable = target_variable
        # Reset the Class Parameters
        TabularClean.int_pred_lst = TabularClean.flt_pred_lst = TabularClean.obj_pred_lst = TabularClean.dt_pred_lst = []

    def __call__(self, prob_type=None, miss_var_present=None):
        """
        :param prob_type: 1 - Regression, 2 - Classification
        :param miss_var_present: 0: Missing Value Variable NOT Present, 1: Missing Value Variable IS Present
        """

        # Lower the column Names
        self.df.columns = self.df.columns.str.lower()
        print("Dataframe Column Names have been lowered.")
        print('**'*20)

        # Dtype Grouping
        self.dtype_categorize()
        if self.dtype_sanity_check() != 1:
            print("Dtype Categorization did not process accurately")
        print('\n')

        # Missing Value Variable
        if miss_var_present == 1:
            self.sort_miss_vars()

        if self.target_variable in TabularClean.int_pred_lst:
            TabularClean.int_pred_lst.remove(self.target_variable)

        # Checking for the Outliers in the Predictors
        self.check_outlier()

        if len(TabularClean.predictors_with_outliers) == 0:
            print("There are NO outliers present in the Integer dtype predictors.")
        else:
            print("There is presence of outliers in the integer dtype predictors.")
            print(f"The Predictors are: {TabularClean.predictors_with_outliers}")
