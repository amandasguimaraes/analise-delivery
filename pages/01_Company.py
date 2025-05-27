import streamlit as st
from src.data_processing import load_and_clean_data
from src.utils import setup_sidebar
from src.visualizations import (
    order_metric, traffic_order_share, traffic_order_city,
    order_by_week, order_share_by_week, country_maps
)

st.set_page_config(page_title='Visão da Empresa', page_icon='📈', layout='wide')

def main():
    st.header('Marketplace - Visão da Empresa')
    df_raw = load_and_clean_data('data/processed/curry_company_processed.csv')
    df_filtered = setup_sidebar(df_raw)

    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

    with tab1:
        st.plotly_chart(order_metric(df_filtered), use_container_width=True)
        col1, col2 = st.columns(2)
        col1.plotly_chart(traffic_order_share(df_filtered), use_container_width=True)
        col2.plotly_chart(traffic_order_city(df_filtered), use_container_width=True)

    with tab2:
        st.plotly_chart(order_by_week(df_filtered), use_container_width=True)
        st.plotly_chart(order_share_by_week(df_filtered), use_container_width=True)

    with tab3:
        country_maps(df_filtered)

if __name__ == "__main__":
    main()