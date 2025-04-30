from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import joblib
from dotenv import load_dotenv
import warnings

# Suppress HDF5 version warning
warnings.filterwarnings('ignore', category=UserWarning, module='h5py')

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize models as None
cnn_model = None
logistic_model = None
pca_transformer = None

def load_models():
    """Load all models"""
    global cnn_model, logistic_model, pca_transformer
    
    try:
        # Get the absolute path to the models directory
        models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        
        # Load CNN model
        cnn_path = os.path.join(models_dir, 'cnn_model.h5')
        if os.path.exists(cnn_path):
            cnn_model = tf.keras.models.load_model(
                cnn_path,
                custom_objects={
                    'InputLayer': tf.keras.layers.InputLayer,
                    'Conv2D': tf.keras.layers.Conv2D,
                    'MaxPooling2D': tf.keras.layers.MaxPooling2D,
                    'Flatten': tf.keras.layers.Flatten,
                    'Dense': tf.keras.layers.Dense,
                    'Dropout': tf.keras.layers.Dropout
                }
            )
            print("CNN model loaded successfully!")
        else:
            print(f"CNN model not found at {cnn_path}")
        
        # Load Logistic Regression model and PCA
        logistic_path = os.path.join(models_dir, 'logistic_regression_model.pkl')
        pca_path = os.path.join(models_dir, 'pca_transformer.pkl')
        
        if os.path.exists(logistic_path) and os.path.exists(pca_path):
            logistic_model = joblib.load(logistic_path)
            pca_transformer = joblib.load(pca_path)
            print("Logistic Regression model and PCA loaded successfully!")
        else:
            print(f"Logistic model or PCA not found at {logistic_path} or {pca_path}")
            
    except Exception as e:
        print(f"Error loading models: {str(e)}")

# Load models at startup
load_models()

def preprocess_image(image, model_type='cnn'):
    """Preprocess the image for model prediction"""
    # Resize image to match model input size
    image = image.resize((150, 150))
    # Convert to numpy array
    image_array = np.array(image)
    # Normalize pixel values
    image_array = image_array / 255.0
    
    if model_type == 'cnn':
        # Add batch dimension for CNN
        image_array = np.expand_dims(image_array, axis=0)
    else:
        # Flatten image for logistic regression
        image_array = image_array.reshape(1, -1)
        # Apply PCA transformation
        if pca_transformer is not None:
            image_array = pca_transformer.transform(image_array)
            
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if image is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        # Get the image file and model type
        image_file = request.files['file']
        model_type = request.args.get('model_type', 'cnn')  # Default to CNN
        
        # Check if file is empty
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Open and preprocess the image
        image = Image.open(image_file)
        processed_image = preprocess_image(image, model_type)
        
        # Make prediction based on model type
        if model_type == 'cnn':
            if cnn_model is None:
                return jsonify({'error': 'CNN model not loaded'}), 500
            prediction = cnn_model.predict(processed_image)
            probability = float(prediction[0][0])
        else:
            if logistic_model is None:
                return jsonify({'error': 'Logistic Regression model not loaded'}), 500
            prediction = logistic_model.predict_proba(processed_image)
            probability = float(prediction[0][1])  # Assuming 1 is positive class
        
        # Return result
        result = {
            'probability': probability,
            'has_pneumonia': probability > 0.5,
            'confidence': f"{probability * 100:.2f}%",
            'model_used': model_type
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'models': {
            'cnn': cnn_model is not None,
            'logistic': logistic_model is not None and pca_transformer is not None
        }
    }
    return jsonify(status)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug to False for production 