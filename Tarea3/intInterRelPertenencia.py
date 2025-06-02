import pandas as pd
import os
import sys
from DB.db_operations import DBOperations

def check_referential_integrity(file_path, reference_file, db, execution_id):
    """
    Verifica la integridad referencial entre books y ratings.
    Calcula el porcentaje de ratings que tienen book_ids que no existen en books.
    """
    try:
        # Leer ambos archivos CSV
        df_books = pd.read_csv(file_path, encoding='latin-1', low_memory=False)
        df_ratings = pd.read_csv(reference_file, encoding='latin-1', low_memory=False)
        
        # Verificar que las columnas existan
        if 'Id' not in df_books.columns or 'Id' not in df_ratings.columns:
            print(f"Error: No se encontraron las columnas necesarias")
            return
        
        # Obtener los IDs válidos de books
        valid_book_ids = set(df_books['Id'].unique())
        
        # Contar referencias inválidas (book_ids que no existen en books)
        invalid_references = ~df_ratings['Id'].isin(valid_book_ids)
        total_references = len(df_ratings)
        invalid_count = invalid_references.sum()
        
        # Calcular porcentaje de referencias inválidas
        # Redondear a 2 cifras significativas
        invalid_percentage = round(invalid_count / total_references * 100, 2)
        
        # Guardar resultado de columna - porcentaje de referencias inválidas
        db.guardar_resultado_columna(
            execution_id=execution_id,
            nombre_tabla=os.path.basename(reference_file).replace('.csv', ''),
            nombre_atributo='Id',
            valor={
                'id': 'float',
                'valor': invalid_percentage
            }
        )
        
        print(f"\nArchivo principal: {os.path.basename(file_path)}")
        print(f"Archivo de referencia: {os.path.basename(reference_file)}")
        print(f"Total de ratings: {total_references}")
        print(f"Ratings con Ids inválidos: {invalid_count}")
        print(f"Porcentaje de referencias inválidas: {invalid_percentage:.2f}%")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar uno de los archivos")
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise

if __name__ == "__main__":
    try:
        # Conectar a la base de datos
        db = DBOperations()
        
        # 1. Crear una nueva ejecución
        execution_id = db.crear_ejecucion(
            metodo="IntInterRel-Pertenencia_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Verificar integridad referencial entre books y ratings
        books_path = os.path.join(integrated_csvs_dir, 'books.csv')
        ratings_path = os.path.join(integrated_csvs_dir, 'ratings.csv')
        check_referential_integrity(books_path, ratings_path, db, execution_id)

        print(f"\n{'='*10} Verificación de integridad referencial completada {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close() 