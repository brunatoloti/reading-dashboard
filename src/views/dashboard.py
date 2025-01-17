import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.db import get_all_finished_books, get_all_countries


st.title('Leituras finalizadas')

finished_books = get_all_finished_books()
finished_books['Nota'] = finished_books['Nota'].apply(lambda x: float(x.replace(',', '.')))

col1, col2, col3, col4, col5 = st.columns(5)
card1 = go.Figure()
card1.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.shape[0],
    title = {"text": "Quantidade de livros"}))
card1.update_layout(
    height=250,
)
card2 = go.Figure()
card2.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.Nota.mean(),
    title = {"text": "Média de notas"}))
card2.update_layout(
    height=250,
)
card3 = go.Figure()
card3.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.QuantidadePaginas.sum(),
    title = {"text": "Total de páginas lidas"}))
card3.update_layout(
    height=250,
)
card4 = go.Figure()
card4.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.QuantidadePaginas.median(),
    title = {"text": "Mediana de páginas"}))
card4.update_layout(
    height=250,
)
card5 = go.Figure()
card5.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.Autor.nunique(),
    title = {"text": "Quantidade de escritores"}))
card5.update_layout(
    height=250,
)
with col1:
    st.plotly_chart(card1)
with col2:
    st.plotly_chart(card2)
with col3:
    st.plotly_chart(card3)
with col4:
    st.plotly_chart(card4)
with col5:
    st.plotly_chart(card5)

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

col1, col2 = st.columns([1, 1])

with col1:
    # chart of number of books read by country
    finished_books_countries = finished_books.groupby('Pais')['Livro'].count().reset_index()
    finished_books_countries = finished_books_countries.merge(get_all_countries(), left_on='Pais', right_on='value').drop(columns=['value'])
    finished_books_countries = finished_books_countries.rename(columns={'id': 'IdISO3166'})
    chart3 = px.scatter_geo(finished_books_countries, locations="IdISO3166",
                        hover_name="Pais", size="Livro")
    chart3.update_layout(
        title_text = 'Quantidade de livros lidos por país',
        geo=dict(
            projection_type='equirectangular')
    )
    st.plotly_chart(chart3)

    # chart of top 5 publishers
    count_finished_books_by_publisher_top5 = finished_books.groupby('Editora')['Livro'].count().reset_index()
    count_finished_books_by_publisher_top5 = count_finished_books_by_publisher_top5.sort_values('Livro', ascending=False).head()
    chart5 = px.bar(count_finished_books_by_publisher_top5, x="Livro", y="Editora", orientation='h',
                height=400,
                title='Top 5 editoras mais lidas')
    chart5.update_layout(
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(chart5)

with col2:
    # chart of number of books read by type and genre of author
    count_finished_books_by_type_gender = finished_books.groupby(['Tipo', 'GeneroAutor'])['Livro'].count().reset_index()
    chart4 = px.bar(count_finished_books_by_type_gender, x="Livro", y="Tipo", color='GeneroAutor', orientation='h',
                height=400,
                title='Quantidade de livros lidos por tipo e gênero do autor')
    chart4.update_layout(
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(chart4)

    count_finished_books_by_author_qtd_books = finished_books.groupby('Autor')['Livro'].count().reset_index()
    count_finished_books_by_author_qtd_pages = finished_books.groupby('Autor')['QuantidadePaginas'].sum().reset_index()
    count_finished_books_by_author_mean = finished_books.groupby('Autor')['Nota'].mean().reset_index()
    count_finished_books_by_author_details = count_finished_books_by_author_qtd_books.merge(count_finished_books_by_author_qtd_pages, on='Autor')
    count_finished_books_by_author_details = count_finished_books_by_author_details.merge(count_finished_books_by_author_mean, on='Autor')
    count_finished_books_by_author_details = count_finished_books_by_author_details.rename(columns={'Livro': 'Quantidade de livros', 'Nota': 'Média de notas', 'QuantidadePaginas': 'Número de páginas'})
    st.dataframe(count_finished_books_by_author_details.sort_values(['Quantidade de livros', 'Autor'], ascending=[0,1]).reset_index(drop=True))

with st.expander('Ver detalhes'):
    st.write(finished_books)