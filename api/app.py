from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model
model_path = os.getenv('MODEL_PATH', 'models/pneumonia_model.h5')
model = None

try:
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
    else:
        print(f"Model not found at {model_path}. Please make sure the model file exists.")
        print("Running in simulation mode with random predictions.")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    print("Running in simulation mode with random predictions.")

def preprocess_image(image):
    """Preprocess the image for model prediction"""
    # Resize image
    image = image.resize((224, 224))
    # Convert to numpy array
    image_array = np.array(image)
    # Normalize pixel values
    image_array = image_array / 255.0
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def generate_simulated_prediction():
    """Generate a simulated prediction result"""
    # Generate a random probability between 0 and 1
    pneumonia_probability = random.uniform(0, 1)
    
    # Determine if the patient has pneumonia based on the probability
    has_pneumonia = pneumonia_probability > 0.5
    
    # Calculate confidence
    confidence = f"{pneumonia_probability * 100:.2f}%" if has_pneumonia else f"{(1 - pneumonia_probability) * 100:.2f}%"
    
    return {
        'pneumonia_probability': pneumonia_probability,
        'has_pneumonia': has_pneumonia,
        'confidence': confidence
    }

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        # Return simulated results when model is not loaded
        print("Model not loaded. Returning simulated results.")
        return jsonify(generate_simulated_prediction())
        
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        # Get the image file
        image_file = request.files['image']
        
        # Check if file is empty
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Open and preprocess the image
        image = Image.open(image_file)
        processed_image = preprocess_image(image)
        
        # Make prediction
        prediction = model.predict(processed_image)
        
        # Get the probability of pneumonia
        pneumonia_probability = float(prediction[0][0])
        
        # Determine the result
        result = {
            'pneumonia_probability': pneumonia_probability,
            'has_pneumonia': pneumonia_probability > 0.5,
            'confidence': f"{pneumonia_probability * 100:.2f}%" if pneumonia_probability > 0.5 else f"{(1 - pneumonia_probability) * 100:.2f}%"
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy' if model is not None else 'simulation',
        'model_loaded': model is not None
    }
    return jsonify(status)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 