import pandas as pd
import os

def check_isbn_uniqueness(file_path):
    """
    Verifica si los valores de la columna ISBN son únicos en el archivo especificado.
    
    Args:
        file_path: Ruta al archivo CSV a verificar
    """
    print(f"\n--- Verificando unicidad de ISBN en {os.path.basename(file_path)} ---")
    
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
        
        # Obtener valores no nulos
        non_null_isbns = df['isbn'].dropna()
        
        # Verificar duplicados
        duplicates = non_null_isbns[non_null_isbns.duplicated(keep=False)]
        
        if duplicates.empty:
            print("¡Éxito! Todos los valores de ISBN son únicos (ignorando valores nulos).")
        else:
            print(f"¡Advertencia! Se encontraron {len(duplicates)} valores duplicados de ISBN.")
            print("\nPrimeros 10 ISBNs duplicados:")
            
            # Obtener las filas duplicadas
            duplicate_rows = df[df['isbn'].isin(duplicates.unique())]
            
            # Agrupar por ISBN y mostrar la distribución de fuentes
            for isbn in duplicates.unique()[:10]:
                isbn_rows = duplicate_rows[duplicate_rows['isbn'] == isbn]
                sources = isbn_rows['source'].value_counts()
                print(f"\nISBN: {isbn}")
                print(f"Título: {isbn_rows['title'].iloc[0]}")
                print("Distribución por fuente:")
                for source, count in sources.items():
                    print(f"- {source}: {count} ocurrencias")
            
            if len(duplicates.unique()) > 10:
                print(f"\n... y {len(duplicates.unique()) - 10} ISBNs duplicados más.")
            
            # Mostrar estadísticas generales
            print("\nEstadísticas generales de duplicados:")
            total_duplicates = len(duplicates)
            unique_duplicate_isbns = len(duplicates.unique())
            print(f"Total de filas duplicadas: {total_duplicates}")
            print(f"Total de ISBNs únicos que están duplicados: {unique_duplicate_isbns}")
            
            # Distribución de fuentes en duplicados
            print("\nDistribución de fuentes en duplicados:")
            source_distribution = duplicate_rows['source'].value_counts()
            for source, count in source_distribution.items():
                percentage = (count / total_duplicates) * 100
                print(f"- {source}: {count} filas ({percentage:.2f}%)")
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Verificar unicidad en el archivo integrado de libros
    integrated_books_path = os.path.join(project_root, 'integrated_books.csv')
    check_isbn_uniqueness(integrated_books_path)
    
    print(f"\n{'='*10} Verificación de unicidad de ISBN completada {'='*10}") 