import pandas as pd
import os

# Configurar rutas
L1_PATH = '../../L1'
L2_PATH = '../../L2'
OUTPUT_PATH = '../../integratedCSVs'

# Crear directorio de salida si no existe
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("Integrando ratings...")

try:
    # Leer ratings de L1
    print("Leyendo ratings de L1...")
    l1_ratings = pd.read_csv(os.path.join(L1_PATH, 'Books_rating.csv'), 
                            dtype={'Id': str, 'User_id': str, 'review/score': float, 
                                   'review/time': int, 'review/summary': str, 
                                   'review/text': str, 'Price': str, 'Title': str},
                            encoding='latin1',
                            on_bad_lines='warn')
    print(f"L1 - Total de registros leídos: {len(l1_ratings)}")
    
    # Seleccionar y renombrar columnas de L1
    l1_ratings = l1_ratings[['Id', 'User_id', 'review/score', 'review/time', 
                            'review/summary', 'review/text', 'Price', 'Title']]
    print(f"L1 - Después de seleccionar columnas: {len(l1_ratings)}")
    
    # Leer ratings de L2
    print("\nLeyendo ratings de L2...")
    l2_ratings = pd.read_csv(os.path.join(L2_PATH, 'ratings.csv'),
                            sep=';',
                            dtype={'User-ID': str, 'ISBN': str, 'Book-Rating': float},
                            encoding='latin1',
                            on_bad_lines='warn')
    print(f"L2 - Total de registros leídos: {len(l2_ratings)}")
    
    # Crear DataFrame de L2 con todas las columnas de L1
    l2_ratings_processed = pd.DataFrame()
    
    # Mapear columnas existentes
    l2_ratings_processed['Id'] = l2_ratings['ISBN']
    l2_ratings_processed['User_id'] = l2_ratings['User-ID']
    l2_ratings_processed['review/score'] = l2_ratings['Book-Rating']
    
    # Agregar columnas vacías para datos que no existen en L2
    l2_ratings_processed['review/time'] = None
    l2_ratings_processed['review/summary'] = None
    l2_ratings_processed['review/text'] = None
    l2_ratings_processed['Price'] = None
    l2_ratings_processed['Title'] = None
    print(f"L2 - Después de procesar: {len(l2_ratings_processed)}")
    
    # Combinar los ratings
    print("\nCombinando ratings...")
    integrated_ratings = pd.concat([l1_ratings, l2_ratings_processed], ignore_index=True)
    print(f"Total después de concatenar: {len(integrated_ratings)}")
    
    # Eliminar duplicados (mismo usuario, mismo libro)
    #print("\nEliminando duplicados...")
    #print(f"Duplicados encontrados: {len(integrated_ratings) - len(integrated_ratings.drop_duplicates(subset=['Id', 'User_id'], keep='first'))}")
    #integrated_ratings = integrated_ratings.drop_duplicates(subset=['Id', 'User_id'], keep='first')
    #print(f"Total después de eliminar duplicados: {len(integrated_ratings)}")
    
    # Guardar resultado
    print("\nGuardando ratings integrados...")
    integrated_ratings.to_csv(os.path.join(OUTPUT_PATH, 'ratings.csv'), 
                            index=False,
                            encoding='latin1')
    
    print("\nResumen final:")
    print(f"Ratings de L1: {len(l1_ratings)}")
    print(f"Ratings de L2: {len(l2_ratings)}")
    print(f"Total de ratings: {len(integrated_ratings)}")
    
except Exception as e:
    print(f"Error durante la integración: {str(e)}") 