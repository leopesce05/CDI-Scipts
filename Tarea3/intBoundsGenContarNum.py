import pandas as pd

def contar_datos_en_rango():
    # Leer los archivos CSV
    print("Leyendo archivos CSV...")
    users_df = pd.read_csv('../../integrated_users.csv')
    ratings_df = pd.read_csv('../../integrated_ratings.csv')
    books_df = pd.read_csv('../../integrated_books.csv')
    
    # Contar edades entre 18 y 123 (inclusive)
    edad_count = users_df['age'].between(18, 123, inclusive='both').sum()
    print(f"\nCantidad de usuarios con edad entre 18 y 123 (inclusive): {edad_count}")
    print("Cantidad de usuarios analizados: ", len(users_df))
    print(f"Porcentaje de usuarios en rango: {edad_count/len(users_df)*100}% \n")

    # Contar scores entre 5 y 10 (inclusive)
    score_count = ratings_df['rating'].between(5, 10, inclusive='both').sum()
    print(f"Cantidad de ratings con score entre 5 y 10 (inclusive): {score_count}")
    print("Cantidad de ratings analizados: ", len(ratings_df))
    print(f"Porcentaje de ratings en rango: {score_count/len(ratings_df)*100}% \n")

    # Contar ratingscount entre 5 y 10 (inclusive)
    ratingscount_count = books_df['ratings_count'].between(5, 10, inclusive='both').sum()
    print(f"Cantidad de ratings con ratingscount entre 5 y 10 (inclusive): {ratingscount_count}")
    print("Cantidad de libros analizados: ", len(books_df))
    print(f"Porcentaje de libros en rango: {ratingscount_count/len(books_df)*100}% \n")

if __name__ == "__main__":
    contar_datos_en_rango()
