import streamlit as st
from database.database import verify_user
from pages.BasePage import BasePage

class LoginPage(BasePage):
    def __init__(self):
        super().__init__()
        self.title = "Login"
        self.icon = "🔑"
        
    def apply_custom_css(self):
        st.markdown("""
            <style>
            .login-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 2rem;
                background: #1E1E1E;
                border-radius: 12px;
                border: 1px solid #333;
            }
            
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .login-logo {
                width: 80px;
                height: 80px;
                margin: 0 auto 1rem;
                display: block;
            }
            
            .login-title {
                font-size: 1.5rem;
                color: #E0E0E0;
                margin-bottom: 0.5rem;
            }
            
            .login-subtitle {
                color: #888;
                font-size: 0.9rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 1rem 0;
            }
            
            .forgot-password {
                color: #2196F3;
                text-decoration: none;
                font-size: 0.9rem;
            }
            
            .forgot-password:hover {
                text-decoration: underline;
            }
            
            .social-login {
                margin-top: 2rem;
                text-align: center;
            }
            
            .divider {
                display: flex;
                align-items: center;
                text-align: center;
                margin: 1.5rem 0;
                color: #666;
            }
            
            .divider::before,
            .divider::after {
                content: '';
                flex: 1;
                border-bottom: 1px solid #333;
            }
            
            .divider span {
                padding: 0 1rem;
                color: #888;
                font-size: 0.85rem;
            }
            
            .social-buttons {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin: 1rem 0;
            }
            
            .social-button {
                background: #1A1A1A;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 0.75rem;
                color: #CCC;
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .social-button:hover {
                background: #242424;
                border-color: #444;
            }
            
            .social-button img {
                width: 20px;
                height: 20px;
                filter: brightness(0) invert(0.7);
            }
            
            .register-link {
                text-align: center;
                margin-top: 1.5rem;
                padding: 1rem;
                background: #1A1A1A;
                border: 1px solid #333;
                border-radius: 8px;
            }
            
            .register-text {
                color: #888;
                font-size: 0.9rem;
                margin: 0;
            }
            
            .register-link a {
                color: #2196F3;
                text-decoration: none;
                font-weight: 500;
                margin-left: 0.25rem;
            }
            
            .register-link a:hover {
                color: #64B5F6;
            }
            
            /* Override Streamlit's default styles */
            .stButton > button {
                width: 100%;
                background: #2196F3;
                color: white;
                border: none;
                padding: 0.75rem;
                border-radius: 8px;
                font-weight: 500;
                margin-top: 1rem;
            }
            
            .stButton > button:hover {
                background: #1976D2;
                color: white;
                border: none;
            }
            
            .stTextInput > div > div {
                background-color: #1A1A1A;
                border: 1px solid #333;
                border-radius: 8px;
                color: white;
            }
            
            .stTextInput > div > div:focus-within {
                border-color: #2196F3;
                box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
            }
            </style>
        """, unsafe_allow_html=True)
    
    def render(self):
        super().render()
        self.apply_custom_css()
        
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=80)
                st.markdown("<h1 class='login-title'>Welcome back</h1>", unsafe_allow_html=True)
                st.markdown("<p class='login-subtitle'>Please enter your credentials to continue</p>", unsafe_allow_html=True)
                
                with st.form("login_form", clear_on_submit=True):
                    username = st.text_input("Username", placeholder="Enter your username")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        remember_me = st.checkbox("Remember me")
                    with col2:
                        st.markdown('<div style="text-align: right;"><a href="#" class="forgot-password">Forgot password?</a></div>', unsafe_allow_html=True)
                    
                    submit = st.form_submit_button("Sign in")
                    
                    if submit:
                        if not username or not password:
                            st.error("Please fill in all fields")
                            return
                        
                        success, user_id = verify_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_id = user_id
                            st.session_state.current_page = "Home"
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                
                st.markdown('<div class="divider"><span>or continue with</span></div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                        <div class="social-button">
                            <img src="https://cdn-icons-png.flaticon.com/512/2991/2991148.png" alt="Google">
                            Google
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("""
                        <div class="social-button">
                            <img src="https://cdn-icons-png.flaticon.com/512/3291/3291695.png" alt="GitHub">
                            GitHub
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div class="register-link">
                        <p class="register-text">
                            Don't have an account?
                            <a href="?page=register">Create an account</a>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
