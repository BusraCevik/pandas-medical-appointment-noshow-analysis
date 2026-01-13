import os
import pandas as pd

def prepare_data(input_path, output_path):
    df = pd.read_csv(input_path)

    df.isnull().sum()
    print(df.isnull().sum())


