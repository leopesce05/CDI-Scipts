import pandas as pd

# Configure the files and the functional dependencies to check
# For each file, specify: path, separator, left-hand-side columns (lhs_cols), right-hand-side columns (rhs_cols)
files_config = [
    {
        'path': '../L1/books_data.csv',
        'sep': ',',
        'lhs_cols': ['Title'],        # Example: Title -> Publisher
        'rhs_cols': ['publisher']
    },
    {
        'path': '../L1/Books_rating.csv',
        'sep': ',',
        'lhs_cols': ['User_id', 'Id'], # Example: (User_id, Id) -> Rating
        'rhs_cols': ['Rating']
    },
    # Add more file and functional dependency configurations here
]

# Configure general pandas read_csv options (applied to all files)
# Specific options like 'sep' will be taken from files_config
read_csv_options = {
    'header': 'infer', # Row number(s) to use as the column names
    'encoding': None,  # Encoding (e.g., 'utf-8')
    # Add other general pandas.read_csv options here
}

print("--- Functional Dependency Check ---")

if not files_config:
    print("No file configurations specified.")
else:
    for config in files_config:
        file_path = config.get('path')
        separator = config.get('sep', ',')
        lhs_cols = config.get('lhs_cols')
        rhs_cols = config.get('rhs_cols')

        if not file_path or not lhs_cols or not rhs_cols:
            print(f"Skipping invalid configuration (missing path, lhs_cols, or rhs_cols): {config}")
            continue

        print(f"\n--- Checking File: {file_path} ---")
        print(f"    Dependency: {lhs_cols} -> {rhs_cols}")

        try:
            # Use general options but override separator
            current_read_options = read_csv_options.copy()
            current_read_options['sep'] = separator

            df = pd.read_csv(file_path, **current_read_options)

            # Check if all necessary columns exist
            all_needed_cols = list(set(lhs_cols + rhs_cols))
            if not all(col in df.columns for col in all_needed_cols):
                missing = [col for col in all_needed_cols if col not in df.columns]
                print(f"  Error: Missing required columns: {missing}")
                continue

            # Check for functional dependency violations
            # Group by LHS and count unique RHS combinations for each group
            grouped = df.groupby(lhs_cols)
            violations = []
            for name, group in grouped:
                unique_rhs_count = group[rhs_cols].drop_duplicates().shape[0]
                if unique_rhs_count > 1:
                    # Found a violation for this LHS group
                    # Get the first few violating rows for illustration
                    violating_rows = group[all_needed_cols].drop_duplicates().head()
                    violations.append(violating_rows)


            if not violations:
                print(f"  OK: Functional dependency {lhs_cols} -> {rhs_cols} holds.")
            else:
                print(f"  VIOLATION: Functional dependency {lhs_cols} -> {rhs_cols} is violated.")
                print("    Examples of violations (LHS values with multiple RHS values):")
                # Combine violation examples into one DataFrame for printing
                violations_df = pd.concat(violations, ignore_index=True)
                print(violations_df.to_string(index=False))


        except FileNotFoundError:
            print(f"  Error: File not found {file_path}")
        except Exception as e:
            print(f"  Error: Could not read or process file {file_path}: {e}")

    print("\n------------------------------------") 