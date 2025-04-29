import streamlit as st
from config.config import THEME_CONFIG

class BasePage:
    def __init__(self):
        self.title = "Base Page"
        self.icon = "📄"
    
    def render(self):
        """Base render method that should be overridden by child classes."""
        st.title(f"{self.icon} {self.title}")
        
    def display_error(self, message):
        """Display error message in a styled format."""
        st.markdown(f"""
        <div style="background-color: #FFEBEE; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #F44336;">
            <p style="color: #D32F2F; margin: 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_success(self, message):
        """Display success message in a styled format."""
        st.markdown(f"""
        <div style="background-color: #E8F5E9; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #4CAF50;">
            <p style="color: #2E7D32; margin: 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_info(self, message):
        """Display info message in a styled format."""
        st.markdown(f"""
        <div style="background-color: #E3F2FD; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #2196F3;">
            <p style="color: #1565C0; margin: 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_warning(self, message):
        """Display warning message in a styled format."""
        st.markdown(f"""
        <div style="background-color: #FFF3E0; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #FF9800;">
            <p style="color: #E65100; margin: 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def create_card(self, title, content):
        """Create a styled card component."""
        st.markdown(f"""
        <div style="background-color: {THEME_CONFIG['secondaryBackgroundColor']}; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: {THEME_CONFIG['primaryColor']}; margin-top: 0;">{title}</h3>
            {content}
        </div>
        """, unsafe_allow_html=True) 