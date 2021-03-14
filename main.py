import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('My first app')

data = pd.read_csv('./archive/unemployment.csv')

st.table(data.head())

st.write("Information")
data.info()

st.write("Description")
st.write("We need to determine is there any unknow information on the Distrinct name data.")
st.write(data['Number'].describe())

st.write("Figure")
data_load_state = st.text('Loading data...')
plt.figure(figsize=(20,15))
sns.barplot(data=data,y='Number',x='Year',hue='Gender',estimator=sum)
st.pyplot()
data_load_state.text('Loading data...done!')


data_load_state = st.text('Loading data...')
plt.figure(figsize=(20,15))
sns.barplot(data=data[data['District Name']!='No consta'],y='Number',x='District Name',hue='Year',estimator=sum)
st.pyplot()
data_load_state.text('Loading data...done!')

data_load_state = st.text('Loading data...')
plt.figure(figsize=(20,15))
sns.barplot(data=data,y='Number',x='Year',hue='Month',estimator=sum)
st.pyplot()
data_load_state.text('Loading data...done!')

data_load_state = st.text('Loading data...')
plt.figure(figsize=(20,15))
sns.barplot(data=data,y='Number',x='Year',hue='Demand_occupation',estimator=sum)
st.pyplot()
data_load_state.text('Loading data...done!')


data_load_state = st.text('Loading data...')
unemploy_df = pd.read_csv('./archive/unemployment.csv')
data_uneploy = unemploy_df.groupby(['District Name']).sum().sort_values(by=['Number'],ascending=False)

f, ax = plt.subplots(1, 1, figsize=(16, 4))
sns.barplot(x=data_uneploy.index, y=data_uneploy.Number, palette="rocket", ax=ax)
st.pyplot()
data_load_state.text('Loading data...done!')


data_load_state = st.text('Loading data...')
data_uneploy = unemploy_df.groupby(['District Name']).sum().apply(lambda g: round(g / g.sum() * 100, 2))\
.sort_values(by=['Number'],ascending=False)
f, ax = plt.subplots(1, 1, figsize=(16, 6))
sns.barplot(x=data_uneploy.Number, y=data_uneploy.index, palette="deep", ax=ax)
ax.set(ylabel='District', xlabel='Population percentage %')
st.pyplot()
data_load_state.text('Loading data...done!')



data_load_state = st.text('Loading data...')

unemployment = pd.read_csv('./archive/unemployment.csv')
births=pd.read_csv("./archive/births.csv")

district_list=list(unemployment["District Name"].unique())
district_list
unemployment.Number=unemployment.Number.astype(float)
unemployment_ratio=[]
for i in district_list:
    x=unemployment[unemployment["District Name"]==i]
    ratio=sum(x.Number)/len(x)
    unemployment_ratio.append(ratio)

data=pd.DataFrame({"district_list" : district_list , "unemployment_ratio" : unemployment_ratio})
new_index=(data["unemployment_ratio"].sort_values(ascending=False)).index.values
sortedData=data.reindex(new_index)
sortedData


births.Number=births.Number.astype(float)
births_ratio=[]
for j in district_list:
    y=births[births["District Name"]==j]
    ratio2=sum(y.Number)/len(y)
    births_ratio.append(ratio2)

data2=pd.DataFrame({"district_list" : district_list , "births_ratio" : births_ratio })
new_index2=(data2["births_ratio"].sort_values(ascending=True)).index.values
sortedData2=data2.reindex(new_index2)


sortedData["unemployment_ratio"]=sortedData["unemployment_ratio"]/max(sortedData["unemployment_ratio"])
sortedData2["births_ratio"]=sortedData2["births_ratio"]/max(sortedData2["births_ratio"])
data=pd.concat([sortedData,sortedData2["births_ratio"]],axis=1)
data.sort_values("unemployment_ratio", inplace=True)

#visualization

plt.figure(figsize=(20,10))
sns.pointplot(x="district_list" , y ="unemployment_ratio", data=data , color="blue" , alpha=0.2)
sns.pointplot(x="district_list", y="births_ratio" , data=data, color="green" , alpha=0.5)
#plt.text(40,0.6 , "average unemployment people" , color="blue")
#plt.text(40, 0.55 , "average births" , color="green")
plt.xlabel("District Names")
plt.ylabel("Numerical Values")
plt.title("Correlation between unemployment and births")
plt.grid()
st.pyplot()
#st.altair_chart(chart)
data_load_state.text('Loading data...done!')


data_load_state = st.text('Loading data...')
#We can show correlation detailly with joint plot.
a=sns.jointplot(data["unemployment_ratio"] , data["births_ratio"], kind="kde",size=7)
plt.show()
st.pyplot()
data_load_state.text('Loading data...done!')


data_load_state = st.text('Loading data...')
sns.lmplot(x="unemployment_ratio", y="births_ratio", data=data)
plt.show()
st.pyplot()
data_load_state.text('Loading data...done!')


data_load_state = st.text('Loading data...')
f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(data.corr(), annot=True,ax=ax)
plt.show()
st.pyplot()
data_load_state.text('Loading data...done!')
