import pandas as pd

# Configure the files and their specific settings
files_config = [
    {
        'path': '../L1/books_data.csv',
        'columns': ['Title'],  # Columns to check for uniqueness in this file
        'sep': ','       # Separator for this file
    },
    {
        'path': '../L1/Books_rating.csv',
        'columns': ['Id', 'User_id'], # Different columns and separator
        'sep': ','
    },
    # Add more file configurations here
]

# Configure general pandas read_csv options (applied to all files)
# Specific options like 'sep' will be taken from files_config
read_csv_options = {
    'header': 'infer', # Row number(s) to use as the column names
    'encoding': None, # Encoding to use for UTF when reading/writing (e.g., 'utf-8')
    # Add other general pandas.read_csv options here
}

if not files_config:
    print("No file configurations specified.")
else:
    for config in files_config:
        file_path = config.get('path')
        columns_to_check = config.get('columns')
        separator = config.get('sep', ',') # Default to comma if not specified

        if not file_path or not columns_to_check:
            print(f"Skipping invalid configuration: {config}")
            continue

        print(f"--- Checking file: {file_path} ---")

        try:
            # Use general options but override separator
            current_read_options = read_csv_options.copy()
            current_read_options['sep'] = separator

            df = pd.read_csv(file_path, **current_read_options)

            if not all(col in df.columns for col in columns_to_check):
                print(f"  Error: One or more columns {columns_to_check} not found in this CSV.")
                missing_cols = [col for col in columns_to_check if col not in df.columns]
                print(f"  Missing columns: {missing_cols}")
                continue

            duplicates = df[df.duplicated(subset=columns_to_check, keep=False)]

            if duplicates.empty:
                print(f"  OK: The combination of columns {columns_to_check} is unique in this file.")
            else:
                print(f"  DUPLICATES FOUND based on columns {columns_to_check}:")
                # Display limited info to avoid large output
                print(duplicates.head().to_string())
                if len(duplicates) > 5:
                    print(f"  ... and {len(duplicates) - 5} more duplicate rows.")

        except FileNotFoundError:
            print(f"  Error: File not found {file_path}")
        except Exception as e:
            print(f"  Error: Could not read or process file {file_path}: {e}")
        print("-------------------------\
") # Separator line
