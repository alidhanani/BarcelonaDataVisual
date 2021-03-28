#How do we divide data into different files so that we can each work independently?
#Data in different in files has different column names.(District Name vs District.Name). WTF?!?
#https://towardsdatascience.com/how-to-build-interactive-dashboards-in-python-using-streamlit-1198d4f7061b

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json # library to handle JSON files
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import requests # library to handle requests
import numpy as np
import folium # map rendering library
from streamlit_folium import folium_static

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
# st.write("The selected dataset is: " + str(select_category))
if  select_gender == "Both":
    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)]
else:
    # st.write(select_gender)
    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)
    & (selected_dataframe['Gender'] == select_gender)]


# st.table(selected_data.head())

# st.write("This is the concatenated dataframe")
summed_data = selected_data.groupby(['District.Code'])['Number'].sum().reset_index()

df_map = summed_data.merge(right = df_geo, on = "District.Code", how = "outer")
# st.write(df_map.shape)
# st.write("This is the merged Dataframe")
# st.table(df_map.head())


data_all = df_map
data_geo = json.load(open('shapefiles_barcelona_distrito.geojson'))

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
        line_opacity=0.2,
        legend_name=dicts[data],
        highlight=True,
        reset=True).add_to(map_sby)

    folium.LayerControl().add_to(map_sby)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['n_distri',data],
                                                        aliases=['District.Name: ', dicts[data]],
                                                        labels=True))                                                       
    folium_static(map_sby)

centers = center()

select_maps = st.sidebar.selectbox(
    "What data do you want to see?",
    ("OpenStreetMap", "Stamen Terrain","Stamen Toner")
)
select_data = st.sidebar.radio(
    "What data do you want to see?",
    ("Total_Pop",)
)

map_sby = folium.Map(tiles=select_maps, location=[centers[0], centers[1]], zoom_start=12)
st.title('Map of Barca')

data_all['District.Name'] = data_all['District.Name'].str.title()
# data_all = data_all.replace({'District':'Pabean Cantikan'},'Pabean Cantian')
# data_all = data_all.replace({'District':'Karangpilang'},'Karang Pilang')

dicts = {
    "Total_Pop":'Number',
}

for idx in range(10):
    data_geo['features'][idx]['properties']['Total_Pop'] = int(data_all['Number'][idx])
    # data_geo['features'][idx]['properties']['Total_Pop'] = int(data_all['Total Population'][idx])
    # data_geo['features'][idx]['properties']['Male_Pop'] = int(data_all['Male Population'][idx])
    # data_geo['features'][idx]['properties']['Female_Pop'] = int(data_all['Female Population'][idx])
    # data_geo['features'][idx]['properties']['Area_Region'] = float(data_all['Areas Region(km squared)'][idx])

show_maps(select_data, threshold(select_data))


def get_data():
    return pd.read_csv('./archive/unemployment.csv')



st.sidebar.header('Comparing')
df = get_data()
min_year = int(df['Year'].min()) 
max_year = int(df['Year'].max()) 
district_names = df['District Name'].unique()
#selected_year = st.sidebar.slider('Year', min_year, max_year)
neighborhood_names = df['Neighborhood Name'].unique()
# selected_district_1 = st.sidebar.selectbox('District Name 1', district_names)
# selected_district_2 = st.sidebar.selectbox('District Name 2', district_names)

num_dist = st.sidebar.text_input('Number of district')
all_dist = [] 
if num_dist == "":
    num_dist = "0"
for i in range(0, int(num_dist)):
	all_dist.append(st.sidebar.selectbox('District Name '+str(i), district_names))

dataframes = []
for i in all_dist:
	df4 = df[(df['District Name'] == i) 
        & (df['Year'] == select_year)]
       # & (df['Neighborhood Name'] == selected_neighborhood)]
	df4 = df4.groupby(df4["Gender"])["Number"].sum()
	dataframes.append(df4)

newData = []
for i in range(len(dataframes)-1):
	newData.append(pd.merge(dataframes[i], dataframes[i+1], on='Gender'))


for i in newData:
	df6 = i.T
	df6.plot.bar(rot=15, title="Compare unemployment")
	plt.show(block=True)
	st.pyplot()
