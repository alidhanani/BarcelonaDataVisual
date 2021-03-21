#How do we divide data into different files so that we can each work independently?
#Data in different in files has different column names.(District Name vs District.Name). WTF?!?
#https://towardsdatascience.com/how-to-build-interactive-dashboards-in-python-using-streamlit-1198d4f7061b

import streamlit as st
import pandas as pd
import pydeck as pdk 
import altair as alt
from bokeh.plotting import figure,output_file
# from bokeh.charts import Bar
from bokeh.palettes import magma

# I was thinking it would be good for performance to read 
# all files at the start(What do you guys think?).
# All dataframes begin with "df" for ease in autocomplete (CTRL + Space)
df_unemployment = pd.read_csv('./archive/unemployment.csv')
df_population = pd.read_csv('./archive/population.csv')



#Get values for user selection
categories = ["Population","Unemployment","Immigrant Data"]
districts = df_unemployment["District Name"].unique()
year_min = int(df_population.Year.min())
year_max = int(df_population.Year.max())


#Generate Sidebar for user selection.
#All variables start with "select" for ease in autocomplete
select_category = st.sidebar.selectbox("Category", categories)
select_district = st.sidebar.selectbox("District", districts)
select_year = st.sidebar.slider("Year", min_value= year_min, max_value= year_max)

#Data Slicing
#Note that Categories is not included any condition for now,
# will probably make a switch case for that to show the correct dataframe
#For multiple conditions in df slice, always use () for each condition
slice_population = df_population[(df_population['Year'] == select_year) 
& (df_population["District.Name"] == select_district)]

# st.write("This is unemployment data")
# st.table(df_unemployment.head())

st.write("This is population data")
st.table(slice_population.head())

# total_cases_graph  =alt.Chart(subset_data).transform_filter(
#    alt.datum.total_cases > 0  
# ).mark_line().encode(
#     x=alt.X('neighborhood', type='nominal', title='Date'),
#     y=alt.Y('sum(total_cases):Q',  title='Confirmed cases'),
#     color='Country',
#     tooltip = 'sum(total_cases)',
# ).properties(
#     width=1500,
#     height=600
# ).configure_axis(
#     labelFontSize=17,
#     titleFontSize=20
# )

# st.altair_chart(total_cases_graph)

# output_file("line.html")
# # xa = [1, 2, 3, 4, 5]
# # ya = [6, 7, 2, 4, 5]
st.write("This is the current size of the dataset(after Group by function): ")
slice_population = slice_population.groupby(['Neighborhood.Code'])['Number'].sum().reset_index()
st.write(slice_population.shape)

p = figure(
title='simple line example',
x_axis_label='x',
y_axis_label='y')
p.line(slice_population["Neighborhood.Code"], slice_population["Number"], legend='Trend', line_width=2)
st.bokeh_chart(p, use_container_width=True)

st.write("<H1>something</H1>")

# # instantiating the figure object  
# graph = figure(title = "Bokeh Multiple Line Graph")      
# # name of the x-axis  
# graph.xaxis.axis_label = "x-axis"
# # name of the y-axis  
# graph.yaxis.axis_label = "y-axis"
# # the points to be plotted 
# x = [n for n in range(-100, 101)] 
# x.reverse() 
# xs = [[n, 0] for n in x] 
# y1 = [n for n in range(1, 101)] 
# y1.reverse() 
# y = [n for n in range(1, 101)] + [0] + y1 
# ys = [[0, n] for n in y]  
# # color of the lines 
# line_color = magma(201) 
# # plotting the graph  
# graph.multi_line(xs, ys, 
#                  line_color = line_color)
# st.bokeh_chart(graph, use_container_width=True)

# bar = Bar(slice_population, values='Number', label='Neighborhood.Code', stack='Age', agg='mean',
#           title="Python Interpreter Sampling", legend='top_right', width=400)
# st.bokeh_chart(bar)
