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
from Fact import fact_table
import plotly.express as px

st.set_page_config(layout="wide", page_title='Explore Barcelona!')

# @st.cache
def load_csv():
    df_unemployment = pd.read_csv('./archive/unemployment.csv')
    df_population = pd.read_csv('./archive/population.csv')
    df_immigrants_by_nationality = pd.read_csv('./archive/immigrants_by_nationality.csv')
    df_immigrants_emigrants_by_age = pd.read_csv('./archive/immigrants_emigrants_by_age.csv')
    df_immigrants_emigrants_by_sex = pd.read_csv('./archive/immigrants_emigrants_by_sex.csv')
    df_deaths = pd.read_csv('./archive/deaths.csv')
    df_births = pd.read_csv('./archive/births.csv')
    df_geo = pd.read_csv("barcelona_geo.csv")
    return df_unemployment, df_population, df_immigrants_by_nationality, df_immigrants_emigrants_by_age, df_immigrants_emigrants_by_sex,df_deaths,df_births,df_geo

df_unemployment, df_population, df_immigrants_by_nationality, df_immigrants_emigrants_by_age,df_immigrants_emigrants_by_sex,df_deaths,df_births,df_geo = load_csv()


x = fact_table(df_population,df_unemployment,df_deaths,
               df_immigrants_by_nationality,df_immigrants_emigrants_by_age,
               df_immigrants_emigrants_by_sex,df_births)

@st.cache(suppress_st_warning=True)
def makingProgressBar():
    my_bar = st.progress(0)
    for i in range(100):
        my_bar.progress(i + 1)
        time.sleep(0.01)
    my_bar.empty()  # Remove the progress bar

makingProgressBar()

# Hard coded names and dataframe names for categories
category_dict = {
    "Key Trends": df_population,
    "Yearly Data (Population)" : df_population,
    "Yearly Data (Immigration)": df_immigrants_by_nationality,
    "Immigrants (By Nationality)": df_immigrants_by_nationality,
    "District Comparison":df_population
}


categories = list(category_dict.keys())
districts = df_population["District.Name"].unique()
year_min = int(df_population.Year.min())
year_max = int(df_population.Year.max())
gender = df_population["Gender"].unique()
nationalities = np.sort(df_immigrants_by_nationality["Nationality"].unique())
age = np.sort(df_immigrants_emigrants_by_age['Age'].unique())


#Generate Sidebar for user selection.

st.sidebar.title("Explore Barcelona!")
st.sidebar.write("This App will inform you of the key statistics about the beautiful city of Barcelona. ")
#All variables start with "select" for ease in autocomplete
select_category = st.sidebar.selectbox("Dashboard", categories)
selected_dataframe = category_dict.get(select_category)

if select_category == "Immigrants (By Nationality)":
    select_year = st.sidebar.slider("Year", 
        min_value= int(2015), 
        max_value= int(df_population.Year.max()))
    select_nationality = st.sidebar.selectbox("Nationality", nationalities)
    # selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)]
    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year) & (selected_dataframe['Nationality'] == select_nationality)]
elif select_category == "Yearly Data (Population)" or select_category == "Yearly Data (Immigration)" or select_category == "District Comparison":
    select_year = st.sidebar.slider("Year", 
        min_value= int(2015), 
        max_value= int(df_population.Year.max()))
    selected_data = selected_dataframe[(selected_dataframe['Year'] == select_year)]
elif select_category == "Key Trends":
    st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("<h4 style='text-align: left; color: black;'>Tip: You can interact with each chart by hovering over the values and clicking the respective buttons on the top right corner of each figure. You can also interact with the legend by clicking and double clicking.</h4>", unsafe_allow_html=True)


####################################################################################    
# if select_category != 'Immigrants (By Nationality)':
map1, map2 = st.beta_columns(2)
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
                              5, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    # threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale

