import pandas as pd
import os

# Configurar rutas
L1_PATH = '../../L1'
L2_PATH = '../../L2'
OUTPUT_PATH = '../../integratedCSVs'

# Crear directorio de salida si no existe
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("Integrando libros...")

try:
    # Leer libros de L1
    print("Leyendo libros de L1...")
    l1_books = pd.read_csv(os.path.join(L1_PATH, 'books_data.csv'), 
                          dtype={'Id': str, 'Title': str, 'Price': str, 'Author': str},
                          encoding='latin1',
                          on_bad_lines='warn')
    print(f"L1 - Total de libros leídos: {len(l1_books)}")
    
    # Seleccionar columnas de L1
    l1_books = l1_books[['Id', 'Title', 'Price', 'Author']]
    print(f"L1 - Después de seleccionar columnas: {len(l1_books)}")
    
    # Leer libros de L2
    print("\nLeyendo libros de L2...")
    l2_books = pd.read_csv(os.path.join(L2_PATH, 'books.csv'),
                          dtype={'book_id': str, 'title': str, 'price': str, 'author': str},
                          encoding='latin1',
                          on_bad_lines='warn')
    print(f"L2 - Total de libros leídos: {len(l2_books)}")
    
    # Crear DataFrame de L2 con todas las columnas de L1
    l2_books_processed = pd.DataFrame()
    
    # Mapear columnas existentes
    l2_books_processed['Id'] = l2_books['book_id']
    l2_books_processed['Title'] = l2_books['title']
    l2_books_processed['Price'] = l2_books['price']
    l2_books_processed['Author'] = l2_books['author']
    print(f"L2 - Después de procesar: {len(l2_books_processed)}")
    
    # Combinar los libros
    print("\nCombinando libros...")
    integrated_books = pd.concat([l1_books, l2_books_processed], ignore_index=True)
    print(f"Total después de concatenar: {len(integrated_books)}")
    
    # Eliminar duplicados (mismo Id)
    #print("\nEliminando duplicados...")
    #print(f"Duplicados encontrados: {len(integrated_books) - len(integrated_books.drop_duplicates(subset=['Id'], keep='first'))}")
    #integrated_books = integrated_books.drop_duplicates(subset=['Id'], keep='first')
    #print(f"Total después de eliminar duplicados: {len(integrated_books)}")
    
    # Guardar resultado
    print("\nGuardando libros integrados...")
    integrated_books.to_csv(os.path.join(OUTPUT_PATH, 'books.csv'), 
                          index=False,
                          encoding='latin1')
    
    print("\nResumen final:")
    print(f"Libros de L1: {len(l1_books)}")
    print(f"Libros de L2: {len(l2_books)}")
    print(f"Total de libros: {len(integrated_books)}")
    
except Exception as e:
    print(f"Error durante la integración: {str(e)}") 