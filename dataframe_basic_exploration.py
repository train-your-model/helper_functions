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
        8.
        9.
    """

    # Properties

    @property
    def nan_vals(self):
        return self.nan_vals

    @nan_vals.setter
    def nan_vals(self, val):
        self.nan_vals = val

    @property
    def targvar_name(self):
        return self.targvar_name

    @targvar_name.setter
    def targvar_name(self, val):
        self.targvar_name = val

    def __init__(self, train_df):
        self.df = train_df
        self.targvar_name = ""
        self.miss_vars_list = []
        self.non_miss_var_list = []
        self.miss_var_dict = dict()

    def __call__(self, class_f=0):
        print(f"Shape of the Dataframe is: {self.df.shape}")

        self.stand_col_names()
        self.check_remove_dupl_val()

        print(list(zip(range(len(self.df)), self.df.columns)))
        targvar_ind = int(input("Enter the index of the Target Variable: "))
        self.targvar_name = self.df.columns[targvar_ind]

        self.check_na()
        if self.nan_vals != 0:
            self.sort_miss_vars()
        else:
            print('Dataset has NO Variables with Missing Values')

        if class_f == 1:  # Classification Problem Statement
            self.class_imbalance()

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
        self.nan_vals = len(self.df.columns[self.df.isnull().any()].tolist())

    def sort_miss_vars(self):
        for ind, row in enumerate(self.df.isnull().sum()):
            if row != 0:
                self.miss_var_list.append(self.df.columns[ind])
                self.miss_var_dict.update({self.df.columns[ind]: np.round((row / len(self.df)) * 100, 2)})

            else:
                self.non_miss_var_list.append(self.df.columns[ind])

    def miss_var_prop(self):
        sorted_dict = dict(sorted(self.miss_var_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
        return sorted_dict

    def miss_n_nonmiss(self):
        return self.miss_vars_list, self.non_miss_var_list

    def miss_vars_thr(self, miss_var_prop_dict, thr_val: float):
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

    def class_imbalance(self, targ_var):
        """
        Determine the Degree of Imbalance of a predictor containing discrete classes, based on the percentage
        of data belonging to minority class

        :param targ_var: Target Variable consisting of classes
        :return: Prints the degree of imbalance in the Target Variable
        """

        min_perc = np.floor(min(self.df[targ_var].value_counts(1) * 100))

        if min_perc in range(20, 41):
            print("Target variable has Mild Degree of Imbalance: 20-40%")
        elif min_perc in range(1, 20):
            print("Target variable has Moderate Degree of Imbalance: 1-20%")
        elif min_perc < 1:
            print("Target variable has Extreme Degree of Imbalance: <1%")

    def thr_vals_and_count_dict(self, col, thr_val: int, operator: int) -> dict:
        """
        A function to create a dictionary of unique column observations with their number of occurrences, when the number
        of occurrences are greater/smaller/equal to the threshold value.

        :param col: Column to be considered
        :param thr_val: Threshold value to filter the column observations
        :param operator: For Comparing with the Threshold (-1: Lower, 0:Equal, 1:Greater)

        :return: A dictionary of observations and their counts as key-value pairs, sorted in an increasing order
        """
        filtered_obs = dict()
        for uniq_obs in self.df[col].unique():
            if operator == -1:
                if self.df[col].value_counts()[uniq_obs] < thr_val:
                    filtered_obs.update({uniq_obs: self.df[col].value_counts()[uniq_obs]})
            elif operator == 0:
                if self.df[col].value_counts()[uniq_obs] == thr_val:
                    filtered_obs.update({uniq_obs: self.df[col].value_counts()[uniq_obs]})
            else:
                if self.df[col].value_counts()[uniq_obs] > thr_val:
                    filtered_obs.update({uniq_obs: self.df[col].value_counts()[uniq_obs]})

        sorted_dict = {k: v for k, v in sorted(filtered_obs.items(), key=lambda item: item[1])}
        return sorted_dict

    def check_multirecord_preds(self) -> list:
        """
        Checks for the presence of Predictors having multiple values for a single record.
        :return: A list of predictors satisfying the above condition
        """
        col_names = [col for col in self.df.columns.to_list() if self.df[col].dtypes == 'O']
        multi_rec_preds = []
        for col in col_names:
            try:
                split_rw_mx = max(self.df[col].dropna().apply(lambda x: len(x.split(' '))))
                if split_rw_mx > 1:
                    multi_rec_preds.append(col)

            except:
                continue

        return multi_rec_preds

    def multi_valued_rows(self, pred_list, split_criteria):
        """
        To get the frequency of occurrences of different values in multiple object valued record.
        :param pred_list: Columns with multi-valued records
        :param split_criteria: Criteria on the basis of which values are separated.

        :return: A dictionary with records and their occurrence frequency
        """
        ...
        for pred in pred_list:
            self.df[pred] = self.df[pred].str.lower()
            splits_list = []
            for i in range(len(self.df)):
                split_row = self.df[pred][i].split(split_criteria)
                splits_list.extend(split_row)

            col_split_dict = dict()
            for value in splits_list:
                if value not in col_split_dict.keys():
                    col_split_dict.update({value: 1})
                else:
                    col_split_dict.update({value: col_split_dict[value] + 1})

            yield col_split_dict

    def assign_unqvalues(self, colname) -> dict:
        """
        Function that assigns integer values to the unique records based on their occurrences
        :param colname: Name of the predictor containing records
        :return: A dictionary with the record and their newly assigned integer values
        """

        self.df[colname] = self.df[colname].str.lower()

        pred_uniques = self.df[colname].unique()
        int_eqv = dict()

        for unq in pred_uniques:
            int_eqv.update({unq: (self.df[colname] == unq).value_counts()[0]})

        top_k = list()
        top_v = 0
        for k, v in int_eqv.items():
            if len(top_k) == 0:
                top_k.append(k)

            else:
                if v > top_v:
                    top_v = v
                    top_k.insert(0, k)

                else:
                    for i in top_k[1:]:
                        if v > int_eqv[i]:
                            top_k.insert(top_k.index(i), k)

        mod_dict = {}
        for i, j in zip(top_k, range(1, len(top_k) + 1)):
            mod_dict.update({i: j})

        return mod_dict
