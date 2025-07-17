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
    existing_data = conn.read(worksheet='in_progress', usecols=list(range(14))).dropna()
    return existing_data

def get_all_countries():
    conn = st.connection('gsheets', type=GSheetsConnection)
    country = conn.read(worksheet='country', usecols=list(range(2))).dropna()
    return country

def insert_in_progress_books(updated_df):
    conn = st.connection('gsheets', type=GSheetsConnection)
    conn.update(worksheet='in_progress', data=updated_df)
    st.cache_data.clear()
    st.rerun()

def insert_in_finished_books_and_remove_in_progress_books(updated_df, remove_df):
    conn = st.connection('gsheets', type=GSheetsConnection)
    conn.update(worksheet='finished_books', data=updated_df)
    conn.update(worksheet='in_progress', data=remove_df)
    st.cache_data.clear()
    st.rerun()