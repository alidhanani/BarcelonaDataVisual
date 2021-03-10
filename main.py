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