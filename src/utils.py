import streamlit as st
from datetime import datetime
from PIL import Image
import pandas as pd

def setup_sidebar(df_input):
    """Configura a barra lateral com filtros interativos para o dashboard."""
    df1 = df_input.copy()

    # --- Seção do Logo e Título ---
    st.sidebar.markdown(' ') 
    try:
        image = Image.open('assets/logo.png')
        st.sidebar.image(image, width=120)
    except FileNotFoundError:
        st.sidebar.warning("Logo 'assets/logo.png' não encontrada. Verifique o caminho.")

    st.sidebar.markdown('# Curry Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown("---") 

    st.sidebar.header('Opções de Filtragem')
    st.sidebar.write("Utilize os filtros abaixo para refinar os dados exibidos no dashboard.")

    # --- Filtro de Data ---
    st.sidebar.markdown("### Período")
    # Garante que a coluna Order_Date seja datetime para min/max
    if not pd.api.types.is_datetime64_any_dtype(df1['Order_Date']):
        df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], errors='coerce')
    
    valid_dates = df1['Order_Date'].dropna()
    if not valid_dates.empty:
        min_date_data = valid_dates.min().date() 
        max_date_data = valid_dates.max().date() 
    else:
        # Define um intervalo padrão 
        min_date_data = datetime(2022, 2, 11).date()
        max_date_data = datetime(2022, 4, 6).date()

    date_range = st.sidebar.date_input(
        "Selecione o período de tempo:",
        value=(min_date_data, max_date_data),
        min_value=min_date_data,
        max_value=max_date_data,
        help="Define o intervalo de datas dos pedidos a serem analisados."
    )
    st.sidebar.markdown("---")

    # --- Filtros Agrupados por Expander ---

    # Filtro de Cidade
    with st.sidebar.expander("Cidade", expanded=True): 
        st.write("Selecione os tipos de cidade:")
        cities_options = df1['City'].unique().tolist()
        cities_options = [c for c in cities_options if pd.notna(c) and c != 'NaN']
        
        cities = st.multiselect(
            'Tipos de Cidade:',
            options=cities_options,
            default=cities_options, # Seleciona todos por padrão
            key='filter_cities'
        )
        st.write("---") 

    # Filtro de Tráfego
    with st.sidebar.expander("Condição de Trânsito"):
        st.write("Selecione as condições de tráfego:")
        traffic_options = df1['Road_traffic_density'].unique().tolist()
        traffic_options = [t for t in traffic_options if pd.notna(t) and t != 'NaN'] # Remove 'NaN'
        
        traffic = st.multiselect(
            'Condições do Trânsito:',
            options=traffic_options,
            default=traffic_options, # Seleciona todos por padrão
            key='filter_traffic'
        )
        st.write("---")

    # Filtro de Clima
    with st.sidebar.expander("Condição Climática"):
        st.write("Selecione as condições climáticas:")
        weather_options = df1['Weatherconditions'].unique().tolist()
        weather_options = [w for w in weather_options if pd.notna(w) and w != 'NaN'] # Remove 'NaN'
        
        weather = st.multiselect(
            'Condições Climáticas:',
            options=weather_options,
            default=weather_options, # Seleciona todos por padrão
            key='filter_weather'
        )
        st.write("---")

    # Filtro de Veículo
    with st.sidebar.expander("Tipo de Veículo"):
        st.write("Selecione os tipos de veículo:.")
        vehicle_options = df1['Type_of_vehicle'].unique().tolist()
        vehicle_options = [v for v in vehicle_options if pd.notna(v) and v != 'NaN'] # Remove 'NaN'
        
        vehicle = st.multiselect(
            'Tipo de Veículo:',
            options=vehicle_options,
            default=vehicle_options, # Seleciona todos por padrão
            key='filter_vehicle'
        )
        st.write("---")

    # Retorna o DataFrame filtrado
    df_filtered = apply_filters(df1, date_range, traffic, weather, vehicle, cities)

    return df_filtered

# Aplicação dos filtros
def apply_filters(df1, date_range, traffic, weather, vehicle, cities):
    """Aplica os filtros selecionados pelo usuário ao DataFrame."""
    if not pd.api.types.is_datetime64_any_dtype(df1['Order_Date']):
        df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], errors='coerce')

    df_filtered = df1[
        (df1['Order_Date'].dt.date >= date_range[0]) & 
        (df1['Order_Date'].dt.date <= date_range[1]) & 
        (df1['Road_traffic_density'].isin(traffic)) &
        (df1['Weatherconditions'].isin(weather)) &
        (df1['Type_of_vehicle'].isin(vehicle)) &
        (df1['City'].isin(cities))
    ].copy()
    return df_filtered