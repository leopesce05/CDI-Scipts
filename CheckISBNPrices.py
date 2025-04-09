import pandas as pd
import os

def check_isbn_prices(ratings_file):
    """
    Verifica si hay ISBNs que tengan diferentes precios asociados.
    
    Args:
        ratings_file: Ruta al archivo CSV de ratings
    """
    print(f"\n--- Verificando consistencia de precios por ISBN ---")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(ratings_file, encoding='utf-8')
        
        if 'isbn' not in df.columns or 'Price' not in df.columns:
            print("Error: No se encontraron las columnas 'isbn' o 'Price' en el archivo.")
            return
        
        # Agrupar por ISBN y contar precios únicos
        price_counts = df.groupby('isbn')['Price'].nunique()
        
        # Encontrar ISBNs con múltiples precios
        inconsistent_isbns = price_counts[price_counts > 1]
        
        # Estadísticas
        total_isbns = len(price_counts)
        inconsistent_count = len(inconsistent_isbns)
        
        print(f"\nEstadísticas:")
        print(f"- Total de ISBNs únicos: {total_isbns}")
        print(f"- ISBNs con múltiples precios: {inconsistent_count}")
        print(f"- Porcentaje de ISBNs inconsistentes: {(inconsistent_count/total_isbns)*100:.2f}%")
        
        if not inconsistent_isbns.empty:
            print("\nPrimeros 10 ISBNs con múltiples precios:")
            for isbn, count in inconsistent_isbns.head(10).items():
                print(f"\nISBN: {isbn}")
                print(f"Número de precios diferentes: {count}")
                # Mostrar los diferentes precios para este ISBN
                prices = df[df['isbn'] == isbn]['Price'].unique()
                print("Precios asociados:")
                for price in prices:
                    print(f"- {price}")
            
            if len(inconsistent_isbns) > 10:
                print(f"\n... y {len(inconsistent_isbns) - 10} ISBNs más con múltiples precios.")
            
            # Mostrar algunos ejemplos de ratings con ISBNs inconsistentes
            print("\nEjemplos de ratings con ISBNs inconsistentes:")
            sample_isbns = list(inconsistent_isbns.head(3).index)
            inconsistent_ratings = df[df['isbn'].isin(sample_isbns)]
            print(inconsistent_ratings[['isbn', 'Price', 'title', 'source']].head(10))
            
            # Análisis adicional: distribución de precios por fuente
            print("\nDistribución de precios inconsistentes por fuente:")
            for isbn in sample_isbns:
                isbn_data = df[df['isbn'] == isbn]
                print(f"\nISBN: {isbn}")
                print("Distribución por fuente:")
                for source, group in isbn_data.groupby('source'):
                    unique_prices = group['Price'].unique()
                    print(f"- {source}: {len(unique_prices)} precios diferentes: {unique_prices}")
        else:
            print("\n¡Éxito! No se encontraron ISBNs con múltiples precios.")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Ruta al archivo de ratings
    ratings_path = os.path.join(project_root, 'integrated_ratings.csv')
    
    check_isbn_prices(ratings_path)
    
    print(f"\n{'='*10} Verificación de consistencia de precios completada {'='*10}") 