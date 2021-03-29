import streamlit as st
import pandas as pd

df= pd.read_csv('./archive/unemployment.csv')

st.table(df.head())

df.rename(columns={"District Name":"District.Name"})
df.rename(columns={"District Code":"District.Code"})
df.rename(columns={"Neighborhood Name":"Neighborhood.Name"})
df.rename(columns={"District Name":"District.Name"})