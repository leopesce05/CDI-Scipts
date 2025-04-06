import pandas as pd
import os
import sys
import io
import contextlib
import re

def analyze_csv_file(target_file_path, source_dir_name, bad_rows_dir, project_root_dir):
    target_filename = os.path.basename(target_file_path)
    print(f"\n=== Analizando {target_filename} (desde {source_dir_name}) ===")

    if not os.path.exists(target_file_path):
        print(f"Error: El archivo {target_file_path} no fue encontrado.")
        return

    if not target_filename.lower().endswith('.csv'):
        print(f"Info: El archivo '{target_filename}' no parece ser un CSV, omitiendo análisis detallado.")
        return

    print(f"Leyendo {target_filename}...")
    total_lines_count = 0
    bad_line_numbers = set()
    df = pd.DataFrame()
    skipped_lines_reported = -1

    try:
        try:
            with open(target_file_path, 'r', encoding='latin-1') as f:
                total_lines_count = sum(1 for _ in f)
        except Exception as e:
            print(f"Advertencia: No se pudo contar el total de líneas original: {e}")
            total_lines_count = 0

        read_params = {
            'encoding': 'latin-1',
            'on_bad_lines': 'warn',
            'low_memory': False
        }

        separator_used = ','
        if source_dir_name == 'L1':
            read_params['sep'] = ','
            separator_used = ','
            print("Usando separador: ',' (coma)")
        elif source_dir_name == 'L2':
            read_params['sep'] = ';'
            separator_used = ';'
            print("Usando separador: ';'")
        else:
            read_params['sep'] = ','
            separator_used = ','
            print(f"Advertencia: Directorio '{source_dir_name}' no es L1 ni L2, usando separador por defecto (',').")

        captured_stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(captured_stderr):
                df = pd.read_csv(target_file_path, **read_params)
        finally:
            warnings_text = captured_stderr.getvalue()
            if warnings_text:
                line_num_pattern = r"(?:Skipping|Error tokenizing data|C error).*[Ll]ine (\d+)"
                found_lines = re.findall(line_num_pattern, warnings_text)
                bad_line_numbers = set(map(int, found_lines))


        if total_lines_count > 0:
            calculated_skipped = total_lines_count - len(df) - 1
            skipped_lines_reported = max(0, calculated_skipped)
        elif total_lines_count == 0:
            skipped_lines_reported = -1
        else:
            skipped_lines_reported = 0

    except pd.errors.EmptyDataError:
        print(f"Error: El archivo CSV {target_filename} está vacío.")
        skipped_lines_reported = 0
    except Exception as e:
        print(f"Error al leer el archivo CSV {target_filename} con separador '{read_params.get('sep', 'default')}': {e}")
        return

    if bad_line_numbers:
        bad_rows_filename = os.path.join(bad_rows_dir, f"{os.path.splitext(target_filename)[0]}_bad.csv")
        print(f"Guardando {len(bad_line_numbers)} líneas con errores específicos")
        try:
            with open(target_file_path, 'r', encoding='latin-1') as infile, \
                open(bad_rows_filename, 'w', encoding='latin-1') as outfile:
                try:
                    header = next(infile)
                    outfile.write(header)
                    bad_lines_to_check = {num -1 for num in bad_line_numbers}
                    current_line_num_in_loop = 1
                except StopIteration:
                    print("Advertencia: Archivo original vacío o sin cabecera al intentar guardar filas erróneas.")
                    bad_lines_to_check = set()

                for line in infile:
                    if current_line_num_in_loop in bad_lines_to_check:
                        outfile.write(line)
                    current_line_num_in_loop += 1
        except Exception as e:
            print(f"Error al escribir el archivo de filas incorrectas {bad_rows_filename}: {e}")

    total_rows = len(df)
    if df.empty and total_lines_count <= 1:
        print("Info: El archivo parece contener solo la cabecera o está vacío.")

    print(f"\nTotal de filas leídas: {total_rows:,}")

    if skipped_lines_reported >= 0:
        print(f"Número de líneas omitidas: {skipped_lines_reported:,}")
    else:
        print("No se pudo determinar el número de líneas omitidas (falló el conteo inicial de líneas).")

    if not df.empty:
        print("Columnas y tipos de datos:")
        print(df.dtypes)
        print("\n--- Análisis de Valores Nulos (NaN) ---")
        null_counts = df.isnull().sum()
        if null_counts.sum() == 0:
            print("No se encontraron valores nulos (NaN).")
        else:
            print("Valores nulos (NaN) por columna:")
            null_summary = null_counts[null_counts > 0]
            for col, count in null_summary.items():
                percentage = (count / total_rows) * 100 if total_rows > 0 else 0
                print(f"- {col}: {count:,} ({percentage:.2f}%)")
    else:
        print("DataFrame vacío, no se realiza análisis de nulos.")


if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)

    bad_rows_directory = os.path.join(project_root, 'bad_rows')
    try:
        os.makedirs(bad_rows_directory, exist_ok=True)
        print(f"Directorio para filas incorrectas: '{bad_rows_directory}'")
    except OSError as e:
        print(f"Error al crear el directorio '{bad_rows_directory}': {e}")
        sys.exit(1)

    files_to_analyze = [
        'L2/books.csv',
        'L2/ratings.csv',
        'L2/users.csv',
        'L1/Books_rating.csv',
        'L1/books_data.csv',

    ]

    print(f"Iniciando análisis para {len(files_to_analyze)} archivo(s) especificado(s)...")

    for relative_path in files_to_analyze:
        full_path = os.path.join(project_root, relative_path)
        source_dir_name = os.path.basename(os.path.dirname(full_path))
        if not source_dir_name:
            source_dir_name = "[RAÍZ]"

        try:
            analyze_csv_file(full_path, source_dir_name, bad_rows_directory, project_root)
        except Exception as e:
            print(f"\nERROR INESPERADO al procesar la ruta {relative_path}: {e}")
            print("Continuando con el siguiente archivo...")

    print(f"\n{'='*10} ANÁLISIS COMPLETADO PARA ARCHIVOS ESPECIFICADOS {'='*10}") 