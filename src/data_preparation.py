import os
import pandas as pd

def prepare_data(input_path, output_path):
    df = pd.read_csv(input_path)

    print(df.isnull().sum())

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("-", "_")
        .str.replace(" ", "_")
    )

    df["scheduledday"] = pd.to_datetime(df["scheduledday"])
    df["appointmentday"] = pd.to_datetime(df["appointmentday"])

    df = df[(df["age"] >= 0) & (df["age"] <= 110)]

    print(df["age"].dtype)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Processed data saved to:", output_path)




