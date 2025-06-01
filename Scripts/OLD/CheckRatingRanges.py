import pandas as pd
import os

def check_rating_ranges(ratings_file):
    """
    Calcula el rango de ratings para cada fila y determina qué porcentaje de filas
    tienen un rating que supera o iguala el 50% del rango.
    
    Args:
        ratings_file: Ruta al archivo CSV de ratings
    """
    print(f"\n--- Análisis de rangos de ratings ---")
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(ratings_file, encoding='utf-8')
        
        if 'rating' not in df.columns:
            print("Error: No se encontró la columna 'rating' en el archivo.")
            return
        
        # Convertir ratings a numérico
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        
        # Calcular estadísticas generales
        min_rating = df['rating'].min()
        max_rating = df['rating'].max()
        total_range = max_rating - min_rating
        mid_point = min_rating + (total_range / 2)
        
        print(f"\nEstadísticas generales:")
        print(f"- Rating mínimo: {min_rating}")
        print(f"- Rating máximo: {max_rating}")
        print(f"- Rango total: {total_range}")
        print(f"- Punto medio (50% del rango): {mid_point}")
        
        # Calcular porcentaje de ratings que superan o igualan el 50% del rango
        above_or_equal_mid_point = df[df['rating'] >= mid_point]
        percentage_above = (len(above_or_equal_mid_point) / len(df)) * 100
        
        print(f"\nAnálisis de ratings por encima o igual al 50% del rango:")
        print(f"- Total de ratings: {len(df)}")
        print(f"- Ratings por encima o igual al 50% del rango: {len(above_or_equal_mid_point)}")
        print(f"- Porcentaje por encima o igual al 50%: {percentage_above:.2f}%")
        
        # Análisis adicional: distribución de ratings
        print("\nDistribución de ratings:")
        rating_counts = df['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            percentage = (count / len(df)) * 100
            print(f"- Rating {rating}: {count} registros ({percentage:.2f}%)")
            
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    
    # Ruta al archivo de ratings
    ratings_path = os.path.join(project_root, 'integrated_ratings.csv')
    
    check_rating_ranges(ratings_path)
    
    print(f"\n{'='*10} Análisis de rangos de ratings completado {'='*10}") 