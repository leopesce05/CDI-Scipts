import pandas as pd
import os
import re

def check_book_titles(books_file):
    """
    Verifica la calidad de los títulos de los libros.
    Analiza diferentes aspectos para determinar si están correctamente escritos.
    """
    print(f"\n--- Verificando calidad de títulos en {os.path.basename(books_file)} ---")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(books_file, encoding='utf-8')
        
        if 'title' not in df.columns:
            print("Error: No se encontró la columna 'title' en el archivo.")
            return
        
        # Contar valores nulos
        null_count = df['title'].isnull().sum()
        if null_count > 0:
            print(f"Advertencia: Se encontraron {null_count} valores nulos en la columna title.")
        
        # Función para verificar si un título es válido
        def is_valid_title(title):
            if pd.isna(title):
                return False, "NULO"
            
            title = str(title).strip()
            
            # Verificar si el título está vacío
            if not title:
                return False, "VACÍO"
            
            # Verificar si el título es solo números
            if title.isdigit():
                return False, "SOLO_NÚMEROS"
            
            # Verificar si el título es demasiado corto (menos de 2 caracteres)
            if len(title) < 2:
                return False, "MUY_CORTO"
            
            # Verificar si el título es demasiado largo (más de 500 caracteres)
            if len(title) > 500:
                return False, "MUY_LARGO"
            
            # Verificar si el título contiene caracteres no imprimibles
            if not title.isprintable():
                return False, "CARACTERES_NO_IMPRIMIBLES"
            
            # Verificar si el título contiene solo caracteres especiales
            if not any(c.isalnum() for c in title):
                return False, "SOLO_ESPECIALES"
            
            return True, "VÁLIDO"
        
        # Aplicar la verificación a cada título
        title_analysis = df['title'].apply(is_valid_title)
        valid_titles = title_analysis.apply(lambda x: x[0]).sum()
        total_titles = len(df['title'])
        
        # Contar diferentes tipos de problemas
        problem_types = {}
        for _, problem_type in title_analysis:
            problem_types[problem_type] = problem_types.get(problem_type, 0) + 1
        
        # Estadísticas
        print(f"\nEstadísticas:")
        print(f"- Total de títulos: {total_titles}")
        print(f"- Títulos válidos: {valid_titles}")
        print(f"- Porcentaje de títulos válidos: {(valid_titles/total_titles)*100:.2f}%")
        
        print("\nDesglose de problemas:")
        for problem_type, count in problem_types.items():
            if problem_type != "VÁLIDO":
                percentage = (count/total_titles)*100
                print(f"- {problem_type}: {count} ({percentage:.2f}%)")
        
        # Mostrar ejemplos de títulos con problemas
        print("\nEjemplos de títulos con problemas:")
        for problem_type in problem_types:
            if problem_type != "VÁLIDO":
                examples = df[df['title'].apply(lambda x: is_valid_title(x)[1] == problem_type)]['title'].head(5)
                if not examples.empty:
                    print(f"\n{problem_type}:")
                    for title in examples:
                        print(f"- {title}")
        
        # Mostrar ejemplos de títulos válidos
        print("\nEjemplos de títulos válidos:")
        valid_examples = df[df['title'].apply(lambda x: is_valid_title(x)[0])]['title'].head(10)
        for title in valid_examples:
            print(f"- {title}")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Ruta al archivo de libros
    books_path = os.path.join(project_root, 'integrated_books.csv')
    
    check_book_titles(books_path)
    
    print(f"\n{'='*10} Verificación de títulos completada {'='*10}") 