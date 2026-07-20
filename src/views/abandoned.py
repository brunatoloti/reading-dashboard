import streamlit as st

from src.db import  get_all_abandoned_books


gaab = get_all_abandoned_books()

col1, col2, col3 = st.columns([1, 1, 1])

st.title('Leituras abandonadas')

if not gaab.empty:
    for i, row in gaab.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns(2)
            m = f'''
            ## {row.Livro}
            **Autor:**  {row.Autor}

            **Quantidade de páginas:**  {int(row.QuantidadePaginas)}

            **Última página lida:**  {int(row.PaginaAtual)}

            **Editora:**  {row.Editora}

            **País:**  {row.Pais}

            **Tipo:**  {row.Tipo}

            **Formato:**  {row.Formato}

            **Data do abandono da leitura:**  {row.DataAbandono}
            '''
            c1.markdown(m)
            
else:
    st.info('Você não possui leituras abandonadas.')