import pandas as pd
import os

# Configurar rutas
L1_PATH = '../L1'
L2_PATH = '../L2'
OUTPUT_PATH = 'integratedCSVs'

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
                          on_bad_lines='warn')
    print(f"L1 - Total de usuarios leídos: {len(l1_users)}")
    
    # Seleccionar columnas de L1
    l1_users = l1_users[['User_id', 'profileName']]
    print(f"L1 - Después de seleccionar columnas: {len(l1_users)}")
    
    # Leer usuarios de L2
    print("\nLeyendo usuarios de L2...")
    l2_users = pd.read_csv(os.path.join(L2_PATH, 'users.csv'),
                          dtype={'user_id': str, 'username': str},
                          encoding='latin1',
                          on_bad_lines='warn')
    print(f"L2 - Total de usuarios leídos: {len(l2_users)}")
    
    # Crear DataFrame de L2 con todas las columnas de L1
    l2_users_processed = pd.DataFrame()
    
    # Mapear columnas existentes
    l2_users_processed['User_id'] = l2_users['user_id']
    l2_users_processed['profileName'] = l2_users['username']
    print(f"L2 - Después de procesar: {len(l2_users_processed)}")
    
    # Combinar los usuarios
    print("\nCombinando usuarios...")
    integrated_users = pd.concat([l1_users, l2_users_processed], ignore_index=True)
    print(f"Total después de concatenar: {len(integrated_users)}")
    
    # Eliminar duplicados (mismo User_id)
    #print("\nEliminando duplicados...")
    #print(f"Duplicados encontrados: {len(integrated_users) - len(integrated_users.drop_duplicates(subset=['User_id'], keep='first'))}")
    #integrated_users = integrated_users.drop_duplicates(subset=['User_id'], keep='first')
    #print(f"Total después de eliminar duplicados: {len(integrated_users)}")
    
    # Guardar resultado
    print("\nGuardando usuarios integrados...")
    integrated_users.to_csv(os.path.join(OUTPUT_PATH, 'users.csv'),
                          index=False,
                          encoding='latin1')
    
    print("\nResumen final:")
    print(f"Usuarios de L1: {len(l1_users)}")
    print(f"Usuarios de L2: {len(l2_users)}")
    print(f"Total de usuarios: {len(integrated_users)}")
    
except Exception as e:
    print(f"Error durante la integración: {str(e)}") 