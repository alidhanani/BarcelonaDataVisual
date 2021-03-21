import streamlit as st

import pandas as pd

def get_data():
    return pd.read_csv('./archive/unemployment.csv')


df = get_data()
min_year = int(df['Year'].min()) 
max_year = int(df['Year'].max()) 
district_names = df['District Name'].unique()

st.title('Barcelona')
st.table(df.head())

st.sidebar.header('Filter Options')

selected_year = st.sidebar.slider('Year', min_year, max_year)
##df[df['Year'] == selected_year]

##selected_year = st.sidebar.selectbox('Year', list(reversed(range(2013,2018))))
selected_district = st.sidebar.selectbox('District Name', district_names)
df[(df['District Name'] == selected_district) & (df['Year'] == selected_year)]


