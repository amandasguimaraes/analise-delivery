# Importando bibliotecas
import pandas as pd
import os

# Limpeza do DataFrame
def clean_data(df1):
    df_clean = df1.copy()

    columns_to_clean = ['Delivery_person_Age', 'Road_traffic_density',
                        'City', 'Festival', 'multiple_deliveries']

    for col in columns_to_clean:
        df_clean = df_clean.loc[df_clean[col] != 'NaN '].copy()

    df_clean['Delivery_person_Age'] = df_clean['Delivery_person_Age'].astype(int)
    df_clean['Delivery_person_Ratings'] = df_clean['Delivery_person_Ratings'].astype(float)
    df_clean['Order_Date'] = pd.to_datetime(df_clean['Order_Date'], format='%Y-%m-%d')
    df_clean['multiple_deliveries'] = df_clean['multiple_deliveries'].astype(int)

    string_columns = ['ID', 'Road_traffic_density', 'Type_of_order',
                      'Type_of_vehicle', 'City', 'Festival']

    for col in string_columns:
        df_clean[col] = df_clean[col].str.strip()

    df_clean['Time_taken(min)'] = df_clean['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df_clean['Time_taken(min)'] = df_clean['Time_taken(min)'].astype(int)

    return df_clean

# Para uso via importação
def load_and_clean_data(filepath):
    df_raw = pd.read_csv(filepath)
    df_clean = clean_data(df_raw)
    return df_clean

# Para execução direta (modo script)
def extract_transform_load(input_file_path, output_file_path):
    df_raw = pd.read_csv(input_file_path)
    df_processed = clean_data(df_raw)
    df_processed.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    input_path = 'data/raw/curry_company_dataset.csv'
    output_path = 'data/processed/curry_company_processed.csv'
    extract_transform_load(input_path, output_path)
