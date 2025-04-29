import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import pickle
from PIL import Image

# Load models
with open('models/logistic_regression_model.pkl', 'rb') as f:

    lr_model = pickle.load(f)

cnn_model = load_model('models/cnn_model.h5')

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
                lr_preds = lr_model.predict(img_flat)

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
