import pandas as pd
import os
import sys
from DB.db_operations import DBOperations

def is_valid_year(date):
    """
    Verifica si una fecha tiene el formato YYYY.
    """
    if pd.isna(date):
        return False
    
    # Convertir a string y eliminar espacios
    date = str(date).strip()
    
    # Verificar que sea un año válido (4 dígitos entre 1000 y 2024)
    if len(date) == 4 and date.isdigit():
        year = int(date)
        if 1000 <= year <= 2024:
            return True
    
    return False

def check_year_format(file_path, db, execution_id):
    """
    Verifica el formato de las fechas de publicación en el archivo especificado y guarda los resultados en la base de datos.
    """
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path, encoding='latin-1')
        
        if 'publishedDate' not in df.columns:
            print(f"Error: No se encontró la columna 'publishedDate' en {os.path.basename(file_path)}")
            return
        
        total_rows = len(df)
        valid_years = sum(df['publishedDate'].apply(is_valid_year))
        percentage_valid = round((valid_years/total_rows)*100, 2)
        
        # Guardar resultado de columna - porcentaje de fechas válidas
        db.guardar_resultado_columna(
            execution_id=execution_id,
            nombre_tabla=os.path.basename(file_path).replace('.csv', ''),
            nombre_atributo='publishedDate',
            valor={
                'id': 'float',
                'valor': percentage_valid
            }
        )
        
        print(f"\nArchivo: {os.path.basename(file_path)}")
        print(f"Total de filas leídas: {total_rows}")
        print(f"Fechas válidas (YYYY): {valid_years}")
        print(f"Porcentaje de fechas correctas: {percentage_valid:.2f}%")
        
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
            metodo="Precision-Fechas_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Verificar formato en el archivo de libros
        file_path = os.path.join(integrated_csvs_dir, 'books.csv')
        check_year_format(file_path, db, execution_id)

        print(f"\n{'='*10} Verificación de formato de fechas completada {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close() 