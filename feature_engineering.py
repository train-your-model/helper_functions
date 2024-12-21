# 1 Function to Binarize Features
def binarize(df, feat, thr):
    """
    Function that binarize numeric features based on a threshold value

    :param df: Dataframe
    :param feat: array of numeric values that need to be binarized
    :param thr: Threshold value for the features to be binned
    :return: A list of binarized values of the features
    """
    from sklearn.preprocessing import Binarizer

    x = df[feat].values
    x = x.reshape(1, -1)
    binarizer = Binarizer(thr)
    transform = binarizer.fit_transform(x)
    return transform

# 2 Function to Create Custom Quarter Determination
def custom_qtr_determination(start_month, end_month, df_col):
    """
    :param start_month: Starting Month of Fiscal Year
    :param end_month: Ending Month of Fiscal Year
    :param df_col: Dataframe Columns/ List containing Months that need to be binned
    :return: A list with quarter numbers for the corresponding month
    """
    month_range = [x for x in range(1, 13)]
    max_month_ind = month_range.index(max(month_range))

    start_month_ind = month_range.index(start_month)
    end_month_ind = month_range.index(end_month)

    from_strt = [x for x in range(start_month_ind, max_month_ind + 1)]
    to_end = [x for x in range(0, end_month_ind + 1)]

    rearrg_lst = from_strt + to_end

    financial_months = [month_range[x] for x in rearrg_lst]
    financial_month_bins = financial_months[::3]

    qtr_lst = []
    for month in df_col:
        if financial_month_bins[0] <= month < financial_month_bins[1]:
            qtr_lst.append(1)
        elif financial_month_bins[1] <= month < financial_month_bins[2]:
            qtr_lst.append(2)
        elif financial_month_bins[2] <= month < financial_month_bins[3]:
            qtr_lst.append(3)
        elif financial_month_bins[3] <= month < financial_month_bins[0]:
            qtr_lst.append(4)

    return qtr_lst
