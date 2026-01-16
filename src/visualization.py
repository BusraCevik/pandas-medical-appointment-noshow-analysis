import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# -----------------------------
# Color Theme
# -----------------------------
MAIN_COLOR = "#5FA8A8"
LIGHT_COLOR = "#9ED6D6"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
PINK_COLOR = "#F2B6C6"



FIG_SIZE = (8, 5)


# -----------------------------
# Shared Plot Helpers
# -----------------------------
def _save_bar_plot(df, x_col, y_col, title, ylabel, xlabel, save_path):
    """
    Generic bar plot helper for consistent styling.
    """

    plt.figure(figsize=FIG_SIZE)

    bars = plt.bar(
        df[x_col],
        df[y_col],
        color=MAIN_COLOR,
        edgecolor=DARK_COLOR,
        width=0.3
    )

    plt.title(title, color=DARK_COLOR)
    plt.ylabel(ylabel, color=DARK_COLOR)
    plt.xlabel(xlabel, color=DARK_COLOR)

    plt.grid(axis="y", color=GRID_COLOR)

    plt.xticks(color=DARK_COLOR)
    plt.yticks(color=DARK_COLOR)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f"{height:.2%}",
            ha="center",
            va="bottom",
            color=DARK_COLOR,
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


# -----------------------------
# Individual Plot Functions
# -----------------------------
def _plot_overall_noshow(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "overall_noshow_rate.csv"))

    total = int(df.loc[0, "total_patients"])
    noshow = int(df.loc[0, "noshow_number"])
    attended = total - noshow

    pie_df = pd.DataFrame({
        "status": ["Attended", "No-show"],
        "count": [attended, noshow]
    })

    fig = px.pie(
        pie_df,
        names="status",
        values="count",
        hole=0.45,
        title="Overall Appointment Attendance",
        color="status",
        color_discrete_map={
            "Attended": LIGHT_COLOR,
            "No-show": DARK_COLOR
        }
    )

    os.makedirs(fig_dir, exist_ok=True)
    fig.write_image(os.path.join(fig_dir, "overall_noshow_donut.png"))

def _plot_noshow_by_age_group(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "noshow_by_age_group.csv"))

    _save_bar_plot(
        df,
        x_col="age_group",
        y_col="noshow_rate",
        title="No-show Rate by Age Group",
        ylabel="No-show Rate",
        xlabel="Age Group",
        save_path=os.path.join(fig_dir, "noshow_by_age_group.png")

    )

def _plot_noshow_by_weekday(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "noshow_by_weekday.csv"))

    _save_bar_plot(
        df,
        x_col="appointment_weekday",
        y_col="noshow_rate",
        title="No-show Rate by Appointment Weekday",
        ylabel="No-show Rate",
        xlabel="Appointment Weekday",
        save_path=os.path.join(fig_dir, "noshow_by_weekdays.png")

    )


def _plot_noshow_by_waiting_bucket(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "noshow_by_waitingdays.csv"))

    _save_bar_plot(
        df,
        x_col="waiting_bucket",
        y_col="noshow_rate",
        title="No-show Rate by the Waiting Bucket",
        ylabel="No-show Rate",
        xlabel="Waiting Bucket",
        save_path=os.path.join(fig_dir, "noshow_by_waitingdays.png")

    )


def _plot_noshow_by_sms(csv_dir, fig_dir):
    df = pd.read_csv(os.path.join(csv_dir, "noshow_by_sms.csv"))

    df["sms_received"] = df["sms_received"].replace({
        0: "No SMS",
        1: "SMS Sent",
        "0": "No SMS",
        "1": "SMS Sent"
    })

    _save_bar_plot(
        df,
        x_col="sms_received",
        y_col="noshow_rate",
        title="No-show Rate by SMS Reminder",
        ylabel="No-show Rate",
        xlabel="SMS Received",
        save_path=os.path.join(fig_dir, "noshow_by_sms.png")
    )


def _plot_noshow_by_gender(csv_dir, fig_dir):
    df = pd.read_csv(os.path.join(csv_dir, "noshow_by_gender.csv"))

    color_map = {
        "F": PINK_COLOR,
        "M": LIGHT_COLOR,
    }

    colors = df["gender"].map(color_map)

    plt.figure(figsize=FIG_SIZE)

    bars = plt.bar(
        df["gender"],
        df["noshow_rate"],
        color=colors,
        edgecolor=DARK_COLOR,
        width=0.4
    )

    plt.title("No-show Rate by Gender", color=DARK_COLOR)
    plt.ylabel("No-show Rate", color=DARK_COLOR)
    plt.xlabel("Gender", color=DARK_COLOR)
    plt.grid(axis="y", color=GRID_COLOR)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2%}",
            ha="center",
            va="bottom",
            color=DARK_COLOR,
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "noshow_by_gender.png"), dpi=300)
    plt.close()



def generate_visualizations(csv_dir: str, fig_dir: str) -> None:
    os.makedirs(fig_dir, exist_ok=True)

    _plot_overall_noshow(csv_dir, fig_dir)
    _plot_noshow_by_age_group(csv_dir, fig_dir)
    _plot_noshow_by_weekday(csv_dir, fig_dir)
    _plot_noshow_by_waiting_bucket(csv_dir, fig_dir)
    _plot_noshow_by_sms(csv_dir, fig_dir)
    _plot_noshow_by_gender(csv_dir, fig_dir)

    print("Visualization files created in:", fig_dir)
