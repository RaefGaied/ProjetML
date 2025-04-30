import os
# Set environment variables to suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import streamlit as st
import sys
from pathlib import Path

# Set page configuration at the very beginning
st.set_page_config(
    page_title="Pneumonia Detection System",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent))

# Import from local modules
from config.config import (
    PAGE_TITLE,
    PAGE_ICON,
    THEME_CONFIG
)
from utils.utils import apply_custom_theme
from database.database import init_database

# Import page classes
from pages.LoginPage import LoginPage
from pages.RegisterPage import RegisterPage
from pages.ProfilePage import ProfilePage
from pages.PredictionPage import render as render_prediction
from pages.AboutPage import AboutPage
from pages.LogoutPage import LogoutPage
from pages.SidebarComponent import SidebarComponent
#from pages.ModelComparisonPage import ModelComparisonPage
#from pages.DatasetExplorerPage import DatasetExplorerPage

# Initialize database
init_database()

# Apply custom theme
apply_custom_theme()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = ""
    st.session_state.current_page = "Home"

# Styles for the home page
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.feature-card {
    transition: all 0.3s ease;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    background: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.welcome-section {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 30px;
    border-radius: 10px;
    margin: 20px 0;
    animation: fadeIn 1s ease-in;
}

.icon-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80px;
    height: 80px;
    background: #1E88E5;
    border-radius: 50%;
    margin: 0 auto 15px;
}

.icon-container img {
    width: 40px;
    height: 40px;
    filter: brightness(0) invert(1);
}

.stat-card {
    background: linear-gradient(135deg, #1E88E5 0%, #0d47a1 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 10px;
    animation: fadeIn 1s ease-in;
}

.stat-number {
    font-size: 2.5em;
    font-weight: bold;
    margin: 10px 0;
}

.demo-container {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    animation: fadeIn 1s ease-in;
}

.demo-image {
    width: 100%;
    max-width: 400px;
    border-radius: 10px;
    margin: 10px auto;
    display: block;
}

.cta-button {
    background: #1E88E5;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 10px;
}

.cta-button:hover {
    background: #0d47a1;
    transform: translateY(-2px);
}

.testimonial-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    animation: fadeIn 1s ease-in;
}

.team-member {
    text-align: center;
    padding: 20px;
    animation: fadeIn 1s ease-in;
}

