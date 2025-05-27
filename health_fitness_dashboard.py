
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Health & Fitness Dashboard", layout="wide")
st.title("🏋️ Health & Fitness Dashboard (2025)")

uploaded_file = st.file_uploader("Upload your formatted workout CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["start", "end"], dayfirst=False)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()]
    df["workout_type"] = df["workout_type"].str.title().str.strip()

    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Date Range", [df["date"].min(), df["date"].max()])
    view_mode = st.sidebar.radio("Aggregate By", ["Day", "Week", "Month"])

    if len(date_range) == 2:
        df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

    color_map = {
        "Pilates": "red",
        "Yoga": "orange",
        "Cycling": "black",
        "Swimming": "blue",
        "Tennis": "green"
    }

    st.subheader("Workout Volume by Type")
    if view_mode == "Day":
        group = df.groupby(["date", "workout_type"]).size().reset_index(name="count")
        chart1 = px.bar(group, x="date", y="count", color="workout_type",
                        title="Daily Workout Volume", color_discrete_map=color_map)
        chart1.update_layout(barmode="stack", xaxis=dict(tickformat="%b %d", tickangle=45, rangeslider_visible=True))
    elif view_mode == "Week":
        df["week"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit='d')
        group = df.groupby(["week", "workout_type"]).size().reset_index(name="count")
        chart1 = px.bar(group, x="week", y="count", color="workout_type",
                        title="Weekly Workout Volume", color_discrete_map=color_map)
        chart1.update_layout(barmode="stack")
    else:
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
        group = df.groupby(["month", "workout_type"]).size().reset_index(name="count")
        chart1 = px.bar(group, x="month", y="count", color="workout_type",
                        title="Monthly Workout Volume", color_discrete_map=color_map)
        chart1.update_layout(barmode="stack")

    st.plotly_chart(chart1, use_container_width=True)

    st.subheader("Calories Burned by Workout Type")
    if view_mode == "Day":
        group2 = df.groupby(["date", "workout_type"])["calories"].sum().reset_index()
        chart2 = px.bar(group2, x="date", y="calories", color="workout_type",
                        title="Daily Calories Burned", color_discrete_map=color_map)
        chart2.update_layout(barmode="stack", xaxis=dict(tickformat="%b %d", tickangle=45, rangeslider_visible=True))
    elif view_mode == "Week":
        group2 = df.groupby(["week", "workout_type"])["calories"].sum().reset_index()
        chart2 = px.bar(group2, x="week", y="calories", color="workout_type",
                        title="Weekly Calories Burned", color_discrete_map=color_map)
        chart2.update_layout(barmode="stack")
    else:
        group2 = df.groupby(["month", "workout_type"])["calories"].sum().reset_index()
        chart2 = px.bar(group2, x="month", y="calories", color="workout_type",
                        title="Monthly Calories Burned", color_discrete_map=color_map)
        chart2.update_layout(barmode="stack")

    st.plotly_chart(chart2, use_container_width=True)

    st.subheader("Heart Rate: Average vs. Max (by Workout Type)")
    if view_mode == "Day":
        hr_group = df.groupby(["date", "workout_type"]).agg(
            avg_hr=("avg_hr", "mean"),
            max_hr=("max_hr", "mean")
        ).reset_index()
        hr_group = hr_group.melt(id_vars=["date", "workout_type"], value_vars=["avg_hr", "max_hr"], var_name="HR Type", value_name="BPM")
        chart3 = px.bar(hr_group, x="date", y="BPM", color="HR Type", barmode="group", facet_col="workout_type",
                        title="Daily Avg/Max Heart Rate by Workout Type")
        chart3.update_layout(xaxis=dict(tickangle=45))
    elif view_mode == "Week":
        hr_group = df.groupby(["week", "workout_type"]).agg(
            avg_hr=("avg_hr", "mean"),
            max_hr=("max_hr", "mean")
        ).reset_index()
        hr_group = hr_group.melt(id_vars=["week", "workout_type"], value_vars=["avg_hr", "max_hr"], var_name="HR Type", value_name="BPM")
        chart3 = px.bar(hr_group, x="week", y="BPM", color="HR Type", barmode="group", facet_col="workout_type",
                        title="Weekly Avg/Max Heart Rate by Workout Type")
    else:
        hr_group = df.groupby(["month", "workout_type"]).agg(
            avg_hr=("avg_hr", "mean"),
            max_hr=("max_hr", "mean")
        ).reset_index()
        hr_group = hr_group.melt(id_vars=["month", "workout_type"], value_vars=["avg_hr", "max_hr"], var_name="HR Type", value_name="BPM")
        chart3 = px.bar(hr_group, x="month", y="BPM", color="HR Type", barmode="group", facet_col="workout_type",
                        title="Monthly Avg/Max Heart Rate by Workout Type")

    st.plotly_chart(chart3, use_container_width=True)
else:
    st.info("Upload a workout CSV file to get started.")
