import pandas as pd
from typing import Dict, List, Any
import json

class DataIntegrator:
    def __init__(self, mapping_config: Dict[str, Dict[str, str]]):
        """
        Inicializa el integrador de datos con una configuración de mapeo.
        
        Args:
            mapping_config: Diccionario que define cómo mapear columnas entre diferentes fuentes
        """
        self.mapping_config = mapping_config

    def transform_data(self, data: pd.DataFrame, source_name: str) -> pd.DataFrame:
        """
        Transforma los datos de una fuente específica al formato estándar.
        
        Args:
            data: DataFrame con los datos de la fuente
            source_name: Nombre de la fuente de datos
            
        Returns:
            DataFrame con los datos transformados al formato estándar
        """
        if source_name not in self.mapping_config:
            raise ValueError(f"No se encontró configuración para la fuente: {source_name}")

        mapping = self.mapping_config[source_name]
        transformed_data = pd.DataFrame()

        # Aplicar el mapeo de columnas
        for standard_col, source_col in mapping.items():
            if source_col in data.columns:
                transformed_data[standard_col] = data[source_col]
            else:
                print(f"Advertencia: La columna {source_col} no existe en los datos de {source_name}")

        return transformed_data

    def integrate_data(self, data_sources: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Integra datos de múltiples fuentes en un único DataFrame.
        
        Args:
            data_sources: Diccionario con los DataFrames de cada fuente
            
        Returns:
            DataFrame con todos los datos integrados
        """
        transformed_dfs = []
        
        for source_name, df in data_sources.items():
            transformed_df = self.transform_data(df, source_name)
            transformed_dfs.append(transformed_df)

        # Concatenar todos los DataFrames transformados
        integrated_data = pd.concat(transformed_dfs, ignore_index=True)
        return integrated_data

    @staticmethod
    def load_mapping_config(config_file: str) -> Dict[str, Dict[str, str]]:
        """
        Carga la configuración de mapeo desde un archivo JSON.
        
        Args:
            config_file: Ruta al archivo de configuración JSON
            
        Returns:
            Diccionario con la configuración de mapeo
        """
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

# Ejemplo de uso con las bases de datos de libros
if __name__ == "__main__":
    try:
        # Cargar datos de usuarios
        users_cleaned = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L2/users_cleaned.csv', 
                                  sep=',',
                                  quotechar='"',
                                  encoding='latin-1',
                                  on_bad_lines='warn')
        
        # Cargar datos de ratings
        book_ratings = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L1/Books_rating.csv', 
                                 sep=',', 
                                 quotechar='"',
                                 encoding='latin-1',
                                 on_bad_lines='warn')
        
        # Cargar datos de ratings de la otra base
        ratings = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L2/ratings.csv', 
                            sep=';', 
                            quotechar='"',
                            encoding='latin-1',
                            on_bad_lines='warn')

        # Imprimir nombres de columnas para diagnóstico
        print("\nColumnas en users_cleaned:")
        print(users_cleaned.columns.tolist())
        
        print("\nColumnas en book_ratings:")
        print(book_ratings.columns.tolist())
        
        print("\nColumnas en ratings:")
        print(ratings.columns.tolist())

        # Integrar datos de usuarios
        users_config = {
            "users_cleaned": {
                "user_id": "User-ID",
                "location": "Location",
                "age": "Age"
            },
            "book_ratings": {
                "user_id": "User_id",
                "profile_name": "profileName"
            }
        }

        # Integrar datos de ratings
        ratings_config = {
            "book_ratings": {
                "isbn": "Id",
                "Title": "Title",
                "Price": "Price",
                "user_id": "User_id",
                "profileName": "profileName",
                "review/helpfulness": "review/helpfulness",
                "rating": "review/score",
                "review/time": "review/time",
                "review/summary": "review/summary",
                "review/text": "review/text"
            },
            "ratings": {
                "user_id": "User-ID",  # Ajustado según las columnas reales
                "isbn": "ISBN",
                "rating": "Book-Rating"
            }
        }

        # Crear instancias del integrador
        users_integrator = DataIntegrator(users_config)
        ratings_integrator = DataIntegrator(ratings_config)

        # Preparar datos para usuarios
        users_sources = {
            "users_cleaned": users_cleaned,
            "book_ratings": book_ratings[['User_id', 'profileName']].drop_duplicates()
        }

        # Preparar datos para ratings
        ratings_sources = {
            "book_ratings": book_ratings[["Id", "Title", "Price", "User_id", "profileName", "review/helpfulness", "review/score", "review/time", "review/summary", "review/text"]],
            "ratings": ratings[['User-ID', 'ISBN', 'Book-Rating']]  # Ajustado según las columnas reales
        }

        # Integrar datos
        integrated_users = users_integrator.integrate_data(users_sources)
        integrated_ratings = ratings_integrator.integrate_data(ratings_sources)

        # Eliminar duplicados de usuarios
        integrated_users = integrated_users.drop_duplicates(subset=['user_id'])

        # Guardar datos integrados
        integrated_users.to_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/integrated_users.csv', 
                              index=False, 
                              quotechar='"',
                              encoding='utf-8')
        
        integrated_ratings.to_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/integrated_ratings.csv', 
                                index=False, 
                                quotechar='"',
                                encoding='utf-8')

        print("\nDatos integrados guardados:")
        print(f"- Usuarios: {len(integrated_users)} registros")
        print(f"- Ratings: {len(integrated_ratings)} registros")
        
        # Mostrar las primeras filas de los datos integrados
        print("\nPrimeras filas de usuarios integrados:")
        print(integrated_users.head())
        
        print("\nPrimeras filas de ratings integrados:")
        print(integrated_ratings.head())
        
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo de datos: {e}")
    except Exception as e:
        print(f"Error durante la integración: {e}")
        # Imprimir más detalles sobre el error
        import traceback
        print(traceback.format_exc()) 