import pandas as pd
import os

# Configurar rutas
L1_PATH = '../../L1'
L2_PATH = '../../L2'
OUTPUT_PATH = '../../integratedCSVs'

# Crear directorio de salida si no existe
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("Integrando usuarios...")

try:
    # Leer usuarios de L1
    print("Leyendo usuarios de L1...")
    l1_users = pd.read_csv(os.path.join(L1_PATH, 'Books_rating.csv'),
                          usecols=['User_id', 'profileName'],
                          dtype={'User_id': str, 'profileName': str},
                          encoding='latin1',
                          on_bad_lines='warn',
                          low_memory=False)
    print(f"L1 - Total de usuarios leídos: {len(l1_users)}")
    
    # Leer usuarios de L2
    print("\nLeyendo usuarios de L2...")
    l2_users = pd.read_csv(os.path.join(L2_PATH, 'users.csv'),
                          sep=';',
                          usecols=['User-ID', 'Location', 'Age'],
                          dtype={'User-ID': str, 'Location': str, 'Age': str},
                          encoding='latin1',
                          on_bad_lines='warn',
                          low_memory=False)
    print(f"L2 - Total de usuarios leídos: {len(l2_users)}")
    
    # Crear DataFrame de L1 con todas las columnas
    l1_users_processed = pd.DataFrame()
    l1_users_processed['User_id'] = l1_users['User_id']
    l1_users_processed['profileName'] = l1_users['profileName']
    l1_users_processed['Location'] = None  # L1 no tiene Location
    l1_users_processed['Age'] = None  # L1 no tiene Age
    print(f"L1 - Después de procesar: {len(l1_users_processed)}")
    
    # Crear DataFrame de L2 con todas las columnas
    l2_users_processed = pd.DataFrame()
    l2_users_processed['User_id'] = l2_users['User-ID']
    l2_users_processed['profileName'] = None  # L2 no tiene profileName
    l2_users_processed['Location'] = l2_users['Location']
    l2_users_processed['Age'] = l2_users['Age']
    print(f"L2 - Después de procesar: {len(l2_users_processed)}")
    
    # Combinar los usuarios
    print("\nCombinando usuarios...")
    integrated_users = pd.concat([l1_users_processed, l2_users_processed], ignore_index=True)
    print(f"Total después de concatenar: {len(integrated_users)}")
    
    # Guardar resultado
    print("\nGuardando usuarios integrados...")
    integrated_users.to_csv(os.path.join(OUTPUT_PATH, 'users.csv'),
                          index=False,
                          encoding='latin1')
    
    print("\nResumen final:")
    print(f"Usuarios de L1: {len(l1_users_processed)}")
    print(f"Usuarios de L2: {len(l2_users_processed)}")
    print(f"Total de usuarios: {len(integrated_users)}")

except Exception as e:
    print(f"Error durante la integración: {str(e)}")
    import traceback
    print("Detalles del error:")
    print(traceback.format_exc()) 