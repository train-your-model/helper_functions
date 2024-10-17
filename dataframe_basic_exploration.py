# 1
import numpy as np


def thr_vals_and_count_dict(df, col, thr_val: int, operator: int) -> dict:
    """
    A function to create a dictionary of unique column observations with their number of occurrences, when the number
    of occurrences are greater/smaller/equal to the threshold value.

    :param df: Dataframe
    :param col: Column to be considered
    :param thr_val: Threshold value to filter the column observations
    :param operator: For Comparing with the Threshold (-1: Lower, 0:Equal, 1:Greater)

    :return: A dictionary of observations and their counts as key-value pairs, sorted in an increasing order
    """
    filtered_obs = dict()
    for uniq_obs in df[col].unique():
        if operator == -1:
            if df[col].value_counts()[uniq_obs] < thr_val:
                filtered_obs.update({uniq_obs: df[col].value_counts()[uniq_obs]})
        elif operator == 0:
            if df[col].value_counts()[uniq_obs] == thr_val:
                filtered_obs.update({uniq_obs: df[col].value_counts()[uniq_obs]})
        else:
            if df[col].value_counts()[uniq_obs] > thr_val:
                filtered_obs.update({uniq_obs: df[col].value_counts()[uniq_obs]})

    sorted_dict = {k: v for k, v in sorted(filtered_obs.items(), key=lambda item: item[1])}
    return sorted_dict


# 2
def multi_valued_rows(df, pred_list, split_criteria):
    """
    To get the frequency of occurrences of different values in multiple object valued record.

    :param df: Dataframe
    :param pred_list: Columns with multi-valued records
    :param split_criteria: Criteria on the basis of which values are separated.

    :return: A dictionary with records and their occurrence frequency
    """
    ...
    for pred in pred_list:
        df[pred] = df[pred].str.lower()
        splits_list = []
        for i in range(len(df)):
            split_row = df[pred][i].split(split_criteria)
            splits_list.extend(split_row)

        col_split_dict = dict()
        for value in splits_list:
            if value not in col_split_dict.keys():
                col_split_dict.update({value: 1})
            else:
                col_split_dict.update({value: col_split_dict[value] + 1})

        yield col_split_dict


# 3
def check_multirecord_preds(df) -> list:
    """
    Checks for the presence of Predictors having multiple values for a single record.
    :param df: Dataframe in consideration
    :return: A list of predictors satisfying the above condition
    """
    col_names = [col for col in df.columns.to_list() if df[col].dtypes == 'O']
    multi_rec_preds = []
    for col in col_names:
        try:
            split_rw_mx = max(df[col].dropna().apply(lambda x: len(x.split(' '))))
            if split_rw_mx > 1:
                multi_rec_preds.append(col)

        except:
            continue

    return multi_rec_preds


# 4
def assign_unqvalues(df, colname) -> dict:
    """
    Function that assigns integer values to the unique records based on their occurrences
    :param df: Dataframe
    :param colname: Name of the predictor containing records
    :return: A dictionary with the record and their newly assigned integer values
    """

    df[colname] = df[colname].str.lower()

    pred_uniques = df[colname].unique()
    int_eqv = dict()

    for unq in pred_uniques:
        int_eqv.update({unq: (df[colname] == unq).value_counts()[0]})

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


# 5
def class_imbalance(df, targ_var):
    """
    Determine the Degree of Imbalance of a predictor containing discrete classes, based on the percentage
    of data belonging to minority class

    :param df: Dataframe
    :param targ_var: Target Variable consisting of classes
    :return: Prints the degree of imbalance in the Target Variable
    """

    min_perc = np.floor(min(df[targ_var].value_counts(1)*100))

    if min_perc in range(20, 41):
        print("Target variable has Mild Degree of Imbalance: 20-40%")
    elif min_perc in range(1, 20):
        print("Target variable has Moderate Degree of Imbalance: 1-20%")
    elif min_perc < 1:
        print("Target variable has Extreme Degree of Imbalance: <1%")
