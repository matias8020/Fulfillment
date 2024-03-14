import pandas as pd
import os

def check_and_create_extras_folder(folder_path):
    """Verificar si la carpeta 'extras' existe, si no, crearla."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def load_and_unify_dupes(folder_path):
    """Cargar y unificar todos los archivos de duplicados en un único DataFrame."""
    df_list = []
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file)
            try:
                df_temp = pd.read_excel(file_path, engine='openpyxl')
                df_temp['unique_id'] = df_temp['OWNER FULL NAME'] + "_" + df_temp['ADDRESS'] + "_" + df_temp['ZIP'].astype(str)
                df_list.append(df_temp)
            except Exception as e:
                print(f"Error al procesar {file}: {e}")
    if df_list:
        # Concatenar todos los DataFrames en uno solo y eliminar duplicados basados en el identificador único
        df_unified_dupes = pd.concat(df_list, ignore_index=True).drop_duplicates(subset=['unique_id'])
        return df_unified_dupes
    else:
        return pd.DataFrame(columns=['OWNER FULL NAME', 'ADDRESS', 'ZIP', 'unique_id'])

def process_files_for_duplication_v5(clean_file_folder, dupes_folder, extras_folder):
    check_and_create_extras_folder(extras_folder)

    # Cargar y unificar los DataFrames de duplicados
    df_unified_dupes = load_and_unify_dupes(dupes_folder)
    
    # Procesar cada archivo en la carpeta 'clean file'
    for file in os.listdir(clean_file_folder):
        if file.endswith('.xlsx'):
            file_path = os.path.join(clean_file_folder, file)
            df_data = pd.read_excel(file_path, engine='openpyxl')
            df_data['unique_id'] = df_data['OWNER FULL NAME'] + "_" + df_data['ADDRESS'] + "_" + df_data['ZIP'].astype(str)

            # Filtrar las propiedades únicas
            if not df_unified_dupes.empty:
                unique_properties = df_data[~df_data['unique_id'].isin(df_unified_dupes['unique_id'])]
            else:
                unique_properties = df_data

            # Generar el nombre del archivo con el número de propiedades únicas
            num_unique_properties = unique_properties.shape[0]
            output_file_path = os.path.join(extras_folder, f"{num_unique_properties} extra properties_{file}")

            # Guardar el archivo con propiedades únicas, excluyendo la columna 'unique_id' antes de guardar
            unique_properties.drop('unique_id', axis=1).to_excel(output_file_path, index=False, engine='openpyxl')

            print(f"Archivo {file} procesado. {num_unique_properties} propiedades únicas guardadas en {output_file_path}.")

# Ajusta las rutas según tus necesidades y descomenta para ejecutar
process_files_for_duplication_v5("clean file", "dupes", "extras")
