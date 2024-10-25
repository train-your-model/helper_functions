# Imports
import numpy as np


# Working Class
class Tabular:
    """
    This class performs the following tasks:
        1. Lowers the column names.
        2. Checks the presence of duplicated rows and drop them if present.
        3. Sorts the variables into variables with and without Missing Values.
        4. Threshold the Missing Variables on the basis of given threshold value.
        5. Checks for the presence of degree of Class Imbalance for the given Target Variable.
        6. Checks for the presence of records with multiple values.
        7. Determine the frequency of single value in a multiple values record.
    """
    # Parameters
    miss_var_list = list()  # List containing variable names with missing values
    non_miss_var_list = list()  # List containing the variables names without the missing values
    miss_var_dict = dict()  # Dictionary containing the variable names and their missing value proportion
    multi_record_predictors = list()  # List containing variable names having multiple records

    # Class Methods
    @classmethod
    def get_nan_values(cls):
        return cls.nan_values

    @classmethod
    def set_nan_values(cls, value):
        cls.nan_values = value

    @classmethod
    def reset_nan_values(cls):
        cls.nan_values = None

    @classmethod
    def get_target_variable_name(cls):
        return cls.target_variable_name

    @classmethod
    def set_target_variable_name(cls, value):
        cls.target_variable_name = value

    @classmethod
    def reset_target_variable_name(cls):
        cls.target_variable_name = None

    # Methods
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
        nan_present = len(self.df.columns[self.df.isnull().any()].tolist())
        Tabular.set_nan_values(value=nan_present)

    def sort_miss_vars(self):
        for ind, row in enumerate(self.df.isnull().sum()):
            if row != 0:
                Tabular.miss_var_list.append(self.df.columns[ind])
                Tabular.miss_var_dict.update({self.df.columns[ind]: np.round((row / len(self.df)) * 100, 2)})

            else:
                Tabular.non_miss_var_list.append(self.df.columns[ind])

    def miss_var_prop(self):
        sorted_dict = dict(sorted(self.miss_var_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
        return sorted_dict

    def miss_nonmiss_list(self):
        return Tabular.miss_var_list, Tabular.non_miss_var_list

    def threshold_miss_vars(self, threshold_val: float):
        """
        Thresholding missing variables based on the missing variable proportion
        :param threshold_val: maximum proportion of missing value allowed for each variable
        :return: A tuple of lists containing filtered and rejected missing variables
        """
        thr_miss_vars = []  # List of predictors meeting the criteria
        miss_vars_thr_rej = []  # List of predictors not meeting the criteria

        for k in Tabular.miss_var_dict.keys():
            if Tabular.miss_var_dict[k] <= threshold_val:
                thr_miss_vars.append(k)
            else:
                miss_vars_thr_rej.append(k)

        return thr_miss_vars, miss_vars_thr_rej

    def check_multi_record_predictors(self) -> list:
        """
        Checks for the presence of Predictors having multiple values for a single record.
        :return: A list of predictors satisfying the above condition
        """
        specific_column_names = [col for col in self.df.columns.to_list() if self.df[col].dtypes == 'O']

        for col in specific_column_names:
            split_row_max = max(self.df[col].dropna().apply(lambda x: len(x.split(' '))))
            if split_row_max > 1:
                Tabular.multi_record_predictors.append(col)

    def class_imbalance(self):
        """
        Determine the Degree of Imbalance of a predictor containing discrete classes, based on the percentage
        of data belonging to minority class

        :return: Prints the degree of imbalance in the Target Variable
        """
        min_perc = np.floor(min(self.df[Tabular.get_target_variable_name()].value_counts(1) * 100))
        if min_perc in range(20, 41):
            print("Target variable has Mild Degree of Imbalance: 20-40%")
        elif min_perc in range(1, 20):
            print("Target variable has Moderate Degree of Imbalance: 1-20%")
        elif min_perc < 1:
            print("Target variable has Extreme Degree of Imbalance: <1%")

    # Initialization
    def __init__(self, train_df):
        Tabular.reset_nan_values()
        Tabular.reset_target_variable_name()
        self.df = train_df

    def __call__(self, class_f=0):
        print(f"Shape of the Dataframe is: {self.df.shape}")

        self.df.columns = self.df.columns.str.lower()
        print("Dataframe Column Names have been lowered.")

        # Check for the presence of Duplicated values
        self.check_remove_dupl_val()

        # Target Variable Determination
        print(list(zip(range(len(self.df)), self.df.columns)))
        target_variable_index = int(input("Enter the index of the Target Variable: "))
        Tabular.set_target_variable_name(value=self.df.columns[target_variable_index])

        # Check for the presence of Missing Values
        self.check_na()
        if Tabular.get_nan_values() != 0:
            self.sort_miss_vars()

            if Tabular.target_variable_name in Tabular.miss_var_dict.keys():
                print("Target Variable consists Missing Variable")
            else:
                print("Target Variable is free of Missing Variables")

        else:
            print("Dataset has NO variables with Missing Values")

        # Check for the presence of Multi-Valued records (separated by "")
        self.check_multi_record_predictors()
        if len(Tabular.multi_record_predictors) != 0:
            print("Dataset contains variables with multi-valued records")
        else:
            print("Dataset DOES NOT contain any predictors with multi-valued records")

        # For Tabular Classification Problem Statement
        if class_f == 1:
            self.class_imbalance()

