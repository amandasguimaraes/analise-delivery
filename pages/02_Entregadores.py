import streamlit as st
import pandas as pd
from src.utils import setup_sidebar
from src.data_processing import run_etl
from src.visualizations import (
    get_delivery_key_metrics, 
    get_delivery_rating_by_traffic, 
    get_delivery_rating_by_weather, 
    get_top_n_deliverers, 
    plot_delivery_age_distribution, 
    plot_delivery_ratings_distribution, 
    plot_time_taken_by_vehicle_condition, 
    plot_deliveries_by_age_group_and_city 
)

st.set_page_config(page_title='Visão de Entregadores', page_icon='🚚', layout='wide')

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

# --- Configuração Barra Lateral e Aplicação Filtros ---
df_filtered = setup_sidebar(df)

# --- Layout do Dashboard Streamlit ---
metrics = get_delivery_key_metrics(df_filtered)

# Exibe as métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric('Idade Máxima', metrics['Idade Máxima'])
with col2:
    st.metric('Idade Mínima', metrics['Idade Mínima'])
with col3:
    st.metric('Melhor Condição Veículo', metrics['Melhor Condição Veículo'])
with col4:
    st.metric('Pior Condição Veículo', metrics['Pior Condição Veículo'])
with col5:
    st.metric('Média Avaliação', metrics['Média Avaliação Entregadores'])

st.markdown("---") 

# --- Seção de Análises Detalhadas ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Avaliações por Condição",
    "Top/Piores Entregadores",
    "Distribuições Demográficas e de Avaliação",
    "Impacto da Frota e Demografia"
])

with tab1:
    st.subheader("Avaliação Média por Densidade de Tráfego")
    df_rating_traffic = get_delivery_rating_by_traffic(df_filtered)
    st.dataframe(df_rating_traffic, use_container_width=True)

    st.subheader("Avaliação Média por Condição Climática")
    df_rating_weather = get_delivery_rating_by_weather(df_filtered)
    st.dataframe(df_rating_weather, use_container_width=True)

with tab2:
    st.subheader("Top 10 Entregadores Mais Rápidos por Cidade")
    df_top_10_fastest = get_top_n_deliverers(df_filtered, top_n=10, ascending=True)
    st.dataframe(df_top_10_fastest, use_container_width=True)

    st.subheader("Top 10 Entregadores Mais Lentos por Cidade")
    df_top_10_slowest = get_top_n_deliverers(df_filtered, top_n=10, ascending=False)
    st.dataframe(df_top_10_slowest, use_container_width=True)

with tab3:
    st.subheader("Distribuição da Idade dos Entregadores")
    fig_age_dist = plot_delivery_age_distribution(df_filtered)
    st.plotly_chart(fig_age_dist, use_container_width=True)

    st.subheader("Distribuição das Avaliações dos Entregadores")
    fig_ratings_dist = plot_delivery_ratings_distribution(df_filtered)
    st.plotly_chart(fig_ratings_dist, use_container_width=True)

with tab4:
    st.subheader("Tempo Médio de Entrega por Condição do Veículo")
    fig_time_vehicle = plot_time_taken_by_vehicle_condition(df_filtered)
    st.plotly_chart(fig_time_vehicle, use_container_width=True)

    st.subheader("Número de Entregadores Únicos por Faixa Etária e Cidade")
    fig_age_group_city = plot_deliveries_by_age_group_and_city(df_filtered)
    st.plotly_chart(fig_age_group_city, use_container_width=True)
