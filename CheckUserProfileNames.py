import pandas as pd
import os

def check_user_profile_names(ratings_file):
    """
    Verifica si hay user_ids que tengan diferentes profile names asociados.
    
    Args:
        ratings_file: Ruta al archivo CSV de ratings
    """
    print(f"\n--- Verificando consistencia de profile names por user_id ---")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(ratings_file, encoding='utf-8')
        
        if 'user_id' not in df.columns or 'profileName' not in df.columns:
            print("Error: No se encontraron las columnas 'user_id' o 'profileName' en el archivo.")
            return
        
        # Agrupar por user_id y contar profile names únicos
        profile_name_counts = df.groupby('user_id')['profileName'].nunique()
        
        # Encontrar user_ids con múltiples profile names
        inconsistent_users = profile_name_counts[profile_name_counts > 1]
        
        # Estadísticas
        total_users = len(profile_name_counts)
        inconsistent_count = len(inconsistent_users)
        
        print(f"\nEstadísticas:")
        print(f"- Total de user_ids únicos: {total_users}")
        print(f"- User_ids con múltiples profile names: {inconsistent_count}")
        print(f"- Porcentaje de user_ids inconsistentes: {(inconsistent_count/total_users)*100:.2f}%")
        
        if not inconsistent_users.empty:
            print("\nPrimeros 10 user_ids con múltiples profile names:")
            for user_id, count in inconsistent_users.head(10).items():
                print(f"\nUser ID: {user_id}")
                print(f"Número de profile names diferentes: {count}")
                # Mostrar los diferentes profile names para este user_id
                profile_names = df[df['user_id'] == user_id]['profileName'].unique()
                print("Profile names asociados:")
                for name in profile_names:
                    print(f"- {name}")
            
            if len(inconsistent_users) > 10:
                print(f"\n... y {len(inconsistent_users) - 10} user_ids más con múltiples profile names.")
            
            # Mostrar algunos ejemplos de ratings con user_ids inconsistentes
            print("\nEjemplos de ratings con user_ids inconsistentes:")
            sample_users = list(inconsistent_users.head(3).index)
            inconsistent_ratings = df[df['user_id'].isin(sample_users)]
            print(inconsistent_ratings[['user_id', 'profileName', 'isbn', 'rating']].head(10))
        else:
            print("\n¡Éxito! No se encontraron user_ids con múltiples profile names.")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Ruta al archivo de ratings
    ratings_path = os.path.join(project_root, 'integrated_ratings.csv')
    
    check_user_profile_names(ratings_path)
    
    print(f"\n{'='*10} Verificación de consistencia de profile names completada {'='*10}") 