import streamlit as st
from src.data_processing import load_and_clean_data
from src.visualizations import (
    delivery_metrics, delivery_rating_by_traffic,
    delivery_rating_by_weather, top_deliverers
)
from src.utils import setup_sidebar

st.set_page_config(page_title='Delivery Dashboard', page_icon='🚚', layout='wide')

@st.cache_data

def load_data():
    return load_and_clean_data('data/processed/curry_company_processed.csv')

def main():
    st.header('Marketplace - Visão de Entregadores')
    df_raw = load_and_clean_data('data/processed/curry_company_processed.csv')
    df_filtered = setup_sidebar(df_raw)

    tab1, tab2 = st.tabs(['Indicadores Gerais', 'Top Entregadores'])

    with tab1:
        delivery_metrics(df_filtered)
        col1, col2 = st.columns(2)
        with col1:
            delivery_rating_by_traffic(df_filtered)
        with col2:
            delivery_rating_by_weather(df_filtered)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Rápidos")
            st.dataframe(top_deliverers(df_filtered, ascending=True))
        with col2:
            st.subheader("Top Lentos")
            st.dataframe(top_deliverers(df_filtered, ascending=False))

if __name__ == "__main__":
    main()