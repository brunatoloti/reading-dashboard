import streamlit as st

from src.db import get_all_finished_books


st.text('Dashboard')

finished_books = get_all_finished_books()
st.write(finished_books)