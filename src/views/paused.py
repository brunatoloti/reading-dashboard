from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.db import get_all_paused_books, insert_in_one_and_remove_from_another, get_all_in_progress_books, get_all_abandoned_books


gapb = get_all_paused_books()

col1, col2, col3 = st.columns([1, 1, 1])

st.title('Leituras pausadas')

if not gapb.empty:
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

            **Página atual:**  {int(row.PaginaAtual)}

            **Editora:**  {row.Editora}

            **País:**  {row.Pais}

            **Tipo:**  {row.Tipo}

            **Formato:**  {row.Formato}
            '''
            c1.markdown(m)
            c2.plotly_chart(fig, key=row.Livro)

            b1, b2 = st.columns(2)
            if b1.button('Retomar leitura', key=f'unpause_button_{row.Livro}', use_container_width=True):
                to_unpause = pd.concat([get_all_in_progress_books(), gapb.query(f"Livro == '{row.Livro}'")], ignore_index=True)
                to_keep = gapb.query(f"Livro != '{row.Livro}'")
                insert_in_one_and_remove_from_another(to_unpause, to_keep, 'in_progress', 'paused_books')
            if b2.button('Abandonar de vez a leitura', key=f'abandoned_button_{row.Livro}', use_container_width=True):
                to_abandone = pd.concat([get_all_abandoned_books(), gapb.query(f"Livro == '{row.Livro}'")], ignore_index=True)
                to_abandone['DataAbandono'] = datetime.today().strftime('%d/%m/%Y')
                to_keep = gapb.query(f"Livro != '{row.Livro}'")
                insert_in_one_and_remove_from_another(to_abandone, to_keep, 'abandoned_books', 'paused_books')

else:
    st.info('Você não possui leituras pausadas.')