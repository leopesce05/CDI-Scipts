import pandas as pd

def contar_duplicados():
    # Leer los archivos CSV
    try:
        # Leer los archivos con low_memory=False para evitar las advertencias
        books_df = pd.read_csv("../../integrated_books.csv", low_memory=False)
        users_df = pd.read_csv("../../integrated_users.csv", low_memory=False)
        
        # Verificar que las columnas existan antes de contar duplicados
        print("\nDuplicados en integrated_books.csv:")
        if 'isbn' in books_df.columns:
            print("ISBN duplicados:", books_df['isbn'].duplicated().sum())
        else:
            print("Columna 'ISBN' no encontrada en el archivo")
            
        if 'title' in books_df.columns:
            print("Titulo duplicados:", books_df['title'].duplicated().sum())
        else:
            print("Columna 'title' no encontrada en el archivo")
        
        print("\nDuplicados en integrated_users.csv:")
        if 'user_id' in users_df.columns:
            print("UserID duplicados:", users_df['user_id'].duplicated().sum())
        else:
            print("Columna 'user_id' no encontrada en el archivo")
            
        # Mostrar las columnas disponibles para debugging
        print("\nColumnas disponibles en books_df:", books_df.columns.tolist())
        print("Columnas disponibles en users_df:", users_df.columns.tolist())
        
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    contar_duplicados()