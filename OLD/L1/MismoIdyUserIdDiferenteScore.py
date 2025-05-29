import pandas as pd

files_config = [
    {
        'path': '../L1/Books_rating.csv',
        'columns': ['Id', 'User_id'],
        'sep': ','
    },
]

read_csv_options = {
    'header': 'infer',
    'encoding': None,
}

if not files_config:
    print("No file configurations specified.")
else:
    for config in files_config:
        file_path = config.get('path')
        columns_to_check = config.get('columns')
        separator = config.get('sep', ',')

        if not file_path or not columns_to_check:
            print(f"Skipping invalid configuration: {config}")
            continue

        print(f"--- Checking file: {file_path} ---")

        try:
            current_read_options = read_csv_options.copy()
            current_read_options['sep'] = separator

            df = pd.read_csv(file_path, **current_read_options)

            if not all(col in df.columns for col in columns_to_check):
                print(f"  Error: One or more columns {columns_to_check} not found in this CSV.")
                missing_cols = [col for col in columns_to_check if col not in df.columns]
                print(f"  Missing columns: {missing_cols}")
                continue

            empty_mask = df[columns_to_check].apply(lambda x: x.isna() | (x.astype(str).str.strip() == ''))
            empty_rows = empty_mask.any(axis=1)
            
            ignored_count = empty_rows.sum()
            if ignored_count > 0:
                print(f"  Note: Ignoring {ignored_count} rows where one or more specified columns are empty")
            
            non_empty_df = df[~empty_rows]
            duplicates = non_empty_df[non_empty_df.duplicated(subset=columns_to_check, keep=False)]

            if duplicates.empty:
                print(f"  OK: The combination of columns {columns_to_check} is unique in this file (ignoring empty values).")
            else:
                print(f"  DUPLICATES FOUND based on columns {columns_to_check} (ignoring empty values):")
                display_columns = ['Id', 'User_id']
                if 'review/score' in df.columns:
                    display_columns.append('review/score')

                grouped = duplicates.groupby(['Id', 'User_id'])
                inconsistent_scores = []
                consistent_scores = []
                
                for (id_val, user_id), group in grouped:
                    unique_scores = group['review/score'].unique()
                    if len(unique_scores) > 1:
                        inconsistent_scores.append((id_val, user_id, unique_scores))
                    else:
                        consistent_scores.append((id_val, user_id, unique_scores[0]))
                
                if inconsistent_scores:
                    print("\n  INCONSISTENT SCORES FOUND:")
                    print("  (Same Id and User_id but different scores)")
                    for id_val, user_id, scores in inconsistent_scores[:20]:
                        print(f"  Id: {id_val}, User_id: {user_id}, Different scores: {scores}")
                    if len(inconsistent_scores) > 20:
                        print(f"  ... and {len(inconsistent_scores) - 20} more cases with inconsistent scores")
                
                if consistent_scores:
                    print("\n  CONSISTENT SCORES:")
                    print("  (Same Id and User_id with same score)")
                    for id_val, user_id, score in consistent_scores[:20]:
                        print(f"  Id: {id_val}, User_id: {user_id}, Score: {score}")
                    if len(consistent_scores) > 20:
                        print(f"  ... and {len(consistent_scores) - 20} more cases with consistent scores")
                
                print(f"\n  Summary:")
                print(f"  - Total duplicate pairs: {len(grouped)}")
                print(f"  - Pairs with inconsistent scores: {len(inconsistent_scores)}")
                print(f"  - Pairs with consistent scores: {len(consistent_scores)}")

        except FileNotFoundError:
            print(f"  Error: File not found {file_path}")
        except Exception as e:
            print(f"  Error: Could not read or process file {file_path}: {e}")
        print("-------------------------") 