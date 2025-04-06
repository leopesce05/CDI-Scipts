import pandas as pd
import os
import sys

# --- Función Auxiliar para Leer CSV ---
def _read_and_validate_csv(file_path, col_name, separator, encoding='latin-1'):
    """Lee un CSV, valida la columna y maneja errores básicos."""
    filename = os.path.basename(file_path)
    print(f"Leyendo {filename} (Col: '{col_name}', Sep: '{separator}')...")
    try:
        df = pd.read_csv(
            file_path,
            sep=separator,
            encoding=encoding,
            on_bad_lines='warn',
            low_memory=False,
        )
        print(f" > {len(df)} filas leídas.")
        if col_name not in df.columns:
            print(f"Error: La columna '{col_name}' no existe en {filename}.")
            return None # Retorna None si la columna no existe
        return df # Retorna el DataFrame si todo está bien
    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error al leer archivo {filename}: {e}")
        return None
# --- Fin Función Auxiliar ---

def check_foreign_key(
    fk_file_path, fk_col_name,
    pk_file_path, pk_col_name,
    separator_fk, separator_pk,
    encoding='latin-1'
):
    fk_filename = os.path.basename(fk_file_path)
    pk_filename = os.path.basename(pk_file_path)

    print(f"\n--- Iniciando Verificación de FK ---")
    print(f"Tabla FK: '{fk_filename}' (Columna: '{fk_col_name}')")
    print(f"Tabla PK: '{pk_filename}' (Columna: '{pk_col_name}')")

    # --- Usar función auxiliar para leer ---
    df_fk = _read_and_validate_csv(fk_file_path, fk_col_name, separator_fk, encoding)
    if df_fk is None: return # Salir si hubo error en la lectura FK

    df_pk = _read_and_validate_csv(pk_file_path, pk_col_name, separator_pk, encoding)
    if df_pk is None: return # Salir si hubo error en la lectura PK
    # ---------------------------------------

    fk_values = df_fk[fk_col_name]
    pk_values = df_pk[pk_col_name]

    pk_null_count = pk_values.isnull().sum()
    if pk_null_count > 0:
        print(f"¡Advertencia! La columna PK '{pk_col_name}' en '{pk_filename}' contiene {pk_null_count} valores nulos.")

    valid_pks = set(pk_values.dropna())
    if not valid_pks:
         print(f"Error: No se encontraron valores PK válidos en '{pk_filename}' columna '{pk_col_name}'. No se puede verificar FK.")
         return
    print(f" > {len(valid_pks)} valores únicos de PK encontrados para la verificación.")

    fk_original_count = len(fk_values)
    fk_null_count = fk_values.isnull().sum()
    fk_to_check = fk_values.dropna()
    num_fk_to_check = len(fk_to_check)

    print(f"Total de valores FK en '{fk_col_name}': {fk_original_count}")
    if fk_null_count > 0:
        print(f" > Se encontraron {fk_null_count} valores FK nulos (serán ignorados).")
    print(f" > Verificando {num_fk_to_check} valores FK no nulos...")

    if num_fk_to_check == 0:
        print("No hay valores FK no nulos para verificar.")
        print("--- Verificación de FK Completada (Sin datos para verificar) ---")
        return

    is_valid = fk_to_check.isin(valid_pks)
    orphan_fks = fk_to_check[~is_valid]
    num_orphans = len(orphan_fks)

    if num_orphans == 0:
        print("\n¡Éxito! Todos los valores FK no nulos existen en la columna PK referenciada.")
    else:
        print(f"\n¡Error de Integridad! Se encontraron {num_orphans} valores FK 'huérfanos'.")
        unique_orphans = orphan_fks.unique()
        max_examples = 10
        print(f"   > Primeros {min(len(unique_orphans), max_examples)} valores huérfanos únicos encontrados:")
        for i, orphan in enumerate(unique_orphans):
            if i >= max_examples: break
            print(f"     - {orphan}")

    print("--- Verificación de FK Completada ---")


# --- Bloque Principal (sin cambios significativos) ---
if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)

    # --- === CONFIGURACIÓN === ---
    FK_FILE_RELATIVE = 'L1/Books_rating.csv'
    FK_COLUMN = 'Title'
    PK_FILE_RELATIVE = 'L1/books_data.csv'
    PK_COLUMN = 'Title'

    # FK_FILE_RELATIVE = 'L1/Books_rating.csv'
    # FK_COLUMN = 'ISBN'
    # PK_FILE_RELATIVE = 'L1/books_data.csv'
    # PK_COLUMN = 'ISBN'

    RUN_FOREIGN_KEY_CHECK = True
    # --- === FIN CONFIGURACIÓN === ---

    if RUN_FOREIGN_KEY_CHECK:
        fk_file_abs = os.path.join(project_root, FK_FILE_RELATIVE)
        pk_file_abs = os.path.join(project_root, PK_FILE_RELATIVE)

        sep_fk = ';' if 'L2/' in FK_FILE_RELATIVE.replace('\\', '/') else ','
        sep_pk = ';' if 'L2/' in PK_FILE_RELATIVE.replace('\\', '/') else ','

        try:
             check_foreign_key(
                 fk_file_abs, FK_COLUMN,
                 pk_file_abs, PK_COLUMN,
                 sep_fk, sep_pk
             )
        except Exception as e:
             print(f"\nError inesperado durante la ejecución de la verificación: {e}")
    else:
        print("Verificación de clave foránea desactivada (RUN_FOREIGN_KEY_CHECK = False).")

    print(f"\n{'='*10} Script CheckFK Finalizado {'='*10}") 