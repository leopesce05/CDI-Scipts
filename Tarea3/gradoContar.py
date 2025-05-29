import os
import sys
import pandas as pd

def analyze_csv_file(file_path, source_dir, bad_rows_dir, project_root):
    print(f"\nAnalizando archivo: {os.path.basename(file_path)}")
    print("-" * 50)
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path)
        total_rows = len(df)
        print(f"Total de filas en el archivo: {total_rows}")
        
        # Analizar cada columna
        for column in df.columns:
            null_count = df[column].isnull().sum()
            null_percentage = (null_count / total_rows) * 100
            print(f"\nColumna: {column}")
            print(f"Cantidad de valores nulos: {null_count}")
            print(f"Porcentaje de valores nulos: {null_percentage:.2f}%")
            
    except Exception as e:
        print(f"Error al analizar el archivo: {e}")
        raise

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_script_dir))

    bad_rows_directory = os.path.join(project_root, 'bad_rows')
    try:
        os.makedirs(bad_rows_directory, exist_ok=True)
        print(f"Directorio para filas incorrectas: '{bad_rows_directory}'")
    except OSError as e:
        print(f"Error al crear el directorio '{bad_rows_directory}': {e}")
        sys.exit(1)

    files_to_analyze = [
        'integrated_books.csv',
        'integrated_ratings.csv',
        'integrated_users.csv'
    ]

    print(f"Iniciando análisis para {len(files_to_analyze)} archivo(s) especificado(s)...")

    for relative_path in files_to_analyze:
        full_path = os.path.join(project_root, relative_path)
        source_dir_name = os.path.basename(os.path.dirname(full_path))
        if not source_dir_name:
            source_dir_name = "[RAÍZ]"

        try:
            analyze_csv_file(full_path, source_dir_name, bad_rows_directory, project_root)
        except Exception as e:
            print(f"\nERROR INESPERADO al procesar la ruta {relative_path}: {e}")
            print("Continuando con el siguiente archivo...")

    print(f"\n{'='*10} ANÁLISIS COMPLETADO PARA ARCHIVOS ESPECIFICADOS {'='*10}") 