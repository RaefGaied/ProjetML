import os

# Page Configuration
PAGE_TITLE = "Pneumonia Detection System"
PAGE_ICON = "🫁"

# Model Paths
CNN_MODEL_PATH = "models/cnn_model.h5"
LOGISTIC_REGRESSION_PATH = "models/logistic_regression_model.pkl"
PCA_TRANSFORMER_PATH = "models/pca_transformer.pkl"

# Database Configuration
DATABASE_PATH = "database/users.db"

# API Configuration
API_BASE_URL = os.environ.get("API_BASE_URL", "https://projetml.onrender.com")

def get_api_url(endpoint=""):
    """Get the full API URL for a given endpoint"""
    return f"{API_BASE_URL}/{endpoint.lstrip('/')}"

# Theme Configuration
THEME_CONFIG = {
    "primaryColor": "#1E88E5",
    "backgroundColor": "#1E1E1E",
    "secondaryBackgroundColor": "#2D2D2D",
    "textColor": "#FFFFFF",
    "font": "sans serif"
} 