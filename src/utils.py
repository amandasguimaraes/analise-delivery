# Importando bibliotecas
import streamlit as st
from datetime import datetime
from PIL import Image

# Configurando barra lateral
def setup_sidebar(df1):
    image = Image.open('assets/logo.png')
    st.sidebar.image(image, width=120)
    
    st.sidebar.markdown('# Curry Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown("---")
    st.sidebar.markdown('## Selecione os filtros')

    # Filtro de data
    min_date = df1['Order_Date'].min().date()
    max_date = df1['Order_Date'].max().date()
    
    date_slider = st.sidebar.slider(
        'Período:',
        value=datetime(2022, 4, 13),
        min_value=datetime.combine(min_date, datetime.min.time()),
        max_value=datetime.combine(max_date, datetime.min.time()),
        format='DD/MM/YYYY'
    )

    # Filtro de tráfego
    traffic_options = st.sidebar.multiselect(
        'Condições do trânsito:',
        ['Low', 'Medium', 'High', 'Jam'],
        default=['Low', 'Medium', 'High', 'Jam']
    )
    
    # Filtro de clima
    weather_options = st.sidebar.multiselect(
        'Condições Climáticas:',
        df1['Weatherconditions'].unique().tolist(),
        default=df1['Weatherconditions'].unique().tolist()
    )

    # Filtro de veículo
    order_type = st.sidebar.multiselect(
         'Tipo de Veículo:',
        ['Scooter', 'Motocycle', 'Eletric_sooter'],
        default=['Urban', 'Semi-Urban', 'Metropolitan']
    )

    # Filtro de cidade
    cities = st.sidebar.multiselect(
        'Cidade:',
        ['Urban', 'Semi-Urban', 'Metropolitan'],
        default=['Urban', 'Semi-Urban', 'Metropolitan']
    )
    
    filtered_df = apply_filters(df1, date_slider, traffic_options, weather_options, order_type, cities)
    return date_slider, traffic_options, weather_options, order_type, cities

def apply_filters(df1, date_slider, traffic_options, weather_options, order_type, cities):
    df_filtered = df1[
        (df1['Order_Date'] < date_slider) &
        (df1['Road_traffic_density'].isin(traffic_options)) &
        (df1['Weatherconditions'].isin(weather_options)) &
        (df1['Type_of_order'].isin(order_type)) &
        (df1['City'].isin(cities))
    ].copy()
    return df_filtered