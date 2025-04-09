import pandas as pd
import os
import re

def is_valid_isbn(isbn):
    """
    Verifica si un ISBN tiene un formato válido.
    Retorna (bool, str) donde el bool indica si es válido y el str indica el formato detectado.
    """
    if pd.isna(isbn):
        return False, "NULO"
    
    # Convertir a string y eliminar espacios y guiones
    isbn = str(isbn).strip().replace('-', '')
    

    
    # Verificar ISBN-10
    if len(isbn) == 10:
        # El último dígito puede ser un número o X
        if re.match(r'^\d{9}[\dX]$', isbn):
            return True, "ISBN-10"
        # Verificar si es un código ASIN (comienza con B seguido de números)
        if re.match(r'\b^B[A-Z0-9]{9}\b', isbn):
            return False, "ASIN_CON_B"
        
        if re.match(r'\b[A-Z0-9]{10}\b', isbn):
            return False, "ASIN"
        return False, "ISBN-10_INVALIDO"
    # Verificar ISBN-13
    elif len(isbn) == 13:
        # ISBN-13 debe comenzar con 978 o 979
        if re.match(r'^(978|979)\d{10}$', isbn):
            return True, "ISBN-13"
        return False, "ISBN-13_INVALIDO"
    
    # Otros formatos
    return False, f"LONGITUD_{len(isbn)}"

def check_isbn_format(file_path):
    """
    Verifica el formato de los ISBNs en el archivo especificado.
    
    Args:
        file_path: Ruta al archivo CSV a verificar
    """
    print(f"\n--- Verificando formato de ISBN en {os.path.basename(file_path)} ---")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path, encoding='utf-8')
        
        if 'isbn' not in df.columns:
            print("Error: No se encontró la columna 'isbn' en el archivo.")
            return
        
        # Contar valores nulos
        null_count = df['isbn'].isnull().sum()
        if null_count > 0:
            print(f"Advertencia: Se encontraron {null_count} valores nulos en la columna ISBN.")
        
        # Verificar formato de cada ISBN
        format_counts = {}
        invalid_isbns = []
        isbn13_examples = []
        asin_examples = []
        
        for idx, isbn in df['isbn'].items():
            is_valid, format_type = is_valid_isbn(isbn)
            format_counts[format_type] = format_counts.get(format_type, 0) + 1
            
            if not is_valid and format_type != "ASIN":
                invalid_isbns.append((idx, isbn, format_type))
            
            # Guardar ejemplos de ISBN-13 para análisis
            if len(str(isbn).strip().replace('-', '')) == 13:
                isbn13_examples.append((idx, isbn))
            
            # Guardar ejemplos de ASIN
            if format_type == "ASIN":
                asin_examples.append((idx, isbn))
        
        # Mostrar estadísticas
        print("\nEstadísticas de formatos de ISBN:")
        total_isbns = len(df['isbn'])
        for format_type, count in format_counts.items():
            percentage = (count / total_isbns) * 100
            print(f"- {format_type}: {count} ({percentage:.2f}%)")
        
        # Mostrar ejemplos de ASINs
        if asin_examples:
            print("\nEjemplos de códigos ASIN encontrados:")
            for idx, asin in asin_examples[:20]:
                print(f"Fila {idx}: {asin}")
            if len(asin_examples) > 20:
                print(f"... y {len(asin_examples) - 20} ASINs más.")
        
        # Mostrar ejemplos de ISBNs inválidos (excluyendo ASINs)
        if invalid_isbns:
            print("\nPrimeros 10 ISBNs con formato inválido (excluyendo ASINs):")
            for idx, isbn, format_type in invalid_isbns[:10]:
                print(f"Fila {idx}: {isbn} (Formato: {format_type})")
            if len(invalid_isbns) > 10:
                print(f"... y {len(invalid_isbns) - 10} ISBNs inválidos más.")
        
        # Mostrar ejemplos de ISBN-13
        if isbn13_examples:
            print("\nEjemplos de ISBN-13 encontrados:")
            for idx, isbn in isbn13_examples[:10]:
                is_valid, format_type = is_valid_isbn(isbn)
                print(f"Fila {idx}: {isbn} (Válido: {is_valid}, Tipo: {format_type})")
            if len(isbn13_examples) > 10:
                print(f"... y {len(isbn13_examples) - 10} ISBN-13 más.")
        
        # Calcular porcentaje de ISBNs válidos
        valid_count = format_counts.get("ISBN-10", 0) + format_counts.get("ISBN-13", 0)
        valid_percentage = (valid_count / total_isbns) * 100
        print(f"\nPorcentaje de ISBNs con formato válido: {valid_percentage:.2f}%")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Verificar formato en ambos archivos integrados
    files_to_check = [
        ('integrated_books.csv', 'Libros'),
        ('integrated_ratings.csv', 'Ratings')
    ]
    
    for file_name, description in files_to_check:
        file_path = os.path.join(project_root, file_name)
        print(f"\n{'='*20} Verificando {description} {'='*20}")
        check_isbn_format(file_path)
    
    print(f"\n{'='*10} Verificación de formato de ISBN completada {'='*10}") 