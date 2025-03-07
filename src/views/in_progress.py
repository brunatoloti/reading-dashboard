from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.db import get_all_in_progress_books, insert_in_progress_books, get_all_finished_books, insert_in_finished_books_and_remove_in_progress_books, get_all_countries


gapb = get_all_in_progress_books()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    with st.expander('Adicionar nova leitura'):
        author_gender_options = ['F', 'M', 'N']
        book_type_options = ['Livro', 'Quadrinho']
        countries_options = list(get_all_countries()['value'].unique())

        with st.form(key='reading_form'):
            book_name = st.text_input(label='Nome do livro')
            author_name = st.text_input(label='Nome do autor')
            pages_quantity = st.text_input(label='Quantidade de páginas')
            publisher = st.text_input(label='Editora')
            author_gender = st.selectbox('Gênero do autor', options=author_gender_options, index=None, placeholder='Escolha uma opção')
            book_type = st.selectbox('Tipo do livro', options=book_type_options, index=None, placeholder='Escolha uma opção')
            country = st.selectbox('País', options=countries_options, index=None, placeholder='Escolha uma opção')

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

with col2:
    with st.expander('Atualizar leitura existente'):
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
                            'Progresso': f"""{int((int(actual_page)/gapb.query(f"Livro == '{book_name}'")['QuantidadePaginas'].reset_index(drop=True)[0])*100)}%""",
                            'DataAtualizacao': datetime.today().strftime('%d/%m/%Y')
                        }
                    ]
                )
                update_actual_page = pd.concat([gapb.query(f"Livro != '{book_name}'"), update_actual_page], ignore_index=True)
                insert_in_progress_books(update_actual_page)
                st.success('Página atual atualizada')
with col3:
    with st.expander('Finalizar leitura existente'):
        with st.form(key='finish_reading_form'):
            book_name = st.selectbox('Qual livro você vai finalizar a leitura?', options=list(gapb['Livro'].unique()), index=None, placeholder='Escolha uma opção')
            rate_book = st.text_input(label='Qual nota você dá para essa leitura?')

            submit_button = st.form_submit_button(label='Salvar')
            if submit_button:
                finish_actual_book = pd.DataFrame(
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
                            'DataTermino': datetime.today().strftime('%d/%m/%Y'),
                            'Nota': rate_book
                        }
                    ]
                )
                update_books_finisheds = pd.concat([get_all_finished_books(), finish_actual_book], ignore_index=True).drop_duplicates()
                insert_in_finished_books_and_remove_in_progress_books(update_books_finisheds, gapb.query(f"Livro != '{book_name}'"))
                st.success('Novo livro finalizado')

st.title('Leituras em andamento')

for i, row in gapb.iterrows():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(row.Progresso*100/100, 2),
        number = {'valueformat':'f'},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Progresso"},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "#d6d7dd"},
            'bar': {'color': "#FF4B4B"},
            'borderwidth': 2,
            'bordercolor': "#d6d7dd",
        }
    ))
    fig.update_layout(
        font = {'color': "#d6d7dd"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=400,
        height=300
        )

    with st.container(border=True):
        c1, c2 = st.columns(2)
        m = f'''
        ## {row.Livro}
        **Autor:**  {row.Autor}

        **Quantidade de páginas:**  {int(row.QuantidadePaginas)}

        **Editora:**  {row.Editora}

        **País:**  {row.Pais}

        **Tipo:**  {row.Tipo}
        '''
        c1.markdown(m)
        c2.plotly_chart(fig, key=row.Livro)
