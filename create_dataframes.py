import os
import re
import pandas as pd


class DataPipeline:
    def __init__(self, ext_options=(".csv", ".xlsx")):
        self.ext_options = ext_options
        self.files = []
        self.unq_file_ext = []

        self.sub_f_pres = 0
        self.sub_f_name = None
        self.train_f_name = None
        self.test_f_name = None

        self.train_df = None
        self.test_df = None
        self.sub_df = None

    def scan_directory(self, path='.'):
        """
        Scans current working directory for files with allowed extensions.
        """
        self.files = [
            f for f in os.listdir(path) if f.endswith(self.ext_options)
        ]

        # Scan Detection
        for f in self.files:
            if re.findall("submission", f, re.IGNORECASE):
                self.sub_f_pres = 1
                self.sub_f_name = f

        # Unique Extensions Detection
        self.unq_file_ext = list(
            {ext for f in self.files for ext in self.ext_options if f.endswith(ext)}
        )

        # Detect Train/Test Filenames
        for f in self.files:
            if re.findall("train", f, re.IGNORECASE):
                self.train_f_name = f
            elif re.findall("test", f, re.IGNORECASE):
                self.test_f_name = f

    def load_dataframes(self):
        """
        Load Train, Test (and Submission if Available)
        """
        if not self.unq_file_ext:
            raise RuntimeError("No recognized file extensions found.")

        # Pick Extension - Assuming only 1
        ext = self.unq_file_ext[0]

        # Extension Mapping
        loaders = {
            ".csv": pd.read_csv,
            ".xlsx": pd.read_excel
        }

        if ext not in loaders:
            raise ValueError(f"Unsupported Extension: {ext}")

        reader = loaders[ext]

        # Compulsory Assignment
        self.train_df = reader(self.train_f_name)
        self.test_df = reader(self.test_f_name)

        # Optional Assignment
        if self.sub_f_pres == 1:
            self.sub_df = reader(self.sub_f_name)

        print(f"Dataframes Loaded Successfully!!")

    def sanity_check(self):
        """
        Ensures Train Dataframe is Loaded correctly.
        """
        if self.train_df is None or self.train_df.empty:
            raise Exception("DataFrame Assignment was NOT successful")
        print("Sanity Check passed: train_df is loaded")

    def run(self, path='.'):
        """
        Full Pipeline: Scan, Load, and Check
        """
        self.scan_directory(path)
        self.load_dataframes()
        self.sanity_check()
        return self
