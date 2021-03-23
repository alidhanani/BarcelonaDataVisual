import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
# from vega_datasets import data
# st.set_option('deprecation.showPyplotGlobalUse', False)
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Unemployment', 'Immigrants(Nationality)', 'Transport')
# )
# st.sidebar.button("sample")



path = "./archive/"

st.title('Initial Data Viewer')

data = pd.read_csv(path + 'unemployment.csv')
st.bar_chart(data["District Name"])

fig= sns.displot(data = data, x="District Name", discrete = True, kind = "hist")
st.pyplot(fig)

fig, ax = plt.subplots()
ax.hist(data["District Name"])
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
st.pyplot(fig)

fig, ax = plt.subplots()
ax.hist(data["Neighborhood Name"])
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=7)
st.pyplot(fig)

# source = data.wheat()

# st.table(source.head())

fig = alt.Chart(data).mark_bar().encode(
    x="Year",
    y="Number",
    column = "District Name",
    color="Year"
).properties(width=60)
st.write(fig)

st.table(data.head())



