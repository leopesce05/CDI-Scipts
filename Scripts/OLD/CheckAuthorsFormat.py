import pandas as pd
import os
import re

def check_authors_format(books_file):
    """
    Verifica el formato de los autores en el archivo de libros.
    Cuenta cuántos autores tienen nombre y apellido completos.
    """
    print(f"\n--- Verificando formato de autores en {os.path.basename(books_file)} ---")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(books_file, encoding='utf-8')
        
        if 'authors' not in df.columns:
            print("Error: No se encontró la columna 'authors' en el archivo.")
            return
        
        # Contar valores nulos
        null_count = df['authors'].isnull().sum()
        if null_count > 0:
            print(f"Advertencia: Se encontraron {null_count} valores nulos en la columna authors.")
        
        # Función para verificar si un autor tiene nombre y apellido
        def has_full_name(author):
            if pd.isna(author):
                return False
            # Dividir por espacios y eliminar elementos vacíos
            parts = [p for p in author.split() if p]
            return len(parts) >= 2
        
        # Aplicar la verificación a cada autor
        full_name_count = df['authors'].apply(has_full_name).sum()
        total_authors = len(df['authors'])
        
        # Estadísticas
        print(f"\nEstadísticas:")
        print(f"- Total de registros con autores: {total_authors}")
        print(f"- Autores con nombre y apellido completos: {full_name_count}")
        print(f"- Porcentaje de autores con nombre y apellido completos: {(full_name_count/total_authors)*100:.2f}%")
        
        # Mostrar algunos ejemplos
        print("\nEjemplos de autores con nombre y apellido completos:")
        full_name_examples = df[df['authors'].apply(has_full_name)]['authors'].head(10)
        for author in full_name_examples:
            print(f"- {author}")
            
        print("\nEjemplos de autores sin nombre y apellido completos:")
        incomplete_examples = df[~df['authors'].apply(has_full_name)]['authors'].head(10)
        for author in incomplete_examples:
            print(f"- {author}")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Ruta al archivo de libros
    books_path = os.path.join(project_root, 'integrated_books.csv')
    
    check_authors_format(books_path)
    
    print(f"\n{'='*10} Verificación de formato de autores completada {'='*10}") 