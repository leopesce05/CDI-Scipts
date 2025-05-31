import os
import sys
import pandas as pd
from DB.db_operations import DBOperations

def analyze_csv_file(file_path, db, execution_id):
    """
    Analiza un archivo CSV y cuenta los valores nulos en cada columna.
    """
    try:
        # Intentar diferentes codificaciones
        encodings = ['latin-1', 'utf-8', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise Exception("No se pudo leer el archivo con ninguna codificación")
        
        # Contar valores nulos por columna
        null_counts = df.isnull().sum()
        total_rows = len(df)
        
        # Procesar cada columna
        for column in df.columns:
            try:
                # Guardar resultado de columna - total de valores nulos
                db.guardar_resultado_columna(
                    execution_id=execution_id,
                    nombre_tabla=os.path.basename(file_path).replace('.csv', ''),
                    nombre_atributo=column,
                    valor={
                        'id': 'integer',
                        'valor': int(null_counts[column])
                    }
                )
                
                print(f"\nArchivo: {os.path.basename(file_path)}")
                print(f"Columna: {column}")
                print(f"Total de valores nulos: {null_counts[column]}")
                
            except Exception as e:
                print(f"Error al guardar resultados en la base de datos para la columna {column}: {e}")
                continue
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise

if __name__ == "__main__":
    try:
        # Conectar a la base de datos
        db = DBOperations()
        
        # 1. Crear una nueva ejecución
        execution_id = db.crear_ejecucion(
            metodo="Densidad-Grado-Contar_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Analizar cada archivo CSV
        files = ['books.csv', 'ratings.csv', 'users.csv']
        for file in files:
            file_path = os.path.join(integrated_csvs_dir, file)
            analyze_csv_file(file_path, db, execution_id)

        print(f"\n{'='*10} Análisis de valores nulos completado {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close() 