from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import joblib
import os

app = FastAPI(title="Pneumonia Detection API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the models
try:
    # Load CNN model
    cnn_model = tf.keras.models.load_model('../models/cnn_model.h5')
    
    # Load Logistic Regression model
    lr_model = joblib.load('../models/logistic_regression_model.pkl')
    
    # Load SVM model
    svm_model = joblib.load('../models/svm_model.pkl')
    
    # Load scaler
    scaler = joblib.load('../models/scaler.pkl')
    
    print("All models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    # Set models to None if they can't be loaded
    cnn_model = None
    lr_model = None
    svm_model = None
    scaler = None

def preprocess_image(image_bytes, for_cnn=True):
    # Convert bytes to image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Resize image
    image = image.resize((150, 150))
    
    # Convert to array and preprocess
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalize
    
    if for_cnn:
        # For CNN: add batch dimension and keep channels
        image_array = np.expand_dims(image_array, axis=0)
    else:
        # For traditional ML: flatten and scale
        image_array = image_array.flatten().reshape(1, -1)
        image_array = scaler.transform(image_array)
    
    return image_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image file
    contents = await file.read()
    
    # Initialize results
    results = {
        "cnn": {"prediction": None, "probability": None, "has_pneumonia": None},
        "logistic_regression": {"prediction": None, "probability": None, "has_pneumonia": None},
        "svm": {"prediction": None, "probability": None, "has_pneumonia": None}
    }
    
    # Make predictions with each model if available
    if cnn_model is not None:
        # Preprocess for CNN
        processed_image_cnn = preprocess_image(contents, for_cnn=True)
        
        # CNN prediction
        cnn_prediction = cnn_model.predict(processed_image_cnn)[0][0]
        results["cnn"] = {
            "prediction": float(cnn_prediction),
            "probability": float(cnn_prediction),
            "has_pneumonia": bool(cnn_prediction > 0.5)
        }
    
    if lr_model is not None:
        # Preprocess for Logistic Regression
        processed_image_lr = preprocess_image(contents, for_cnn=False)
        
        # Logistic Regression prediction
        lr_prediction = lr_model.predict_proba(processed_image_lr)[0][1]
        results["logistic_regression"] = {
            "prediction": float(lr_prediction),
            "probability": float(lr_prediction),
            "has_pneumonia": bool(lr_prediction > 0.5)
        }
    
    if svm_model is not None:
        # Preprocess for SVM
        processed_image_svm = preprocess_image(contents, for_cnn=False)
        
        # SVM prediction
        svm_prediction = svm_model.predict_proba(processed_image_svm)[0][1]
        results["svm"] = {
            "prediction": float(svm_prediction),
            "probability": float(svm_prediction),
            "has_pneumonia": bool(svm_prediction > 0.5)
        }
    
    return results

@app.get("/health")
async def health_check():
    # Check if models are loaded
    models_status = {
        "cnn_model": cnn_model is not None,
        "logistic_regression_model": lr_model is not None,
        "svm_model": svm_model is not None,
        "scaler": scaler is not None
    }
    
    return {
        "status": "healthy" if all(models_status.values()) else "degraded",
        "models_loaded": models_status
    } 