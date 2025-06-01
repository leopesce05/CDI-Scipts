import pandas as pd
import numpy as np

# Leer los archivos CSV
print("Leyendo archivos CSV...")
books_df = pd.read_csv('integrated_books.csv', low_memory=False)
ratings_df = pd.read_csv('integrated_ratings.csv', low_memory=False)

# Calcular el número real de ratings por libro
print("\nCalculando número real de ratings por libro...")
real_ratings_count = ratings_df.groupby('isbn').size().reset_index(name='real_ratings_count')

# Unir con books_df
books_with_counts = pd.merge(books_df, real_ratings_count, on='isbn', how='left')

# Filtrar solo libros que tienen ratings_count no nulo
books_with_both_counts = books_with_counts[books_with_counts['ratings_count'].notna()]

# Calcular diferencias
books_with_both_counts['difference'] = books_with_both_counts['real_ratings_count'] - books_with_both_counts['ratings_count']

# Análisis de resultados
print("\nAnálisis de comparación de conteos de ratings:")
print(f"Total de libros con ratings_count no nulo: {len(books_with_both_counts)}")
print(f"Libros con conteos exactamente iguales: {sum(books_with_both_counts['difference'] == 0)}")
print(f"Libros con diferencias: {sum(books_with_both_counts['difference'] != 0)}")

# Mostrar las mayores discrepancias
print("\nTop 10 mayores discrepancias (real_ratings_count - ratings_count):")
top_discrepancies = books_with_both_counts.nlargest(10, 'difference')
for _, row in top_discrepancies.iterrows():
    print(f"\nISBN: {row['isbn']}")
    print(f"Título: {row['title']}")
    print(f"ratings_count: {row['ratings_count']}")
    print(f"real_ratings_count: {row['real_ratings_count']}")
    print(f"Diferencia: {row['difference']}")

# Estadísticas generales
print("\nEstadísticas de diferencias:")
print(books_with_both_counts['difference'].describe())

# Calcular porcentaje de libros con diferencias dentro de ciertos rangos
print("\nDistribución de diferencias:")
bins = [-float('inf'), -100, -10, -1, 0, 1, 10, 100, float('inf')]
labels = ['<-100', '-100 a -10', '-10 a -1', '0', '1', '2-10', '11-100', '>100']
books_with_both_counts['diff_range'] = pd.cut(books_with_both_counts['difference'], bins=bins, labels=labels)
print(books_with_both_counts['diff_range'].value_counts().sort_index()) 