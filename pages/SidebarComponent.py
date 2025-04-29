import streamlit as st
from config.config import THEME_CONFIG

class SidebarComponent:
    def __init__(self):
        self.pages = {
            "Home": {
                "icon": "🏠",
                "title": "Home",
                "auth_required": False
            },
            "Login": {
                "icon": "🔑",
                "title": "Login",
                "auth_required": False,
                "hide_when_auth": True
            },
            "Register": {
                "icon": "📝",
                "title": "Register",
                "auth_required": False,
                "hide_when_auth": True
            },
            "Pneumonia Detection": {
                "icon": "🩻",
                "title": "Pneumonia Detection",
                "auth_required": True
            },
            #"Model Comparison": {
             #   "icon": "📈",
              #  "title": "Model Comparison",
               # "auth_required": True
            #},
            #"Dataset Explorer": {
             #   "icon": "📊",
              #  "title": "Dataset Explorer",
               # "auth_required": True
            #},
            #"Training Insights": {
             #   "icon": "🧠",
              #  "title": "Training Insights",
               # "auth_required": True
            #},
            "Profile": {
                "icon": "👤",
                "title": "Profile",
                "auth_required": True
            },
            "About": {
                "icon": "ℹ️",
                "title": "About",
                "auth_required": False
            },
            "Logout": {
                "icon": "🚪",
                "title": "Logout",
                "auth_required": True
            }
        }
    
    def render(self):
        with st.sidebar:
            st.markdown("""
            <style>
            .sidebar-title {
                text-align: center;
                padding: 15px 0;
                margin-bottom: 20px;
                border-bottom: 1px solid #2c3e50;
            }
            
            .nav-link {
                padding: 10px 15px;
                margin: 5px 0;
                border-radius: 5px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .nav-link:hover {
                background-color: #2c3e50;
            }
            
            .nav-section {
                margin: 20px 0;
                padding-top: 10px;
                border-top: 1px solid #2c3e50;
            }
            
            .nav-section-title {
                font-size: 0.8em;
                color: #7f8c8d;
                text-transform: uppercase;
                margin-bottom: 10px;
                padding-left: 15px;
            }
            </style>
            """, unsafe_allow_html=True)

            # Logo and Title
            st.image("https://cdn-icons-png.flaticon.com/512/4006/4006511.png", width=80)
            st.markdown("<h1 class='sidebar-title'>Pneumonia Detection</h1>", unsafe_allow_html=True)

            # Main Navigation
            st.markdown("<div class='nav-section-title'>MAIN</div>", unsafe_allow_html=True)
            selected = None
            
            # Home is always visible
            if st.sidebar.button(f"🏠 Home", key="home", use_container_width=True):
                selected = "Home"

            # Authentication Section
            if not st.session_state.logged_in:
                st.markdown("<div class='nav-section-title'>AUTHENTICATION</div>", unsafe_allow_html=True)
                if st.sidebar.button("🔑 Login", key="login", use_container_width=True):
                    selected = "Login"
                if st.sidebar.button("📝 Register", key="register", use_container_width=True):
                    selected = "Register"

            # Prediction Section (Only visible when logged in)
            if st.session_state.logged_in:
                st.markdown("<div class='nav-section-title'>PREDICTION</div>", unsafe_allow_html=True)
                if st.sidebar.button("🩻 Pneumonia Detection", key="detection", use_container_width=True):
                    selected = "Pneumonia Detection"

                # Analysis Section
               # st.markdown("<div class='nav-section-title'>ANALYSIS</div>", unsafe_allow_html=True)
                #if st.sidebar.button("📈 Model Comparison", key="comparison", use_container_width=True):
                 #   selected = "Model Comparison"
                #if st.sidebar.button("📊 Dataset Explorer", key="explorer", use_container_width=True):
                 #   selected = "Dataset Explorer"
                #if st.sidebar.button("🧠 Training Insights", key="insights", use_container_width=True):
                 #   selected = "Training Insights"

                # User Section
                st.markdown("<div class='nav-section-title'>USER</div>", unsafe_allow_html=True)
                if st.sidebar.button("👤 Profile", key="profile", use_container_width=True):
                    selected = "Profile"

            # About is always visible
            st.markdown("<div class='nav-section-title'>INFO</div>", unsafe_allow_html=True)
            if st.sidebar.button("ℹ️ About", key="about", use_container_width=True):
                selected = "About"

            # Logout only visible when logged in
            if st.session_state.logged_in:
                if st.sidebar.button("🚪 Logout", key="logout", use_container_width=True):
                    selected = "Logout"

            return selected if selected else st.session_state.current_page 