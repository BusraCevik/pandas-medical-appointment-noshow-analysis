import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


# -----------------------------
# Color Theme
# -----------------------------
MAIN_COLOR = "#5FA8A8"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
BORDER_COLOR = "#000000"


def build_noshow_dashboard(csv_dir: str, featured_csv_path: str, output_html_path: str):

    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    # -----------------------------
    # Load CSVs
    # -----------------------------
    df_age = pd.read_csv(os.path.join(csv_dir, "noshow_by_age_group.csv"))
    df_weekday = pd.read_csv(os.path.join(csv_dir, "noshow_by_weekday.csv"))
    df_waiting = pd.read_csv(os.path.join(csv_dir, "noshow_by_waitingdays.csv"))
    df_sms = pd.read_csv(os.path.join(csv_dir, "noshow_by_sms.csv"))
    df_gender = pd.read_csv(os.path.join(csv_dir, "noshow_by_gender.csv"))

    df_raw = pd.read_csv(featured_csv_path)

    # Label cleanup
    df_sms["sms_received"] = df_sms["sms_received"].replace({
        0: "No SMS",
        1: "SMS Sent",
        "0": "No SMS",
        "1": "SMS Sent"
    })

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    total_appointments = len(df_raw)
    noshow_count = df_raw["no_show_flag"].sum()
    noshow_rate = round((noshow_count / total_appointments) * 100, 2)

    # -----------------------------
    # Build Figure
    # -----------------------------
    fig = go.Figure()

    # 0 — Age Group
    fig.add_trace(go.Bar(
        x=df_age["age_group"],
        y=df_age["noshow_rate"],
        name="Age Group",
        marker_color=MAIN_COLOR,
        visible=True
    ))

    # 1 — Weekday
    fig.add_trace(go.Bar(
        x=df_weekday["appointment_weekday"],
        y=df_weekday["noshow_rate"],
        name="Weekday",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    # 2 — Waiting Bucket
    fig.add_trace(go.Bar(
        x=df_waiting["waiting_bucket"],
        y=df_waiting["noshow_rate"],
        name="Waiting Time",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    # 3 — SMS
    fig.add_trace(go.Bar(
        x=df_sms["sms_received"],
        y=df_sms["noshow_rate"],
        name="SMS Reminder",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    # 4 — Gender
    fig.add_trace(go.Bar(
        x=df_gender["gender"],
        y=df_gender["noshow_rate"],
        name="Gender",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    # -----------------------------
    # Layout
    # -----------------------------
    fig.update_layout(
        title=dict(text="No-show Rate by Age Group", x=0.5),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_COLOR),
        margin=dict(t=80),
        yaxis=dict(
            title="No-show Rate",
            gridcolor=GRID_COLOR,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor=BORDER_COLOR,
            mirror=True
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor=BORDER_COLOR,
            mirror=True
        ),
        bargap=0.6
    )

    plot_html = pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs="cdn",
        div_id="noshowChart"
    )

    # -----------------------------
    # Write HTML
    # -----------------------------
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(f"""
<html>
<head>
<title>Medical Appointment No-show Dashboard</title>
</head>

<body style="background:#FAFEFE; font-family:Arial;">

<h1 style="color:{DARK_COLOR}; text-align:center;">
Medical Appointment No-show Dashboard
</h1>

<!-- SUMMARY CARD -->
<div style="
    max-width: 520px;
    margin: 20px auto;
    padding: 22px;
    border-radius: 16px;
    background-color: #EAF6F6;
    text-align: center;
    color: {DARK_COLOR};
    font-size: 18px;
    line-height: 1.8;
">
<b>Total Appointments:</b> {total_appointments}<br>
<b>No-show Count:</b> {noshow_count}<br>
<b>Overall No-show Rate:</b> {noshow_rate}%
</div>

<!-- DROPDOWN -->
<div style="text-align:center; margin-top:20px;">
<select id="metricSelect" style="
    padding:10px 16px;
    border-radius:10px;
    border:1px solid #BFDCDC;
    font-size:15px;
    color:{DARK_COLOR};
" onchange="updateChart()">
    <option value="0">Age Group</option>
    <option value="1">Appointment Weekday</option>
    <option value="2">Waiting Time Bucket</option>
    <option value="3">SMS Reminder</option>
    <option value="4">Gender</option>
</select>
</div>

<!-- GRAPH CARD -->
<div style="
    max-width: 1100px;
    margin: 25px auto;
    padding: 30px;
    border: 1px solid #E6F2F2;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    background-color: white;
">
{plot_html}
</div>

<script>
function updateChart() {{
    const val = document.getElementById("metricSelect").value;
    let visibility = [false, false, false, false, false];
    visibility[val] = true;

    let titles = [
        "No-show Rate by Age Group",
        "No-show Rate by Appointment Weekday",
        "No-show Rate by Waiting Time Bucket",
        "No-show Rate by SMS Reminder",
        "No-show Rate by Gender"
    ];

    Plotly.restyle("noshowChart", "visible", visibility);
    Plotly.relayout("noshowChart", {{
        title: {{ text: titles[val], x: 0.5 }}
    }});
}}
</script>

</body>
</html>
""")

    print("Dashboard created at:", output_html_path)
