import pandas as pd
import os

def check_user_references(ratings_file, users_file):
    """
    Verifica que todos los user_id en el archivo de ratings existan en el archivo de usuarios.
    
    Args:
        ratings_file: Ruta al archivo CSV de ratings
        users_file: Ruta al archivo CSV de usuarios
    """
    print(f"\n--- Verificando referencias de user_id entre ratings y usuarios ---")
    
    try:
        # Leer los archivos CSV
        ratings_df = pd.read_csv(ratings_file, encoding='utf-8')
        users_df = pd.read_csv(users_file, encoding='utf-8')
        
        if 'user_id' not in ratings_df.columns:
            print("Error: No se encontró la columna 'user_id' en el archivo de ratings.")
            return
            
        if 'user_id' not in users_df.columns:
            print("Error: No se encontró la columna 'user_id' en el archivo de usuarios.")
            return
        
        # Obtener conjuntos de user_ids
        ratings_user_ids = set(ratings_df['user_id'].dropna().unique())
        users_user_ids = set(users_df['user_id'].dropna().unique())
        
        # Encontrar user_ids en ratings que no están en usuarios
        missing_user_ids = ratings_user_ids - users_user_ids
        
        # Estadísticas
        total_ratings_user_ids = len(ratings_user_ids)
        total_users_user_ids = len(users_user_ids)
        total_missing = len(missing_user_ids)
        
        print(f"\nEstadísticas:")
        print(f"- Total de user_ids únicos en ratings: {total_ratings_user_ids}")
        print(f"- Total de user_ids únicos en usuarios: {total_users_user_ids}")
        print(f"- Total de user_ids en ratings que no están en usuarios: {total_missing}")
        
        if missing_user_ids:
            print("\nPrimeros 10 user_ids en ratings que no están en usuarios:")
            for user_id in list(missing_user_ids)[:10]:
                print(f"- {user_id}")
            if len(missing_user_ids) > 10:
                print(f"... y {len(missing_user_ids) - 10} más.")
            
            # Mostrar algunos ejemplos de ratings con user_ids faltantes
            print("\nEjemplos de ratings con user_ids faltantes:")
            missing_ratings = ratings_df[ratings_df['user_id'].isin(missing_user_ids)]
            print(missing_ratings[['user_id', 'isbn', 'rating']].head(10))
            
            # Calcular porcentaje de ratings afectados
            total_ratings = len(ratings_df)
            affected_ratings = len(missing_ratings)
            percentage = (affected_ratings / total_ratings) * 100
            print(f"\nTotal de ratings afectados: {affected_ratings} ({percentage:.2f}% del total)")
        else:
            print("\n¡Éxito! Todos los user_ids en ratings existen en la tabla de usuarios.")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Rutas a los archivos
    ratings_path = os.path.join(project_root, 'integrated_ratings.csv')
    users_path = os.path.join(project_root, 'integrated_users.csv')
    
    check_user_references(ratings_path, users_path)
    
    print(f"\n{'='*10} Verificación de referencias de user_id completada {'='*10}") 