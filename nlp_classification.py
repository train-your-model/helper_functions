import numpy as np
from tensorflow.keras.layers import TextVectorization, Embedding


class RnnClassify:

    def __init__(self, df, texts_ind: int, labels_ind: int):
        self.df = df
        self.texts_ind = texts_ind
        self.labels_ind = labels_ind
        self.vectorization_hparams()

    def __call__(self):
        # DataFrame Split into Texts and Labels
        self.texts, self.labels = self.split_df()

        # Vectorization
        print(self.vectorization_hparams())
        params_updt = int(input("Do you want to change any of the given default hyperparameter values? : "))
        if params_updt == 1:
            ...

    def split_df(self):
        """
        Function to split the given dataframe into different lists of predictors and labels.
        :return: Returns 2 separate lists each containing Texts and Labels
        """
        texts_arr = np.array(self.df.iloc[:, self.texts_ind])
        labels_arr = np.array(self.df.iloc[:, self.labels_ind])

        return texts_arr, labels_arr

    def words_per_sample(self, arr):
        """
        Returns the median number of words per sample Array.
        :return: int; median number of words per sample
        """
        num_words = [len(s.split()) for s in arr]
        return np.median(num_words)

    def vectorization_hparams(self):
        hparams_dict = {
            max_tok : 500,
            opseq_len : self.words_per_sample(arr=self.texts)
        }
        return hparams_dict
