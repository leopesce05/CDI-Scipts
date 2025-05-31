import pandas as pd
import os
import sys
from DB.db_operations import DBOperations

def contar_duplicados(file_path, db, execution_id):
    """
    Cuenta los valores duplicados en las columnas especificadas del archivo.
    """
    try:
        # Intentar diferentes codificaciones
        encodings = ['latin-1', 'utf-8', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                # Leer el archivo con low_memory=False para evitar advertencias de tipos mixtos
                df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise Exception("No se pudo leer el archivo con ninguna codificación")
        
        # Imprimir las columnas disponibles para debug
        print(f"Columnas disponibles: {df.columns.tolist()}")
        
        # Determinar las columnas a verificar según el archivo
        if 'books.csv' in file_path:
            columns_to_check = ['Id', 'Title']
        elif 'users.csv' in file_path:
            columns_to_check = ['User_id']
        else:
            print(f"Archivo no soportado: {os.path.basename(file_path)}")
            return
        
        # Verificar que las columnas existan
        missing_columns = [col for col in columns_to_check if col not in df.columns]
        if missing_columns:
            print(f"Error: No se encontraron las columnas: {', '.join(missing_columns)}")
            return
        
        # Procesar cada columna
        for column in columns_to_check:
            try:
                # Contar duplicados para la columna actual
                duplicates = df[column].duplicated().sum()
                
                # Guardar resultado de columna - total de duplicados
                db.guardar_resultado_columna(
                    execution_id=execution_id,
                    nombre_tabla=os.path.basename(file_path).replace('.csv', ''),
                    nombre_atributo=column,
                    valor={
                        'id': 'integer',
                        'valor': int(duplicates)
                    }
                )
                
                print(f"\nArchivo: {os.path.basename(file_path)}")
                print(f"Columna: {column}")
                print(f"Total de duplicados: {duplicates}")
                
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
            metodo="NoDuplicación-CantDups-Contar_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Verificar duplicados en los archivos
        files = ['books.csv', 'users.csv']
        for file in files:
            file_path = os.path.join(integrated_csvs_dir, file)
            contar_duplicados(file_path, db, execution_id)

        print(f"\n{'='*10} Verificación de duplicados completada {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close()