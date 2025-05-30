import streamlit as st
import pandas as pd
from streamlit_folium import folium_static 
from src.utils import setup_sidebar
from src.data_processing import run_etl
from src.visualizations import (
    get_company_key_metrics, 
    plot_orders_by_date, 
    plot_traffic_order_share,
    plot_traffic_order_city,
    get_country_map, 
    plot_order_types_distribution,
    plot_time_by_order_type_and_traffic
)

st.set_page_config(page_title='Visão da Empresa', page_icon='📈', layout='wide')

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
metrics = get_company_key_metrics(df_filtered)

# Exibe as métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric('Total Pedidos', metrics['Total Pedidos'])
with col2:
    st.metric('Total Entregadores Únicos', metrics['Total Entregadores Únicos'])
with col3:
    st.metric('Tempo Médio Entrega (min)', metrics['Tempo Médio de Entrega (min)'])
with col4:
    st.metric('Tempo Médio (Festival)', metrics['Tempo Médio (Festival)'])
with col5:
    st.metric('Tempo Médio (Não Festival)', metrics['Tempo Médio (Não Festival)'])

st.markdown("---") 

# --- Seção de Análises Detalhadas ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Visão Geral de Pedidos",
    "Impacto do Tráfego",
    "Mapa Geográfico",
    "Análises de Tipo de Pedido"
])

with tab1:
    st.subheader("Volume de Pedidos por Data")
    fig_orders_by_date = plot_orders_by_date(df_filtered)
    st.plotly_chart(fig_orders_by_date, use_container_width=True)

with tab2:
    st.subheader("Distribuição de Pedidos por Densidade de Tráfego")
    fig_traffic_share = plot_traffic_order_share(df_filtered)
    st.plotly_chart(fig_traffic_share, use_container_width=True)

    st.subheader("Volume de Pedidos por Cidade e Densidade de Tráfego")
    fig_traffic_city = plot_traffic_order_city(df_filtered)
    st.plotly_chart(fig_traffic_city, use_container_width=True)

with tab3:
    st.subheader("Localização Mediana das Entregas por Cidade e Tráfego")
    st.info("Este mapa mostra a localização mediana das entregas, agrupadas por cidade e densidade de tráfego. Use o zoom e clique nos marcadores para mais detalhes.")
    map_obj = get_country_map(df_filtered)
    folium_static(map_obj, width=1024, height=600)

with tab4:
    st.subheader("Distribuição dos Tipos de Pedido")
    fig_order_types_dist = plot_order_types_distribution(df_filtered)
    st.plotly_chart(fig_order_types_dist, use_container_width=True)

    st.subheader("Tempo Médio de Entrega por Tipo de Pedido e Tráfego")
    fig_time_order_traffic = plot_time_by_order_type_and_traffic(df_filtered)
    st.plotly_chart(fig_time_order_traffic, use_container_width=True)