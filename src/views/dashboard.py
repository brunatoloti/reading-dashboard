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
finished_books['LeituraNova'] = finished_books['LeituraNova'].apply(lambda x: 'Leitura nova' if x else 'Releitura')

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

filter_by = st.selectbox('Você quer ver por quantidade de livros ou por quantidade de páginas?',
                         ['Quantidade de livros', 'Quantidade de páginas'],
                         placeholder='Quantidade de livros')
if filter_by == 'Quantidade de livros':
    col_filter_by = 'Livro'
    title_filter_by = 'livros lidos'
else:
    col_filter_by = 'QuantidadePaginas'
    title_filter_by = 'páginas lidas'

finished_books = finished_books.query(f"Ano in {year_filter} & Editora in {publisher_filter} & Autor in {author_filter} & Pais in {country_filter}")

#graphs

col_indicator = st.columns((1.5, 1.5, 1, 1, 1.25, 1.5))
card1 = go.Figure()
card1.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.drop_duplicates(subset=['Livro', 'Autor']).shape[0],
    title = {"text": "Quantidade de livros"}))
card1.update_layout(
    height=250,
)
card2 = go.Figure()
card2.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.shape[0],
    title = {"text": "Quantidade de leituras"}))
card2.update_layout(
    height=250,
)
card3 = go.Figure()
card3.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.Nota.mean(),
    title = {"text": "Média de notas"}))
card3.update_layout(
    height=250,
)
card4 = go.Figure()
card4.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.QuantidadePaginas.sum(),
    title = {"text": "Páginas lidas"}))
card4.update_layout(
    height=250,
)
card5 = go.Figure()
card5.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.QuantidadePaginas.median(),
    title = {"text": "Mediana de páginas"}))
card5.update_layout(
    height=250,
)
card6 = go.Figure()
card6.add_trace(go.Indicator(
    mode = "number",
    value = finished_books.Autor.nunique(),
    title = {"text": "Quantidade de autores"}))
card6.update_layout(
    height=250,
)
with col_indicator[0]:
    st.plotly_chart(card1)
with col_indicator[1]:
    st.plotly_chart(card2)
with col_indicator[2]:
    st.plotly_chart(card3)
with col_indicator[3]:
    st.plotly_chart(card4)
with col_indicator[4]:
    st.plotly_chart(card5)
with col_indicator[5]:
    st.plotly_chart(card6)

# chart of number of books read per year
if filter_by == 'Quantidade de livros':
    count_finished_books_by_years = finished_books.groupby('Ano')[col_filter_by].count().reset_index()
else:
    count_finished_books_by_years = finished_books.groupby('Ano')[col_filter_by].sum().reset_index()
count_finished_books_by_years['Ano'] = count_finished_books_by_years['Ano'].apply(lambda x: str(int(x)))
chart1 = px.line(count_finished_books_by_years, x="Ano", y=col_filter_by, 
                 title=f'Quantidade de {title_filter_by} por ano', color_discrete_sequence=["#FF4B4B"], text=col_filter_by)
