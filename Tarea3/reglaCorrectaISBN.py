import pandas as pd
import os
import sys

def is_valid_isbn(isbn):
    """
    Verifica si un ISBN tiene un formato válido.
    """
    if pd.isna(isbn):
        return False
    
    # Convertir a string y eliminar espacios y guiones
    isbn = str(isbn).strip().replace('-', '')
    
    # Verificar ISBN-10
    if len(isbn) == 10:
        if isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1].upper() == 'X'):
            return True
    # Verificar ISBN-13
    elif len(isbn) == 13:
        if isbn.isdigit() and (isbn.startswith('978') or isbn.startswith('979')):
            return True
    
    return False

def check_isbn_format(file_path):
    """
    Verifica el formato de los ISBNs en el archivo especificado.
    """
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path, encoding='utf-8')
        
        if 'isbn' not in df.columns:
            print(f"Error: No se encontró la columna 'isbn' en {os.path.basename(file_path)}")
            return
        
        total_rows = len(df)
        valid_isbns = sum(df['isbn'].apply(is_valid_isbn))
        
        print(f"\nArchivo: {os.path.basename(file_path)}")
        print(f"Total de filas leídas: {total_rows}")
        print(f"ISBNs válidos: {valid_isbns}")
        print(f"Porcentaje de ISBNs correctos: {(valid_isbns/total_rows)*100:.2f}%")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)

    # Verificar formato en ambos archivos integrados
    files_to_check = [
        ('../integrated_books.csv', 'Libros'),
        ('../integrated_ratings.csv', 'Ratings')
    ]
    
    for file_name, description in files_to_check:
        file_path = os.path.join(project_root, file_name)
        check_isbn_format(file_path)

    print(f"\n{'='*10} Verificación de formato de ISBN completada {'='*10}") 
