import os
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

def download_model():
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Check if model already exists
    if os.path.exists('models/pneumonia_model.h5'):
        print("Model already exists. Skipping download.")
        return
    
    try:
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()
        
        # Download the model
        print("Downloading model...")
        api.dataset_download_file(
            'paultimothymooney/chest-xray-pneumonia',
            'model.h5',
            path='models',
            force=True
        )
        
        # Unzip the file
        with zipfile.ZipFile('models/model.h5.zip', 'r') as zip_ref:
            zip_ref.extractall('models')
        
        # Rename the file
        os.rename('models/model.h5', 'models/pneumonia_model.h5')
        
        # Clean up
        os.remove('models/model.h5.zip')
        print("Model downloaded successfully!")
        
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        print("Please download the model manually and place it in the models directory.")

if __name__ == "__main__":
    download_model() 