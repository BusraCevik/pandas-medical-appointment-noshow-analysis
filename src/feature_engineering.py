import os
import numpy as np
import pandas as pd



def create_featured_dataset(input_path, output_path):

    df = pd.read_csv(input_path)

    # datetime columns tekrar parse
    df["scheduledday"] = pd.to_datetime(df["scheduledday"])
    df["appointmentday"] = pd.to_datetime(df["appointmentday"])

    # waiting_days
    scheduled_date = df["scheduledday"].dt.normalize()
    appointment_date = df["appointmentday"].dt.normalize()

    df["waiting_days"] = (appointment_date - scheduled_date).dt.days

    # appointment_weekday
    df["appointment_weekday"] = df["appointmentday"].dt.day_name()

    # scheduled_weekday
    df["scheduled_weekday"] = df["scheduledday"].dt.day_name()

    # scheduled_hour
    df["scheduled_hour"] = df["scheduledday"].dt.hour

    # age_group (pd.cut or np.select)
    bins = [0, 13, 18, 55, np.inf]
    labels = ["child", "teen", "adult", "senior"]

    df["age_group"] = pd.cut(
        df["age"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )

    # no_show_flag mapping
    # no_show_flag: 1 = patient did NOT attend the appointment, 0 = patient attended
    df["no_show_flag"] = (df["no_show"]=="Yes").astype(int)

    # save featured csv
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)








