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


def thr_vals_and_count_dict(df, col, thr_val: int, operator: int) -> dict:
    """
    A function to create a dictionary of unique column observations with their number of occurrences, when the
    number of occurrences are greater/smaller/equal to the threshold value.

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
