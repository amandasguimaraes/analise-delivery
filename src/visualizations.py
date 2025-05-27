import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

def order_metric(df):
    df_aux = df.groupby('Order_Date')['ID'].count().reset_index()
    fig = px.bar(df_aux, x='Order_Date', y='ID', title='Pedidos por Data')
    return fig

def traffic_order_share(df):
    df_aux = df.groupby('Road_traffic_density')['ID'].count().reset_index()
    df_aux['Percentual'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, names='Road_traffic_density', values='Percentual', title='Distribuição por Trânsito')
    return fig

def traffic_order_city(df):
    df_aux = df.groupby(['City', 'Road_traffic_density'])['ID'].count().reset_index()
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City',
                     title='Volume por Cidade e Trânsito')
    return fig

def order_by_week(df):
    df['week'] = df['Order_Date'].dt.isocalendar().week
    df_aux = df.groupby('week')['ID'].count().reset_index()
    fig = px.line(df_aux, x='week', y='ID', title='Pedidos por Semana')
    return fig

def order_share_by_week(df):
    df['week'] = df['Order_Date'].dt.isocalendar().week
    orders = df.groupby('week')['ID'].count().reset_index()
    deliverers = df.groupby('week')['Delivery_person_ID'].nunique().reset_index()
    df_aux = pd.merge(orders, deliverers, on='week')
    df_aux['Pedidos por Entregador'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week', y='Pedidos por Entregador', title='Pedidos por Entregador/Semana')
    return fig

def country_maps(df):
    df_aux = df.groupby(['City', 'Road_traffic_density'])[['Delivery_location_latitude','Delivery_location_longitude']].median().reset_index()
    map_obj = folium.Map(location=[df_aux['Delivery_location_latitude'].mean(), df_aux['Delivery_location_longitude'].mean()], zoom_start=10)
    for i in range(len(df_aux)):
        folium.Marker([
            df_aux.loc[i, 'Delivery_location_latitude'],
            df_aux.loc[i, 'Delivery_location_longitude']
        ], popup=f"{df_aux.loc[i, 'City']} - {df_aux.loc[i, 'Road_traffic_density']}").add_to(map_obj)
    folium_static(map_obj, width=1024, height=600)

def delivery_metrics(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Idade Máxima', df['Delivery_person_Age'].max())
    col2.metric('Idade Mínima', df['Delivery_person_Age'].min())
    col3.metric('Cond. Veículo - Melhor', df['Vehicle_condition'].max())
    col4.metric('Cond. Veículo - Pior', df['Vehicle_condition'].min())

def delivery_rating_by_traffic(df):
    st.subheader('Avaliação por Trânsito')
    df_aux = df.groupby('Road_traffic_density')['Delivery_person_Ratings'].agg(['mean','std']).reset_index()
    st.dataframe(df_aux)

def delivery_rating_by_weather(df):
    st.subheader('Avaliação por Clima')
    df_aux = df.groupby('Weatherconditions')['Delivery_person_Ratings'].agg(['mean','std']).reset_index()
    st.dataframe(df_aux)

def top_deliverers(df, ascending):
    df_aux = df.groupby(['City','Delivery_person_ID'])['Time_taken(min)'].mean().reset_index()
    df_aux = df_aux.sort_values(['City','Time_taken(min)'], ascending=ascending)
    return df_aux.groupby('City').head(10)

def restaurant_metrics(df):
    col1, col2, col3 = st.columns(3)
    col1.metric("Entregadores Únicos", df['Delivery_person_ID'].nunique())
    col2.metric("Distância Média (km)", df.apply(lambda x:
        haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                  (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1).mean().round(2))
    col3.metric("Tempo Médio (Festival)", round(df[df['Festival']=='Yes']['Time_taken(min)'].mean(), 2))

def avg_time_by_city(df):
    df_aux = df.groupby('City')['Time_taken(min)'].agg(['mean','std']).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_aux['City'], y=df_aux['mean'], error_y=dict(type='data', array=df_aux['std'])))
    st.plotly_chart(fig, use_container_width=True)

def avg_time_by_order(df):
    df_aux = df.groupby(['City','Type_of_order'])['Time_taken(min)'].agg(['mean','std']).reset_index()
    st.dataframe(df_aux)

def distance_chart(df):
    df['distance'] = df.apply(lambda x:
        haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                  (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
    df_aux = df.groupby('Type_of_vehicle')['distance'].mean().reset_index()
    fig = px.bar(df_aux, x='Type_of_vehicle', y='distance', title='Distância por Veículo')
    st.plotly_chart(fig, use_container_width=True)

def traffic_time_sunburst(df):
    df_aux = df.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'].agg(['mean','std']).reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='mean', color='std')
    st.plotly_chart(fig, use_container_width=True)
