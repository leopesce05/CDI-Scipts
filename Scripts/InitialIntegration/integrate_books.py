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
    # Leer books_data.csv de L1
    print("Leyendo books_data.csv de L1...")
    l1_books_data = pd.read_csv(os.path.join(L1_PATH, 'books_data.csv'),
                               dtype={'Title': str, 'description': str, 'authors': str,
                                     'image': str, 'previewLink': str, 'publisher': str,
                                     'publishedDate': str, 'infoLink': str, 'categories': str,
                                     'ratingsCount': str},
                               encoding='latin1',
                               on_bad_lines='warn',
                               low_memory=False)
    print(f"L1 - Total de libros en books_data.csv: {len(l1_books_data)}")
    
    # Leer Books_rating.csv de L1 para complementar
    print("\nLeyendo Books_rating.csv de L1 para complementar...")
    l1_books_rating = pd.read_csv(os.path.join(L1_PATH, 'Books_rating.csv'),
                                 usecols=['Id', 'Title', 'Price'],
                                 dtype={'Id': str, 'Title': str, 'Price': str},
                                 encoding='latin1',
                                 on_bad_lines='warn',
                                 low_memory=False)
    print(f"L1 - Total de libros en Books_rating.csv: {len(l1_books_rating)}")
    
    # Leer libros de L2
    print("\nLeyendo libros de L2...")
    l2_books = pd.read_csv(os.path.join(L2_PATH, 'books.csv'),
                          sep=';',
                          usecols=['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 
                                 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L'],
                          dtype={'ISBN': str, 'Book-Title': str, 'Book-Author': str, 
                                'Year-Of-Publication': str, 'Publisher': str,
                                'Image-URL-S': str, 'Image-URL-M': str, 'Image-URL-L': str},
                          encoding='latin1',
                          on_bad_lines='warn',
                          low_memory=False)
    print(f"L2 - Total de libros leídos: {len(l2_books)}")
    
    # Crear DataFrame de L1 con todas las columnas
    l1_books_processed = pd.DataFrame()
    l1_books_processed['Title'] = l1_books_data['Title']
    l1_books_processed['description'] = l1_books_data['description']
    l1_books_processed['authors'] = l1_books_data['authors']
    l1_books_processed['image'] = l1_books_data['image']
    l1_books_processed['previewLink'] = l1_books_data['previewLink']
    l1_books_processed['publisher'] = l1_books_data['publisher']
    l1_books_processed['publishedDate'] = l1_books_data['publishedDate']
    l1_books_processed['infoLink'] = l1_books_data['infoLink']
    l1_books_processed['categories'] = l1_books_data['categories']
    l1_books_processed['ratingsCount'] = l1_books_data['ratingsCount']
    
    # Complementar con datos de Books_rating.csv
    # Crear un diccionario de Title a Id y Price
    title_to_id_price = dict(zip(l1_books_rating['Title'], zip(l1_books_rating['Id'], l1_books_rating['Price'])))
    
    # Aplicar el mapeo
    l1_books_processed['Id'] = l1_books_processed['Title'].map(lambda x: title_to_id_price.get(x, (None, None))[0])
    l1_books_processed['Price'] = l1_books_processed['Title'].map(lambda x: title_to_id_price.get(x, (None, None))[1])
    print(f"L1 - Después de procesar: {len(l1_books_processed)}")
    
    # Crear DataFrame de L2 con todas las columnas
    l2_books_processed = pd.DataFrame()
    l2_books_processed['Id'] = l2_books['ISBN']
    l2_books_processed['Title'] = l2_books['Book-Title']
    l2_books_processed['Price'] = None  # L2 no tiene Price
    l2_books_processed['description'] = None  # L2 no tiene description
    l2_books_processed['authors'] = l2_books['Book-Author']
    l2_books_processed['image'] = None  # L2 no tiene image
    l2_books_processed['previewLink'] = None  # L2 no tiene previewLink
    l2_books_processed['publisher'] = l2_books['Publisher']
    l2_books_processed['publishedDate'] = l2_books['Year-Of-Publication']
    l2_books_processed['infoLink'] = None  # L2 no tiene infoLink
    l2_books_processed['categories'] = None  # L2 no tiene categories
    l2_books_processed['ratingsCount'] = None  # L2 no tiene ratingsCount
    l2_books_processed['Image-URL-S'] = l2_books['Image-URL-S']
    l2_books_processed['Image-URL-M'] = l2_books['Image-URL-M']
    l2_books_processed['Image-URL-L'] = l2_books['Image-URL-L']
    print(f"L2 - Después de procesar: {len(l2_books_processed)}")
    
    # Combinar los libros
    print("\nCombinando libros...")
    integrated_books = pd.concat([l1_books_processed, l2_books_processed], ignore_index=True)
    print(f"Total después de concatenar: {len(integrated_books)}")
    
    # Guardar resultado
    print("\nGuardando libros integrados...")
    integrated_books.to_csv(os.path.join(OUTPUT_PATH, 'books.csv'),
                          index=False,
                          encoding='latin1')
    
    print("\nResumen final:")
    print(f"Libros de L1: {len(l1_books_processed)}")
    print(f"Libros de L2: {len(l2_books_processed)}")
    print(f"Total de libros: {len(integrated_books)}")

except Exception as e:
    print(f"Error durante la integración: {str(e)}")
    import traceback
    print("Detalles del error:")
    print(traceback.format_exc()) 