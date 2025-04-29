import streamlit as st
from pages.BasePage import BasePage
from database.database import get_user_info, get_user_history
from config.config import THEME_CONFIG
from datetime import datetime

class ProfilePage(BasePage):
    def __init__(self):
        super().__init__()
        self.title = "Profile"
        self.icon = "👤"
    
    def render(self):
        super().render()
        
        st.markdown("""
        <style>
        /* Styles globaux */
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        
        /* Cartes d'information */
        .info-card {
            background-color: #2D2D2D;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #3D3D3D;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .card-title {
            color: #2196F3;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            font-weight: bold;
        }
        
        .info-item {
            margin: 0.5rem 0;
            padding: 0.5rem;
            background-color: #3D3D3D;
            border-radius: 5px;
        }
        
        .info-label {
            color: #2196F3;
            font-size: 0.9rem;
            margin-bottom: 0.2rem;
        }
        
        .info-value {
            color: white;
            font-size: 1.1rem;
        }
        
        /* Boutons */
        .danger-button {
            background-color: #dc3545 !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            border-radius: 5px !important;
        }
        
        .primary-button {
            background-color: #2196F3 !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            border-radius: 5px !important;
        }
        
        /* Activité récente */
        .activity-card {
            background-color: #3D3D3D;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .activity-date {
            color: #2196F3;
            font-size: 0.9rem;
        }
        
        .activity-result {
            color: white;
            margin-top: 0.5rem;
        }
        
        /* Statistiques */
        .stat-card {
            background-color: #3D3D3D;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            margin: 0.5rem;
        }
        
        .stat-value {
            color: #2196F3;
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .stat-label {
            color: white;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)

        if not st.session_state.logged_in:
            st.warning("Please login to view your profile.")
            return

        user_info = get_user_info(st.session_state.user_id)
        if not user_info:
            st.error("Could not load user information.")
            return

        # En-tête du profil
        st.title(f"Welcome, {user_info['username']}!")

        # Disposition en colonnes
        col1, col2 = st.columns(2)

        with col1:
            # Informations personnelles
            st.markdown("""
            <div class="info-card">
                <div class="card-title">Personal Information</div>
            """, unsafe_allow_html=True)
            
            for field, value in [
                ("Username", user_info['username']),
                ("Email", user_info['email']),
                ("Full Name", user_info['full_name']),
                ("Member Since", user_info['created_at'])
            ]:
                st.markdown(f"""
                <div class="info-item">
                    <div class="info-label">{field}</div>
                    <div class="info-value">{value or 'Not provided'}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            # Account Settings
            st.markdown("""
            <div class="info-card">
                <div class="card-title">Account Settings</div>
            """, unsafe_allow_html=True)

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.button("Change Password", type="primary", key="change_pwd")
            with btn_col2:
                st.button("Delete Account", type="secondary", key="delete_account")
            
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            # Statistiques du compte
            st.markdown("""
            <div class="info-card">
                <div class="card-title">Account Statistics</div>
            """, unsafe_allow_html=True)
            
            # Récupérer l'historique pour les statistiques
            history = get_user_history(st.session_state.user_id)
            total_predictions = len(history)
            positive_predictions = sum(1 for h in history if "positive" in h['prediction_result'].lower())
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_predictions}</div>
                    <div class="stat-label">Total Predictions</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{positive_predictions}</div>
                    <div class="stat-label">Positive Cases</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            # Activité récente
            st.markdown("""
            <div class="info-card">
                <div class="card-title">Recent Activity</div>
            """, unsafe_allow_html=True)
            
            if history:
                for activity in history[:5]:  # Afficher les 5 dernières activités
                    st.markdown(f"""
                    <div class="activity-card">
                        <div class="activity-date">{activity['prediction_date']}</div>
                        <div class="activity-result">{activity['prediction_result']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="color: #666; text-align: center; padding: 1rem;">
                    No prediction history available
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: {THEME_CONFIG['textColor']};">
            <p>Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True) 