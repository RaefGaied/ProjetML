import streamlit as st
from config.config import THEME_CONFIG

# Hide the default Streamlit sidebar navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

class AboutPage:
    def render(self):
        st.title("About Pneumonia Detection System")
        
        # Hero Section
        st.markdown(f"""
        <div style="background-color: {THEME_CONFIG['secondaryBackgroundColor']}; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h2 style="color: {THEME_CONFIG['primaryColor']}; text-align: center;">Revolutionizing Pneumonia Diagnosis with AI</h2>
            <p style="text-align: center; color: {THEME_CONFIG['textColor']};">
                Our advanced AI-powered system helps medical professionals detect pneumonia with high accuracy using chest X-ray images.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features Section
        st.markdown("### Key Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background-color: {THEME_CONFIG['secondaryBackgroundColor']}; border-radius: 10px;">
                <h3>🔬 High Accuracy</h3>
                <p>State-of-the-art deep learning models trained on thousands of X-ray images</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background-color: {THEME_CONFIG['secondaryBackgroundColor']}; border-radius: 10px;">
                <h3>⚡ Fast Results</h3>
                <p>Get instant predictions to help make timely medical decisions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background-color: {THEME_CONFIG['secondaryBackgroundColor']}; border-radius: 10px;">
                <h3>📊 Detailed Analysis</h3>
                <p>Comprehensive reports and confidence scores for each prediction</p>
            </div>
            """, unsafe_allow_html=True)
        
        # How It Works Section
        st.markdown("### How It Works")
        steps = [
            ("1. Upload X-ray", "Upload a chest X-ray image in DICOM or JPEG format"),
            ("2. AI Analysis", "Our deep learning model analyzes the image for pneumonia indicators"),
            ("3. Get Results", "Receive detailed analysis and prediction results"),
            ("4. Save & Share", "Save results to your profile and share with medical professionals")
        ]
        
        for step, description in steps:
            st.markdown(f"""
            <div style="background-color: {THEME_CONFIG['secondaryBackgroundColor']}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <h4>{step}</h4>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Team Section
        st.markdown("### Our Team")
        team_members = [
            ("Mohamed Aziz Romdhane", "Software Engineering Student", "👨‍💻"),
            ("Raef Gaied", "Software Engineering Student", "👨‍💻"),
            ("Mahmoud Frayeh", "Software Engineering Student", "👨‍💻")
        ]
        
        cols = st.columns(3)
        for i, (name, role, emoji) in enumerate(team_members):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background-color: {THEME_CONFIG['secondaryBackgroundColor']}; border-radius: 10px;">
                    <h3>{emoji}</h3>
                    <h4>{name}</h4>
                    <p>{role}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Contact Section
        #st.markdown("### Contact Us")
        #st.markdown(f"""
        #<div style="background-color: {THEME_CONFIG['secondaryBackgroundColor']}; padding: 1rem; border-radius: 10px;">
         #   <p>📧 Email: mohamedaziz.romdhane@polytechnicien.tn</p>
        #    <p>📞 Phone: +216 99055322</p>
        #    <p>🏢 Address: Eljem 5160 Rue arbi zarrouk</p>
        #</div>
        #""", unsafe_allow_html=True)

        # Contact Section
        st.markdown("### Contact Us")
        st.markdown(f"""
        <div style="background-color: {THEME_CONFIG['secondaryBackgroundColor']}; padding: 1rem; border-radius: 10px;">
        <p>📧 Emails:</p>
        <ul>
            <li>Raef Gaied: raefgaied@gmail.com</li>
            <li>Mohamed Aziz Romadhane: mohamedazizromdhane509@gmail.com</li>
            <li>Mahmoud FRAYEH: frayahmahmoud620@gmail.com</li>
        </ul>
        </div>
            """, unsafe_allow_html=True)


        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: {THEME_CONFIG['textColor']};">
            <p>© 2025 Pneumonia Detection System. All rights reserved.</p>
            <p>This system is intended for medical professionals and should be used as a supplementary tool.</p>
        </div>
        """, unsafe_allow_html=True) 