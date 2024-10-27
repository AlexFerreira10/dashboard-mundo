import streamlit as st
import plotly.express as px
import json

# Dashboard Mundo

# Configuração da página do Streamlit
st.set_page_config(page_title="Mundo", page_icon="🌍", layout="wide")

st.title("Dashboard Mundo")

st.subheader("Introdução")
st.markdown("""
        Este é um dashboard interativo que nos
         apresenta informações sobre os **continentes do mundo**, como população, PIB per capita, expectativa de vida, etc. 
         
        Com ele poderemos observar as principais características de cada continente e comparar os dados entre eles.
            
         Use o menu lateral para navegar entre as páginas e
         explorar as principais informações de cada continente!
            """)

# Cria uma linha de separação
st.divider()

# Carrega dados geográficos e os dados do Gapminder
linhas_territoriais = json.load(open("world-countries.json",'r'))
mundo = px.data.gapminder().rename(columns={
    "country": "país",
    "continent": "continente",
    "year": "ano",
    "lifeExp": "ExpVida",
    "pop": "pop",
    "gdpPercap": "PIBpercap",
    "iso_alpha": "sigla",
    "iso_num": "num_sigla",
})

# Função para criar um mapa-múndi com as populações
def mapa_mundi(lat, lon):
     fig1 = px.choropleth_mapbox(mundo,
                     geojson=linhas_territoriais,
                     locations="sigla",
                     color="pop",
                     color_continuous_scale="Sunsetdark",
                     mapbox_style="open-street-map",
                     zoom=1.1,
                     opacity=1,
                     width=1300,
                     height=700,
                     center={"lat": lat, "lon": lon})
     # Atualiza a configuração do mapa
     fig1.update_geos(fitbounds="locations", visible=False)
     fig1.update_layout(title="Mapa-múndi",
                        xaxis_title="Longitude",
                        yaxis_title="Latitude",
                        legend_title="População")

     return fig1

st.markdown("**Clique abaixo para visualizar o mapa-múndi**") 

# Botão para exibir o mapa
btn = st.button("Mapa-múndi")

# Se o botão for clicado, exibe o mapa e algumas métricas
if btn:
    st.plotly_chart(mapa_mundi(20, 0))  # Exibe o mapa com coordenadas centrais
    col1, col2, col3 = st.columns(3)  # Cria colunas para exibir métricas
    col1.metric(label="População Mundial", value=f"{mundo[mundo['ano'] == 2007]['pop'].sum():,.0f}")
    col2.metric(label="Países", value=f"{mundo['país'].nunique()}")
    col3.metric(label="Continentes", value=f"{mundo['continente'].nunique()}")

# Função para criar um gráfico de barras dos países mais populosos em 2007
def grafico_barras_populosos(continente, tema):
    continente = mundo[mundo["continente"] == continente]
    continente_2007_populosos = continente[continente["ano"] == 2007].sort_values("pop", ascending=False).head(5)

    fig1 = px.bar(
        continente_2007_populosos,
        x="país",
        y="pop",
        color="pop",
        color_continuous_scale=tema,
        text_auto=True
    )
    # Atualiza layout do gráfico
    fig1.update_layout(title="Os 5 países mais populosos em 2007",
                        xaxis_title="Países",
                        yaxis_title="População",
                        legend_title="População")

    return fig1

# Função para criar um gráfico de bolhas com Expectativa de Vida vs PIB per capita
def grafico_bolhas(continente):
    continente = mundo[mundo["continente"] == continente]
    fig2 = px.scatter(
        continente[continente["ano"] == 2007],
        x="ExpVida",
        y="PIBpercap",
        size="pop",
        color="país",
        color_discrete_sequence=px.colors.qualitative.Set1,
        log_y=True,
        size_max=60,
        range_x=[40, 85]
    )

    # Atualiza layout do gráfico
    fig2.update_layout(title="Expectativa de vida x PIB per capita",
                        xaxis_title="Expectativa de vida",
                        yaxis_title="PIB per capita",
                        legend_title="Países")

    return fig2

# Função para calcular métricas específicas de um continente
def calcular_metricas_continente(continente):
    continente_data = mundo[mundo['continente'] == continente]
    
    mais_populoso = continente_data.loc[continente_data['pop'].idxmax()]["país"]  # País mais populoso
    maior_expectativa_vida = continente_data.loc[continente_data['ExpVida'].idxmax()]["país"]  # Maior expectativa de vida
    maior_pib_per_capita = continente_data.loc[continente_data['PIBpercap'].idxmax()]["país"]  # Maior PIB per capita
    menos_populoso = continente_data.loc[continente_data['pop'].idxmin()]["país"]  # País menos populoso
    menor_expectativa_vida = continente_data.loc[continente_data['ExpVida'].idxmin()]["país"]  # Menor expectativa de vida
    menor_pib_per_capita = continente_data.loc[continente_data['PIBpercap'].idxmin()]["país"]  # Menor PIB per capita
    
    return mais_populoso, maior_expectativa_vida, maior_pib_per_capita, menos_populoso, menor_expectativa_vida, menor_pib_per_capita
