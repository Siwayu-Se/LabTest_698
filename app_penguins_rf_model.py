
# Import necessary libraries
import streamlit as st
import pickle
import numpy as np
import os

# Set page configuration
st.set_page_config(page_title="Penguin Species Predictor", page_icon="🐧", layout="centered")

# Set background image URL
background_image_url = "https://images.pexels.com/photos/300857/pexels-photo-300857.jpeg"

# Set desired colors
text_color = "#FFA500"  # Text color
result_bg_color = "#FFFAFA"  # Result background color

# Apply CSS for background and text colors
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        height: 100vh;
    }}
    h1, h2, h3, p, div {{
        color: {text_color} !important;
    }}
    .result-container {{
        background-color: {result_bg_color};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        opacity: 0.9;
        border: 2px solid {text_color};
    }}
    .image-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0; /* Add margin for spacing */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load the trained Random Forest model
model_path = 'penguins_rf_model.pkl'

# Ensure the model file exists
if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        rf_model = pickle.load(file)
else:
    st.error(f"Error: {model_path} not found. Please make sure the model file is available.")
    st.stop()

# Streamlit App
st.title("🐧 Penguin Species Prediction ")
st.write("This app predicts the **species** of a penguin based on its physical characteristics. "
         "Please enter the details on the left and click 'Predict Species' to see the result.")

# Sidebar inputs for user to input penguin features
st.sidebar.header("Penguin Features")
st.sidebar.write("Provide the following features to predict the penguin's species:")

# Input options in sidebar with descriptions
island = st.sidebar.selectbox("Island", ['Biscoe', 'Dream', 'Torgersen'])
bill_length_mm = st.sidebar.slider("Bill Length (mm)", 32.1, 59.6, 45.0)
bill_depth_mm = st.sidebar.slider("Bill Depth (mm)", 13.1, 21.5, 17.2)
flipper_length_mm = st.sidebar.slider("Flipper Length (mm)", 172.0, 231.0, 200.0)
body_mass_g = st.sidebar.slider("Body Mass (g)", 2700, 6300, 4200)
sex = st.sidebar.selectbox("Sex", ['Male', 'Female'])

# Move the Predict button to the sidebar
if st.sidebar.button("Predict Species"):
    # Map the island and sex inputs to their encoded values
    island_map = {'Biscoe': 0, 'Dream': 1, 'Torgersen': 2}
    sex_map = {'Male': 0, 'Female': 1}

    # Convert inputs to model-compatible format
    input_data = np.array([[island_map[island], bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex_map[sex]]])

    # Predict species
    prediction = rf_model.predict(input_data)
    species_dict = {0: "Adelie", 1: "Chinstrap", 2: "Gentoo"}  # Mapping encoded values to species names
    species = species_dict[prediction[0]]

    # Display results with style
    st.subheader("Prediction Result")

    # Using markdown for better styling
    st.markdown(
        f"<div class='result-container'>"
        f"<h3 style='color: {text_color};'>The predicted species of the penguin is: <strong>{species}</strong></h3>"
        "</div>",
        unsafe_allow_html=True
    )

    # Show species image in the center
    species_image_path = f"images/{species.lower()}.jpg"  # Ensure images are in the 'images' directory
    if os.path.exists(species_image_path):
        st.image(species_image_path, width=300, caption=f"{species} Penguin", use_column_width='auto')
    else:
        st.warning(f"Image for {species} not found. Please ensure the image is in the 'images' folder.")

    # Display characteristics with a result container
    st.markdown(
        f"<div class='result-container'>"
        f"<h4 style='color: {text_color};'>Penguin Species Characteristics</h4>"
        f"<p style='color: {text_color};'>- Island: {island}</p>"
        f"<p style='color: {text_color};'>- Bill Length: {bill_length_mm} mm</p>"
        f"<p style='color: {text_color};'>- Bill Depth: {bill_depth_mm} mm</p>"
        f"<p style='color: {text_color};'>- Flipper Length: {flipper_length_mm} mm</p>"
        f"<p style='color: {text_color};'>- Body Mass: {body_mass_g} g</p>"
        f"<p style='color: {text_color};'>- Sex: {sex}</p>"
        "</div>",
        unsafe_allow_html=True
    )
else:
    st.info("Please enter the penguin features on the left and click 'Predict Species'.")
