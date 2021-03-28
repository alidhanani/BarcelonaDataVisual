#How do we divide data into different files so that we can each work independently?
#Data in different in files has different column names.(District Name vs District.Name). WTF?!?
#https://towardsdatascience.com/how-to-build-interactive-dashboards-in-python-using-streamlit-1198d4f7061b

import streamlit as st
import pandas as pd

# I was thinking it would be good for performance to read 
# all files at the start(What do you guys think?).
# All dataframes begin with "df" for ease in autocomplete (CTRL + Space)
df_unemployment = pd.read_csv('./archive/unemployment.csv')
df_population = pd.read_csv('./archive/population.csv')
df_geo = pd.read_csv("barcelona_geo.csv")

# Hard coded names and dataframe names for categories
category_dict = {
    "Population" : df_population,
    "Unemployment": df_unemployment
}

#Get values for user selection
categories = list(category_dict.keys())
districts = df_population["District.Name"].unique()
year_min = int(df_population.Year.min())
year_max = int(df_population.Year.max())
gender = df_population["Gender"].unique()

#Generate Sidebar for user selection.
#All variables start with "select" for ease in autocomplete
select_category = st.sidebar.selectbox("Category", categories)
select_year = st.sidebar.slider("Year", min_value= year_min, max_value= year_max)
select_gender = st.sidebar.radio("Gender",("Both", "Male", "Female"))
# st.sidebar.write("This is disabled")
# select_district = st.sidebar.selectbox("District", districts)

#Data Slicing
#Note that Categories is not included any condition for now,
# will probably make a switch case for that to show the correct dataframe
#For multiple conditions in df slice, always use () for each condition
selected_dataframe = category_dict.get(select_category)
st.write("The selected dataset is: " + str(select_category))
if  select_gender == "Both":
    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)]
else:
    st.write(select_gender)
    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
    & (selected_dataframe['Gender'] == select_gender)]


st.table(selected_data.head())

st.write("This is the concatenated dataframe")
summed_data = selected_data.groupby(['District.Code'])['Number'].sum().reset_index()

df_map = summed_data.merge(right = df_geo, on = "District.Code", how = "outer")
st.write(df_map.shape)
st.write("This is the merged Dataframe")
st.table(df_map.head())



