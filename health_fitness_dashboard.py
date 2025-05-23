
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Health & Fitness Dashboard", layout="wide")
st.title("🏋️ Health & Fitness Dashboard (2025)")

uploaded_file = st.file_uploader("Upload your formatted workout CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["start", "end"], dayfirst=False)

    # ✅ Fix: parse and filter valid date values
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()]

    df["workout_type"] = df["workout_type"].str.title().str.strip()

    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Date Range", [df["date"].min(), df["date"].max()])
    view_mode = st.sidebar.radio("Aggregate By", ["Day", "Week", "Month"])

    if len(date_range) == 2:
        df = df[
            (df["date"] >= pd.to_datetime(date_range[0])) &
            (df["date"] <= pd.to_datetime(date_range[1]))
        ]

    st.subheader("Workout Volume by Type")
    if view_mode == "Day":
        group = df.groupby(["date", "workout_type"]).size().reset_index(name="count")
        chart = px.bar(group, x="date", y="count", color="workout_type", title="Daily Workout Volume")
    elif view_mode == "Week":
        df["week"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit='d')
        group = df.groupby(["week", "workout_type"]).size().reset_index(name="count")
        chart = px.bar(group, x="week", y="count", color="workout_type", title="Weekly Workout Volume")
    else:
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
        group = df.groupby(["month", "workout_type"]).size().reset_index(name="count")
        chart = px.bar(group, x="month", y="count", color="workout_type", title="Monthly Workout Volume")

    st.plotly_chart(chart, use_container_width=True)
else:
    st.info("Upload a workout CSV file to get started.")
