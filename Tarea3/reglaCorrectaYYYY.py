import pandas as pd
import os
import sys

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

def check_year_format(file_path):
    """
    Verifica el formato de las fechas de publicación en el archivo especificado.
    """
    try:
        # Leer el archivo CSV
        df = pd.read_csv(file_path, encoding='utf-8')
        
        if 'publication_date' not in df.columns:
            print(f"Error: No se encontró la columna 'publication_date' en {os.path.basename(file_path)}")
            return
        
        total_rows = len(df)
        valid_years = sum(df['publication_date'].apply(is_valid_year))
        
        print(f"\nArchivo: {os.path.basename(file_path)}")
        print(f"Total de filas leídas: {total_rows}")
        print(f"Fechas válidas (YYYY): {valid_years}")
        print(f"Porcentaje de fechas correctas: {(valid_years/total_rows)*100:.2f}%")
        
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
    ]
    
    for file_name, description in files_to_check:
        file_path = os.path.join(project_root, file_name)
        check_year_format(file_path)

    print(f"\n{'='*10} Verificación de formato de fechas completada {'='*10}") 
