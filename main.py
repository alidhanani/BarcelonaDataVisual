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
from Compare import Compare, DesignSideBarText



st.set_page_config(layout="wide", page_title='Barcelona Data')
LoadData = st.title("Barcelona Data Load")
my_bar = st.progress(0)
for i in range(100):
    my_bar.progress(i + 1)
    time.sleep(0.01)

my_bar.empty()  # Remove the progress bar
LoadData.title("")

# I was thinking it would be good for performance to read 
# all files at the start(What do you guys think?).
# All dataframes begin with "df" for ease in autocomplete (CTRL + Space)
df_unemployment = pd.read_csv('./archive/unemployment.csv')
df_population = pd.read_csv('./archive/population.csv')
df_immigrants_by_nationality = pd.read_csv('./archive/immigrants_by_nationality.csv')
df_immigrants_emigrants_by_age = pd.read_csv('./archive/immigrants_emigrants_by_age.csv')
df_immigrants_emigrants_by_sex = pd.read_csv('./archive/immigrants_emigrants_by_sex.csv')
df_geo = pd.read_csv("barcelona_geo.csv")

# Hard coded names and dataframe names for categories
category_dict = {
    "Population" : df_population,
    "Unemployment": df_unemployment,
    "Immigrants By Nationality": df_immigrants_by_nationality
    # "Immigrants By Age": df_immigrants_emigrants_by_age,
    # "Immigrants By Sex": df_immigrants_emigrants_by_sex
}


categories = list(category_dict.keys())
districts = df_population["District.Name"].unique()
year_min = int(df_population.Year.min())
year_max = int(df_population.Year.max())
gender = df_population["Gender"].unique()
nationalities = np.sort(df_immigrants_by_nationality["Nationality"].unique())
age = np.sort(df_immigrants_emigrants_by_age['Age'].unique())


#Generate Sidebar for user selection.
#All variables start with "select" for ease in autocomplete
select_category = st.sidebar.selectbox("Category", categories)
select_year = st.sidebar.slider("Year", min_value= year_min, max_value= year_max)
selected_dataframe = category_dict.get(select_category)


if select_category == "Population":
    select_gender = st.sidebar.radio("Gender",("Both", "Male", "Female"))
    select_age = st.sidebar.selectbox("Age", age)

    if  select_gender == "Both":
        selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
        & (selected_dataframe['Age'] == select_age)]
    else:
        selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
        & (selected_dataframe['Gender'] == select_gender)
        & (selected_dataframe['Age'] == select_age)]
    
    year_data = df_unemployment.groupby(['Year'])['Number'].sum()
    age_data = df_population.groupby(['Age'])['Number'].sum()
    gender_data = df_unemployment.groupby(['District.Name'])['Number'].sum()

    

elif select_category == "Unemployment":
    select_gender = st.sidebar.radio("Gender",("Both", "Male", "Female"))

    if  select_gender == "Both":
        selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)]
    else:
        selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
        & (selected_dataframe['Gender'] == select_gender)]

elif select_category == "Immigrants By Nationality":
    select_nationality = st.sidebar.selectbox("Nationality", nationalities)

    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
        & (selected_dataframe['Nationality'] == select_nationality)]
    year_data = df_immigrants_by_nationality.groupby(['Year'])['Number'].sum()
    age_data = df_immigrants_emigrants_by_age.groupby(['Age'])['Number'].sum()
    gender_data = df_immigrants_by_nationality.groupby(['District.Name'])['Number'].sum()
    
elif select_category == "Immigrants By Age":
    select_age = st.sidebar.selectbox("Age", age)

    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
        & (selected_dataframe['Age'] == select_age)]


elif select_category == "Immigrants By Sex":
    select_gender = st.sidebar.radio("Gender",("Both", "Male", "Female"))

    if  select_gender == "Both":
        selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)]
    else:
        selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
        & (selected_dataframe['Gender'] == select_gender)]

