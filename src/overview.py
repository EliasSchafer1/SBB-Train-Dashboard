from datetime import date
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from map_maker import draw_map
import plotly.express as px
from layout import sbb_header
from data_store import get_trains_df

trains_df = get_trains_df()

#display sbb header
sbb_header("Home SBB Trains per Month")
st.write("Welcome on the Dashboard of the Project SBB Trains Per Month! " \
"Here you can explore a real-life dataset from SBB " \
"containing the number of passenger and freight trains for each SBB route section in Switzerland. " \
"Have fun!")
st.space("large")

c1, c2, c3 = st.columns(3)
c1.metric("Rows", trains_df.shape[0])
c2.metric("Columns", trains_df.shape[1])
c3.metric("Missing values", trains_df.isna().sum().sum())
st.space("large")


c1, c2 = st.columns([3, 1], gap = "large")
with c1:
    st.subheader("Preview")
    st.dataframe(trains_df)
with c2:
    st.subheader("Missing Values")
    st.write(trains_df.isna().sum())
st.space("large")


years = [2024, 2025]
ref_cols = ["dtv_reference_month", "dtv_previous_year_month"]
p_cols = ["dtv_p_reference_month", "dtv_p_previous_year_month"]
g_cols = ["dtv_g_reference_month", "dtv_g_previous_year_month"]

# Barplots per month
st.subheader("Passenger and Freight Trains by Month")
st.write("This chart shows the monthly average of daily trains across all route sections, split by passenger and freight.")
c1, c2 = st.columns(2, gap="large")
for i, col in enumerate([c1, c2]):
    with col:
        st.markdown(f"**{years[i]}**")
        avg_per_month = trains_df.groupby("reference_month").agg(
            passenger_trains=(p_cols[i], "mean"),
            freight_trains=(g_cols[i], "mean")
        ).reset_index()
        fig = px.bar(avg_per_month, x="reference_month", y=["passenger_trains", "freight_trains"],
                     barmode="stack",
                     labels={"value": "Average Daily Trains", "variable": "Train Type"},
                     color_discrete_map={"passenger_trains": "#F67469", "freight_trains": "#D50000"})
        st.plotly_chart(fig, width="stretch")

# Top 10 Route Sections
st.subheader("Top 10 Route Sections by Average Daily Trains")
st.write("This chart shows the average daily number of passenger and freight trains on the ten busiest route sections.")
c3, c4 = st.columns(2, gap="large")
for i, col in enumerate([c3, c4]):
    with col:
        st.markdown(f"**{years[i]}**")
        top_10 = trains_df.groupby("section").agg(
            avg_trains=(ref_cols[i], "mean"),
            passenger_trains=(p_cols[i], "mean"),
            freight_trains=(g_cols[i], "mean")
        ).reset_index()
        top_10 = top_10.sort_values("avg_trains", ascending=False).head(10)
        fig = px.bar(top_10, x="section", y=["passenger_trains", "freight_trains"],
                     barmode="stack",
                     labels={"value": "Average Daily Trains", "variable": "Train Type"},
                     color_discrete_map={"passenger_trains": "#F67469", "freight_trains": "#D50000"})
        st.plotly_chart(fig, width="stretch")

# Distribution of Average Daily Trains
st.subheader("Distribution of Average Daily Trains")
st.write("This histogram shows the distribution of average daily trains across all route sections.")
c5, c6 = st.columns(2, gap="large")
for i, col in enumerate([c5, c6]):
    with col:
        st.markdown(f"**{years[i]}**")
        avg_per_section = trains_df.groupby("section")[ref_cols[i]].mean().reset_index()
        fig = px.histogram(avg_per_section, x=ref_cols[i],
                           nbins=60,
                           color_discrete_sequence=["#D50000"],
                           labels={ref_cols[i]: "Average Daily Trains"})
        fig.update_yaxes(title_text="Number of Route Sections")
        fig.update_traces(xbins=dict(start=0, size=30)) # Fixed size bins anchored at zero
        fig.update_xaxes(range=[0, avg_per_section[ref_cols[i]].max() * 1.05], dtick=100)
        st.plotly_chart(fig, width="stretch")
        


st.subheader("Handle Missing Values")

# fill missing previous-year train counts with column mean
if st.button("Fill missing previous-year values (mean)"):
    cols = [
        "dtv_previous_year_month",
        "dtv_p_previous_year_month",
        "dtv_g_previous_year_month",
    ]

    for col in cols:
        trains_df[col] = trains_df[col].fillna(
            trains_df[col].mean()
        )

    st.success("Missing values filled")
    st.rerun()

st.dataframe(trains_df.dtypes.astype(str))