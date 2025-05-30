import pandas as pd
import streamlit as st
from datetime import datetime
import numpy as np

# Extraction
def extract(filepath):
    """Extrai dados do arquivo CSV"""
    try:
        df = pd.read_csv(filepath)
        #st.info(f"✅ Dados extraídos com sucesso: {df.shape[0]} linhas, {df.shape[1]} colunas")
        return df
    except FileNotFoundError:
        #st.error(f"❌ Arquivo não encontrado: {filepath}")
        return None
    except Exception as e:
        #st.error(f"❌ Erro ao extrair dados: {e}")
        return None

# Transformation
def transform(df):
    """Transforma e limpa os dados"""
    df1 = df.copy()

    # Limpeza de colunas textuais
    text_columns = ['Delivery_person_Age', 'Road_traffic_density', 'City', 'Festival', 'multiple_deliveries']
    for col in text_columns:
        df1[col] = df1[col].astype(str).str.strip()
        df1 = df1[~df1[col].isin(['NaN', 'nan', '', 'null', 'NULL'])].copy()

    # Conversões de tipos
    df1['Delivery_person_Age'] = pd.to_numeric(df1['Delivery_person_Age'], errors='coerce')
    df1['Delivery_person_Ratings'] = pd.to_numeric(df1['Delivery_person_Ratings'], errors='coerce')
    df1['multiple_deliveries'] = pd.to_numeric(df1['multiple_deliveries'], errors='coerce')
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y', errors='coerce')
    df1['Time_Orderd'] = pd.to_datetime(df1['Time_Orderd'], format='%H:%M:%S', errors='coerce')
    df1['Time_Order_picked'] = pd.to_datetime(df1['Time_Order_picked'], format='%H:%M:%S', errors='coerce')

    df1['City'] = df1['City'].str.title().str.strip()
    df1['Weatherconditions'] = df1['Weatherconditions'].str.replace('conditions ', '', regex=False).str.strip()

    # Tempo de entrega
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.extract(r'(\d+)').astype(float)

    # Coordenadas
    coordinate_columns = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    for col in coordinate_columns:
        df1[col] = pd.to_numeric(df1[col], errors='coerce')
    
    # Validação de coordenadas
    lat_cols = ['Restaurant_latitude', 'Delivery_location_latitude']
    lon_cols = ['Restaurant_longitude', 'Delivery_location_longitude']
    
    for col in lat_cols:
        df1.loc[(df1[col] < -90) | (df1[col] > 90), col] = np.nan
    
    for col in lon_cols:    
        df1.loc[(df1[col] < -180) | (df1[col] > 180), col] = np.nan

    df1.dropna(subset=['Delivery_person_Age', 'Delivery_person_Ratings', 'Order_Date', 'Time_taken(min)'], inplace=True)
    
    return df1

# Loading
def load(df, output_path):
    """Salva o DataFrame processado"""
    try:
        df.to_csv(output_path, index=False)
        #print(f"Dataset limpo salvo em: {output_path}")
        return True
    except Exception as e:
        #print(f"Erro ao salvar arquivo: {e}")
        return False

# Pipeline ETL
@st.cache_data
def run_etl(input_path, output_path):
    """Executa o pipeline ETL completo"""
    # Extract
    df_raw = extract(input_path)

    # Transform
    df_clean = transform(df_raw)

    # Load
    load(df_clean, output_path)

    return df_clean 