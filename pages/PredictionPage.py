import streamlit as st
import base64
from utils.api_client import predict_pneumonia
import os
from pathlib import Path

def get_available_models():
    """Get list of available models from the models directory"""
    models = []
    model_descriptions = {
        "cnn_model.h5": {
            "name": "CNN Model",
            "description": "Le modèle CNN (Convolutional Neural Network) est spécialement conçu pour l'analyse d'images médicales. Il utilise des couches de convolution pour détecter automatiquement les caractéristiques importantes dans les radiographies thoraciques."
        },
        "logistic_regression_model.pkl": {
            "name": "Logistic Regression",
            "description": "La régression logistique est un modèle classique qui utilise des caractéristiques extraites des images pour classifier la présence ou l'absence de pneumonie."
        },
        "pca_transformer.pkl": {
            "name": "PCA Transformer",
            "description": "Le transformateur PCA est utilisé pour réduire la dimensionnalité des données avant l'application du modèle de régression logistique."
        }
    }
    
    # Get the root directory of the project
    root_dir = Path(__file__).parent.parent
    models_dir = root_dir / "models"
    
    try:
        # Check for model files in the models directory
        model_files = os.listdir(models_dir)
        # st.write("Available model files:", model_files)  # Debug info
        
        for model_file in model_files:
            if model_file in model_descriptions:
                models.append(model_descriptions[model_file])
        
        if not models:
            st.warning("No compatible models found in the models directory.")
        
    except Exception as e:
        st.error(f"Error accessing models directory: {str(e)}")
        return []
    
    return models

def render():
    st.markdown("""
    <style>
    /* Styles globaux */
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    
    /* Container principal */
    .main-container {
        background-color: #2D2D2D;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    /* Titre principal */
    h1 {
        color: #2196F3 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    /* Container de téléchargement */
    .upload-container {
        background-color: #2D2D2D;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        text-align: center;
        border: 1px solid #3D3D3D;
    }
    
    /* Avatar médical */
    .medical-avatar {
        width: 80px;
        height: 80px;
        margin-bottom: 1rem;
        filter: invert(1);
    }
    
    /* Titre de l'upload */
    .upload-title {
        color: #2196F3;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Container de l'image X-ray */
    .xray-container {
        background: #2D2D2D;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem auto;
        max-width: 400px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        border: 1px solid #3D3D3D;
    }
    
    /* Image X-ray */
    .xray-image {
        max-width: 350px;
        width: 100%;
        height: auto;
        border-radius: 10px;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sélecteur de modèle */
    div[data-baseweb="select"] {
        background-color: #2D2D2D !important;
        border: 1px solid #3D3D3D !important;
        border-radius: 8px !important;
        margin: 10px 0 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #2D2D2D !important;
        border: none !important;
        color: white !important;
    }
    
    /* Bouton d'analyse */
    .stButton > button {
        background-color: #2196F3 !important;
        color: white !important;
        width: 100% !important;
        padding: 0.5rem !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        background-color: #1976D2 !important;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3) !important;
    }
    
    /* Résultats */
    .results-container {
        background-color: #2D2D2D;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        border: 1px solid #3D3D3D;
    }
    
    /* Métriques */
    .metric-container {
        background-color: #3D3D3D;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-value {
        color: #2196F3;
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Description des modèles */
    .model-description {
        background-color: #3D3D3D;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        color: #CCC;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Pneumonia Detection")
    
    # Medical avatar and upload container
    st.markdown("""
    <div class="upload-container">
        <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0iIzIxOTZGMyI+PHBhdGggZD0iTTI0IDRjLTExLjA1IDAtMjAgOC45NS0yMCAyMHM4Ljk1IDIwIDIwIDIwIDIwLTguOTUgMjAtMjBTMzUuMDUgNCAyNCA0em0wIDM2Yy04LjgyIDAtMTYtNy4xOC0xNi0xNnM3LjE4LTE2IDE2LTE2IDE2IDcuMTggMTYgMTYtNy4xOCAxNi0xNiAxNnptLTQtMjJ2MTJoOFYxOGgtOHoiLz48L3N2Zz4=" 
             class="medical-avatar" alt="Medical Avatar"/>
        <div class="upload-title">Upload Chest X-ray Image</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get available models
    available_models = get_available_models()
    model_names = [model["name"] for model in available_models]
    
    # Model selector with custom styling
    st.markdown('<p style="color: #2196F3; font-size: 1.2rem; margin: 1rem 0;">Select a Model</p>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        "Select a Model",
        model_names,
        index=0,
        key="model_selector",
        label_visibility="collapsed"
    )

    # Display model description
    selected_model_info = next((model for model in available_models if model["name"] == selected_model), None)
    if selected_model_info:
        st.markdown(f"""
        <div class="model-description">
            {selected_model_info["description"]}
        </div>
        """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an X-ray image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image_bytes = uploaded_file.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        st.markdown(
            f'''
            <div class="xray-container">
                <img src="data:image/jpeg;base64,{image_base64}" 
                     alt="Uploaded X-ray" 
                     class="xray-image"/>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Center the analyze button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button("Analyze Image", use_container_width=True)
        
        if analyze_button:
            with st.spinner(f"Analyzing with {selected_model}..."):
                # Convert model name to API parameter
                model_type = selected_model.lower().replace(" ", "_")
                result = predict_pneumonia(uploaded_file, model_type=model_type)
                
                if result:
                    st.markdown("""
                    <div class="results-container">
                        <h2 style="color: #2196F3; text-align: center; margin-bottom: 1.5rem;">Analysis Results</h2>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-container">
                            <p style="color: #2196F3;">Pneumonia Probability</p>
                            <div class="metric-value">{result['pneumonia_probability']*100:.2f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        status = "Positive" if result['has_pneumonia'] else "Negative"
                        status_color = "#FF5252" if result['has_pneumonia'] else "#4CAF50"
                        st.markdown(f"""
                        <div class="metric-container">
                            <p style="color: #2196F3;">Diagnosis</p>
                            <div class="metric-value" style="color: {status_color}">{status}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display confidence
                    confidence_color = "#FF5252" if result['has_pneumonia'] else "#4CAF50"
                    st.markdown(f"""
                    <div class="metric-container" style="margin-top: 1rem;">
                        <p style="color: #2196F3;">Confidence</p>
                        <div class="metric-value" style="color: {confidence_color}">{result['confidence']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display interpretation
                    interpretation_style = "background-color: #3D3D3D; padding: 1rem; border-radius: 10px; margin-top: 1rem;"
                    if result['has_pneumonia']:
                        st.markdown(f"""
                        <div style="{interpretation_style}">
                            <h3 style="color: #FF5252;">Clinical Interpretation:</h3>
                            <ul style="color: white;">
                                <li>The X-ray shows signs of pneumonia</li>
                                <li>Please consult with a healthcare professional</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="{interpretation_style}">
                            <h3 style="color: #4CAF50;">Clinical Interpretation:</h3>
                            <ul style="color: white;">
                                <li>No clear signs of pneumonia detected</li>
                                <li>Regular monitoring recommended</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True) 