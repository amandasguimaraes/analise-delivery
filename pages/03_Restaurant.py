import streamlit as st
from src.data_processing import load_and_clean_data
from src.utils import setup_sidebar
from src.visualizations import (
    restaurant_metrics, avg_time_by_city, avg_time_by_order,
    distance_chart, traffic_time_sunburst
)

st.set_page_config(page_title='Visão de Restaurantes', page_icon='🍽️', layout='wide')

def main():
    st.header('Marketplace - Visão de Restaurantes')
    df_raw = load_and_clean_data('data/processed/curry_company_processed.csv')
    df_filtered = setup_sidebar(df_raw)

    restaurant_metrics(df_filtered)
    col1, col2 = st.columns(2)
    col1.subheader("Tempo Médio por Cidade")
    avg_time_by_city(df_filtered)
    col2.subheader("Tempo Médio por Tipo de Pedido")
    avg_time_by_order(df_filtered)

    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.subheader("Distância Média por Veículo")
    distance_chart(df_filtered)
    col2.subheader("Tempo por Cidade e Trânsito")
    traffic_time_sunburst(df_filtered)

if __name__ == "__main__":
    main()