from Levenshtein import distance
import pandas as pd
import csv
from multiprocessing import Pool, cpu_count
from functools import partial

def calcular_distancia_normalizada(str1, str2):
    if pd.isna(str1) or pd.isna(str2):
        return 1.0
    str1 = str(str1).lower()
    str2 = str(str2).lower()
    dist = distance(str1, str2)
    max_len = max(len(str1), len(str2))
    return dist / max_len if max_len > 0 else 0

def procesar_fila(args):
    i, texto_combinado, todos_textos, titulos, descripciones = args
    min_distancia = float('inf')
    fila_mas_similar = -1
    
    # Calcular distancia con todos los demás
    for j, otro_texto in enumerate(todos_textos):
        if i != j:
            dist = calcular_distancia_normalizada(texto_combinado, otro_texto)
            if dist < min_distancia:
                min_distancia = dist
                fila_mas_similar = j
    
    print(f"Fila {i + 1} completada - Distancia mínima: {min_distancia:.4f}")
    return (i, min_distancia, fila_mas_similar)

if __name__ == "__main__":
    try:
        print("Leyendo archivo CSV...")
        books_df = pd.read_csv('../../integratedCSVs/books.csv', encoding='latin-1')
        
        # Obtener títulos y descripciones
        titulos = books_df['Title'].values
        descripciones = books_df['description'].values
        total = len(titulos)
        
        print(f"Analizando {total} registros (título + descripción)...")
        print(f"Usando {cpu_count()} núcleos para procesamiento paralelo")

        # Preprocesar textos combinados
        todos_textos = [f"{t} {d}" for t, d in zip(titulos, descripciones)]
        
        # Preparar argumentos para el procesamiento paralelo
        args = [(i, texto, todos_textos, titulos, descripciones) 
                for i, texto in enumerate(todos_textos)]

        # Procesar en paralelo
        with Pool() as pool:
            resultados = pool.map(procesar_fila, args)

        # Ordenar resultados por distancia mínima
        resultados.sort(key=lambda x: x[1])

        # Guardar resultados en CSV
        with open('resultados_similitud.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Número de Fila', 'Título', 'Descripción', 'Distancia Mínima', 'Fila Más Similar', 'Título Similar', 'Descripción Similar'])
            for fila, distancia, fila_similar in resultados:
                writer.writerow([
                    fila,
                    titulos[fila],
                    descripciones[fila],
                    distancia,
                    fila_similar,
                    titulos[fila_similar] if fila_similar != -1 else "N/A",
                    descripciones[fila_similar] if fila_similar != -1 else "N/A"
                ])

        # Resultados finales
        print("\nResultados finales:")
        print(f"Total de registros analizados: {total}")
        print(f"Resultados guardados en 'resultados_similitud.csv'")
        
        # Mostrar algunos ejemplos de los más similares
        print("\nTop 5 registros más similares:")
        for fila, distancia, fila_similar in resultados[:5]:
            print(f"\nFila {fila}:")
            print(f"Título: {titulos[fila]}")
            print(f"Descripción: {descripciones[fila]}")
            print(f"Distancia: {distancia:.4f}")
            print(f"Similar a Fila {fila_similar}:")
            print(f"Título: {titulos[fila_similar]}")
            print(f"Descripción: {descripciones[fila_similar]}")
            print("-" * 80)

    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
