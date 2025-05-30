import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
import numpy as np
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt
from folium.plugins import MarkerCluster
from haversine import haversine, Unit

# === VISÃO EMPRESA ===
def get_company_key_metrics(df):
    """Dicionário com métricas-chave para a visão da empresa."""
    metrics = {}
    metrics['Total Pedidos'] = df['ID'].nunique()
    metrics['Total Entregadores Únicos'] = df['Delivery_person_ID'].nunique()
    metrics['Tempo Médio de Entrega (min)'] = round(df['Time_taken(min)'].mean(), 2)

    festival_time = df[df['Festival'] == 'Yes']['Time_taken(min)'].mean()
    metrics["Tempo Médio (Festival)"] = round(festival_time, 2) if pd.notna(festival_time) else "N/A"

    non_festival_time = df[df['Festival'] == 'No']['Time_taken(min)'].mean()
    metrics["Tempo Médio (Não Festival)"] = round(non_festival_time, 2) if pd.notna(non_festival_time) else "N/A"

    return metrics

def plot_orders_by_date(df):
    """Volume de pedidos por data."""
    df_aux = df.groupby('Order_Date')['ID'].count().reset_index()
    fig = px.bar(df_aux, x='Order_Date', y='ID',
                 title='Volume de Pedidos por Data',
                 labels={'Order_Date': 'Data do Pedido', 'ID': 'Número de Pedidos'})
    return fig