summed_data = selected_data.groupby(['District.Code'])['Number'].sum().reset_index()
df_map = summed_data.merge(right = df_geo, on = "District.Code", how = "outer")
df_map = df_map.fillna(0)
###################################################


data_all = df_map
data_geo = json.load(open('shapefiles_barcelona_distrito.geojson'))
map1, map2, map3 = st.beta_columns(3)
def center():
    address = 'Barcelona, Spain'
    geolocator = Nominatim(user_agent="id_explorer")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

def threshold(data):
    threshold_scale = np.linspace(data_all[dicts[data]].min(),
                              data_all[dicts[data]].max(),
                              10, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale

def show_maps(data, threshold_scale):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_all,
        columns=['District.Name',dicts[data]],
        key_on='feature.properties.n_distri',
        threshold_scale=threshold_scale,
        fill_color='YlOrRd', 
        fill_opacity=0.7, 
        line_opacity=0.5,
        legend_name=dicts[data],
        highlight=True,
        reset=True).add_to(map_sby)

    folium.LayerControl().add_to(map_sby)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['n_distri',data],
                                                        aliases=['District.Name: ', dicts[data]],
                                                        labels=True))                                                       
    with map2:
        folium_static(map_sby)

centers = center()

select_data = st.sidebar.radio(
    "What data do you want to see?",
    ("Total_Pop",)
)

map_sby = folium.Map(width='100%', height='100%', left='0%', top='0%', position='relative',tiles="Stamen Terrain", location=[centers[0], centers[1]], zoom_start=12)

#map2.markdown("<h1 style='text-align: center; color: red;'>Barcelona</h1>", unsafe_allow_html=True)

data_all['District.Name'] = data_all['District.Name'].str.title()


dicts = {
    "Total_Pop":'Number',
}

for idx in range(10):
    data_geo['features'][idx]['properties']['Total_Pop'] = int(data_all['Number'][idx])


show_maps(select_data, threshold(select_data))

###########################################################
## Show Home Map
###########################################################
col1, col2, col3 = st.beta_columns(3)
# year_data = df_immigrants_by_nationality.groupby(['Year'])['Number'].sum()
# age_data = df_immigrants_emigrants_by_age.groupby(['Age'])['Number'].sum()
# gender_data = df_immigrants_by_nationality.groupby(['District.Name'])['Number'].sum()

year_data.plot.bar(rot=15, title='Nationality', color=['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'])
plt.show(block=True)
col1.pyplot()

gender_data.plot.bar(rot=15, title='District', color=['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'])
plt.xticks(rotation=90)
plt.show(block=True)
col3.pyplot()

age_data.plot.bar(rot=15, title='Age', color=['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'])
plt.xticks(rotation=90)
plt.show(block=True)
col2.pyplot()

###########################################################
## Compare Work
###########################################################

st.sidebar.header('Comparing')

col1, col2, col3 = st.beta_columns(3)
making_textbox = DesignSideBarText()
all_dist = making_textbox.making_textbox()

st.set_option('deprecation.showPyplotGlobalUse', False)
unemploy = Compare('./archive/unemployment.csv')
unemploy.makeDataframe(all_dist, select_year, 'Gender')
unemploy.showFigure('Unemploy', col1)

st.set_option('deprecation.showPyplotGlobalUse', False)
unemploy = Compare('./archive/unemployment.csv')
unemploy.makeDataframe(all_dist, select_year, 'Gender')
unemploy.showFigure('Unemploy', col2)

st.set_option('deprecation.showPyplotGlobalUse', False)
unemploy = Compare('./archive/unemployment.csv')
unemploy.makeDataframe(all_dist, select_year, 'Gender')
unemploy.showFigure('Unemploy', col3)

# population = Compare('./archive/population.csv')
# population.makeDataframe(all_dist, select_year, 'Age')
# population.showFigure('Population',col2)

# immigration = Compare('./archive/immigrants_by_nationality.csv')
# immigration.makeDataframe(all_dist, select_year, 'Nationality')
# immigration.showFigure('Nationality',col3)