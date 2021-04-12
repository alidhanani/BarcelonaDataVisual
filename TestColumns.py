import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go




# I was thinking it would be good for performance to read 
# all files at the start(What do you guys think?).
# All dataframes begin with "df" for ease in autocomplete (CTRL + Space)
df_unemployment = pd.read_csv('./BarcelonaDataVisual/archive/unemployment.csv')
df_population = pd.read_csv('./BarcelonaDataVisual/archive/population.csv')
df_immigrants_by_nationality = pd.read_csv('./BarcelonaDataVisual/archive/immigrants_by_nationality.csv')
df_immigrants_emigrants_by_age = pd.read_csv('./BarcelonaDataVisual/archive/immigrants_emigrants_by_age.csv')
df_immigrants_emigrants_by_sex = pd.read_csv('./BarcelonaDataVisual/archive/immigrants_emigrants_by_sex.csv')
df_geo = pd.read_csv("./BarcelonaDataVisual/barcelona_geo.csv")

# Hard coded names and dataframe names for categories
category_dict = {
    "Population" : df_population,
    "Unemployment": df_unemployment,
    "Immigrants By Nationality": df_immigrants_by_nationality,
    "Immigrants By Age": df_immigrants_emigrants_by_age,
    "Immigrants By Sex": df_immigrants_emigrants_by_sex
}


fig = make_subplots(rows=1, cols=2)

data_pop = df_population[(df_population['Year'] == 2017)
        & (df_population['District.Code'] == 1)]

data_unem = df_unemployment[(df_unemployment['Year'] == 2017)
        & (df_unemployment['District.Code'] == 1)]


fig = make_subplots(rows=1, cols=2, shared_yaxes=False)

fig.add_trace(go.Bar(x=data_pop['Neighborhood.Name'], y=data_pop['Number']),
              1, 1)

fig.add_trace(go.Bar(x=data_unem['Neighborhood.Name'], y=data_pop['Number']),
              1, 2)

fig.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=False)
fig.update_layout(height=500, width=700,
                  title_text="Multiple Subplots")

st.plotly_chart(fig)