def plot_traffic_order_share(df):
    """Distribuição de pedidos por densidade de tráfego."""
    df_aux = df.groupby('Road_traffic_density')['ID'].count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :].copy()
    df_aux['Percentual'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie(df_aux, values='Percentual', names='Road_traffic_density',
                 title='Distribuição de Pedidos por Densidade de Tráfego',
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    return fig

def plot_traffic_order_city(df):
    """Volume de pedidos por cidade e densidade de tráfego."""
    df_aux = df.groupby(['City', 'Road_traffic_density'])['ID'].count().reset_index()
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City',
                     title='Volume de Pedidos por Cidade e Densidade de Tráfego',
                     labels={'City': 'Cidade', 'Road_traffic_density': 'Densidade de Tráfego', 'ID': 'Número de Pedidos'})
    return fig

def get_country_map(df):
    """Localizações medianas de entrega agrupadas por cidade e densidade de tráfego."""
    df_aux = df.dropna(subset=['Delivery_location_latitude', 'Delivery_location_longitude']).copy()
    df_aux = df_aux.groupby(['City', 'Road_traffic_density'])[['Delivery_location_latitude', 'Delivery_location_longitude']].median().reset_index()

    # Define um centro inicial para o mapa
    if not df_aux.empty:
        center_lat = df_aux['Delivery_location_latitude'].mean()
        center_lon = df_aux['Delivery_location_longitude'].mean()
    else:
        center_lat, center_lon = 0, 0 # Default se não houver dados válidos

    map_obj = folium.Map(location=[center_lat, center_lon], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(map_obj) # Adiciona cluster de marcadores

    for _, row in df_aux.iterrows():
        # Verifica se as coordenadas são válidas
        if pd.notna(row['Delivery_location_latitude']) and pd.notna(row['Delivery_location_longitude']):
            folium.Marker(
                [row['Delivery_location_latitude'], row['Delivery_location_longitude']],
                popup=f"Cidade: {row['City']}<br>Tráfego: {row['Road_traffic_density']}",
                tooltip=f"{row['City']} ({row['Road_traffic_density']})"
            ).add_to(marker_cluster) # Adiciona ao cluster

    return map_obj

def plot_order_types_distribution(df):
    """Distribuição dos tipos de pedido."""
    df_aux = df['Type_of_order'].value_counts(normalize=True).reset_index()
    df_aux.columns = ['Tipo de Pedido', 'Percentual']
    fig = px.pie(df_aux, values='Percentual', names='Tipo de Pedido',
                 title='Distribuição dos Tipos de Pedido',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def plot_time_by_order_type_and_traffic(df):
    """Tempo médio de entrega por tipo de pedido e densidade de tráfego."""
    df_aux = df.groupby(['Type_of_order', 'Road_traffic_density'])['Time_taken(min)'].mean().reset_index()
    df_aux.columns = ['Tipo de Pedido', 'Densidade de Tráfego', 'Tempo Médio (min)']

    fig = px.bar(df_aux, x='Tipo de Pedido', y='Tempo Médio (min)',
                 color='Densidade de Tráfego', barmode='group',
                 title='Tempo Médio de Entrega por Tipo de Pedido e Tráfego',
                 labels={'Tipo de Pedido': 'Tipo de Pedido', 'Tempo Médio (min)': 'Tempo (min)'})
    return fig

# === VISÃO ENTREGADORES ===
def get_delivery_key_metrics(df):
    """Dicionário com métricas-chave para a visão de entregadores."""
    metrics = {}
    metrics['Idade Máxima'] = int(df['Delivery_person_Age'].max())
    metrics['Idade Mínima'] = int(df['Delivery_person_Age'].min())
    metrics['Melhor Condição Veículo'] = df['Vehicle_condition'].max() # Supondo que 0=pior, N=melhor
    metrics['Pior Condição Veículo'] = df['Vehicle_condition'].min() # Supondo que 0=pior, N=melhor
    metrics['Total Entregadores Únicos'] = df['Delivery_person_ID'].nunique()
    metrics['Média Avaliação Entregadores'] = round(df['Delivery_person_Ratings'].mean(), 2)
    return metrics

def get_delivery_rating_by_traffic(df):
    """Avaliação média e desvio padrão dos entregadores por densidade de tráfego."""
    df_aux = df.groupby('Road_traffic_density')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
    df_aux.columns = ['Densidade de Tráfego', 'Média Avaliação', 'STD Avaliação']
    return df_aux

def get_delivery_rating_by_weather(df):
    """Avaliação média e desvio padrão dos entregadores por condição climática."""
    df_aux = df.groupby('Weatherconditions')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
    df_aux.columns = ['Condição Climática', 'Média Avaliação', 'STD Avaliação']
    return df_aux

def get_top_n_deliverers(df, top_n=10, ascending=True):
    """Identifica os top N (ou piores N) entregadores com base no tempo médio de entrega por cidade."""
    # Agrupa por cidade e entregador, calcula o tempo médio
    df_aux = df.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].mean().reset_index()
    df_aux.columns = ['City', 'Delivery_person_ID', 'Avg_Time_taken(min)']

    # Ordena e seleciona o top N por cidade
    df_aux = df_aux.sort_values(['City', 'Avg_Time_taken(min)'], ascending=ascending)
    result = df_aux.groupby('City').head(top_n).reset_index(drop=True)
    return result

def plot_delivery_age_distribution(df):
    """Distribuição de idade dos entregadores."""
    fig = px.histogram(df.dropna(subset=['Delivery_person_Age']), x='Delivery_person_Age',
                       title='Distribuição de Idade dos Entregadores',
                       labels={'Delivery_person_Age': 'Idade do Entregador'},
                       nbins=20 # Número de barras no histograma
                      )
    fig.update_layout(xaxis_title='Idade', yaxis_title='Número de Entregadores')
    return fig

def plot_delivery_ratings_distribution(df):
    """Distribuição de avaliações dos entregadores."""
    fig = px.histogram(df.dropna(subset=['Delivery_person_Ratings']), x='Delivery_person_Ratings',
                       title='Distribuição de Avaliações dos Entregadores',
                       labels={'Delivery_person_Ratings': 'Avaliação'},
                       nbins=10, # Avaliações geralmente de 1 a 5, então umas 10 bins deve ser bom
                       color_discrete_sequence=px.colors.qualitative.Plotly
                      )
    fig.update_layout(xaxis_title='Avaliação', yaxis_title='Frequência')
    return fig

def plot_time_taken_by_vehicle_condition(df):
    """Tempo médio de entrega por condição do veículo."""
    df_aux = df.groupby('Vehicle_condition')['Time_taken(min)'].agg(['mean', 'std']).reset_index()
    df_aux.columns = ['Condição do Veículo', 'Tempo Médio (min)', 'STD Tempo (min)']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_aux['Condição do Veículo'], y=df_aux['Tempo Médio (min)'],
                         error_y=dict(type='data', array=df_aux['STD Tempo (min)']),
                         name='Tempo Médio'))
    fig.update_layout(
        title='Tempo Médio de Entrega por Condição do Veículo',
        xaxis_title='Condição do Veículo',
        yaxis_title='Tempo (min)',
        hovermode="x unified"
    )
    return fig

def plot_deliveries_by_age_group_and_city(df):
    """Número de entregadores por faixa etária e por cidade"""
    df_temp = df.dropna(subset=['Delivery_person_Age', 'City']).copy()
    # Criar faixas etárias (ex: 18-25, 26-35, etc.)
    bins = [18, 25, 35, 45, 55, 65]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65']
    df_temp['Age_Group'] = pd.cut(df_temp['Delivery_person_Age'], bins=bins, labels=labels, right=False)

    df_aux = df_temp.groupby(['City', 'Age_Group'])['Delivery_person_ID'].nunique().reset_index()
    df_aux.columns = ['City', 'Age_Group', 'Unique_Deliverers']

    fig = px.bar(df_aux, x='Age_Group', y='Unique_Deliverers', color='City',
                 title='Número de Entregadores Únicos por Faixa Etária e Cidade',
                 labels={'Age_Group': 'Faixa Etária', 'Unique_Deliverers': 'Número de Entregadores Únicos'})
    return fig

