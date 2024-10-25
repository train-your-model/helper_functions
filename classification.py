from basic_exploration import Tabular


class ClassifyTabular(Tabular):

    def __init__(self, tr_df):
        self.class_df = tr_df
        super().__init__(self.class_df)

    def __call__(self, class_f=1):
        super().__call__(class_f=1)
