def thr_vals_and_count_dict(df, col, thr_val:int, operator:int) -> dict:
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
                filtered_obs.update({uniq_obs:df[col].value_counts()[uniq_obs]})
        elif operator == 0:
            if df[col].value_counts()[uniq_obs] == thr_val:
                filtered_obs.update({uniq_obs:df[col].value_counts()[uniq_obs]})
        else:
            if df[col].value_counts()[uniq_obs] > thr_val:
                filtered_obs.update({uniq_obs:df[col].value_counts()[uniq_obs]})

    sorted_dict = {k:v for k,v in sorted(filtered_obs.items(), key=lambda item: item[1])}
    return sorted_dict

