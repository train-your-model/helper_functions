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


# 3 Function to determine the next values in the set of sequence of arrays
def univariate_seq_det(x_array, y_array, x_pred: list, save_model=False) -> list:
    """
    :param x_array: Given set of Labels - Can be used for Train Data
    :param y_array: Given set of Values - Can be used for Train Data
    :param x_pred: Provided separately, for the predictions to be made
    :param save_model: When True, saves the trained model into the working directory
    :return: An array of predictions from the saved model in the function
    """
    # Imports
    from keras import Sequential
    from keras.layers import Dense
    import numpy as np
    from keras.callbacks import EarlyStopping

    # Model Architecture
    model = Sequential([
        Dense(units=1, input_shape=[1])
    ])

    # Model Compilation
    model.compile(optimizer='sgd', loss='mean_squared_error')

    # Model Training
    stop_early = EarlyStopping(monitor='loss', patience=3)
    model.fit(x=x_array, y=y_array, epochs=150, callbacks=[stop_early])

    # Save Model
    model.save("univariate_model.h5")

    # Making Prediction
    preds = model.predict(list(x_pred))

    # Formatting
    preds = preds.tolist()

    return preds
