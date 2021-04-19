###################################################
#How do we divide data into different files so that we can each work independently?
#Data in different in files has different column names.(District Name vs District.Name). WTF?!?
#https://towardsdatascience.com/how-to-build-interactive-dashboards-in-python-using-streamlit-1198d4f7061b

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json # library to handle JSON files
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import requests # library to handle requests
import numpy as np
import folium # map rendering library
from streamlit_folium import folium_static
from plotly.subplots import make_subplots
import time
# from Compare import Compare, DesignSideBarText


st.set_page_config(layout="wide", page_title='Barcelona Data')
LoadData = st.title("Barcelona Data Load")
my_bar = st.progress(0)
for i in range(100):
    my_bar.progress(i + 1)
    time.sleep(0.01)

my_bar.empty()  # Remove the progress bar
LoadData.title("")

# # I was thinking it would be good for performance to read 
# # all files at the start(What do you guys think?).
# # All dataframes begin with "df" for ease in autocomplete (CTRL + Space)
df_unemployment = pd.read_csv('./archive/unemployment.csv')
df_population = pd.read_csv('./archive/population.csv')
df_immigrants_by_nationality = pd.read_csv('./archive/immigrants_by_nationality.csv')
df_immigrants_emigrants_by_age = pd.read_csv('./archive/immigrants_emigrants_by_age.csv')
df_immigrants_emigrants_by_sex = pd.read_csv('./archive/immigrants_emigrants_by_sex.csv')
df_geo = pd.read_csv("barcelona_geo.csv")

#############################################
#https://plotly.com/python/bubble-charts/
df_immigrant_sum = df_immigrants_by_nationality.groupby(['Nationality','Year'])['Number'].sum().reset_index()
df_immigrant_sum.columns = ["Nationality","Year","Number"]
st.write(df_immigrant_sum.columns)
import plotly.express as px
fig = px.scatter(df_immigrant_sum, x="Number", y="Year",
	         size="Number", color="Nationality",
                 hover_name="Nationality", log_x=True, size_max=100)
st.write("If I swap X axis and y axis, it doesnt work. What mistake am I making?")
st.plotly_chart(fig, use_container_width= True)
############################################


#############################################
#https://plotly.com/python/bubble-charts/
df_population_sum = df_population.groupby(['District.Name','Year'])['Number'].sum().reset_index()
df_population_sum.columns = ["District.Name","Year","Number"]
st.write(df_population_sum.columns)
import plotly.express as px
fig = px.scatter(df_population_sum, x="Year", y="Number",
	         size="Number", color="District.Name",
                 hover_name="District.Name", log_x=True, size_max=20)
st.write("If I swap X axis and y axis, it doesnt work. What mistake am I making?")
st.plotly_chart(fig, use_container_width= True)
############################################


#############################################
#https://plotly.com/python/line-charts/

df_unemployment_sum = df_unemployment.groupby(['District.Name','Year'])['Number'].sum().reset_index()
df_unemployment_sum.columns = ["District.Name","Year","Number"]
st.table(df_unemployment_sum.head())
# df = px.data.gapminder().query("continent != 'Asia'") # remove Asia for visibility
fig = px.line(df_unemployment_sum, x="Year", y="Number", color="District.Name",
               hover_name="District.Name")

st.plotly_chart(fig)
############################################

#############################################
#https://plotly.com/python/time-series/
df_unemployment_sum = df_unemployment.groupby(['District.Name','Year'])['Number'].sum().reset_index()
df_unemployment_sum.columns = ["District.Name","Year","Number"]
st.table(df_population_sum.head())
# df = px.data.gapminder().query("continent != 'Asia'") # remove Asia for visibility
fig = px.bar(df_population_sum, x="Year", y="Number", color="District.Name",
               hover_name="District.Name", barmode='group')

st.plotly_chart(fig)
############################################



#############################################
#https://plotly.com/python/pie-charts/
df_population_sum = df_population.groupby(['Age'])['Number'].sum().reset_index()
df_population_sum.columns = ["Age","Number"]
st.table(df_population_sum.head())
fig = px.pie(df_population_sum, values='Number', names='Age', color_discrete_sequence=px.colors.sequential.RdBu)

st.plotly_chart(fig)
############################################