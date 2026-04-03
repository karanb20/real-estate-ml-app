import streamlit as st
import pickle
import numpy as np
import pandas as pd
import gdown
import os

st.set_page_config(page_title='viz_demo')

# Download files from Google Drive if not present
if not os.path.exists('df.pkl'):
    with st.spinner('Loading data...'):
        gdown.download('https://drive.google.com/file/d/1OdaPoKoLSv91qUppKca458C0pIEXB3RV/view?usp=drive_link', 'df.pkl', quiet=False)

if not os.path.exists('pipeline.pkl'):
    with st.spinner('Loading model...'):
        gdown.download('https://drive.google.com/file/d/14PLYhfRgT8jJG4wlVgDeRaIT6S1Oqlm8/view?usp=drive_link', 'pipeline.pkl', quiet=False)

with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

st.header('enter your inputs')

property_type = st.selectbox('property type', ['flat', 'house'])
sector_name = st.selectbox('sector', sorted(df['sector'].unique().tolist()))
bedroom = float(st.selectbox('bedRoom', sorted(df['bedRoom'].unique().tolist())))
bath_room = float(st.selectbox('bathroom', sorted(df['bathroom'].unique().tolist())))
balconyy = (st.selectbox('balcony', sorted(df['balcony'].unique().tolist())))
age = st.selectbox('agePossession', sorted(df['agePossession'].unique().tolist()))
area = float(st.number_input('built_up_area'))
room = float(st.selectbox('servant room', [0.0, 1.0]))
room2 = float(st.selectbox('store room', [0.0, 1.0]))
furnishing = st.selectbox('furnishing_type', sorted(df['furnishing_type'].unique().tolist()))
luxury = st.selectbox('luxury_category', sorted(df['luxury_category'].unique().tolist()))
floor = st.selectbox('floor_category', sorted(df['floor_category'].unique().tolist()))

if st.button('predict'):
    data = [[property_type, sector_name, bedroom, bath_room, balconyy, age, area, room, room2, furnishing, luxury, floor]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data, columns=columns)
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22
    st.text('the price of the flat is between {} Cr and {} Cr'.format(round(low, 2), round(high, 2)))