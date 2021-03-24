import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import altair as alt


def get_data():
    return pd.read_csv('./archive/unemployment.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)

df = get_data()
min_year = int(df['Year'].min()) 
max_year = int(df['Year'].max()) 
district_names = df['District Name'].unique()
neighborhood_names = df['Neighborhood Name'].unique()

st.title('Barcelona')

#st.table(df.head())

st.sidebar.header('Filter Options')

selected_year = st.sidebar.slider('Year', min_year, max_year)

selected_district = st.sidebar.selectbox('District Name', district_names)

st.sidebar.header('Comparing')

# selected_district_1 = st.sidebar.selectbox('District Name 1', district_names)
# selected_district_2 = st.sidebar.selectbox('District Name 2', district_names)

num_dist = st.sidebar.text_input('Number of district')
all_dist = [] 
if num_dist == "":
    num_dist = "0"
for i in range(0, int(num_dist)):
	all_dist.append(st.sidebar.selectbox('District Name '+str(i), district_names))



#selected_neighborhood = st.sidebar.selectbox('Neighborhood Name', neighborhood_names)
df1 = df[(df['District Name'] == selected_district) 
        & (df['Year'] == selected_year)]
       # & (df['Neighborhood Name'] == selected_neighborhood)]

df1


#number per Neighborhood
st.write("Number per Neighborhood")
d1 = df1.groupby(df['Neighborhood Name'])['Number'].sum()
d1

#number per gender
st.write("Number per Gender")
d2 = df1.groupby(df['Gender'])['Number'].sum()
d2

#number per month
st.write("Number per Month")
d3 = df1.groupby(df['Month'])['Number'].sum()
d3

d3.hist()
plt.show()
st.pyplot()

#st.bar_chart(d3['Month'])

dataframes = []
for i in all_dist:
	df4 = df[(df['District Name'] == i) 
        & (df['Year'] == selected_year)]
       # & (df['Neighborhood Name'] == selected_neighborhood)]
	df4 = df4.groupby(df4["Gender"])["Number"].sum()
	dataframes.append(df4)


# df4 = df[(df['District Name'] == selected_district_1) 
#         & (df['Year'] == selected_year)]
#        # & (df['Neighborhood Name'] == selected_neighborhood)]
# df4 = df4.groupby(df4["Gender"])["Number"].sum()
# df4

# df5 = df[(df['District Name'] == selected_district_2) 
#         & (df['Year'] == selected_year)]
#        # & (df['Neighborhood Name'] == selected_neighborhood)]
# df5 = df5.groupby(df5["Gender"])["Number"].sum()
# df5
newData = []
for i in range(len(dataframes)-1):
	newData.append(pd.merge(dataframes[i], dataframes[i+1], on='Gender'))

#newData = pd.concat(dataframes)
#len(newData)

for i in newData:
	df6 = i.T
	df6.plot.bar(rot=15, title="Car Price vs Car Weight comparision for Sedans made by a Car Company")
	plt.show(block=True)
	st.pyplot()


# df6_Trans = newData[len(newData)-1].T
# # df6 = pd.merge(df4, df5, on='Gender')
# # df6_Trans = df6.T
# df6_Trans

# df6_Trans.plot.bar(rot=15, title="Car Price vs Car Weight comparision for Sedans made by a Car Company")
# plt.show(block=True)
# st.pyplot()

# df6 = df6.groupby(df['Neighborhood Name'])['Number'].sum()
# df6
#fig = px.bar(df, x="Gender", y=["Number_x", "Number_y"], barmode='group', height=400)
# st.dataframe(df) # if need to display dataframe
#st.plotly_chart(fig)
# chart = alt.Chart(y2k_pop).mark_bar().encode(
#     x='age:O',
#     y='sum(people):Q',
#     color=alt.Color('sex:N', scale=alt.Scale(range=["#e377c2","#1f77b4"]))
# )


# df.plot.bar(x='Year', logy=True)
# plt.xticks(rotation=0)
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.show()
# st.pyplot()



