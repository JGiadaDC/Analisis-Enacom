import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from vega_datasets import data
import geopandas as gpd

###############################################
# Configuaracion  de pagina
st.set_page_config(
    page_title = "TELECOMUNICACIONES/Internet",
    page_icon = '',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

# CSS styling
st.markdown("""
<style>
[data-testid="block-container"] {
padding-left: 2rem;
padding-right: 2rem;
padding-top: 1rem;
padding-bottom: 0rem;
margin-bottom: -7rem;
}
[data-testid="stVerticalBlock"] {
padding-left: 0rem;
padding-right: 0rem;
}
[data-testid="stMetric"] {
background-color: #393939;
text-align: center;
padding: 15px 0;
}
[data-testid="stMetricLabel"] {
display: flex;
justify-content: center;
align-items: center;
}
</style>
""", unsafe_allow_html=True)


##############################################
# importamos los datos 
ingresos = pd.read_csv('ingresos_usd.csv')
internet = pd.read_csv('internet.csv')

# file de las provincias
gdf = gpd.read_file("ProvinciasArgentina.geojson")


# Titulo
st.title("Analisis de la empresa Nacional de telecomunicaciones")
st.header("Como se puede implementar el sistema de internet a nivel nacional")
st.subheader("Datos oficiales de Enacom, Argentina")

pd.options.display.float_format = '{:.2f}'.format

# Filtrar los datos para el año 2023
vel_perc_2023 = internet[internet['Año'] == 2023]

# Calcular la media nacional de Mbps para el año 2023
media_nacional_mbps_2023 = vel_perc_2023['Mbps (Media de bajada)'].mean()

# Filtrar las provincias cuya media de bajada es menor que la media nacional en 2023
provincias_por_debajo_media_2023 = vel_perc_2023[vel_perc_2023['Mbps (Media de bajada)'] < media_nacional_mbps_2023]

# Establecer la meta para el próximo año como la media nacional de 2023
provincias_por_debajo_media_2023.loc[:, 'Meta para 2024'] = media_nacional_mbps_2023

# Mantener solo los valores únicos de las provincias
provincias_por_debajo_media_2023_unicas = provincias_por_debajo_media_2023.drop_duplicates(subset=['Provincia'])

# Ordinare i valori
vel_perc = internet.sort_values('Mbps (Media de bajada)', ascending=False).reset_index(drop=True)


###########################################
# Penetracion - calcular KPI
# Calcular el nuevo acceso proyectado
internet['Acceso proyectado/100 hogares'] = internet['Accesos por cada 100 hogares'] * 1.02

# Filtrar solo el último trimestre para la comparación
ultimo_trimestre = internet[internet['Trimestre'] == internet['Trimestre'].max()]

#############################################
# Ingresos
# Ordenar los datos por año
ingresos = ingresos.sort_values(by='Año')

################################################
## Media de bajada
# # Filtrar los datos para el cuarto trimestre
# df_q4 = internet[internet['Trimestre'] == 4]



# Sidebar
st.sidebar.markdown('### Bienvenido!')
st.sidebar.markdown('Con estos filtros, al seleccionar la provincia y el Año de interes, se veran los datos correspondientes')

with st.sidebar:
    st.title('Dashboard de Telecomunicaciones')
    # selecciona el ano de interes
    years_unique = internet['Año'].unique()
    selected_year = st.selectbox('Select a year', sorted(years_unique))
    # selecciona la provincia de interes
    provinces_unique = internet['Provincia'].unique()
    selected_province = st.selectbox('Seleziona una provincia', sorted(provinces_unique))
    # filtrar los datos en base al input del utente
    internet_filtered = internet[(internet['Año'] == selected_year)]
    ingresos_filtered = ingresos[(ingresos['Año'] == selected_year)]


# ingresos_selected_year = ingresos[ingresos['Año'] == int(selected_year)]

# Excluir la columna 'Total' para el gráfico de torta
value_vars = ['HASTA 512 kbps', '+ 512 Kbps - 1 Mbps', '+ 1 Mbps - 6 Mbps', 
              '+ 6 Mbps - 10 Mbps', '+ 10 Mbps - 20 Mbps', '+ 20 Mbps - 30 Mbps', '+ 30 Mbps']

# Transformar los datos para el gráfico de torta
df_melted = internet_filtered.melt(id_vars=['Provincia'], value_vars=['HASTA 512 kbps', '+ 512 Kbps - 1 Mbps', 
                                                        '+ 1 Mbps - 6 Mbps', '+ 6 Mbps - 10 Mbps', 
                                                        '+ 10 Mbps - 20 Mbps', '+ 20 Mbps - 30 Mbps', 
                                                        '+ 30 Mbps'])
# agrupar por ano y trimestre la media de bajada
#grouped_data = internet_filtered.groupby(['Año', 'Trimestre']).mean().reset_index()

################################################################################

# Filtrar los datos por años 2022 y 2023, excluyendo Buenos Aires
filtro = (internet['Año'].isin([2022, 2023])) & (internet['Provincia'] != 'Buenos Aires')
df_fibra = internet.loc[filtro]

# Raggruppare per anno e calcolare il totale dell'uso della fibra ottica
df_fibra_agrupado = df_fibra.groupby('Año')['Fibra óptica'].sum().reset_index()

# Calcolare l'aumento percentuale dal 2022 al 2023
fibra_2022 = df_fibra_agrupado.loc[df_fibra_agrupado['Año'] == 2022, 'Fibra óptica'].iloc[0]
fibra_2023 = df_fibra_agrupado.loc[df_fibra_agrupado['Año'] == 2023, 'Fibra óptica'].iloc[0]
aumento_percentuale = ((fibra_2023 - fibra_2022) / fibra_2022) * 100

#calculo del 3 KPI
incremento_proyectado = 13.52/100  # Convertimos el porcentaje a fracción

# Calcular el uso actual de fibra óptica
fibra_optica_2023 = internet[(internet['Año'] == 2023) & (internet['Provincia'] != 'Buenos Aires')]['Fibra óptica'].sum()

# Calcular el incremento proyectado
incremento_fibra_optica = fibra_optica_2023 * incremento_proyectado
uso_fibra_optica_proyectado = fibra_optica_2023 + incremento_fibra_optica


############################################################
# VISUALIZACIONES 
#1 
# Creare il grafico di torta con Plotly Express
def make_pie(selected_province):
    df_filtered = internet[internet['Provincia'] == selected_province]
    
    # Melt del DataFrame per avere una struttura adatta a px.pie
    df_melted = df_filtered.melt(id_vars=['Año', 'Trimestre', 'Provincia'], 
                                 value_vars=['ADSL', 'Cablemodem', 'Fibra óptica'],
                                 var_name='Tecnología', value_name='Accesos')

    fig = px.pie(df_melted, names='Tecnología', values='Accesos', 
                 title=f'Distribución de Accesos a Internet por Tecnología en {selected_province}')

    return fig

# 2: KPI2 Alcanzar la media de bajada nacional para el 2025
# Crear figura interactiva con Plotly
def make_bar(selected_year):
    fig = px.bar(provincias_por_debajo_media_2023_unicas,
             x='Provincia',
             y='Mbps (Media de bajada)',
             color='Mbps (Media de bajada)',  # Aplicar color según el valor de Mbps
             color_continuous_scale='viridis',  # Escala cromática
             title='Meta de Mbps para 2025 por Provincia',
             labels={'Mbps (Media de bajada)': 'Mbps (Media de bajada)'})

    # Añadir la línea de meta como una línea punteada
    fig.add_hline(y=media_nacional_mbps_2023, line_dash='dash', line_color='red',
              annotation_text=f'Meta para 2025: {media_nacional_mbps_2023:.2f} Mbps',
              annotation_position='bottom right')

    # Configurar el diseño del gráfico
    fig.update_layout(xaxis_title='Provincia', yaxis_title='Mbps (Media de bajada)',
                  xaxis_tickangle=-45, showlegend=False)
    return fig

# 3 KPI propuesto: incremento del 2% en el acceso a 100hogares
def make_bar2(penetracion):
    fig = px.bar(ultimo_trimestre,x='Provincia', y=['Accesos por cada 100 hogares', 'Acceso proyectado/100 hogares'],
                 barmode='group',
                 title='Acceso al servicio de internet: Actual vs Proyectado por Provincia',
                 labels={'value': 'Accesos por cada 100 hogares'})
    
    fig.update_traces(hovertemplate='Provincia: %{x}<br>' +
                            'Accesos por cada 100 hogares: %{y[0]:.2f}<br>' +
                            'Nuevo_Acceso_por_100_hogares: %{y[1]:.2f}')
    fig.update_layout(xaxis_title='Provincia', yaxis_title='Accesos por cada 100 hogares',
                  xaxis_tickangle=-45, showlegend=True)
    return fig


# 4 Ingresos anuales
def make_area(ingresos):
    fig = px.area(ingresos, x='Trimestre', y='Ingresos (USD)',
              title=f'Ingresos trimestrales en USD por el año {selected_year}',
              labels={'trimestre': 'Trimestre', 'Ingresos (USD)': 'Ingresos (USD)'})

    fig.update_layout(
    xaxis_title='Trimestre',
    yaxis_title='Ingresos (USD)',
    xaxis=dict(tickmode='linear'),
    template='plotly_white')
    
    return fig
# 5 Media de descarga en el tiempo
def make_line(selected_province):
    df_mean_bajada = internet.groupby('Año').agg({'Mbps (Media de bajada)': 'mean'}).reset_index()
    fig = px.line(df_mean_bajada, x='Año', y='Mbps (Media de bajada)',
              title='Media de Bajada por Años',
              labels={'Año': 'Año', 'Mbps (Media de bajada)': 'Media de Mbps (Bajada)'})
    fig.update_layout(
    xaxis_title='Año',
    yaxis_title='Media de Mbps (Bajada)',
    xaxis=dict(tickmode='linear'),
    template='plotly_white')
    return fig

# 6 Verificar el incremento percentual del uso de fibra en el ultimo ano
def make_line2(df_fibra_agrupado):
        fig = px.line(df_fibra_agrupado, x='Año', y='Fibra óptica',
              title='Uso de Fibra Óptica por Año (excluyendo Buenos Aires)',
              labels={'Fibra óptica': 'Número de conexiones', 'Año': 'Año'},
              template='plotly_white')
        fig.update_traces(textposition='top center', texttemplate='%{y:.2s}')
        return fig

# 7 KPI incremento uso fibra optica
# Datos para el gráfico
def make_pie2(selected_province):
    fig = px.pie(names=['Uso actual', 'Uso proyectado'], values=[fibra_optica_2023, uso_fibra_optica_proyectado], hole=0.3,
                 title=f'Uso de Fibra Óptica en {selected_province} - Proyección')
    return fig

#############################################################################
# Dashboard Main Panel
col = st.columns((1.5, 5, 5), gap='medium')

with col[0]:
  st.metric(label='Records', value=internet_filtered.shape[0], delta=None)
  st.markdown('#### Ingresos anuales')
  area = make_area(ingresos_filtered)
  st.plotly_chart(area)
with st.expander('', expanded=True):
   st.write()
with col[1]:
  st.markdown('#### Media de descarga a lo largo de los anos')
  line = make_line(selected_province)
  st.plotly_chart(line)
  st.markdown('#### Uso de fibra optica en el periodo 2022-2023')
  line2 = make_line2(df_fibra_agrupado)
  st.write(f"El incremento porcentual del uso de fibra óptica del 2022 al 2023 (excluyendo Buenos Aires) es: {aumento_percentuale:.2f}%")
  st.plotly_chart(line2)
  st.markdown('#### Incremento del 2% en el acceso por cada 100 hogares en el proximo trimestre')
  bar2 = make_bar2(internet)
  st.plotly_chart(bar2)
  
with col[2]:
   st.markdown('#### Distribucion de accesos de tecnologias por provincia')
   pie = make_pie(selected_province)
   st.plotly_chart(pie)

   st.markdown('#### Incremento proyectado en el uso de fibra optica para el proximo trimestre')
   pie2 = make_pie2(selected_province)
   st.plotly_chart(pie2)
   
  
   st.markdown('#### Media de bajada')
   bar = make_bar(selected_year)
   st.plotly_chart(bar)

   
   
   
   
   
   
   

# Mostra il DataFrame filtrato
st.write('Datos para el año seleccionado:', internet_filtered)
st.write('Datos de ingresos para el año seleccionado: ', ingresos_filtered)




'''def make_line(vel_perc):
    fig = px.line(vel_perc, x='Trimestre', y='Mbps (Media de bajada)', color = 'Año',
              title='Media de Bajada en los Años',
              labels={'Trimestre': 'Trimestre', 'Mbps (Media de bajada)': 'Media de Mbps (Bajada)', 'Año' : 'Año' })

    fig.update_layout(
    xaxis_title='Trimestre',
    yaxis_title='Media de Mbps (Bajada)',
    xaxis=dict(tickmode='linear'),
    template='plotly_white')
    
    return fig'''






