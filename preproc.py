# Imports
import numpy as np


class TabularClean:
    """
    This class performs the following operations:
        1. Categorizes predictors based on their dtypes
        2. Sorts the variables into variables with and without Missing Values.
        3. Threshold the Missing Variables on the basis of given threshold value.
        4. Checks for the presence of outliers in the predictors of the dataframe.
        5. Checks for the presence of row indices within the missing variables where the records have missing values.
    """
    # Parameters
    miss_var_list = list()  # List containing variable names with missing values
    non_miss_var_list = list()  # List containing the variables names without the missing values
    miss_var_dict = dict()  # Dictionary containing the variable names and their missing value proportion

    commn_missvars_indx = list() # List containing the indices of rows with all Missing Values

    obj_pred_lst = []  # List containing variables of object dtype
    int_pred_lst = []  # List containing variables of int dtype
    flt_pred_lst = []  # List containing variables of float dtype
    dt_pred_lst = []  # List containing variables of datetime dtype

    predictors_with_outliers = []  # List containing the names of the predictors with outliers

    # Methods
    def parameters_reset(self):
        """
        :return: Class parameters at their initial state of empty lists.
        """
        TabularClean.var_list = []
        TabularClean.non_miss_var_list = []
        TabularClean.miss_var_list = []

        TabularClean.obj_pred_lst = []
        TabularClean.int_pred_lst = []
        TabularClean.flt_pred_lst = []
        TabularClean.dt_pred_lst = []

    def clean_df_col_names(self):
        "Removes the white-spaces from the column names"
        self.df.columns = list(map(lambda x: x.strip(), self.df.columns))

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
        :return: An integer 1 - Successful Categorization, 0 - Failed Categorization
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
        for col in TabularClean.int_pred_lst + TabularClean.flt_pred_lst:
            q1, q3 = np.percentile(np.array(self.df[col]), [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - (iqr * 1.5)
            upper_bound = q3 + (iqr * 1.5)
            outlier_sum = sum(np.where((np.array(self.df[col]) > upper_bound) | (np.array(self.df[col]) < lower_bound),
                                       1, 0))
            if outlier_sum != 0:
                TabularClean.predictors_with_outliers.append(col)

    def preds_with_outliers(self) -> list:
        return TabularClean.predictors_with_outliers

    def check_allrow_nan(self) -> int:
        """
        Function to check if the Dataframe consists of rows with missing variables for that particular row
        :return: A list of indices where all the records of the rows have missing values
        """
        func_copy = self.df.fillna('None')
        col_ind_dict = {}

        for col in TabularClean.miss_var_list:
            row_idx = []
            for i in range(self.df.shape[0]):
                if func_copy[col][i] == 'None':
                    row_idx.append(i)

            col_ind_dict.update({col: row_idx})

        indxs = [v for _,v in col_ind_dict.items()]
        indxs_len = len(indxs)

        commn_indxs = []
        for i in range(indxs_len - 1):
            if len(commn_indxs) == 0:
                tmp_indx = np.intersect1d(indxs[i], indxs[i + 1])
                commn_indxs.extend(tmp_indx)
            else:
                tmp_indx = np.intersect1d(indxs[i], indxs[i + 1])
                new_commn_indxs = np.intersect1d(tmp_indx, commn_indxs)
                commn_indxs = new_commn_indxs

        if len(commn_indxs) == 0:
            print("There are NO instances where the Missing Values are present at particular row indices.")
            return 0
        else:
            print(f"There are {len(commn_indxs)} instances where the Missing Values are present at particular row indices.")
            TabularClean.commn_missvars_indx = commn_indxs
            return len(commn_indxs)

    @staticmethod
    def check_neg_columns(df, num_dtype_columns: list) -> list:
        """
        A function to check for the presence of numeric dtype columns with negative columns
        :param df: Dataframe in consideration
        :param num_dtype_columns: Columns of numeric dtypes
        :return: A list of column names having negative value(s)
        """
        col_vals = df[num_dtype_columns].describe().loc['min'].values
        neg_cols = []
        for ind, vals in enumerate(col_vals):
            if vals < 0:
                col_name = num_dtype_columns[ind]
                neg_cols.append(col_name)
        return neg_cols

    # Initialization
    def __init__(self, df, target_variable=None):
        self.df = df
        self.target_variable = target_variable

    def __call__(self, prob_type=None, miss_var_present=None):
        """
        :param prob_type: 1 - Regression, 2 - Classification
        :param miss_var_present: 0: Missing Value Variable NOT Present, 1: Missing Value Variable IS Present
        """
        # Parameters Reset
        self.parameters_reset()

        # Standardizing the column Names
        self.df.columns = self.df.columns.str.lower()
        self.clean_df_col_names()
        print("Dataframe Column Names have been lowered.", end='\n')

        # Dtype Grouping
        if self.dtype_sanity_check() != 1:
            print("Dtype Categorization did not process accurately", end='\n')

        # Missing Value Variable
        if miss_var_present == 1:
            self.sort_miss_vars()
            self.check_allrow_nan()

        # Lowering the name of the Target variable before being looked-up in the lists
        if self.target_variable in TabularClean.int_pred_lst:
            TabularClean.int_pred_lst.remove(self.target_variable.str.lower())
        elif self.target_variable in TabularClean.flt_pred_lst:
            TabularClean.flt_pred_lst.remove(self.target_variable.str.lower())

        # Checking for the Outliers in the Predictors
        self.check_outlier()

        if len(TabularClean.predictors_with_outliers) == 0:
            print("There are NO outliers present in the Integer dtype predictors.", end="\n")
        else:
            print("There is presence of outliers in the numerical predictors.")
            print(f"The Predictors are: {TabularClean.predictors_with_outliers}", end="\n")

        # Checking for the presence of negative values in integer dtype predictors
        negative_columns = []
        if (len(TabularClean.int_pred_lst) != 0) or (len(TabularClean.int_pred_lst) != 0):
            if (len(TabularClean.int_pred_lst) != 0):
                negative_columns = TabularClean.check_neg_columns(df=self.df,
                                                                  num_dtype_columns=TabularClean.int_pred_lst)
            elif (len(TabularClean.flt_pred_lst) != 0):
                negative_columns = TabularClean.check_neg_columns(df=self.df,
                                                                  num_dtype_columns=TabularClean.flt_pred_lst)
        if len(negative_columns) == 0:
            print("No Negative values bearing Columns in the Dataframe", end="\n")
        else:
            print("Presence of Columns bearing Negative Values.", end="\n")
            print(f"Name(s) of above-mentioned columns: {negative_columns}", end="\n")