chart1.update_traces(
    hovertemplate =
                "<b>%{x}</b><br>" +
                "Quantidade: %{y}<br>" +
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
chart1.update_yaxes(title_text='')
chart1.update_xaxes(title_text='')
st.plotly_chart(chart1)

chart8 = px.histogram(
    finished_books,
    x='QuantidadePaginas',
    title='Distribuição do tamanho dos livros lidos',
    color_discrete_sequence=["#CF7C7C"]
)
chart8.update_xaxes(title_text='Quantidade de páginas')
chart8.update_yaxes(title_text='')
chart8.update_layout(
    title=dict(
        subtitle={
            'text': 'Este gráfico não sofre alterações com o filtro de ordenação por número de livros ou quantidade de páginas'
        }
    )
)
st.plotly_chart(chart8)

col1, col2 = st.columns([1, 1])

with col1:
    # chart of number of books read by country
    if filter_by == 'Quantidade de livros':
        finished_books_countries = finished_books.groupby('Pais')[col_filter_by].count().reset_index()
    else:
        finished_books_countries = finished_books.groupby('Pais')[col_filter_by].sum().reset_index()
    finished_books_countries = finished_books_countries.merge(get_all_countries(), left_on='Pais', right_on='value').drop(columns=['value'])
    finished_books_countries = finished_books_countries.rename(columns={'id': 'IdISO3166'})
    chart3 = px.scatter_geo(finished_books_countries, locations="IdISO3166",
                        hover_name="Pais", size=col_filter_by, color_discrete_sequence=["#FF4B4B"], custom_data=[col_filter_by, 'Pais'])
    chart3.update_traces(
        hovertemplate =
                    "<b>%{customdata[1]}</b><br>" +
                    "Quantidade: %{customdata[0]}<br>" +
                    "<extra></extra>",
    )
    chart3.update_layout(
        title_text = f'Quantidade de {title_filter_by} por país',
        geo=dict(
            projection_type='equirectangular')
    )
    chart3.update_geos(
        showcoastlines=True, coastlinecolor="black",
        showland=True, landcolor="beige",
        showcountries=True, countrycolor="black",
        showocean=True, oceancolor="LightBlue"
    )
    st.plotly_chart(chart3)

    # chart of top 5 publishers
    if filter_by == 'Quantidade de livros':
        count_finished_books_by_publisher_top5 = finished_books.groupby('Editora')[col_filter_by].count().reset_index()
    else:
        count_finished_books_by_publisher_top5 = finished_books.groupby('Editora')[col_filter_by].sum().reset_index()
    count_finished_books_by_publisher_top5 = count_finished_books_by_publisher_top5.sort_values(col_filter_by, ascending=False).head()
    chart5 = px.bar(count_finished_books_by_publisher_top5, x=col_filter_by, y="Editora", orientation='h',
                height=400,
                title='Top 5 editoras mais lidas', color_discrete_sequence=["#FF4B4B"],
                text=col_filter_by)
    chart5.update_traces(
        hovertemplate =
                    "<b>%{y}</b><br>" +
                    "Quantidade: %{x}<br>" +
                    "<extra></extra>",
        textfont_color='#d6d7dd'
    )
    chart5.update_layout(
        yaxis=dict(autorange="reversed")
    )
    chart5.update_yaxes(title_text='')
    chart5.update_xaxes(title_text='')
    st.plotly_chart(chart5)

    # Pie chart (oh no!!! But we only have two categories)
    count_finished_books_by_new_reading = finished_books['LeituraNova'].value_counts().reset_index()
    count_finished_books_by_new_reading.columns = ['LeituraNova', 'Qtd']
    chart10 = px.pie(count_finished_books_by_new_reading, names='LeituraNova', values='Qtd',
                     hole=0.5, title='Quantidade de leituras novas e releituras', color_discrete_sequence=["#FF4B4B", "#CF7C7C"])
    chart10.update_traces(textinfo='value',
                          hovertemplate =
                            "<b>%{label}</b><br>" +
                            "Quantidade de livros: %{value}<br>" +
                            "<extra></extra>",
                          textfont_color='#d6d7dd')
    chart10.update_layout(showlegend=True,
                          title=dict(
                            subtitle={
                                'text': 'Este gráfico não sofre alterações com o filtro de ordenação por número de livros ou quantidade de páginas'
                            }
                        ))
    st.plotly_chart(chart10)

with col2:
    # chart of number of books read by type and genre of author
    if filter_by == 'Quantidade de livros':
        count_finished_books_by_type_gender = finished_books.groupby(['Tipo', 'GeneroAutor'])[col_filter_by].count().reset_index()
    else:
        count_finished_books_by_type_gender = finished_books.groupby(['Tipo', 'GeneroAutor'])[col_filter_by].sum().reset_index()
    chart4 = px.bar(count_finished_books_by_type_gender, x=col_filter_by, y="Tipo", color='GeneroAutor', orientation='h',
                height=400,
                title=f'Quantidade de {title_filter_by} por tipo e gênero do autor', 
                color_discrete_sequence=["#FF4B4B", "#CF7C7C"],
                custom_data=['GeneroAutor'], text=col_filter_by)
    chart4.update_traces(
        hovertemplate =
                    "<b>%{y}</b><br>" +
                    "Quantidade: %{x}<br>" +
                    "Gênero do autor: %{customdata[0]}<br>" +
                    "<extra></extra>",
        textfont_color='#d6d7dd'
    )
    chart4.update_layout(
        yaxis=dict(autorange="reversed")
    )
    chart4.update_yaxes(title_text='')
    chart4.update_xaxes(title_text='')
    st.plotly_chart(chart4)

    # Number of books by read format
    if filter_by == 'Quantidade de livros':
        count_finished_books_by_read_format = finished_books.groupby('Formato')[col_filter_by].count().reset_index()
    else:
        count_finished_books_by_read_format = finished_books.groupby('Formato')[col_filter_by].sum().reset_index()
    count_finished_books_by_read_format = count_finished_books_by_read_format.sort_values(col_filter_by, ascending=False)
    chart9 = px.bar(count_finished_books_by_read_format, x="Formato", y=col_filter_by,
                height=400,
                title=f'Quantidade de {title_filter_by} lidos por formato', color_discrete_sequence=["#FF4B4B"],
                text=col_filter_by)
    chart9.update_traces(
        hovertemplate =
                    "<b>%{y}</b><br>" +
                    "Quantidade: %{x}<br>" +
                    "<extra></extra>",
        textfont_color='#d6d7dd'
    )
    chart9.update_yaxes(title_text='')
    chart9.update_xaxes(title_text='')
    st.plotly_chart(chart9)

    # chart of top 5 countries
    if filter_by == 'Quantidade de livros':
        count_finished_books_by_country_top5 = finished_books.groupby('Pais')[col_filter_by].count().reset_index()
    else:
        count_finished_books_by_country_top5 = finished_books.groupby('Pais')[col_filter_by].sum().reset_index()
    count_finished_books_by_country_top5 = count_finished_books_by_country_top5.sort_values(col_filter_by, ascending=False).head()
    chart11 = px.bar(count_finished_books_by_country_top5, x=col_filter_by, y="Pais", orientation='h',
                height=400,
                title=f'Top 5 países mais lidos', color_discrete_sequence=["#CF7C7C"],
                text=col_filter_by)
    chart11.update_traces(
        hovertemplate =
                    "<b>%{y}</b><br>" +
                    "Quantidade: %{x}<br>" +
                    "<extra></extra>",
        textfont_color='#d6d7dd'
    )
    chart11.update_layout(
        yaxis=dict(autorange="reversed")
    )
    chart11.update_yaxes(title_text='')
    chart11.update_xaxes(title_text='')
    st.plotly_chart(chart11)

st.write('A tabela abaixo não sofre alterações com o filtro de ordenação por número de livros ou quantidade de páginas')
count_finished_books_by_author_qtd_books = finished_books.drop_duplicates(subset=['Autor', 'Livro']).groupby('Autor')['Livro'].count().reset_index()
count_finished_books_by_author_qtd_rereading = finished_books.groupby(['Autor', 'LeituraNova']).size().unstack(fill_value=0)
count_finished_books_by_author_qtd_pages = finished_books.groupby('Autor')['QuantidadePaginas'].sum().reset_index()
count_finished_books_by_author_mean = finished_books.groupby('Autor')['Nota'].mean().reset_index()
count_finished_books_by_author_details = count_finished_books_by_author_qtd_books.merge(count_finished_books_by_author_qtd_pages, on='Autor')
count_finished_books_by_author_details = count_finished_books_by_author_details.merge(count_finished_books_by_author_mean, on='Autor')
count_finished_books_by_author_details = count_finished_books_by_author_details.merge(count_finished_books_by_author_qtd_rereading, on='Autor')
count_finished_books_by_author_details['QuantidadePaginas'] = count_finished_books_by_author_details['QuantidadePaginas'].apply(lambda x: str(int(x)))
count_finished_books_by_author_details['Nota'] = count_finished_books_by_author_details['Nota'].apply(lambda x: round(x, 1))
count_finished_books_by_author_details = count_finished_books_by_author_details.rename(columns={'Livro': 'Livros lidos', 'Nota': 'Média de notas', 'QuantidadePaginas': 'Total de páginas',
                                                                                                'Leitura nova': 'Leituras novas', 'Releitura': 'Releituras'})
st.dataframe(count_finished_books_by_author_details.sort_values(['Livros lidos', 'Autor'], ascending=[0,1]).reset_index(drop=True), hide_index=True, use_container_width=True)

with st.expander('Ver detalhes'):
    st.dataframe(finished_books, hide_index=True)

    finished_books_by_date = finished_books[['Livro', 'DataTermino', 'Ano']].sort_values('Ano')
    finished_books_by_date = finished_books_by_date.groupby(['Ano', 'DataTermino']).count().rename(columns={'Livro': 'QtLivros'}).reset_index(drop=False)
    finished_books_by_date['DataTermino'] = pd.to_datetime(finished_books_by_date['DataTermino'], format='%d/%m/%Y').dt.date
    finished_books_by_date = finished_books_by_date.set_index('DataTermino')['QtLivros']
    finished_books_by_date = finished_books_by_date.fillna(0)
    finished_books_by_date = finished_books_by_date.reindex(pd.date_range(finished_books_by_date.index.min(), finished_books_by_date.index.max()), fill_value=0)
    finished_books_by_date = finished_books_by_date.reset_index(drop=False).rename(columns={'index': 'DataTermino'})
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