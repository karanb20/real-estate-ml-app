import streamlit as st
import pickle
import numpy as np
import pandas as pd
import gdown
import os

st.set_page_config(page_title="Price Predictor")

# -------------------------------
# ✅ DOWNLOAD + LOAD FILES (FIXED)
# -------------------------------
@st.cache_resource
def load_files():

    # Download df.pkl
    if not os.path.exists("df.pkl"):
        with st.spinner("Downloading data..."):
            gdown.download(
                "https://drive.google.com/uc?id=1OdaPoKoLSv91qUppKca458C0pIEXB3RV",
                "df.pkl",
                quiet=False
            )

    # Download pipeline.pkl
    if not os.path.exists("pipeline.pkl"):
        with st.spinner("Downloading model..."):
            gdown.download(
                "https://drive.google.com/uc?id=14PLYhfRgT8jJG4wlVgDeRaIT6S1Oqlm8",
                "pipeline.pkl",
                quiet=False
            )

    # Load files
    with open("df.pkl", "rb") as f:
        df = pickle.load(f)

    with open("pipeline.pkl", "rb") as f:
        pipeline = pickle.load(f)

    return df, pipeline


# Load once
df, pipeline = load_files()

# -------------------------------
# ✅ UI START
# -------------------------------
st.title("🏠 Real Estate Price Predictor")

st.header("Enter Property Details")

property_type = st.selectbox('Property Type', ['flat', 'house'])

sector_name = st.selectbox(
    'Sector',
    sorted(df['sector'].dropna().unique().tolist())
)

bedroom = float(st.selectbox(
    'Bedrooms',
    sorted(df['bedRoom'].dropna().unique().tolist())
))

bathroom = float(st.selectbox(
    'Bathrooms',
    sorted(df['bathroom'].dropna().unique().tolist())
))

balcony = st.selectbox(
    'Balcony',
    sorted(df['balcony'].dropna().unique().tolist())
)

age = st.selectbox(
    'Age of Property',
    sorted(df['agePossession'].dropna().unique().tolist())
)

area = float(st.number_input('Built-up Area (sq.ft)', min_value=0.0))

servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

furnishing = st.selectbox(
    'Furnishing',
    sorted(df['furnishing_type'].dropna().unique().tolist())
)

luxury = st.selectbox(
    'Luxury Category',
    sorted(df['luxury_category'].dropna().unique().tolist())
)

floor = st.selectbox(
    'Floor Category',
    sorted(df['floor_category'].dropna().unique().tolist())
)

# -------------------------------
# ✅ PREDICTION
# -------------------------------
if st.button("Predict Price"):

    try:
        input_data = [[
            property_type,
            sector_name,
            bedroom,
            bathroom,
            balcony,
            age,
            area,
            servant_room,
            store_room,
            furnishing,
            luxury,
            floor
        ]]

        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
            'agePossession', 'built_up_area', 'servant room', 'store room',
            'furnishing_type', 'luxury_category', 'floor_category'
        ]

        input_df = pd.DataFrame(input_data, columns=columns)

        prediction = pipeline.predict(input_df)[0]
        price = np.expm1(prediction)

        low = price - 0.22
        high = price + 0.22

        st.success(f"💰 Estimated Price: {round(low,2)} Cr - {round(high,2)} Cr")

    except Exception as e:
        st.error(f"Error: {e}")