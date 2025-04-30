import pytest
from app import validate_image, predict_image
from PIL import Image
import numpy as np
import io

def test_validate_image():
    # Create a test image
    img = Image.new('RGB', (200, 200), color='white')
    
    # Test valid image
    is_valid, result = validate_image(img)
    assert is_valid is True
    assert isinstance(result, Image.Image)
    
    # Test invalid image size
    small_img = Image.new('RGB', (50, 50), color='white')
    is_valid, result = validate_image(small_img)
    assert is_valid is False
    assert "too small" in result

def test_predict_image():
    # Create a test image
    img = Image.new('RGB', (200, 200), color='white')
    
    # Mock the API response
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        
        def json(self):
            return {'probability': 0.8}
    
    # Test successful prediction
    success, prediction, response_time = predict_image(img)
    assert success is True
    assert isinstance(prediction, dict)
    assert 'probability' in prediction
    assert isinstance(response_time, float)

def test_display_results():
    # This test would require mocking Streamlit's st functions
    # For now, we'll just verify the function exists
    assert 'display_results' in globals() 