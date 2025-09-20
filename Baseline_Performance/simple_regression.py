# Imports
from sklearn.model_selection import train_test_split as tts
import tensorflow as tf
from tensorflow.keras import layers, Model, losses


class BaselineTF:
    """"
    Assumption:
        1. The dataframe presented at this point, HAS NOT been preprocessed.
    Checks for the Baseline performance based on a given metric, for a given dataset.
    Applicable for Single output Regression Prediction.
    """

    @classmethod
    def get_seed_value(cls):
        return cls.seed_value

    @classmethod
    def set_seed_value(cls, val):
        cls.seed_value = val

    @classmethod
    def reset_seed_value(cls):
        cls.seed_value = None

    def get_all_inputs(self):
        return self.all_inputs

    def update_all_inputs(self, k, v):
        self.all_inputs[k] = v

    def get_encoded_feat(self):
        return self.encoded_features

    def add_encoded_feat(self, item):
        self.encoded_features.append(item)

    def reorder_df(self):
        "Makes it certain that the Target Variable is at position -1"
        if self.target_variable_idx != -1:
            cols_to_move = self.df.columns[self.target_variable_idx]
            rem_cols = [col for col in self.df.columns if col not in cols_to_move]
            ## New Reordered Dataframe
            self.df = self.df[rem_cols+cols_to_move]

    def df_filtering(self):
        "Creates separate variables with Training Predictors and Target Variable"
        train_df = self.df.copy()
        targ_name = train_df.columns[-1]
        X = train_df.iloc[:,:-1]
        y = train_df.loc[:,targ_name].astype(int)
        return X, y

    def split_size(self):
        "Generates the Split Sizes for Training and Test Data"
        df_len = len(self.df)
        tr_splt = 1-int(0.8 * df_len)
        ts_splt = 0.5-int(df_len - tr_splt)
        return tr_splt, ts_splt

    def seed_gene(self):
        import random
        min_val = 0
        max_val = 2**32-1
        s_val = random.randint(min_val, max_val)
        self.set_seed_value(val=s_val)

    def train_test_splt(self, train_pred, test_var):
        "Creates the dataframe split for Train, Validation and Test Split"
        tst_splt, val_splt = self.split_size()
        self.seed_gene()
        X_train, X_temp, y_train, y_temp = tts(train_pred, test_var, test_size=tst_splt,
                                               random_state=self.get_seed_value())
        X_val, X_test, y_val, y_test = tts(X_temp, y_temp, test_size=val_splt,
                                           random_state=self.get_seed_value())
        return X_train, X_val, X_test, y_train, y_val, y_test

    def df_to_dataset(self, X, y=None, shuffle=True):
        "Builds a Data Pipeline from the Pandas Dataframe"
        ds = tf.data.Dataset.from_tensor_slices((dict(X)))
        if y is not None:
            ds = tf.data.Dataset.from_tensor_slices((dict(X), y))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(X), seed=self.get_seed_value())
        ds = ds.batch(32).prefetch(tf.data.AUTOTUNE)
        return ds

    def get_normalizer_layer(self,ds, col):
        "Normalizes the Numeric Predictors"
        normalizer = layers.Normalization(axis=None)
        feature_ds = ds.map(lambda x,y: x[col])
        normalizer.adapt(feature_ds)
        return normalizer

    def normalize_num_preds(self, ds):
        for col in self.num_preds_lst:
            num_col = tf.keras.Input(shape=(1,), name=col)
            norm_layer = self.get_normalizer_layer(ds=ds, col=col)
            encoded_norm_layer = norm_layer(num_col)
            self.update_all_inputs(k=col, v=num_col)
            self.add_encoded_feat(item=encoded_norm_layer)

    def get_str_cat_encoding_layer(self, ds, col, max_tokens=None):
        "Creates a layer that turns strings into integer indices"
        indx = layers.StringLookup(max_tokens=max_tokens)
        feature_ds = ds.map(lambda x,y: x[col])
        indx.adapt(feature_ds)
        encoder = layers.CategoryEncoding(num_tokens=index.vocabulary_size())
        return lambda feature: encoder(indx(feature))

    def encode_str_cat_preds(self, ds):
        for col in self.str_cat_preds_lst:
            max_tk = ds.nunique()
            str_col = tf.keras.Input(shape=(1,), name=col, dtype='string')
            encoding_layer = self.get_str_cat_encoding_layer(ds=ds, col=col, max_tokens=max_tk)
            encoding_cat_col = encoding_layer(str_col)
            self.update_all_inputs(k=col, v=str_col)
            self.add_encoded_feat(item=encoding_cat_col)

    def __init__(self, df, target_variable_idx, num_preds_lst:list = None, str_cat_preds_lst:list = None,
                 int_cat_preds_lst:list = None):

        self.all_inputs = dict()
        self.encoded_features = list()
        self.df = df
        self.target_variable_idx = target_variable_idx
        self.num_preds_lst : list = num_preds_lst
        self.str_cat_preds_lst : list = str_cat_preds_lst
        self.int_cat_preds_lst: list = int_cat_preds_lst

    def __call__(self):
        # Initialization
        self.reset_seed_value()
        self.reorder_df()

        # Dataframe Splitting
        X, y = self.df_filtering()
        X_train, X_val, X_test, y_train, y_val, y_test = self.train_test_splt(train_pred=X, test_var=y)
        train_ds = self.df_to_dataset(X=X_train, y=y_train, shuffle=True)
        val_ds = self.df_to_dataset(X=X_val, y=y_val, shuffle=False)
        test_ds = self.df_to_dataset(X=X_test, y=y_test, shuffle=False)

        # Preprocessing
        if self.num_preds_lst is not None:
            self.normalize_num_preds(ds=train_ds)

        if self.cat_preds_lst is not None:
            self.encode_str_cat_preds(ds=train_ds)

        # Create, Compile and Training Model
        all_features = layers.concatenate(self.get_encoded_feat())
        x = layers.Dense(32, activation='relu')(all_features)
        x=layers.Dropout(0.5)(x)
        output = layers.Dense(1)(x)

        model = Model(all_inputs, output)

        model.compile(optimizer='adam', loss = losses.MeanSquaredError(), metrics=['accuracy'], run_eagerly=True)

        model.fit(train_ds, epochs=10, validation_data=val_ds)

        result = model.evaluate(test_ds, return_dict=True)
        print(f'Expected Baseline Accuracy from the Model: {result["accuracy"]*100}')