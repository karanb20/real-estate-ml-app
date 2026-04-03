import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv('datasets/data_viz1.csv')

group_df = new_df.groupby('sector').mean(numeric_only=True)[['price', 'price_per_sqft', 'built_up_area', 'Latitude', 'Longitude']]
st.header('GEOMAP')

fig = px.scatter_mapbox(group_df, lat="Latitude", lon="Longitude",
                        color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom=10,
                        mapbox_style="open-street-map", width=1200,
                        height=700, hover_name=group_df.index)

st.plotly_chart(fig, use_container_width=True)
st.header('SCATTER PLOT (AREA VS PRICE)')
property_type=st.selectbox('select property type',['flat','house'])
if property_type=='house':
    fig1 = px.scatter(new_df[new_df['property_type'] =='house'], x='built_up_area' , y='price', color='bedRoom',title=' Area Vs Price')
    st.plotly_chart(fig1,use_container_width=True)
else:
     fig1 = px.scatter(new_df[new_df['property_type']=='flat'], x='built_up_area' , y='price', color='bedRoom',title=' Area Vs Price')
     st.plotly_chart(fig1,use_container_width=True)
st.header('BHK PIE CHART')
sector_options=new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')
selected_sector=st.selectbox('select sector', sector_options)
if selected_sector=='overall':
     fig3 = px.pie(new_df, names='bedRoom')
     st.plotly_chart(fig3,use_container_width=True)
else:
     fig3 = px.pie(new_df[new_df['sector']== selected_sector] , names='bedRoom')
     st.plotly_chart(fig3,use_container_width=True)
     
st.header('SIDE BY SIDE BHK PRICE COMPARISON')
fig4 = px.box(new_df[new_df['bedRoom']<= 4],x='bedRoom',y='price' , title='bhk price comaprison')
st.plotly_chart(fig4,use_container_width=True)
st.header('SIDE BY SIDE DISTPLOT FOR PROPERTY TYPE')
fig5=plt.figure(figsize=(10,4))
sns.distplot(new_df[new_df['property_type']=='house']['price'])
sns.distplot(new_df[new_df['property_type']=='flat']['price'])
st.pyplot(fig5)







