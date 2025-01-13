import streamlit as st
from streamlit_gsheets import GSheetsConnection


def get_all_users():
    conn = st.connection('gsheets', type=GSheetsConnection)
    result = conn.query('SELECT * FROM users;')
    return result

def get_all_finished_books():
    conn = st.connection('gsheets', type=GSheetsConnection)
    result = conn.query('SELECT * FROM finished_books;')
    return result

def get_all_in_progress_books():
    conn = st.connection('gsheets', type=GSheetsConnection)
    existing_data = conn.read(worksheet='in_progress', usecols=list(range(11))).dropna()
    return existing_data

def insert_in_progress_books(updated_df):
    conn = st.connection('gsheets', type=GSheetsConnection)
    conn.update(worksheet='in_progress', data=updated_df)
