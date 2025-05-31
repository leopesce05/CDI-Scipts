import pandas as pd
import os
import sys
from DB.db_operations import DBOperations

def calcular_distancia_normalizada(str1, str2):
    """
    Calcula la distancia de Levenshtein normalizada entre dos strings.
    """
    if pd.isna(str1) or pd.isna(str2):
        return 1.0
    
    str1 = str(str1).lower()
    str2 = str(str2).lower()
    
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    
    if len(str2) == 0:
        return 1.0
    
    previous_row = range(len(str2) + 1)
    for i, c1 in enumerate(str1):
        current_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1] / max(len(str1), len(str2))

def encontrar_similares(file_path, db, execution_id):
    """
    Encuentra entradas similares en el archivo especificado y guarda los resultados en la base de datos.
    """
    try:
        # Intentar diferentes codificaciones
        encodings = ['latin-1', 'utf-8', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise Exception("No se pudo leer el archivo con ninguna codificación")
        
        # Verificar columnas necesarias
        required_columns = ['Title', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Error: No se encontraron las columnas: {', '.join(missing_columns)}")
            return
        
        # Calcular similitudes para cada columna
        for column in required_columns:
            try:
                # Calcular similitudes para la columna actual
                similares = []
                for i in range(len(df)):
                    for j in range(i + 1, len(df)):
                        dist = calcular_distancia_normalizada(df.iloc[i][column], df.iloc[j][column])
                        if dist < 0.3:
                            similares.append((i, j, dist))
                
                # Guardar resultado de columna - cantidad de pares similares
                db.guardar_resultado_columna(
                    execution_id=execution_id,
                    nombre_tabla='books',
                    nombre_atributo=column,
                    valor={
                        'id': 'integer',
                        'valor': len(similares)
                    }
                )
                
                print(f"\nArchivo: {os.path.basename(file_path)}")
                print(f"Columna: {column}")
                print(f"Total de pares similares encontrados: {len(similares)}")
                
            except Exception as e:
                print(f"Error al guardar resultados en la base de datos para la columna {column}: {e}")
                continue
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise

if __name__ == "__main__":
    try:
        # Conectar a la base de datos
        db = DBOperations()
        
        # 1. Crear una nueva ejecución
        execution_id = db.crear_ejecucion(
            metodo="ExactSint-LeveshteinDistanceInterCSV_ap"
        )
        
        # 2. Procesar y guardar resultados
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        integrated_csvs_dir = os.path.join(project_root, 'integratedCSVs')

        # Verificar similitudes en el archivo de libros
        file_path = os.path.join(integrated_csvs_dir, 'books.csv')
        encontrar_similares(file_path, db, execution_id)

        print(f"\n{'='*10} Verificación de similitudes completada {'='*10}")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if 'db' in locals():
            db.close()


