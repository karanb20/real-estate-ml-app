import streamlit as st
import pickle
import numpy as np
import pandas as pd
import gdown
import os

st.set_page_config(page_title="Price Predictor")

# -------------------------------
# ✅ LOAD FILES (ROBUST VERSION)
# -------------------------------
@st.cache_resource
def load_files():

    df_path = "df.pkl"
    pipeline_path = "pipeline.pkl"

    # -------------------------------
    # DOWNLOAD df.pkl
    # -------------------------------
    if not os.path.exists(df_path):
        st.info("Downloading df.pkl...")
        gdown.download(
            "https://drive.google.com/uc?export=download&id=1OdaPoKoLSv91qUppKca458C0pIEXB3RV",
            df_path,
            quiet=False
        )

    # -------------------------------
    # DOWNLOAD pipeline.pkl
    # -------------------------------
    if not os.path.exists(pipeline_path):
        st.info("Downloading pipeline.pkl...")
        gdown.download(
            "https://drive.google.com/uc?export=download&id=14PLYhfRgT8jJG4wlVgDeRaIT6S1Oqlm8",
            pipeline_path,
            quiet=False
        )

    # -------------------------------
    # DEBUG CHECKS
    # -------------------------------
    st.write("✅ df.pkl exists:", os.path.exists(df_path))
    st.write("✅ pipeline.pkl exists:", os.path.exists(pipeline_path))

    if os.path.exists(df_path):
        st.write("📦 df.pkl size:", os.path.getsize(df_path))
    if os.path.exists(pipeline_path):
        st.write("📦 pipeline.pkl size:", os.path.getsize(pipeline_path))

    # -------------------------------
    # LOAD FILES SAFELY
    # -------------------------------
    try:
        with open(df_path, "rb") as f:
            df = pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading df.pkl: {e}")
        st.stop()

    try:
        with open(pipeline_path, "rb") as f:
            pipeline = pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading pipeline.pkl: {e}")
        st.stop()

    return df, pipeline


# Load data
df, pipeline = load_files()

# -------------------------------
# ✅ UI
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
        st.error(f"❌ Prediction Error: {e}")