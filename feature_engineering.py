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