# === VISÃO RESTAURANTES ===
def get_restaurant_key_metrics(df):
    """Calcula e retorna um dicionário com métricas-chave para a visão de restaurantes."""
    metrics = {}

    # 1. Quantidade de entregadores únicos
    metrics["Entregadores Únicos"] = df['Delivery_person_ID'].nunique()

    # 2. Distância média entre restaurantes e locais de entrega
    df_valid_coords = df.dropna(subset=['Restaurant_latitude', 'Restaurant_longitude',
                                       'Delivery_location_latitude', 'Delivery_location_longitude']).copy()
    if not df_valid_coords.empty:
        df_valid_coords['distance'] = df_valid_coords.apply(lambda x:
            haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                      (x['Delivery_location_latitude'], x['Delivery_location_longitude']), unit=Unit.KILOMETERS), axis=1)
        metrics["Distância Média (km)"] = round(df_valid_coords['distance'].mean(), 2)
    else:
        metrics["Distância Média (km)"] = "N/A (Dados de localização insuficientes)"

    # 3. Tempo médio de entrega durante os Festivais
    festival_time = df[df['Festival'] == 'Yes']['Time_taken(min)'].mean()
    metrics["Tempo Médio (Festival)"] = round(festival_time, 2) if pd.notna(festival_time) else "N/A"

    # 4. Tempo Médio de Entrega Fora de Festivais
    non_festival_time = df[df['Festival'] == 'No']['Time_taken(min)'].mean()
    metrics["Tempo Médio (Não Festival)"] = round(non_festival_time, 2) if pd.notna(non_festival_time) else "N/A"

    return metrics

def plot_avg_std_time_by_city(df):
    """Tempo médio e desvio padrão do tempo de entrega por cidade."""
    df_aux = df.groupby('City')['Time_taken(min)'].agg(['mean', 'std']).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_aux['City'], y=df_aux['mean'],
                         error_y=dict(type='data', array=df_aux['std']),
                         name='Tempo Médio'))
    fig.update_layout(
        title='Tempo Médio e Desvio Padrão de Entrega por Cidade',
        xaxis_title='Cidade',
        yaxis_title='Tempo (min)',
        hovermode="x unified"
    )
    return fig

def get_avg_std_time_by_city_and_order_type(df):
    """Tempo médio e desvio padrão de entrega por cidade e por tipo de pedido."""
    df_aux = df.groupby(['City', 'Type_of_order'])['Time_taken(min)'].agg(['mean', 'std']).reset_index()
    df_aux.columns = ['City', 'Type_of_order', 'Avg_Time(min)', 'Std_Time(min)']
    return df_aux

def plot_avg_std_time_by_city_and_traffic(df):
    """Tempo médio de entrega por cidade e densidade de tráfego, com a cor indicando o desvio padrão."""
    df_aux = df.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'].agg(['mean', 'std']).reset_index()
    df_aux.columns = ['City', 'Road_traffic_density', 'Avg_Time(min)', 'Std_Time(min)']

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='Avg_Time(min)',
                      color='Std_Time(min)',
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_aux['Std_Time(min)']), # np.average precisa de numpy
                      title='Tempo Médio e Desvio Padrão de Entrega por Cidade e Tráfego')
    return fig

def plot_distance_by_vehicle_type(df):
    """Distância média de entrega por tipo de veículo e retorna um gráfico de barras."""
    df_valid_coords = df.dropna(subset=['Restaurant_latitude', 'Restaurant_longitude',
                                       'Delivery_location_latitude', 'Delivery_location_longitude']).copy()
    if df_valid_coords.empty:
        return go.Figure().add_annotation(text="Sem dados válidos para cálculo de distância.",
                                          xref="paper", yref="paper", showarrow=False)

    df_valid_coords['distance'] = df_valid_coords.apply(lambda x:
        haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                  (x['Delivery_location_latitude'], x['Delivery_location_longitude']), unit=Unit.KILOMETERS), axis=1)

    df_aux = df_valid_coords.groupby('Type_of_vehicle')['distance'].mean().reset_index()
    fig = px.bar(df_aux, x='Type_of_vehicle', y='distance',
                 title='Distância Média de Entrega por Tipo de Veículo',
                 labels={'Type_of_vehicle': 'Tipo de Veículo', 'distance': 'Distância Média (km)'})
    return fig

def get_avg_rating_by_weather_condition(df):
    """Avaliação média dos entregadores por condição climática."""
    df_aux = df.groupby('Weatherconditions')['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
    df_aux.columns = ['Condição Climática', 'Avaliação Média', 'STD Avaliação']
    return df_aux
