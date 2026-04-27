import streamlit as st
import pandas as pd
from data_cleaning import load_data, clean_data
import matplotlib.pyplot as plt

# Pre processing
trains_raw_df = load_data()
trains_df = clean_data(trains_raw_df)

st.title("SBB Trains per Route")
st.write("Here you can explore a real-life dataset from SBB.")

st.subheader("Preview")
st.dataframe(trains_df)

st.subheader("Dataset information")
st.write("Rows:", trains_df.shape[0])
st.write("Columns:", trains_df.shape[1])
st.write(trains_df.dtypes)

#Barplot of Trains per month
total_trains_per_month = trains_df.groupby("bezugsmonat").agg(
    dtv_bezugsmonat = ("dtv_bezugsmonat", "sum"),
    dtv_p_bezugsmonat = ("dtv_p_bezugsmonat", "sum"),
    dtv_g_bezugsmonat =("dtv_g_bezugsmonat", "sum")
).reset_index()

st.bar_chart(data=total_trains_per_month, x = "bezugsmonat", y = {"dtv_p_bezugsmonat", "dtv_g_bezugsmonat"}, stack = True)

#Müll
#st.map(data=total_trains_per_month, latitude=None, longitude=None)
#fig, ax = plt.subplots()
#ax.bar("bezugsmonat", "dtv_bezugsmonat")


