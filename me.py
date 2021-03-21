import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_data():
    return pd.read_csv('./archive/unemployment.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)

df = get_data()
min_year = int(df['Year'].min()) 
max_year = int(df['Year'].max()) 
district_names = df['District Name'].unique()
neighborhood_names = df['Neighborhood Name'].unique()

st.title('Barcelona')

#st.table(df.head())

st.sidebar.header('Filter Options')

selected_year = st.sidebar.slider('Year', min_year, max_year)

selected_district = st.sidebar.selectbox('District Name', district_names)

#selected_neighborhood = st.sidebar.selectbox('Neighborhood Name', neighborhood_names)
df1 = df[(df['District Name'] == selected_district) 
        & (df['Year'] == selected_year)]
       # & (df['Neighborhood Name'] == selected_neighborhood)]

df1

#number per Neighborhood
st.write("Number per Neighborhood")
d1 = df1.groupby(df['Neighborhood Name'])['Number'].sum()
d1

#number per gender
st.write("Number per Gender")
d2 = df1.groupby(df['Gender'])['Number'].sum()
d2

#number per month
st.write("Number per Month")
d3 = df1.groupby(df['Month'])['Number'].sum()
d3

d3.hist()
plt.show()
st.pyplot()

st.bar_chart(d3['Month'])