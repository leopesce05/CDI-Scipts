import pandas as pd
import os
import sys
import re
from DB.db_operations import DBOperations

def is_valid_isbn(isbn):
    """
    Verifica si un ISBN tiene un formato válido usando expresiones regulares.
    """
    if pd.isna(isbn):
        return False
    
    # Convertir a string y eliminar espacios y guiones
    isbn = str(isbn).strip().replace('-', '')
    
    # Patrones para ISBN-10 e ISBN-13
    isbn10_pattern = r'^\d{9}[0-9Xx]$'  # 9 dígitos seguidos de un dígito o X
    isbn13_pattern = r'^(97[89])\d{10}$'  # 978 o 979 seguido de 10 dígitos
    
    # Verificar si coincide con alguno de los patrones
    return bool(re.match(isbn10_pattern, isbn.upper()) or re.match(isbn13_pattern, isbn))

def check_isbn_format(file_path, db, execution_id):
    """
    Verifica el formato de los ISBNs en el archivo especificado y guarda los resultados en la base de datos.
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
        
        if 'Id' not in df.columns:
            print(f"Error: No se encontró la columna 'Id' en {os.path.basename(file_path)}")
            return
        
        valid_isbns = sum(df['Id'].apply(is_valid_isbn))
        total_rows = len(df)
        percentage_valid = round((valid_isbns/total_rows)*100, 2)
        
        # Guardar resultados en la base de datos
        try:
            # Guardar resultado de columna - ISBNs válidos
            db.guardar_resultado_columna(
                execution_id=execution_id,
                nombre_tabla='books',
                nombre_atributo='Id',
                valor={
                    'id': 'float',
                    'valor': percentage_valid
                }
            )
            
            print(f"\nArchivo: {os.path.basename(file_path)}")
            print(f"Total de filas: {total_rows}")
            print(f"ISBNs válidos: {valid_isbns}")
            print(f"Porcentaje de ISBNs válidos: {percentage_valid:.2f}%")
            
        except Exception as e:
            print(f"Error al guardar resultados en la base de datos: {e}")
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
            metodo="ExactSint-ReglaCorrecta-ISBN_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Verificar formato en el archivo de libros
        file_path = os.path.join(integrated_csvs_dir, 'books.csv')
        check_isbn_format(file_path, db, execution_id)

        print(f"\n{'='*10} Verificación de formato de ISBN completada {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close() 
