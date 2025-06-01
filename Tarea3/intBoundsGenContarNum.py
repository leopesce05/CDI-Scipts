import pandas as pd
import os
import sys
from DB.db_operations import DBOperations

def contar_datos_en_rango(file_path, db, execution_id):
    """
    Cuenta los datos que están dentro de los rangos especificados.
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
        
        # Determinar las columnas y rangos según el archivo
        if 'users.csv' in file_path:
            column = 'Age'
            min_val = 18
            max_val = 123
        elif 'ratings.csv' in file_path:
            column = 'review/score'
            min_val = 5
            max_val = 10
        elif 'books.csv' in file_path:
            column = 'ratingsCount'
            min_val = 5
            max_val = 10
        else:
            print(f"Archivo no soportado: {os.path.basename(file_path)}")
            return
        
        # Verificar que la columna exista
        if column not in df.columns:
            print(f"Error: No se encontró la columna {column}")
            return
        
        try:
            # Contar valores en rango
            in_range = ((df[column] >= min_val) & (df[column] <= max_val)).sum()
            
            # Guardar resultado de columna - cantidad de valores en rango
            db.guardar_resultado_columna(
                execution_id=execution_id,
                nombre_tabla=os.path.basename(file_path).replace('.csv', ''),
                nombre_atributo=column,
                valor={
                    'id': 'integer',
                    'valor': int(in_range)
                }
            )
            
            print(f"\nArchivo: {os.path.basename(file_path)}")
            print(f"Columna: {column}")
            print(f"Valores en rango [{min_val}, {max_val}]: {in_range}")
            
        except Exception as e:
            print(f"Error al guardar resultados en la base de datos para la columna {column}: {e}")
            raise
        
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
            metodo="IntDominio-OutBounds-Gen-ContarNum_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Verificar rangos en los archivos
        files = ['users.csv', 'ratings.csv', 'books.csv']
        for file in files:
            file_path = os.path.join(integrated_csvs_dir, file)
            contar_datos_en_rango(file_path, db, execution_id)

        print(f"\n{'='*10} Verificación de rangos completada {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close()
