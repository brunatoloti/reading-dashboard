import plotly.express as px
import streamlit as st

from src.db import get_all_finished_books


st.text('Dashboard')

finished_books = get_all_finished_books()
st.write(finished_books)

# chart of number of books read per year
count_finished_books_by_years = finished_books.groupby('Ano')['Livro'].count().reset_index()
count_finished_books_by_years['Ano'] = count_finished_books_by_years['Ano'].apply(lambda x: str(int(x)))
chart1 = px.line(count_finished_books_by_years, x="Ano", y="Livro", 
                 title='Quantidade de livros lidos por ano')
chart1.update_layout(
    xaxis=dict(
        type='category',
        categoryorder='array',
        categoryarray=sorted(count_finished_books_by_years['Ano'].unique())
    )
)
st.plotly_chart(chart1)