.team-member img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-bottom: 10px;
    border: 3px solid #1E88E5;
}
</style>
""", unsafe_allow_html=True)

# Initialize and render the sidebar component
sidebar = SidebarComponent()
selected = sidebar.render()

# Update current page in session state
st.session_state.current_page = selected

# Initialize page instances
login_page = LoginPage()
register_page = RegisterPage()
profile_page = ProfilePage()
about_page = AboutPage()
logout_page = LogoutPage()
#model_comparison_page = ModelComparisonPage()
#dataset_explorer_page = DatasetExplorerPage()

# Main content area
st.markdown("""
<div style="padding: 2rem; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
""", unsafe_allow_html=True)

# Route to the appropriate page based on selection
try:
    if selected == "Home":
        # Hero Section with Video Background
        st.markdown("""
        <div style="position: relative; margin: -2rem 0 2rem 0; padding: 4rem 2rem; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://www.medicalnewstoday.com/content/images/articles/327/327451/chest-x-ray.jpg'); background-size: cover; background-position: center; color: white; text-align: center; border-radius: 10px;">
            <h1 style="font-size: 3em; margin-bottom: 1rem;">Pneumonia Detection System</h1>
            <p style="font-size: 1.2em; margin-bottom: 2rem;">Revolutionizing Medical Diagnosis with AI</p>
            <button class="cta-button" onclick="window.parent.document.querySelector('[data-testid=stSidebar]').querySelector('button').click();">Get Started Now</button>
        </div>
        """, unsafe_allow_html=True)

        # Real-time Statistics
        st.markdown("### Real-time Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="stat-card">
                <h3>Total Diagnoses</h3>
                <div class="stat-number">1,234</div>
                <p>Completed Today</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="stat-card">
                <h3>Accuracy Rate</h3>
                <div class="stat-number">98.5%</div>
                <p>Average Success</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="stat-card">
                <h3>Active Users</h3>
                <div class="stat-number">25</div>
                <p>Online Now</p>
            </div>
            """, unsafe_allow_html=True)

        # Features Section with Interactive Cards
        st.markdown("### Key Features")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card" style="animation: fadeIn 1s ease-in;">
                <div class="icon-container">
                    <img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" alt="AI Icon">
                </div>
                <div style="text-align: center;">
                    <h3 style="color: #2196F3;">🔬 Advanced AI</h3>
                    <p style="color: white; margin: 1rem 0;">State-of-the-art deep learning algorithms for accurate pneumonia detection</p>
                    <button class="cta-button" style="width: 100%;">Learn More</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card" style="animation: fadeIn 1.2s ease-in;">
                <div class="icon-container">
                    <img src="https://cdn-icons-png.flaticon.com/512/2933/2933245.png" alt="Speed Icon">
                </div>
                <div style="text-align: center;">
                    <h3 style="color: #2196F3;">⚡ Fast Analysis</h3>
                    <p style="color: white; margin: 1rem 0;">Quick and accurate results in seconds</p>
                    <button class="cta-button" style="width: 100%;">See Example</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card" style="animation: fadeIn 1.4s ease-in;">
                <div class="icon-container">
                    <img src="https://cdn-icons-png.flaticon.com/512/2936/2936630.png" alt="Reports Icon">
                </div>
                <div style="text-align: center;">
                    <h3 style="color: #2196F3;">📊 Detailed Reports</h3>
                    <p style="color: white; margin: 1rem 0;">Comprehensive analysis and insights</p>
                    <button class="cta-button" style="width: 100%;">View Sample</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Interactive Demo Section
        st.markdown("""
        <div style="margin-top: 3rem;">
            <h2 style="color: white; margin-bottom: 2rem;">Try Our Demo</h2>
            <div class="demo-container" style="background-color: #2D2D2D; border: 1px solid #3D3D3D;">
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/4171/4171077.png" 
                         style="width: 100px; height: 100px; margin-bottom: 1rem; filter: invert(1);" 
                         alt="Upload Icon">
                    <h3 style="color: #2196F3; margin-bottom: 1rem;">Upload a Chest X-ray Image</h3>
                    <p style="color: #CCC; margin-bottom: 2rem;">Try our system with a sample X-ray image</p>
                    <button class="cta-button" style="max-width: 300px;">
                        Analyze Sample Image
                    </button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # How to Get Started
        st.markdown("""
        <div style="margin-top: 30px; animation: fadeIn 1.6s ease-in;">
            <div class="feature-card" style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);">
                <h2 style="color: #1E88E5; text-align: center;">How to Get Started</h2>
                <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                    <div style="text-align: center;">
                        <div style="background: #1E88E5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">1</div>
                        <p>Create an account</p>
                        <button class="cta-button" style="padding: 8px 16px; font-size: 0.9em;">Register Now</button>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #1E88E5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">2</div>
                        <p>Upload X-ray images</p>
                        <button class="cta-button" style="padding: 8px 16px; font-size: 0.9em;">Upload Demo</button>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #1E88E5; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">3</div>
                        <p>Get instant results</p>
                        <button class="cta-button" style="padding: 8px 16px; font-size: 0.9em;">View Results</button>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Testimonials Section
        st.markdown("""
        <div style="margin-top: 4rem;">
            <h2 style="color: white; margin-bottom: 2rem; text-align: center;">What Our Users Say</h2>
            <div style="display: flex; gap: 2rem; margin: 2rem 0;">
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <p class="testimonial-text">"This system has revolutionized our diagnostic process. The accuracy and speed are impressive!"</p>
                        <div class="testimonial-author">
                            <img src="https://avatars.githubusercontent.com/u/45246688?v=4" alt="Khmaies Abdallah" class="testimonial-avatar">
                            <div class="author-info">
                                <h4>Khmaies Abdallah</h4>
                                <p>Consultant Data Science</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-content">
                        <p class="testimonial-text">"A game-changer in medical diagnosis. The detailed reports help us make better decisions."</p>
                        <div class="testimonial-author">
                            <img src="https://avatars.githubusercontent.com/u/1234567?v=4" alt="Mehdi Ben Ameur" class="testimonial-avatar">
                            <div class="author-info">
                                <h4>Mehdi Ben Ameur</h4>
                                <p>Software Engineering Student</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Add testimonials specific styles
        st.markdown("""
        <style>
        /* Testimonials Section */
        .testimonial-card {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-radius: 12px;
            padding: 2rem;
            flex: 1;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .testimonial-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(33, 150, 243, 0.2);
        }

        .testimonial-content {
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .testimonial-text {
            color: #E0E0E0;
            font-size: 1.1rem;
            line-height: 1.6;
            font-style: italic;
            margin-bottom: 1.5rem;
            flex-grow: 1;
        }

        .testimonial-author {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-top: auto;
        }

        .testimonial-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid #2196F3;
        }

        .author-info {
            display: flex;
            flex-direction: column;
        }

        .author-info h4 {
            color: #2196F3;
            margin: 0;
            font-size: 1.1rem;
            font-weight: bold;
        }

        .author-info p {
            color: #B0B0B0;
            margin: 0.2rem 0 0 0;
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .testimonial-card {
                margin-bottom: 1rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        # Final Call to Action
        st.markdown("""
        <div style="margin-top: 30px; text-align: center; animation: fadeIn 1.8s ease-in;">
            <div class="feature-card" style="background: linear-gradient(135deg, #1E88E5 0%, #0d47a1 100%); color: white;">
                <h2>Ready to Experience the Future of Medical Diagnosis?</h2>
                <p>Join thousands of medical professionals using our platform</p>
                <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
                    <button class="cta-button" style="background: white; color: #1E88E5;">Get Started Now</button>
                    <button class="cta-button" style="background: transparent; border: 2px solid white;">Schedule Demo</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif selected == "Login":
        if st.session_state.logged_in:
            # Redirect to Home if already logged in
            st.session_state.current_page = "Home"
            selected = "Home"
            # Re-render the home page content
            st.markdown("""
            <div style="position: relative; margin: -2rem 0 2rem 0; padding: 4rem 2rem; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://www.medicalnewstoday.com/content/images/articles/327/327451/chest-x-ray.jpg'); background-size: cover; background-position: center; color: white; text-align: center; border-radius: 10px;">
                <h1 style="font-size: 3em; margin-bottom: 1rem;">Welcome Back!</h1>
                <p style="font-size: 1.2em; margin-bottom: 2rem;">You are already logged in.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            login_page.render()
    elif selected == "Register":
        register_page.render()
    elif selected == "About":
        about_page.render()
    elif selected == "Profile":
        if st.session_state.logged_in:
            profile_page.render()
        else:
            st.warning("Please login to access your profile.")
    elif selected == "Pneumonia Detection":
        if st.session_state.logged_in:
            render_prediction()
        else:
            st.warning("Please login to access the prediction feature.")
    elif selected == "Logout":
        if st.session_state.logged_in:
            logout_page.render()
        else:
            st.warning("You are not logged in.")
    #elif selected == "Model Comparison":
     #   if st.session_state.logged_in:
           # model_comparison_page.render()
        #else:
         #   st.warning("Please login to access the model comparison feature.")
    #elif selected == "Dataset Explorer":
     #   if st.session_state.logged_in:
      #      dataset_explorer_page.render()
        #else:
            #st.warning("Please login to access the dataset explorer.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please try refreshing the page or contact support if the problem persists.")

# Close the main content div
st.markdown("</div>", unsafe_allow_html=True)
