import os
import numpy as np
import pandas as pd


def noshow_analysis(input_path, output_path):

    df = pd.read_csv(input_path)

    os.makedirs(output_path, exist_ok=True)

    # Overall no-show rate
    total_number = len(df)
    noshow_number = df["no_show_flag"].sum()
    noshow_rate = noshow_number / total_number

    overall_noshow_rate = pd.DataFrame([{
        "total_patients": total_number,
        "noshow_number": noshow_number,
        "noshow_rate": noshow_rate,
        "confidence_weight": 1.0
    }])

    overall_noshow_rate.to_csv(
        os.path.join(output_path, "overall_noshow_rate.csv"),
        index=False
    )

    # No-show rate by age_group
    noshow_by_age_group = (
        df.groupby("age_group")
          .agg(
              total_patients=("no_show_flag", "size"),
              noshow_number=("no_show_flag", lambda x: (x == 1).sum()),
              noshow_rate=("no_show_flag", lambda x: (x == 1).mean())
          )
          .reset_index()
    )

    noshow_by_age_group["confidence_weight"] = (
        noshow_by_age_group["total_patients"]
        / noshow_by_age_group["total_patients"].sum()
    )

    noshow_by_age_group.to_csv(
        os.path.join(output_path, "noshow_by_age_group.csv"),
        index=False
    )

    # No-show rate by appointment_weekday

    noshow_by_weekday = (
        df.groupby(["appointment_weekday_num", "appointment_weekday"])
        .agg(
            total_patients=("no_show_flag", "size"),
            noshow_number=("no_show_flag", lambda x: (x == 1).sum()),
            noshow_rate=("no_show_flag", lambda x: (x == 1).mean())
        )
        .reset_index()
        .sort_values("appointment_weekday_num")
    )

    noshow_by_weekday["confidence_weight"] = (
            noshow_by_weekday["total_patients"]
            / noshow_by_weekday["total_patients"].sum()
    )

    noshow_by_weekday = noshow_by_weekday.drop(columns="appointment_weekday_num")

    noshow_by_weekday.to_csv(
        os.path.join(output_path, "noshow_by_weekday.csv"),
        index=False
    )

    # No-show rate by waiting_bucket
    waiting_days_bucket = (
        df.groupby("waiting_bucket")
          .agg(
              total_patients=("no_show_flag", "size"),
              noshow_number=("no_show_flag", lambda x: (x == 1).sum()),
              noshow_rate=("no_show_flag", lambda x: (x == 1).mean())
          )
          .reset_index()
    )

    waiting_days_bucket["confidence_weight"] = (
        waiting_days_bucket["total_patients"]
        / waiting_days_bucket["total_patients"].sum()
    )

    waiting_days_bucket.to_csv(
        os.path.join(output_path, "noshow_by_waitingdays.csv"),
        index=False
    )

    # No-show rate by SMS received
    noshow_by_sms = (
        df.groupby("sms_received")
          .agg(
              total_patients=("no_show_flag", "size"),
              noshow_number=("no_show_flag", lambda x: (x == 1).sum()),
              noshow_rate=("no_show_flag", lambda x: (x == 1).mean())
          )
          .reset_index()
    )

    noshow_by_sms["confidence_weight"] = (
        noshow_by_sms["total_patients"]
        / noshow_by_sms["total_patients"].sum()
    )

    noshow_by_sms.to_csv(
        os.path.join(output_path, "noshow_by_sms.csv"),
        index=False
    )

    # No-show rate by gender
    noshow_by_gender = (
        df.groupby("gender")
          .agg(
              total_patients=("no_show_flag", "size"),
              noshow_number=("no_show_flag", lambda x: (x == 1).sum()),
              noshow_rate=("no_show_flag", lambda x: (x == 1).mean())
          )
          .reset_index()
    )

    noshow_by_gender["confidence_weight"] = (
        noshow_by_gender["total_patients"]
        / noshow_by_gender["total_patients"].sum()
    )

    noshow_by_gender.to_csv(
        os.path.join(output_path, "noshow_by_gender.csv"),
        index=False
    )
