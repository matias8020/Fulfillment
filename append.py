import pandas as pd
import os

def merge_excel_files(fulfillment_folder, extras_folder, output_folder):
    # Asumiendo que hay un solo archivo en cada carpeta para simplificar
    fulfillment_file = [f for f in os.listdir(fulfillment_folder) if f.endswith('.xlsx')][0]
    extras_file = [f for f in os.listdir(extras_folder) if f.endswith('.xlsx')][0]

    # Leer los archivos
    df_fulfillment = pd.read_excel(os.path.join(fulfillment_folder, fulfillment_file), engine='openpyxl')
    df_extras = pd.read_excel(os.path.join(extras_folder, extras_file), engine='openpyxl')

    # Filtrar las columnas de df_extras para que coincidan con las de df_fulfillment
    common_columns = df_fulfillment.columns.intersection(df_extras.columns)
    df_extras_filtered = df_extras[common_columns]

    # Combinar los archivos
    df_combined = pd.concat([df_fulfillment, df_extras_filtered], ignore_index=True)

    # Ordenar por BUYBOX SCORE, LIKELY DEAL SCORE y SCORE en orden descendente
    df_combined.sort_values(by=['BUYBOX SCORE', 'LIKELY DEAL SCORE', 'SCORE'], ascending=[False, False, False], inplace=True)

    # Remover duplicados basados en (OWNER FULL NAME, ADDRESS, ZIP) y (MAILING ADDRESS, MAILING ZIP)
    df_combined.drop_duplicates(subset=['OWNER FULL NAME', 'ADDRESS', 'ZIP'], inplace=True)
    df_combined.drop_duplicates(subset=['MAILING ADDRESS', 'MAILING ZIP'], inplace=True)

    # Asegurar que la carpeta de salida existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Guardar el archivo combinado y limpio en la carpeta de salida
    output_file_path = os.path.join(output_folder, 'combined_properties.xlsx')
    df_combined.to_excel(output_file_path, index=False, engine='openpyxl')

    print(f"Archivo combinado creado en: {output_file_path}")

# Ejemplo de llamada a la función
merge_excel_files('fulfillment', 'extras', 'fulfillment')