def show_maps(data, other_data, district_name, death, immigrants, births,threshold_scale):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_all,
        columns=['District.Name',dicts[data], dicts[other_data], dicts[death], dicts[immigrants], dicts[births]],
        key_on='feature.properties.n_distri',
        threshold_scale=threshold_scale,
        fill_color='YlGn', 
        fill_opacity=0.7, 
        line_opacity=0.5,
        legend_name=dicts[data],
        highlight=True,
        reset=True).add_to(map_sby)

    folium.LayerControl().add_to(map_sby)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['n_distri','Total_Pop', 'Unemplyment', 'Deaths', 'Immigrants', 'Births'],
                                                        aliases=['District.Name: ', dicts[data], dicts[other_data], dicts[death], dicts[immigrants], dicts[births]],
                                                        labels=True))                                                       
    if select_category == "Immigrants (By Nationality)":
        with map1:
            folium_static(map_sby)
    elif select_category != "District Comparison" and select_category != 'Key Trends':
        with map1:
            folium_static(map_sby)

centers = center()


if select_category != "District Comparison" and select_category != 'Key Trends' :
    
    if select_category == 'Yearly Data (Population)' :
        with map2:
            st.markdown("<h4 style='text-align: center; color: black;'>Key Facts</h4>", unsafe_allow_html=True)
            pop_data_table = x.get_pop_facts(select_year) 
            pop_data_table =pop_data_table.rename(columns={"Count": "Citizens" })
            st.table(pop_data_table)
    elif select_category == 'Yearly Data (Immigration)':
        with map2:
            st.markdown("<h4 style='text-align: center; color: black;'>Key Facts</h4>", unsafe_allow_html=True)
            img_fact_table = x.get_immigration_facts(select_year).rename(columns={"Count": "Immigrants"})
            st.table(img_fact_table)
    elif select_category == 'Immigrants (By Nationality)':
        with map2:
            st.markdown("<h4 style='text-align: center; color: black;'>Top 10 Popular Neighborhoods for "+select_nationality+"</h4>", unsafe_allow_html=True)
            df_fact_table =x.get_immigration_nationality_facts(select_year,select_nationality)
            df_fact_table =df_fact_table.rename(columns={"Fact": "District", "Category": "Neighborhood", "Count":"People("+select_nationality+")"})
            st.table(df_fact_table)
    # ##########################################################
    df_pop_data = x.merge_df()
    df_pop_data = df_pop_data[df_pop_data.Year == select_year]

    summed_data = selected_data.groupby(['District.Code'])['Number'].sum().reset_index().rename(columns={"Number": "Selected Population"})
    summed_data = summed_data.merge(right = df_geo, on = "District.Code", how = "outer")

    df_map = df_pop_data.merge(right = summed_data, on = ["District.Code"], how = "outer")
    df_map = df_map.fillna(0)
    df_map = df_map.rename(columns={"Population": "Total Population", "Unemployment": "Total Unemployment",
                                    "Deaths": "Total Deaths", "Immigrants": "Total Immigrants",
                                    "Births": "Total Births", "District.Name_x" : "District.Name"})
    data_all = df_map
    # ###################################################
    select_data = "Total_Pop"
    other_data = "Unemplyment"
    district_name = "District_Name"
    deaths = "Deaths"
    immigrants = "Immigrants"
    births = "Births"

    map_sby = folium.Map(width='100%', height='100%', left='0%', top='0%', position='relative',tiles="Stamen Terrain", location=[centers[0], centers[1]], zoom_start=12)


    data_all['District.Name'] = data_all['District.Name'].str.title()


    dicts = {
        "Total_Pop":'Selected Population',
        "Unemplyment": 'Total Unemployment',
        "District_Name": 'District.Name',
        "Deaths": 'Total Deaths',
        "Immigrants": 'Total Immigrants',
        "Births": 'Total Births',
    }

    tooltip_text = []
    for idx in range(10):
        tooltip_text.append(str(data_all['Selected Population'][idx])+ ' / '+str(data_all['Total Population'][idx])+' inhabitants')
    
    tooltip_text_total_pop = []
    for idx in range(10):
        tooltip_text_total_pop.append(str(data_all['Total Population'][idx])+ ' inhabitants')
    
    tooltip_text_distict = []
    for idx in range(10):
        tooltip_text_distict.append(str(data_all['District.Name'][idx]))

    tooltip_text_unemploy = []
    for idx in range(10):
        tooltip_text_unemploy.append(str(data_all['Total Unemployment'][idx])+ ' unemployees')
    
    tooltip_text_deaths = []
    for idx in range(10):
        tooltip_text_deaths.append(str(data_all['Total Deaths'][idx])+ ' deaths')
    
    tooltip_text_immigrants = []
    for idx in range(10):
        tooltip_text_immigrants.append(str(data_all['Total Immigrants'][idx])+ ' immigrants')
    
    tooltip_text_births = []
    for idx in range(10):
        tooltip_text_births.append(str(data_all['Total Births'][idx])+ ' births')

    for idx in range(10):
        index = int(data_geo['features'][idx]['properties']['c_distri'])
        data_geo['features'][idx]['properties']['Total_Pop'] = tooltip_text[index-1]
        data_geo['features'][idx]['properties']['Unemplyment'] = tooltip_text_unemploy[index-1]
        data_geo['features'][idx]['properties']['District_Name'] = tooltip_text_distict[index-1]
        data_geo['features'][idx]['properties']['Deaths'] = tooltip_text_deaths[index-1]
        data_geo['features'][idx]['properties']['Immigrants'] = tooltip_text_immigrants[index-1]
        data_geo['features'][idx]['properties']['Births'] = tooltip_text_births[index-1]


    show_maps(select_data, other_data, district_name,deaths,immigrants,births,threshold(select_data))

