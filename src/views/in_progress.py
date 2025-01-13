from datetime import datetime
import pandas as pd
import streamlit as st

from src.db import get_all_in_progress_books, insert_in_progress_books

st.title('Leituras em andamento')

author_gender_options = ['F', 'M', 'N']
book_type_options = ['Livro', 'Quadrinho']

with st.form(key='reading_form'):
    book_name = st.text_input(label='Nome do livro')
    author_name = st.text_input(label='Nome do autor')
    pages_quantity = st.text_input(label='Quantidade de páginas')
    publisher = st.text_input(label='Editora')
    author_gender = st.selectbox('Gênero do autor', options=author_gender_options, index=None)
    book_type = st.selectbox('Tipo do livro', options=book_type_options)
    country = st.text_input('País')

    submit_nutton = st.form_submit_button(label='Salvar')

    if submit_nutton:
        new_book_in_progress = pd.DataFrame(
            [
                {
                    'Ano': datetime.today().year,
                    'Livro': book_name,
                    'Autor': author_name,
                    'QuantidadePaginas': pages_quantity,
                    'Editora': publisher,
                    'GeneroAutor': author_gender,
                    'Tipo': book_type,
                    'Pais': country,
                    'PaginaAtual': 0,
                    'Progresso': 0,
                    'DataAtualizacao': datetime.today().strftime('%d/%m/%Y')
                }
            ]
        )
        
        update_books_in_progress = pd.concat([get_all_in_progress_books(), new_book_in_progress], ignore_index=True)

        insert_in_progress_books(update_books_in_progress)
        st.success('Novo livro em andamento')

