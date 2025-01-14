from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html

from src.db import get_all_in_progress_books, insert_in_progress_books


gapb = get_all_in_progress_books()

with st.expander('Adicionar nova leitura em andamento'):
    author_gender_options = ['F', 'M', 'N']
    book_type_options = ['Livro', 'Quadrinho']

    with st.form(key='reading_form'):
        book_name = st.text_input(label='Nome do livro')
        author_name = st.text_input(label='Nome do autor')
        pages_quantity = st.text_input(label='Quantidade de páginas')
        publisher = st.text_input(label='Editora')
        author_gender = st.selectbox('Gênero do autor', options=author_gender_options, index=None, placeholder='Escolha uma opção')
        book_type = st.selectbox('Tipo do livro', options=book_type_options, index=None, placeholder='Escolha uma opção')
        country = st.text_input('País')

        submit_button = st.form_submit_button(label='Salvar')

        if submit_button:
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
            
            update_books_in_progress = pd.concat([gapb, new_book_in_progress], ignore_index=True)

            insert_in_progress_books(update_books_in_progress)
            st.success('Novo livro em andamento')


st.title('Leituras em andamento')

card_style = """
    <style>
    .card {
        background-color: #1d1e2e;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
        font-family: 'Tahoma', sans-serif;
    }
    .card h3 {
        margin-top: 0;
        font-size: 36px;
        color: #d6d7dd;
    }
    .card p {
        font-size: 24px;
        color: #666;
    }
    .card .option {
        font-size: 24px;
        color: #d6d7dd;
        font-weight: bold;
        margin: 5px 0;
    }
    </style>
"""

for i, row in gapb.iterrows():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=row.PaginaAtual,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Progresso"},
        gauge={
            'axis': {'range': [0, row.QuantidadePaginas], 'tickwidth': 1, 'tickcolor': "#d6d7dd"},
            'bar': {'color': "#FF4B4B"},
            'borderwidth': 2,
            'bordercolor': "#d6d7dd",
        }
    ))
    fig.update_layout(
        paper_bgcolor= 'rgb(29, 30, 46)',
        font = {'color': "#d6d7dd"}
        )
    fig_html = fig.to_html(full_html=True, include_plotlyjs=True)

    card_content = f"""
    {card_style}
    <div class="card">
        <h3>{row.Livro}</h3>
        <p class="option">Autor: {row.Autor}</p>
        <p class="option">Editora: {row.Editora}</p>
        <p class="option">País: {row.Pais}</p>
        {fig_html}
    </div>
    """

    html(card_content, height=600)

with st.expander('Atualizar página atual'):
    with st.form(key='update_reading_form'):
        book_name = st.selectbox('Para qual livro?', options=list(gapb['Livro'].unique()), index=None, placeholder='Escolha uma opção')
        actual_page = st.text_input(label='Página atual')
        submit_button = st.form_submit_button(label='Salvar')
        
        if submit_button:
            update_actual_page = pd.DataFrame(
                [
                    {
                        'Ano': datetime.today().year,
                        'Livro': book_name,
                        'Autor': gapb.query(f"Livro == '{book_name}'")['Autor'].reset_index(drop=True)[0],
                        'QuantidadePaginas': gapb.query(f"Livro == '{book_name}'")['QuantidadePaginas'].reset_index(drop=True)[0],
                        'Editora': gapb.query(f"Livro == '{book_name}'")['Editora'].reset_index(drop=True)[0],
                        'GeneroAutor': gapb.query(f"Livro == '{book_name}'")['GeneroAutor'].reset_index(drop=True)[0],
                        'Tipo': gapb.query(f"Livro == '{book_name}'")['Tipo'].reset_index(drop=True)[0],
                        'Pais': gapb.query(f"Livro == '{book_name}'")['Pais'].reset_index(drop=True)[0],
                        'PaginaAtual': actual_page,
                        'Progresso': f"""{round(int(actual_page)/gapb.query(f"Livro == '{book_name}'")['QuantidadePaginas'].reset_index(drop=True)[0], 2)*100}%""",
                        'DataAtualizacao': datetime.today().strftime('%d/%m/%Y')
                    }
                ]
            )
            update_actual_page = pd.concat([gapb.query(f"Livro != '{book_name}'"), update_actual_page], ignore_index=True)
            insert_in_progress_books(update_actual_page)
            st.success('Página atual atualizada')