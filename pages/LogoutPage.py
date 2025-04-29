import streamlit as st
from pages.BasePage import BasePage

class LogoutPage(BasePage):
    def __init__(self):
        super().__init__()
        self.title = "Logout"
        self.icon = "🚪"
    
    def render(self):
        super().render()
        
        # Confirmation message
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 2rem; border-radius: 10px; margin: 2rem 0;">
            <h2 style="color: #1E88E5;">Are you sure you want to logout?</h2>
            <p style="font-size: 1.1em;">
                You will need to login again to access your account and make predictions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        if st.button("Logout", type="primary"):
            # Clear session state
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_id = ""
            
            # Show success message
            self.display_success("You have been successfully logged out.")
            
            # Rerun the app to update the UI
            st.experimental_rerun()
        
        # Cancel button
        if st.button("Cancel"):
            st.experimental_rerun() 