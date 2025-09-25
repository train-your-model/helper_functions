# Imports
import numpy as np


# Working Class
class Tabular:
    """
    This class performs the following operations:
        1. Checks the presence of duplicated rows and drop them if present.
        2. Checks for the presence of degree of Class Imbalance for the given Target Variable.
        3. Checks for the presence of records with multiple values.
    """
    # Parameters
    multi_record_predictors_w_space = list()  # List of variables with multiple valued records
    multi_record_predictors_w_comma = list()
    multi_record_common = list()

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

    @classmethod
    def get_target_variable_name_idx(cls):
        return cls.target_variable_name_idx

    @classmethod
    def set_target_variable_name_idx(cls, value):
        cls.target_variable_name_idx = value

    @classmethod
    def reset_target_variable_name_idx(cls):
        cls.target_variable_name_idx = None

    # Methods
    def check_remove_dupl_val(self):
        dupl_val = self.df.duplicated().sum()

        if dupl_val != 0:
            before_drop_shape = self.df.shape()[0]
            print('There is  presence of duplicated rows in the dataset')
            self.df = self.df.drop_duplicates(inplace=True, keep='last')
            after_drop_shape = self.df.shape()[0]
            print(f'Number of duplicated rows dropped: {before_drop_shape-after_drop_shape}')

        else:
            print('Dataset is free of Duplicated rows.')

    def check_na(self):
        nan_present = len(self.df.columns[self.df.isnull().any()].tolist())
        Tabular.set_nan_values(value=nan_present)

    def check_multi_record_predictors(self):
        """
        Checks for the presence of Predictors having multiple values for a single record.
        :return: A list of predictors satisfying the above condition
        """
        specific_column_names = [col for col in self.df.columns.to_list() if self.df[col].dtypes == 'O']

        conf_code_spc, pred_list_spc = self.multi_record_w_spaces(obj_cols=specific_column_names)
        conf_code_com, pred_list_com = self.multi_record_w_comma(obj_cols=specific_column_names)

        if conf_code_spc == 1 and conf_code_com == 0:
            Tabular.multi_record_predictors_w_space.extend(pred_list_spc)
        elif conf_code_spc == 0 and conf_code_com == 1:
            Tabular.multi_record_predictors_w_comma.extend(pred_list_com)
        elif conf_code_spc == 1 and conf_code_com == 1:
            # Check for the common predictors
            common_preds :list = list(set(pred_list_spc)&set(pred_list_com))
            Tabular.multi_record_common.extend(common_preds)

    def multi_record_w_spaces(self,obj_cols):
        split_w_spaces = []
        for col in obj_cols:
            split_row_max = max(self.df[col].dropna().apply(lambda x: len(x.split(' '))))
            if split_row_max > 1:
                split_w_spaces.append(col)

        if len(split_w_spaces) != 0:
            return 1, split_w_spaces
        else:
            return 0, split_w_spaces

    def multi_record_w_comma(self, obj_cols):
        split_w_commas = []
        for col in obj_cols:
            split_row_max = max(self.df[col].dropna().apply(lambda x: len(x.split(' '))))
            if split_row_max > 1:
                split_w_commas.append(col)

        if len(split_w_commas) != 0:
            return 1, split_w_commas
        else:
            return 0, split_w_commas

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
        self.df = train_df

    def __call__(self, prob_type=None):
        """
        :param prob_type: 1 - Regression, 2 - Classification, 3 - Time Series
        """
        # Reset Class Parameters
        Tabular.reset_nan_values()
        Tabular.reset_target_variable_name()
        Tabular.reset_target_variable_name_idx()

        # Shape of the Dataframe
        print(f"Shape of the Dataframe is: {self.df.shape}")
        print('\n')

        # Check for the presence of Duplicated values
        self.check_remove_dupl_val()
        print('\n')

        # Target Variable Determination
        print(list(zip(range(len(self.df)), self.df.columns)))
        target_variable_index = int(input("Enter the index of the Target Variable: "))
        Tabular.set_target_variable_name(value=self.df.columns[target_variable_index])
        print('\n')

        # Check for the presence of Missing Values
        self.check_na()
        if Tabular.get_nan_values() != 0:
            print("Dataset HAS variables with Missing Values")
            if self.df[Tabular.get_target_variable_name()].isnull().any():
                print("Target Variable HAS Missing Values")
            else:
                print("Target Variable is free of Missing Values")
        else:
            print("Dataset has NO variables with Missing Values")

        # Check for the presence of Multi-Valued records (separated by "")
        print('\n')
        self.check_multi_record_predictors()
        if len(Tabular.multi_record_predictors_w_space) != 0 or len(Tabular.multi_record_predictors_w_comma) != 0 or len(Tabular.multi_record_common) != 0:
            print("Dataset contains variables with multi-valued records", end='\n')

            if len(Tabular.multi_record_predictors_w_space) != 0:
                print(f'List of Multi-valued Predictors, separated with spaces: {Tabular.multi_record_predictors_w_space}')
            if len(Tabular.multi_record_predictors_w_comma) != 0:
                print(f'List of Multi-valued Predictors, separated with comma: {Tabular.multi_record_predictors_w_comma}')
            if len(Tabular.multi_record_common) != 0:
                print(f'List of Multi-valued Predictors, separated with spaces and comma: {Tabular.multi_record_common}')

        else:
            print("Dataset DOES NOT contain any predictors with multi-valued records")

        # For Tabular Classification Problem Statement
        if prob_type == 2:
            self.class_imbalance()
