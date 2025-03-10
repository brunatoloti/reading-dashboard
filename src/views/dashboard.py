import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly_calplot import calplot
import streamlit as st

from src.db import get_all_finished_books, get_all_countries


st.title('Leituras finalizadas')

finished_books = get_all_finished_books()
finished_books['Nota'] = finished_books['Nota'].apply(lambda x: float(x.replace(',', '.')))
finished_books['Ano'] = finished_books['Ano'].apply(lambda x: str(int(x)))

# filters
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

year_filter_options = list(finished_books['Ano'].unique())
publisher_filter_options = list(finished_books.sort_values('Editora')['Editora'].unique())
author_filter_options = list(finished_books.sort_values('Autor')['Autor'].unique())
country_filter_options = list(finished_books.sort_values('Pais')['Pais'].unique())

with filter_col1:
    year_filter = st.selectbox('Ano', options=year_filter_options, index=None, placeholder='Todos')
with filter_col2:
    publisher_filter = st.selectbox('Editora', options=publisher_filter_options, index=None, placeholder='Todos')
with filter_col3:
    author_filter = st.selectbox('Autor', options=author_filter_options, index=None, placeholder='Todos')
with filter_col4:
    country_filter = st.selectbox('País', options=country_filter_options, index=None, placeholder='Todos')

if year_filter == None:
    year_filter = year_filter_options
else:
    year_filter = [year_filter]
if publisher_filter == None:
    publisher_filter = publisher_filter_options
else:
    publisher_filter = [publisher_filter]
if author_filter == None:
    author_filter = author_filter_options
else:
    author_filter = [author_filter]
if country_filter == None:
    country_filter = country_filter_options
else:
    country_filter = [country_filter]

finished_books = finished_books.query(f"Ano in {year_filter} & Editora in {publisher_filter} & Autor in {author_filter} & Pais in {country_filter}")

#graphs

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
                 title='Quantidade de livros lidos por ano', color_discrete_sequence=["#FF4B4B"], text='Livro')
chart1.update_traces(
    hovertemplate =
                "<b>%{x}</b><br>" +
                "Quantidade de livros: %{y}<br>" +
                "<extra></extra>",
    textfont_color='#d6d7dd',
    textposition='top center'
)
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
                        hover_name="Pais", size="Livro", color_discrete_sequence=["#FF4B4B"], custom_data=['Livro', 'Pais'])
    chart3.update_traces(
        hovertemplate =
                    "<b>%{customdata[1]}</b><br>" +
                    "Quantidade de livros: %{customdata[0]}<br>" +
                    "<extra></extra>",
    )
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
                title='Top 5 editoras mais lidas', color_discrete_sequence=["#FF4B4B"],
                text='Livro')
    chart5.update_traces(
        hovertemplate =
                    "<b>%{y}</b><br>" +
                    "Quantidade de livros: %{x}<br>" +
                    "<extra></extra>",
        textfont_color='#d6d7dd'
    )
    chart5.update_layout(
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(chart5)

with col2:
    # chart of number of books read by type and genre of author
    count_finished_books_by_type_gender = finished_books.groupby(['Tipo', 'GeneroAutor'])['Livro'].count().reset_index()
    chart4 = px.bar(count_finished_books_by_type_gender, x="Livro", y="Tipo", color='GeneroAutor', orientation='h',
                height=400,
                title='Quantidade de livros lidos por tipo e gênero do autor', 
                color_discrete_sequence=["#FF4B4B", "#CF7C7C"],
                custom_data=['GeneroAutor'], text='Livro')
    chart4.update_traces(
        hovertemplate =
                    "<b>%{y}</b><br>" +
                    "Quantidade de livros: %{x}<br>" +
                    "Gênero do autor: %{customdata[0]}<br>" +
                    "<extra></extra>",
        textfont_color='#d6d7dd'
    )
    chart4.update_layout(
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(chart4)

    count_finished_books_by_author_qtd_books = finished_books.groupby('Autor')['Livro'].count().reset_index()
    count_finished_books_by_author_qtd_pages = finished_books.groupby('Autor')['QuantidadePaginas'].sum().reset_index()
    count_finished_books_by_author_mean = finished_books.groupby('Autor')['Nota'].mean().reset_index()
    count_finished_books_by_author_details = count_finished_books_by_author_qtd_books.merge(count_finished_books_by_author_qtd_pages, on='Autor')
    count_finished_books_by_author_details = count_finished_books_by_author_details.merge(count_finished_books_by_author_mean, on='Autor')
    count_finished_books_by_author_details['QuantidadePaginas'] = count_finished_books_by_author_details['QuantidadePaginas'].apply(lambda x: str(int(x)))
    count_finished_books_by_author_details['Nota'] = count_finished_books_by_author_details['Nota'].apply(lambda x: round(x, 1))
    count_finished_books_by_author_details = count_finished_books_by_author_details.rename(columns={'Livro': 'Livros lidos', 'Nota': 'Média de notas', 'QuantidadePaginas': 'Total de páginas'})
    st.dataframe(count_finished_books_by_author_details.sort_values(['Livros lidos', 'Autor'], ascending=[0,1]).reset_index(drop=True), hide_index=True, use_container_width=True)

with st.expander('Ver detalhes'):
    st.dataframe(finished_books, hide_index=True)

    finished_books_by_date = finished_books[['Livro', 'DataTermino', 'Ano']].sort_values('Ano')
    finished_books_by_date = finished_books_by_date.groupby(['Ano', 'DataTermino']).count().rename(columns={'Livro': 'QtLivros'}).reset_index(drop=False)
    finished_books_by_date['DataTermino'] = pd.to_datetime(finished_books_by_date['DataTermino'], format='%d/%m/%Y').dt.date
    chart6 = calplot(finished_books_by_date, x='DataTermino', y='QtLivros', 
                     cmap_min=0, cmap_max=5, name='Quantidade', colorscale='reds')
    dd = {"title": {"text": "Histórico de finalização de leituras"}}
    j = 1
    for i in finished_books.sort_values('Ano')['Ano'].unique():
        dd.update({f"yaxis{j}" : {"title": str(i), "ticktext": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]}, 
                   f"xaxis{j}": {"ticktext": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
                                              "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]}})
        j = j + 1
    chart6.update_layout(dd)
    st.plotly_chart(chart6)