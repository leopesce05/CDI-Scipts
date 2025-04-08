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
            transformed_df['source'] = source_name  # Agregar columna para identificar la fuente
            transformed_dfs.append(transformed_df)

        # Concatenar todos los DataFrames transformados
        integrated_data = pd.concat(transformed_dfs, ignore_index=True)
        return integrated_data
    
    def merge_duplicate_books(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fusiona registros duplicados de libros basándose en título, autores y fecha de publicación.
        
        Args:
            data: DataFrame con los datos integrados
            
        Returns:
            DataFrame con los registros duplicados fusionados
        """
        # Identificar las columnas clave para la fusión
        key_columns = ['title', 'authors', 'publication_date']
        
        # Verificar que las columnas clave existan
        for col in key_columns:
            if col not in data.columns:
                print(f"Advertencia: La columna clave '{col}' no existe en los datos")
                return data
        
        # Agrupar por las columnas clave
        grouped = data.groupby(key_columns)
        
        # Función para combinar valores de columnas
        def combine_values(series):
            # Eliminar valores nulos y duplicados
            values = series.dropna().unique()
            if len(values) == 0:
                return None
            elif len(values) == 1:
                return values[0]
            else:
                # Para columnas de texto, concatenar valores únicos
                if pd.api.types.is_string_dtype(series):
                    return ' | '.join(values)
                # Para columnas numéricas, tomar el primer valor no nulo
                else:
                    return values[0]
        
        # Aplicar la función de combinación a cada grupo
        merged_data = grouped.agg(combine_values).reset_index()
        
        # Agregar una columna que indique las fuentes combinadas
        source_info = grouped['source'].agg(lambda x: ' | '.join(x.unique())).reset_index()
        merged_data['combined_sources'] = source_info['source']
        
        return merged_data

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
    # Configuración de mapeo para las bases de datos de libros
    config = {
        "books_data_1": {
            "title": "Title",
            "description": "description",
            "authors": "authors",
            "image_url": "image",
            "preview_link": "previewLink",
            "publisher": "publisher",
            "publication_date": "publishedDate",
            "info_link": "infoLink",
            "categories": "categories",
            "ratings_count": "ratingsCount"
        },
        "books_data_2": {
            "isbn": "ISBN",
            "title": "Book-Title",
            "authors": "Book-Author",
            "publication_date": "Year-Of-Publication",
            "publisher": "Publisher",
            "image_url_small": "Image-URL-S",
            "image_url_medium": "Image-URL-M",
            "image_url_large": "Image-URL-L"
        }
    }

    # Crear instancia del integrador
    integrator = DataIntegrator(config)

    # Ejemplo de cómo cargar y transformar los datos
    try:
        # Cargar datos de la primera base (con separador "," y comillas dobles)
        books_data_1 = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L1/books_data.csv', 
                                  sep=',', 
                                  encoding='latin-1',
                                  on_bad_lines='warn')  # Advertir sobre líneas problemáticas
        
        # Cargar datos de la segunda base (con separador ";" y comillas dobles)
        books_data_2 = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L2/books.csv', 
                                  sep=';', 
                                  quotechar='"',
                                  encoding='latin-1',
                                  on_bad_lines='warn')  # Advertir sobre líneas problemáticas

        # Verificar si hay columnas adicionales no esperadas
        print("\nColumnas en books_data_1:", books_data_1.columns.tolist())
        print("Columnas en books_data_2:", books_data_2.columns.tolist())

        # Integrar los datos
        data_sources = {
            "books_data_1": books_data_1,
            "books_data_2": books_data_2
        }

        integrated_data = integrator.integrate_data(data_sources)
        
        # Mostrar estadísticas de fusión
        print(f"Registros originales: {len(integrated_data)}")
        
        # Guardar los datos integrados y fusionados
        integrated_data.to_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/integrated_books.csv', 
                          index=False, 
                          quotechar='"',
                          encoding='utf-8')  # Guardamos en UTF-8
        print("\nDatos integrados y fusionados guardados en 'integrated_books.csv'")
        
        # Mostrar las primeras filas de los datos integrados
        print("\nPrimeras filas de los datos integrados y fusionados:")
        print(integrated_data.head())
        
        # Mostrar información sobre las columnas
        print("\nColumnas en el dataset integrado y fusionado:")
        print(integrated_data.columns.tolist())
        
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo de datos: {e}")
    except Exception as e:
        print(f"Error durante la integración: {e}")
        # Imprimir más detalles sobre el error
        import traceback
        print(traceback.format_exc()) 