###########################################################
## Show Home Map
###########################################################
#https://plotly.com/python/builtin-colorscales/
if select_category != "District Comparison" :
    
    if select_category == "Key Trends":
        col1, col2 = st.beta_columns(2)
        with col1: 
            df_sum = df_population.groupby(['District.Name','Year'])['Number'].sum().reset_index()
            df_sum.columns = ["District","Year","Population"]
            st.markdown("<h5 style='text-align: center; color: black;'>Yearly Population By District(2013-2017)</h5>", unsafe_allow_html=True)
            fig = px.line(df_sum, x="Year", y="Population", color="District",
                        hover_name="Population", color_discrete_sequence=px.colors.qualitative.Prism)#diverging.Portland)
            fig.update_xaxes(tick0=2013, dtick=1)
            fig.update_layout(
                plot_bgcolor="white",
                margin=dict(t=10,l=10,b=10,r=10)
            )            
            st.plotly_chart(fig, use_container_width= False)
            df_immigrant_sum = df_immigrants_by_nationality[(df_immigrants_by_nationality['Nationality'] != 'Spain') ]
            df_immigrant_sum = df_immigrant_sum.groupby(['Year','District.Name'])['Number'].sum().reset_index()
            df_immigrant_sum.columns = ["Year","District","Immigrants"]
            st.markdown("<h5 style='text-align: center; color: black;'>Immigrants By District (Each color represents a unique district)</h5>", unsafe_allow_html=True)
            fig = px.bar(df_immigrant_sum, x="Year", y="Immigrants", color="District", 
            color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_xaxes(tick0=2015, dtick=1)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10)
            )
            #st.write("The stack itself represents the total number of immigrants in Barcelona whereas each color represents a different district within the city")
            st.plotly_chart(fig, use_container_width=False)
        with col2:
            df_unemployment_sum = df_unemployment.groupby(['District.Name','Year'])['Number'].sum().reset_index()
            df_unemployment_sum.columns = ["District","Year","Number"]
            df_unemployment_sum = df_unemployment_sum.assign(Unemployment = lambda row: (row['Number'] / 12))
            st.markdown("<h5 style='text-align: center; color: black;'>Yearly Unemployment By District(2013-2017)</h5>", unsafe_allow_html=True)
            fig = px.line(df_unemployment_sum, x="Year", y="Unemployment", color="District",
                        hover_name="Unemployment", color_discrete_sequence=px.colors.qualitative.Prism)
            fig.update_xaxes(tick0=2013, dtick=1)
            fig.update_layout(
                
                plot_bgcolor="white",
                margin=dict(t=10,l=10,b=10,r=10)
            )         
            st.plotly_chart(fig, use_container_width= False)        
            df_immigrant_sum = df_immigrants_by_nationality[(df_immigrants_by_nationality['Nationality'] != 'Spain') ]
            df_immigrant_sum = df_immigrant_sum.groupby(['Nationality','Year'])['Number'].sum().reset_index()
            df_immigrant_sum2015 = df_immigrant_sum[(df_immigrant_sum['Year'] == 2015)]
            df_immigrant_sum2016 = df_immigrant_sum[(df_immigrant_sum['Year'] == 2016)]
            df_immigrant_sum2017 = df_immigrant_sum[(df_immigrant_sum['Year'] == 2017)]
            df_immigrant_sum2015.columns = ["Nationality","Year","Number"]
            df_immigrant_sum2016.columns = ["Nationality","Year","Number"]
            df_immigrant_sum2017.columns = ["Nationality","Year","Number"]

            #df_immigrant_sum.columns = ["Nationality","Year","Number"]
            df_immigrant_sum2015 = df_immigrant_sum2015.sort_values(by = ['Number','Year'], ascending = False).head(5)
            df_immigrant_sum2016 = df_immigrant_sum2016.sort_values(by = ['Number','Year'], ascending = False).head(5)
            df_immigrant_sum2017 = df_immigrant_sum2017.sort_values(by = ['Number','Year'], ascending = False).head(5)

            #df_immigrant_sum = df_immigrant_sum.sort_values(by = ['Number','Year'], ascending = False)


            df_immigrant_sum = df_immigrant_sum2015.append([df_immigrant_sum2016, df_immigrant_sum2017])

            #df_immigrant_sum = df_immigrant_sum.head(13)
            st.markdown("<h5 style='text-align: center; color: black;'>Immigrants by Nationality (Top 5 Per Year)</h5>", unsafe_allow_html=True)
            #fig = px.scatter(df_immigrant_sum, x="Number", y="Year",
                       # size="Number", color="Nationality",
                        #    hover_name="Nationality", log_x=True, size_max=20, range_y=[2014, 2018],
                         #   color_discrete_sequence=px.colors.qualitative.Light24)
            fig = px.bar(df_immigrant_sum, x="Year", y="Number", color="Nationality", 
            color_discrete_sequence=px.colors.qualitative.Pastel)
            # fig.update_xaxes(range=[0, 4])
            fig.update_xaxes(tick0=2015, dtick=1)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10)
            )
            st.plotly_chart(fig, use_container_width= False)  
    
    elif select_category == "Yearly Data (Population)":
        col1, col2, col3 = st.beta_columns(3)
        with col1:

            df_population_sum = df_population[(df_population['Year']== select_year)]
            df_population_sum = df_population_sum.groupby(['District.Name'])['Number'].sum().reset_index()
            df_population_sum.columns = ["District","Population"]
            st.markdown("<h5 style='text-align: center; color: black;'>Population By District</h5>", unsafe_allow_html=True)            
            fig = px.bar(df_population_sum, x="Population", y="District", color="District",
                        hover_name="Population",  color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10),
                showlegend= False
            )
            st.plotly_chart(fig, use_container_width=True)           
        with col2:
            df_population_sum = df_population[(df_population['Year']== select_year)]
            df_population_sum = df_population_sum.groupby(['Age'])['Number'].sum().reset_index()
            df_population_sum.columns = ["Age","Population"]
            st.markdown("<h5 style='text-align: center; color: black;'>Population By Age Group</h5>", unsafe_allow_html=True)
            fig = px.bar(df_population_sum, x='Population', y='Age',
            color='Age', color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10),
                showlegend= False
            )
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            st.markdown("<h5 style='text-align: center; color: black;'>Death By Age Group</h5>", unsafe_allow_html=True)
            df_death_sum = df_deaths[(df_deaths['Year']== select_year)]
            df_death_sum = df_death_sum.groupby(['Age'])['Number'].sum().reset_index()
            df_death_sum.columns = ["Age","Population"]
            fig = px.bar(df_death_sum, x="Population", y="Age", color="Age", color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10),
                showlegend= False
            )
            st.plotly_chart(fig, use_container_width=True)       
    elif select_category == "Yearly Data (Immigration)":
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            df_unemployment_sum = df_unemployment[(df_unemployment['Year']== select_year)]
            df_unemployment_sum = df_unemployment_sum.groupby(['District.Name'])['Number'].sum().reset_index()
            df_unemployment_sum.columns = ["District","Population"]
            st.markdown("<h5 style='text-align: center; color: black;'>Unemployment By District</h5>", unsafe_allow_html=True)
            fig = px.bar(df_unemployment_sum, x="Population", y="District", color="District",
                        hover_name="District", color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10),
                showlegend = False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            df_age_sum = df_immigrants_emigrants_by_age[(df_immigrants_emigrants_by_age['Year']== select_year)]
            df_age_sum = df_age_sum.groupby(['Age'])['Number'].sum().reset_index()
            df_age_sum.columns = ["Age","Immigrants"]
            st.markdown("<h5 style='text-align: center; color: black;'>Immigrants By Age Group</h5>", unsafe_allow_html=True)
            fig = px.bar(df_age_sum, x='Immigrants', y='Age',
            color='Age', color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10),
                showlegend = False
            )
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            df_gender_sum = df_immigrants_emigrants_by_sex[(df_immigrants_emigrants_by_sex['Year']== select_year)]
            df_gender_sum = df_gender_sum.groupby(['Gender','Year'])['Number'].sum().reset_index()
            df_gender_sum.columns = ["Gender","Year","Number"]
            st.markdown("<h5 style='text-align: center; color: black;'>Immigrants By Gender</h5>", unsafe_allow_html=True)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=100,r=10)
            )
            fig = px.pie(df_gender_sum, values='Number', names='Gender', color_discrete_sequence=px.colors.sequential.Aggrnyl)
            st.plotly_chart(fig, use_container_width=True)
    elif select_category == "Immigrants (By Nationality)":
        # col1 = st.beta_columns(1)
        # with col1:
            df_sum = df_immigrants_by_nationality[(df_immigrants_by_nationality['Year']== select_year) & 
            (df_immigrants_by_nationality['Nationality']== select_nationality)]
            df_sum = df_sum.groupby(['District.Name'])['Number'].sum().reset_index()
            df_sum.columns = ["District","Population"]
            st.markdown("<h5 style='text-align: center; color: black;'>Nationality By District</h5>", unsafe_allow_html=True)
            fig = px.bar(df_sum, x="District", y="Population", color="District",
                        hover_name="District", color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig.update_layout(
                plot_bgcolor="White",
                margin=dict(t=10,l=10,b=150,r=10),
                showlegend = False
            )
            st.plotly_chart(fig, use_container_width=True)
            
###########################################################
## Compare Work
###########################################################

if select_category == "District Comparison":
    st.sidebar.header('Comparing')

    col1, col2, col3 = st.beta_columns(3)
    making_textbox = DesignSideBarText()
    all_dist = making_textbox.making_textbox()

    st.set_option('deprecation.showPyplotGlobalUse', False)
    unemployDistrict = Compare('./archive/unemployment.csv')
    unemployDistrict.makeDataframe(all_dist, select_year, 'District.Name')
    unemployDistrict.showFigure('Unemployment By District Name', col2, graphBar='bar', xlabel='District', ylabel='No of People')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    unemployGender = Compare('./archive/unemployment.csv')
    unemployGender.makeDataframe(all_dist, select_year, 'Gender')
    unemployGender.showFigure('Unemployment By Gender', col2, xlabel='District', ylabel='No of People')



    # col3.write("")
  

    deathsDistrict = Compare('./archive/deaths.csv')
    deathsDistrict.makeDataframe(all_dist, select_year, 'District.Name')
    deathsDistrict.showFigure('Deaths By District Name', col3, graphBar='barh', xlabel='No of People', ylabel='District')
    
    col3.write("")
    col3.write("")
    col3.write("")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    populationNeighbor = Compare('./archive/population.csv')
    populationNeighbor.makeDataframe(all_dist, select_year, 'Gender')
    populationNeighbor.showFigure('Population By Gender',  col3, graphBar='barh', xlabel='No of People', ylabel='District')

    imigrantsDistrict = Compare('./archive/immigrants_by_nationality.csv')
    imigrantsDistrict.makeDataframe(all_dist, select_year, 'District.Name')
    imigrantsDistrict.showFigure('Immigrants By District Name', col1, graphBar='barh', xlabel='No of People', ylabel='District')

    # col1.write("")
    col1.write("")
    col1.write("")
    populationSex = Compare('./archive/immigrants_emigrants_by_sex.csv')
    populationSex.makeDataframe(all_dist, select_year, 'Gender')
    populationSex.showFigure('Immigrants By Gender', col1, graphBar='barh', xlabel='No of People', ylabel='District')
    

    




# st.sidebar.write("You can view each chart in more detail by hovering over their top right corner and clicking the respective buttons.")
