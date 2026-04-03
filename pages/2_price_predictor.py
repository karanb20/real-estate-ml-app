import streamlit as st
import pickle
import numpy as np
import pandas as pd
import gdown
import os

# -------------------------------
# ✅ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Real Estate Price Predictor", layout="wide")

# -------------------------------
# ✅ DATA LOADING (LARGE FILE SUPPORT)
# -------------------------------
@st.cache_resource
def load_assets():
    # ✅ Updated IDs from new Google Drive links
    df_id = "1-NQc0BoJDK2l78p9WLv24yl5uA2c0UVI"
    pipeline_id = "1DYbodUgkZXiRqGu6cBpWeuz4zBn6pjfJ"
    
    df_path = "df.pkl"
    pipeline_path = "pipeline.pkl"

    def secure_download(file_id, output_path):
        if not os.path.exists(output_path):
            with st.spinner(f"Downloading {output_path} (please wait)..."):
                url = f'https://drive.google.com/uc?id={file_id}&confirm=t'
                gdown.download(url, output_path, quiet=False)
        
        # Validation: If file is smaller than 1MB, it's a corrupted HTML page
        if os.path.exists(output_path) and os.path.getsize(output_path) < 1000000:
            st.error(f"❌ {output_path} download failed. Deleting corrupted file...")
            os.remove(output_path)
            st.stop()

    # Run downloads
    secure_download(df_id, df_path)
    secure_download(pipeline_id, pipeline_path)

    # Load Files
    try:
        with open(df_path, "rb") as f:
            df_obj = pickle.load(f)
        with open(pipeline_path, "rb") as f:
            model_obj = pickle.load(f)
        return df_obj, model_obj
    except Exception as e:
        st.error(f"❌ Error loading files: {e}")
        st.info("Tip: Ensure your Python version on Streamlit Cloud matches your local version.")
        st.stop()

# Initialize
df, pipeline = load_assets()

# -------------------------------
# ✅ USER INTERFACE
# -------------------------------
st.title("🏠 Real Estate Price Predictor")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox('Property Type', ['flat', 'house'])
    sector_name = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
    bedroom = float(st.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))
    bathroom = float(st.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))
    balcony = st.selectbox('Balcony', sorted(df['balcony'].unique().tolist()))
    age = st.selectbox('Age of Property', sorted(df['agePossession'].unique().tolist()))

with col2:
    area = float(st.number_input('Built-up Area (sq.ft)', min_value=100.0, value=1200.0))
    servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
    store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
    furnishing = st.selectbox('Furnishing', sorted(df['furnishing_type'].unique().tolist()))
    luxury = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    floor = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# -------------------------------
# ✅ PREDICTION
# -------------------------------
if st.button("Predict Price", use_container_width=True, type="primary"):
    try:
        columns = [
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
            'agePossession', 'built_up_area', 'servant room', 'store room',
            'furnishing_type', 'luxury_category', 'floor_category'
        ]
        
        input_data = [[
            property_type, sector_name, bedroom, bathroom, balcony,
            age, area, servant_room, store_room, furnishing, luxury, floor
        ]]

        input_df = pd.DataFrame(input_data, columns=columns)

        prediction = pipeline.predict(input_df)[0]
        price = np.expm1(prediction)

        st.success(f"### 💰 Estimated Price: {round(price - 0.22, 2)} Cr - {round(price + 0.22, 2)} Cr")
        st.balloons()

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")