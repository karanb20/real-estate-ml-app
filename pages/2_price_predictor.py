import streamlit as st
import pickle
import numpy as np
import pandas as pd
import gdown
import os

st.set_page_config(page_title='Price Predictor')

# =========================
# 🔥 LOAD DATA FUNCTION
# =========================
@st.cache_resource
def load_files():
    # Download df.pkl
    if not os.path.exists('df.pkl'):
        with st.spinner('Downloading data...'):
            gdown.download(
                id="1OdaPoKoLSv91qUppKca458C0pIEXB3RV",
                output='df.pkl',
                quiet=False
            )

    # Download pipeline.pkl
    if not os.path.exists('pipeline.pkl'):
        with st.spinner('Downloading model...'):
            gdown.download(
                id="14PLYhfRgT8jJG4wlVgDeRaIT6S1Oqlm8",
                output='pipeline.pkl',
                quiet=False
            )

    # Load files
    df = pickle.load(open('df.pkl', 'rb'))
    pipeline = pickle.load(open('pipeline.pkl', 'rb'))

    return df, pipeline


# Load once
df, pipeline = load_files()

# =========================
# UI
# =========================
st.header('Enter Property Details')

property_type = st.selectbox('Property Type', ['flat', 'house'])
sector_name = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
bedroom = float(st.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))
bath_room = float(st.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))
balconyy = st.selectbox('Balcony', sorted(df['balcony'].unique().tolist()))
age = st.selectbox('Age Possession', sorted(df['agePossession'].unique().tolist()))
area = float(st.number_input('Built-up Area'))
room = float(st.selectbox('Servant Room', [0.0, 1.0]))
room2 = float(st.selectbox('Store Room', [0.0, 1.0]))
furnishing = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# =========================
# PREDICTION
# =========================
if st.button('Predict Price'):
    try:
        data = [[property_type, sector_name, bedroom, bath_room, balconyy,
                 age, area, room, room2, furnishing, luxury, floor]]

        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                   'agePossession', 'built_up_area', 'servant room', 'store room',
                   'furnishing_type', 'luxury_category', 'floor_category']

        one_df = pd.DataFrame(data, columns=columns)

        base_price = np.expm1(pipeline.predict(one_df))[0]

        low = base_price - 0.22
        high = base_price + 0.22

        st.success(f'Estimated Price Range: {round(low, 2)} Cr - {round(high, 2)} Cr')

    except Exception as e:
        st.error(f"Error: {e}")