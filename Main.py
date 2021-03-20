import streamlit as st
import pandas as pd


df_unemployment = pd.read_csv('./archive/unemployment.csv')
df_population = pd.read_csv('./archive/population.csv')

categories = ["Unemployment","Population","Immigrant Data"]
districts = df_unemployment["District Name"].unique()
year_min = int(df_population.Year.min())
year_max = int(df_population.Year.max())



select_category = st.sidebar.selectbox("Category", categories)
select_district = st.sidebar.selectbox("District", districts)
select_year = st.sidebar.slider("Year", min_value= year_min, max_value= year_max)


st.write("This is unemployment data")
st.table(df_unemployment.head())

st.write("This is population data")
st.table(df_population.head())