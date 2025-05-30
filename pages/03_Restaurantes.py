import streamlit as st
import pandas as pd
from src.utils import setup_sidebar
from src.data_processing import run_etl
from src.visualizations import (
    get_restaurant_key_metrics,
    plot_avg_std_time_by_city,
    get_avg_std_time_by_city_and_order_type,
    plot_avg_std_time_by_city_and_traffic,
    plot_distance_by_vehicle_type,
    get_avg_rating_by_weather_condition
)

st.set_page_config(page_title='Visão de Restaurantes', page_icon='🍽️', layout='wide')

# --- Fluxo de Processamento de Dados ---
# Garante que o DataFrame seja carregado e processado apenas uma vez
if 'df_processed' not in st.session_state:
    df_clean = run_etl(
        input_path='data/raw/curry_company_dataset.csv',
        output_path='data/processed/curry_company_processed.csv'
    )
    if df_clean is None:
        #st.error("Erro ao carregar ou processar os dados. Por favor, verifique os arquivos e caminhos.")
        st.stop()
    st.session_state['df_processed'] = df_clean

df = st.session_state['df_processed']

# --- Configuração da Barra Lateral e Aplicação de Filtros ---
df_filtered = setup_sidebar(df)

# --- Layout do Dashboard Streamlit ---
metrics = get_restaurant_key_metrics(df_filtered)

# Exibe as métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Entregadores Únicos", metrics["Entregadores Únicos"])
with col2:
    st.metric("Distância Média (km)", metrics["Distância Média (km)"])
with col3:
    st.metric("Tempo Médio (Festival)", metrics["Tempo Médio (Festival)"])
with col4:
    st.metric("Tempo Médio (Não Festival)", metrics["Tempo Médio (Não Festival)"])

st.markdown("---") 

# --- Seção de Análises Detalhadas---
tab1, tab2, tab3, tab4 = st.tabs([
    "Tempo por Cidade e Tráfego",
    "Tempo por Cidade e Tipo de Pedido",
    "Distância por Veículo",
    "Impacto do Clima"
])

with tab1:
    st.subheader("Tempo Médio e STD por Cidade e Densidade de Tráfego")
    fig_traffic_sunburst = plot_avg_std_time_by_city_and_traffic(df_filtered)
    st.plotly_chart(fig_traffic_sunburst, use_container_width=True)

    st.subheader("Tempo Médio e STD de Entrega por Cidade (Geral)")
    fig_avg_time_city = plot_avg_std_time_by_city(df_filtered)
    st.plotly_chart(fig_avg_time_city, use_container_width=True)

with tab2:
    st.subheader("Tempo Médio e STD por Cidade e Tipo de Pedido")
    df_time_order_type = get_avg_std_time_by_city_and_order_type(df_filtered)
    st.dataframe(df_time_order_type, use_container_width=True)

with tab3:
    st.subheader("Distância Média de Entrega por Tipo de Veículo")
    fig_distance_vehicle = plot_distance_by_vehicle_type(df_filtered)
    st.plotly_chart(fig_distance_vehicle, use_container_width=True)

with tab4:
    st.subheader("Avaliação de Entregadores por Condição Climática")
    df_rating_weather = get_avg_rating_by_weather_condition(df_filtered)
    st.dataframe(df_rating_weather, use_container_width=True)
