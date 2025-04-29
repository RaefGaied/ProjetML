import requests
import streamlit as st

API_URL = "http://localhost:5000"  # Change this to your API URL in production

def predict_pneumonia(image_file, model_type="logistic_regression"):
    """Send image to API and get prediction"""
    try:
        files = {'image': image_file}
        data = {'model_type': model_type}
        response = requests.post(f"{API_URL}/predict", files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.json().get('error', 'Unknown error')}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure it's running.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None 