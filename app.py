import streamlit as st
import streamlit_authenticator as stauth

from src.db import get_all_users


dashboard = st.Page(
    'src/views/dashboard.py', title='Dashboard', icon=':material/bar_chart_4_bars:', default=True
)
in_progress = st.Page(
    'src/views/in_progress.py', title='Em andamento', icon=':material/rule:'
)

st.set_page_config(layout="wide", page_title="Leituras da Bruna", page_icon="📚")

users = get_all_users().to_dict()

emails = [v for k, v in users['email'].items()]
first_names = [v for k, v in users['first_name'].items()]
last_names = [v for k, v in users['last_name'].items()]
hashed_passwords = [v for k, v in users['password'].items()]

credentials = {"usernames": {first_name+last_name: {"name": first_name, "password": password, "email": email} for first_name, last_name, password, email in zip(first_names, last_names, hashed_passwords, emails)}}

authenticator = stauth.Authenticate(credentials, "reading_dashboard_bru", "abcdef", cookie_expiry_days=30)

authenticator.login("main", "Login", fields={'Form name': 'Login', 'Username': 'Usuário', 'Password': 'Senha', 'Login': 'Entrar'})
authentication_status = st.session_state['authentication_status']
st.session_state["authenticator"] = authenticator

if authentication_status == False:
    st.error("Usuário/senha está incorreto")

if authentication_status == None:
    st.warning("Por favor, entre com seu usuário e senha")

if authentication_status:
    authenticator.logout("Sair", "sidebar")
    pg = st.navigation(
        pages=[dashboard, in_progress]
    )
    pg.run()
else:
    pg = st.navigation(
        pages=[dashboard],
        position='hidden'
    )