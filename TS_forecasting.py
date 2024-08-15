import numpy as np
import tensorflow as tf


class WindowGenerator:
    def __init__(self, input_width, label_width, shift,
                 train_df, val_df, label_columns = None):

        # Store the raw data
        self.df_train = train_df
        self.df_val = val_df

        # Work out the label column indices
        self.label_cols = label_columns
        if self.label_cols is not None:
            self.label_cols_indices = {name: i for i, name in enumerate(label_columns)}
        self.cols_indices = {name: i for i, name in enumerate(train_df.columns)}

        # Work out the Window Parameters
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total Window Size: {self.total_window_size}',
            f'Input Indices: {self.input_indices}',
            f'Label Indices: {self.label_indices}',
            f'Label Column name(s): {self.label_cols}'
        ])

    def split_window(self, features):
        """
        All shapes are: (batch, time, features)
        """
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_cols is not None:
            labels = tf.stack(
                [labels[:, :, self.cols_indices[name]] for name in self.label_cols]
            )

        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def make_dataset(self, data):
        """
        :param data: Time Series Dataframe
        :return: A tf.data.Dataset of (input_window, label_window) pairs
        """
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.utils.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=32
        )

        ds = ds.map(self.split_window)
        return ds

