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
                # Handle potential type inconsistencies, e.g., converting ratings_count to numeric
                if standard_col == 'ratings_count':
                     # Convert to numeric, coercing errors to NaN
                    transformed_data[standard_col] = pd.to_numeric(data[source_col], errors='coerce')
                else:
                    transformed_data[standard_col] = data[source_col]
            else:
                print(f"Advertencia: La columna {source_col} no existe en los datos de {source_name}")
                # Add the standard column with NaNs if the source column is missing
                transformed_data[standard_col] = pd.NA

        # Add missing standard columns present in the config but not in the source data
        # This ensures all transformed DFs have the same columns before concatenation
        for standard_col in self.mapping_config[source_name].keys():
            if standard_col not in transformed_data.columns:
                transformed_data[standard_col] = pd.NA

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
        all_standard_columns = set()
        # First pass to get all possible standard columns from the config
        for source_config in self.mapping_config.values():
            all_standard_columns.update(source_config.keys())

        for source_name, df in data_sources.items():
            transformed_df = self.transform_data(df, source_name)
            transformed_df['source'] = source_name  # Agregar columna para identificar la fuente

             # Ensure all standard columns exist, adding NaNs if necessary
            for col in all_standard_columns:
                 if col not in transformed_df.columns:
                     transformed_df[col] = pd.NA

            transformed_dfs.append(transformed_df)

        # Concatenar todos los DataFrames transformados
        # Ensure consistent column order before concatenating
        final_columns = list(all_standard_columns) + ['source']
        for i in range(len(transformed_dfs)):
            transformed_dfs[i] = transformed_dfs[i].reindex(columns=final_columns)

        integrated_data = pd.concat(transformed_dfs, ignore_index=True, sort=False)
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
    # Configuración de mapeo para las bases de datos de libros
    # Se ajustará después de la fusión previa
    config = {
        "books_data_1": {
            "isbn": "Id", # Mapear ID de books_rating a isbn
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
            # Adding columns that might exist in data_1 but not data_2 for consistency
            "description": None,
            "image_url": None, # Will use image_url_small/medium/large logic if needed later
            "preview_link": None,
            "info_link": None,
            "categories": None,
            "ratings_count": None,
            # Original image columns from data_2
            "image_url_small": "Image-URL-S",
            "image_url_medium": "Image-URL-M",
            "image_url_large": "Image-URL-L"
        }
        # books_data_3 ya no se integra directamente, su info se une a books_data_1
    }

    # Crear instancia del integrador
    integrator = DataIntegrator(config)

    # Ejemplo de cómo cargar y transformar los datos
    try:
        # Cargar datos de la primera base (books_data)
        books_data_1_raw = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L1/books_data.csv',
                                   sep=',',
                                   encoding='latin-1',
                                   on_bad_lines='warn',
                                   low_memory=False) # Added low_memory=False for potential mixed types
        print(f"Columnas originales en books_data_1: {books_data_1_raw.columns.tolist()}")


        # Cargar datos de la tercera base (ratings) solo con ID y Title
        # Asumiendo que las columnas son 'ID' y 'Title'
        try:
            books_data_3_ratings = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L1/Books_rating.csv',
                                     sep=',',
                                     encoding='latin-1',
                                     on_bad_lines='warn',
                                     usecols=['Id', 'Title']) # Cargar solo columnas necesarias
            print(f"Cargado Books_rating.csv con columnas 'ID', 'Title'.")
        except ValueError as e:
             print(f"Error cargando Books_rating.csv con 'ID', 'Title': {e}")
             print("Intentando con 'book_id', 'title'...")
             # Intentar cargar con nombres comunes si falló
             try:
                 books_data_3_ratings = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L1/Books_rating.csv',
                                          sep=',',
                                          encoding='latin-1',
                                          on_bad_lines='warn',
                                          usecols=['book_id', 'title']) # Asumiendo otros nombres comunes
                 books_data_3_ratings = books_data_3_ratings.rename(columns={'book_id': 'Id', 'title': 'Title'}) # Renombrar a estándar interno
                 print("Cargado con éxito usando 'book_id', 'title'.")
             except Exception as final_e:
                 print(f"No se pudo cargar Books_rating.csv con columnas alternativas.")
                 # Intentar inspeccionar columnas
                 try:
                     books_data_3_ratings_inspect = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L1/Books_rating.csv', sep=',', encoding='latin-1', on_bad_lines='warn', nrows=5)
                     print(f"Primeras filas de Books_rating.csv para inspección:\n{books_data_3_ratings_inspect}")
                     print(f"Columnas detectadas: {books_data_3_ratings_inspect.columns.tolist()}")
                 except Exception as inspect_e:
                     print(f"No se pudo siquiera inspeccionar Books_rating.csv: {inspect_e}")
                 raise final_e # Re-lanzar la excepción original si no se puede cargar

        print(f"Columnas en books_data_3_ratings (después de posible renombrado): {books_data_3_ratings.columns.tolist()}")


        # --- Pre-integración: Fusionar books_data_1 con books_data_3 ---
        print("\nIniciando pre-integración de books_data_1 y books_data_3...")
        # Asegurarse que 'Title' existe en ambos y limpiar/estandarizar
        if 'Title' not in books_data_1_raw.columns or 'Title' not in books_data_3_ratings.columns:
             raise ValueError("La columna 'Title' es necesaria para la fusión y no se encontró en ambos DataFrames.")

        books_data_1_raw['Title_merge'] = books_data_1_raw['Title'].astype(str).str.strip().str.lower()
        books_data_3_ratings['Title_merge'] = books_data_3_ratings['Title'].astype(str).str.strip().str.lower()

        # Eliminar duplicados en ratings por Title_merge, manteniendo el primer ID encontrado
        books_data_3_unique = books_data_3_ratings.drop_duplicates(subset=['Title_merge'], keep='first')
        print(f"Registros únicos en ratings por título: {len(books_data_3_unique)}")

        # Realizar left merge para añadir ID a books_data_1
        books_data_1_merged = pd.merge(
            books_data_1_raw,
            books_data_3_unique[['Id', 'Title_merge']], # Seleccionar solo ID y la clave de merge
            on='Title_merge',
            how='left' # Mantener todos los registros de books_data_1_raw
        )
        print(f"Registros en books_data_1 después de fusionar con ratings: {len(books_data_1_merged)}")
        # Limpiar columna temporal de merge
        books_data_1_merged = books_data_1_merged.drop(columns=['Title_merge'])
        # Verificar cuántos IDs se añadieron
        ids_added = books_data_1_merged['Id'].notna().sum()
        print(f"Se añadieron {ids_added} IDs desde books_rating a books_data_1.")
        print(f"Columnas en books_data_1_merged: {books_data_1_merged.columns.tolist()}")
        # --- Fin Pre-integración ---


        # Cargar datos de la segunda base (con separador ";" y comillas dobles)
        books_data_2 = pd.read_csv('C:/Users/apkar/Desktop/Gonza/FING/S7/CDI/L2/books.csv',
                                   sep=';',
                                   quotechar='"',
                                   encoding='latin-1',
                                   on_bad_lines='skip', # Cambiado a 'skip' para evitar errores fatales
                                   low_memory=False)
        print(f"\nColumnas originales en books_data_2: {books_data_2.columns.tolist()}")


        # Preparar las fuentes para la integración principal
        data_sources = {
            "books_data_1": books_data_1_merged, # Usar la versión fusionada
            "books_data_2": books_data_2
            # books_data_3 ya está incorporada en books_data_1
        }

        # Integrar los datos usando la clase DataIntegrator
        print("\nIniciando integración principal...")
        integrated_data = integrator.integrate_data(data_sources)
        print(f"Registros después de la integración inicial: {len(integrated_data)}")
        print(f"Columnas después de la integración inicial: {integrated_data.columns.tolist()}")


        # Guardar los datos integrados (sin fusión de duplicados)
        output_path = 'integrated_books.csv' # Changed output filename
        integrated_data.to_csv(output_path, # Saving integrated_data directly
                                 index=False,
                                 quotechar='"',
                                 encoding='utf-8') # Guardamos en UTF-8
        print(f"\nDatos integrados (sin fusión de duplicados) guardados en '{output_path}'")

        # Mostrar las primeras filas de los datos finales
        print("\nPrimeras filas de los datos integrados:")
        print(integrated_data.head()) # Showing integrated_data

        # Mostrar información sobre las columnas finales
        print("\nColumnas en el dataset final:")
        print(integrated_data.columns.tolist()) # Showing integrated_data columns
        print(f"\nNúmero total de registros finales: {len(integrated_data)}") # Showing integrated_data length

    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo de datos: {e}")
    except ValueError as e:
        print(f"Error de configuración o datos: {e}")
    except Exception as e:
        print(f"Error inesperado durante la integración: {e}")
        # Imprimir más detalles sobre el error
        import traceback
        print(traceback.format_exc()) 