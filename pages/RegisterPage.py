import streamlit as st
from database.database import create_user
from pages.BasePage import BasePage

class RegisterPage(BasePage):
    def __init__(self):
        super().__init__()
        self.title = "Register"
        self.icon = "📝"
        
    def apply_custom_css(self):
        st.markdown("""
            <style>
            .register-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 2rem;
                background: #1E1E1E;
                border-radius: 12px;
                border: 1px solid #333;
            }
            
            .register-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .register-logo {
                width: 80px;
                height: 80px;
                margin: 0 auto 1rem;
                display: block;
            }
            
            .register-title {
                font-size: 1.5rem;
                color: #E0E0E0;
                margin-bottom: 0.5rem;
            }
            
            .register-subtitle {
                color: #888;
                font-size: 0.9rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-info {
                color: #888;
                font-size: 0.8rem;
                margin-top: 0.25rem;
            }
            
            .password-requirements {
                background: #1A1A1A;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            }
            
            .requirement-item {
                color: #888;
                font-size: 0.85rem;
                margin: 0.5rem 0;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .requirement-item.valid {
                color: #4CAF50;
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
            
            .login-link {
                text-align: center;
                margin-top: 1.5rem;
                padding: 1rem;
                background: #1A1A1A;
                border: 1px solid #333;
                border-radius: 8px;
            }
            
            .login-text {
                color: #888;
                font-size: 0.9rem;
                margin: 0;
            }
            
            .login-link a {
                color: #2196F3;
                text-decoration: none;
                font-weight: 500;
                margin-left: 0.25rem;
            }
            
            .login-link a:hover {
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
                st.image("https://cdn-icons-png.flaticon.com/512/4006/4006511.png", width=80)
                st.markdown("<h1 class='register-title'>Create an Account</h1>", unsafe_allow_html=True)
                st.markdown("<p class='register-subtitle'>Join our community of medical professionals</p>", unsafe_allow_html=True)
                
                with st.form("register_form", clear_on_submit=True):
                    # Personal Information
                    st.markdown("##### Personal Information")
                    full_name = st.text_input("Full Name", placeholder="Enter your full name")
                    email = st.text_input("Email", placeholder="Enter your email address")
                    
                    # Account Information
                    st.markdown("##### Account Information")
                    username = st.text_input("Username", placeholder="Choose a username")
                    password = st.text_input("Password", type="password", placeholder="Create a password")
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                    
                    # Password Requirements
                    st.markdown("""
                        <div class="password-requirements">
                            <div class="requirement-item">• At least 8 characters long</div>
                            <div class="requirement-item">• Contains at least one uppercase letter</div>
                            <div class="requirement-item">• Contains at least one number</div>
                            <div class="requirement-item">• Contains at least one special character</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Terms and Conditions
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        terms = st.checkbox("I agree to the Terms and Conditions")
                    with col2:
                        st.markdown('<a href="#" style="color: #2196F3; font-size: 0.9rem;">Read more</a>', unsafe_allow_html=True)
                    
                    # Submit Button
                    submit = st.form_submit_button("Create Account")
                    
                    if submit:
                        if not all([full_name, email, username, password, confirm_password]):
                            st.error("Please fill in all fields")
                            return
                        
                        if not terms:
                            st.error("Please accept the Terms and Conditions")
                            return
                        
                        if password != confirm_password:
                            st.error("Passwords do not match")
                            return
                        
                        # Add password validation here
                        if len(password) < 8:
                            st.error("Password must be at least 8 characters long")
                            return
                        
                        success = create_user(username, password, email, full_name)
                        if success:
                            st.success("Account created successfully! Please login.")
                            st.session_state.current_page = "Login"
                            st.rerun()
                        else:
                            st.error("Username or email already exists")
                
                # Social Registration Options
                st.markdown('<div class="divider"><span>or register with</span></div>', unsafe_allow_html=True)
                
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
                
                # Login Link
                st.markdown("""
                    <div class="login-link">
                        <p class="login-text">
                            Already have an account?
                            <a href="?page=login">Sign in</a>
                        </p>
                    </div>
                """, unsafe_allow_html=True) 