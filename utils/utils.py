import streamlit as st
import numpy as np
from PIL import Image
import pickle
from tensorflow.keras.models import load_model
from config.config import (
    CNN_MODEL_PATH,
    LOGISTIC_REGRESSION_PATH,
    THEME_CONFIG
)
import os

def apply_custom_theme():
    """Apply custom theme to the Streamlit app."""
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {THEME_CONFIG['backgroundColor']};
        }}
        .css-1d391kg {{
            background-color: {THEME_CONFIG['secondaryBackgroundColor']};
        }}
        .stButton>button {{
            background-color: {THEME_CONFIG['primaryColor']};
            color: white;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
        }}
        .stTextInput>div>div>input {{
            border-radius: 10px;
        }}
        .stSelectbox>div>div>div {{
            border-radius: 10px;
        }}
        .stFileUploader>div>div>div>div {{
            border-radius: 10px;
        }}
        h1, h2, h3 {{
            color: {THEME_CONFIG['primaryColor']};
        }}
        p {{
            color: {THEME_CONFIG['textColor']};
        }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Load and cache the machine learning models."""
    try:
        with open(LOGISTIC_REGRESSION_PATH, 'rb') as f:
            lr_model = pickle.load(f)
        cnn_model = load_model(CNN_MODEL_PATH)
        return lr_model, cnn_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

def preprocess_image(image):
    """Preprocess the uploaded image for model prediction."""
    try:
        if image.mode == "RGB":
            image = image.convert("L")
        image = image.resize((224, 224))
        img_array = np.array(image) / 255.0
        img_cnn = img_array.reshape(1, 224, 224, 3)
        img_flat = img_array.flatten().reshape(1, -1)
        return img_cnn, img_flat
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return None, None

def make_prediction(img_cnn, img_flat, lr_model, cnn_model):
    """Make predictions using both models."""
    try:
        cnn_preds = cnn_model.predict(img_cnn)
        cnn_preds = (cnn_preds > 0.5).astype(int)
        lr_preds = lr_model.predict(img_flat)
        
        return {
            "CNN": "Pneumonia" if cnn_preds == 0 else "Normal",
            "Logistic Regression": "Pneumonia" if lr_preds == 0 else "Normal"
        }
    except Exception as e:
        st.error(f"Error making prediction: {e}")
        return None

def display_prediction_result(result):
    """Display prediction results in a beautiful format."""
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3 style="color: {THEME_CONFIG['primaryColor']};">Prediction Results</h3>
        <p><strong>CNN Prediction:</strong> {result['CNN']}</p>
        <p><strong>Logistic Regression Prediction:</strong> {result['Logistic Regression']}</p>
    </div>
    """, unsafe_allow_html=True)

def save_uploaded_file(uploaded_file, user_id):
    """Save uploaded file to user's directory."""
    try:
        # Create user directory if it doesn't exist
        user_dir = f"uploads/user_{user_id}"
        os.makedirs(user_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(user_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None 