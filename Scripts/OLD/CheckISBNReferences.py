import pandas as pd
import os

def check_isbn_references(ratings_file, books_file):
    """
    Verifica que todos los ISBNs en el archivo de ratings existan en el archivo de libros.
    
    Args:
        ratings_file: Ruta al archivo CSV de ratings
        books_file: Ruta al archivo CSV de libros
    """
    print(f"\n--- Verificando referencias de ISBN entre ratings y libros ---")
    
    try:
        # Leer los archivos CSV
        ratings_df = pd.read_csv(ratings_file, encoding='utf-8')
        books_df = pd.read_csv(books_file, encoding='utf-8')
        
        if 'isbn' not in ratings_df.columns:
            print("Error: No se encontró la columna 'isbn' en el archivo de ratings.")
            return
            
        if 'isbn' not in books_df.columns:
            print("Error: No se encontró la columna 'isbn' en el archivo de libros.")
            return
        
        # Obtener conjuntos de ISBNs
        ratings_isbns = set(ratings_df['isbn'].dropna().unique())
        books_isbns = set(books_df['isbn'].dropna().unique())
        
        # Encontrar ISBNs en ratings que no están en libros
        missing_isbns = ratings_isbns - books_isbns
        
        # Estadísticas
        total_ratings_isbns = len(ratings_isbns)
        total_books_isbns = len(books_isbns)
        total_missing = len(missing_isbns)
        
        print(f"\nEstadísticas:")
        print(f"- Total de ISBNs únicos en ratings: {total_ratings_isbns}")
        print(f"- Total de ISBNs únicos en libros: {total_books_isbns}")
        print(f"- Total de ISBNs en ratings que no están en libros: {total_missing}")
        
        if missing_isbns:
            print("\nPrimeros 10 ISBNs en ratings que no están en libros:")
            for isbn in list(missing_isbns)[:10]:
                print(f"- {isbn}")
            if len(missing_isbns) > 10:
                print(f"... y {len(missing_isbns) - 10} más.")
            
            # Mostrar algunos ejemplos de ratings con ISBNs faltantes
            print("\nEjemplos de ratings con ISBNs faltantes:")
            missing_ratings = ratings_df[ratings_df['isbn'].isin(missing_isbns)]
            print(missing_ratings[['isbn', 'user_id', 'rating']].head(10))
            
            # Calcular porcentaje de ratings afectados
            total_ratings = len(ratings_df)
            affected_ratings = len(missing_ratings)
            percentage = (affected_ratings / total_ratings) * 100
            print(f"\nTotal de ratings afectados: {affected_ratings} ({percentage:.2f}% del total)")
        else:
            print("\n¡Éxito! Todos los ISBNs en ratings existen en la tabla de libros.")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Rutas a los archivos
    ratings_path = os.path.join(project_root, 'integrated_ratings.csv')
    books_path = os.path.join(project_root, 'integrated_books.csv')
    
    check_isbn_references(ratings_path, books_path)
    
    print(f"\n{'='*10} Verificación de referencias de ISBN completada {'='*10}") 