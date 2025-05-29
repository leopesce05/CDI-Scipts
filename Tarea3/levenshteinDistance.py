from Levenshtein import distance
import pandas as pd

def calcular_distancia_normalizada(str1, str2):
    if pd.isna(str1) or pd.isna(str2):
        return 1.0  # Si alguno es NaN, consideramos máxima distancia
    
    str1 = str(str1).lower()
    str2 = str(str2).lower()
    
    dist = distance(str1, str2)
    max_len = max(len(str1), len(str2))
    return dist / max_len if max_len > 0 else 0

def encontrar_similares(df, columna, umbral, nombre_archivo):
    print(f"\n=== Similares en {nombre_archivo} - Columna: {columna} (umbral: {umbral}) ===")
    similares = []
    elementos_usados = set()  # Conjunto para trackear elementos ya comparados
    
    for i in range(len(df)):
        if i in elementos_usados:
            continue
            
        for j in range(i + 1, len(df)):
            if j in elementos_usados:
                continue
                
            dist = calcular_distancia_normalizada(df[columna].iloc[i], df[columna].iloc[j])
            if dist < umbral:
                similares.append({
                    'indice1': i,
                    'indice2': j,
                    'valor1': df[columna].iloc[i],
                    'valor2': df[columna].iloc[j],
                    'distancia': dist
                })
                # Agregamos ambos elementos al conjunto de usados
                elementos_usados.add(i)
                elementos_usados.add(j)
                break  # Salimos del bucle interno ya que encontramos un par para i
    
    # Ordenar por distancia
    similares.sort(key=lambda x: x['distancia'])
    
    # Mostrar resultados
    for sim in similares:
        print(f"\nDistancia: {sim['distancia']:.3f}")
        print(f"Valor 1: {sim['valor1']}")
        print(f"Valor 2: {sim['valor2']}")
    
    print(f"\nTotal de pares similares encontrados: {len(similares)}")
    print(f"Total de elementos usados: {len(elementos_usados)}")

# Leer los archivos CSV
if __name__ == "__main__":
    try:
        print("Leyendo archivos CSV...")
        books_df = pd.read_csv('../../integrated_books.csv')
        
        print("Analizando similitudes...")
        # Analizar títulos en integrated_books.csv
        encontrar_similares(books_df, 'title', 0.2, 'integrated_books.csv')
        
        # Analizar descripciones en integrated_books.csv
        encontrar_similares(books_df, 'description', 0.4, 'integrated_books.csv')

    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


