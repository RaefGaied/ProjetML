import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import pickle
from PIL import Image
import os
import warnings
import joblib
import tensorflow as tf

# Load models
def load_model(model_type='cnn'):
    """Load the selected model and return it"""
    try:
        if model_type == 'cnn':
            model_path = 'models/cnn_model.h5'
            if not os.path.exists(model_path):
                print(f"Model not found at {model_path}")
                return None
            
            # Suppress HDF5 version warning
            warnings.filterwarnings('ignore', category=UserWarning, module='h5py')
            
            # Load model with custom_objects to handle version incompatibilities
            model = tf.keras.models.load_model(
                model_path,
                custom_objects={
                    'InputLayer': lambda **kwargs: tf.keras.layers.InputLayer(**{k: v for k, v in kwargs.items() if k != 'batch_shape'}),
                    'Conv2D': tf.keras.layers.Conv2D,
                    'MaxPooling2D': tf.keras.layers.MaxPooling2D,
                    'Flatten': tf.keras.layers.Flatten,
                    'Dense': tf.keras.layers.Dense,
                    'Dropout': tf.keras.layers.Dropout
                }
            )
            print("CNN model loaded successfully!")
            return model
        else:
            # Load Logistic Regression model and PCA
            logistic_path = os.path.join('models', 'logistic_regression_model.pkl')
            pca_path = os.path.join('models', 'pca_transformer.pkl')
            
            if os.path.exists(logistic_path) and os.path.exists(pca_path):
                logistic_model = joblib.load(logistic_path)
                pca_transformer = joblib.load(pca_path)
                print("Logistic Regression model and PCA loaded successfully!")
                return logistic_model, pca_transformer
            else:
                print(f"Logistic model or PCA not found at {logistic_path} or {pca_path}")
                return None, None
            
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return None

# Initialize models
cnn_model = load_model('cnn')
logistic_model, pca_transformer = load_model('logistic')

# Streamlit UI
st.title("Chest X-Ray Pneumonia Detection")

st.markdown("""
    **Upload one or more X-Ray images**, and this app will predict whether each image shows **Pneumonia** or **Normal**. 
    This model uses **CNN** and **Logistic Regression** to make the predictions.
""")

# Function to preprocess the uploaded image
def preprocess_image(image):
    try:
        # Convert image to grayscale if it's RGB
        if image.mode == "RGB":
            image = image.convert("L")
        
        # Resize the image to 150x150 (input size for the models)
        image = image.resize((150, 150))
        
        # Convert image to a numpy array and normalize pixel values
        img_array = np.array(image) / 255.0

        # Reshape for CNN (add batch and channel dimensions)
        img_cnn = img_array.reshape(1, 150, 150, 1)

        # Flatten the image for Logistic Regression (22500 features)
        img_flat = img_array.flatten().reshape(1, -1)

        return img_cnn, img_flat
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return None, None

# Multi-file upload section
uploaded_files = st.file_uploader("Upload one or more X-ray Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# If images are loaded, preview them
if uploaded_files:
    images = []  # List to hold loaded images
    for file in uploaded_files:
        try:
            img = Image.open(file)
            images.append(img)
        except Exception as e:
            st.error(f"Error loading file {file.name}: {e}")

    # Display previews of all images
    st.subheader("Preview Images")
    cols = st.columns(min(len(images), 4))  # Display up to 4 images per row
    for i, img in enumerate(images):
        with cols[i % len(cols)]:
            st.image(img, caption=f"Image {i + 1}", use_column_width=True)

    # Add a button to confirm before running predictions
    if st.button("Classify Images"):
        results = []  # To store results
        for i, img in enumerate(images):
            st.write(f"Classifying Image {i + 1}...")
            img_cnn, img_flat = preprocess_image(img)

            if img_cnn is not None and img_flat is not None:
                # CNN Prediction
                cnn_preds = cnn_model.predict(img_cnn)
                cnn_preds = (cnn_preds > 0.5).astype(int)

                # Logistic Regression Prediction
                lr_preds = logistic_model.predict(img_flat)

                # Append results
                results.append({
                    "Image": f"Image {i + 1}",
                    "CNN": "Pneumonia" if cnn_preds == 0 else "Normal",
                    "Logistic Regression": "Pneumonia" if lr_preds == 0 else "Normal"
                })
            else:
                results.append({
                    "Image": f"Image {i + 1}",
                    "CNN": "Error in processing",
                    "Logistic Regression": "Error in processing"
                })

        # Display results
        st.subheader("Prediction Results")
        for res in results:
            st.write(f"**{res['Image']}**")
            st.write(f"- CNN Prediction: {res['CNN']}")
            st.write(f"- Logistic Regression Prediction: {res['Logistic Regression']}")

else:
    st.info("Please upload one or more images to classify.")
