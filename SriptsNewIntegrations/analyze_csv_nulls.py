import pandas as pd
import os
from pathlib import Path

def analyze_csv_nulls(csv_path):
    """Analyze null values in a CSV file and return statistics."""
    print(f"\nAnalyzing file: {csv_path}")
    
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            print(f"Successfully read file with {encoding} encoding")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file with {encoding} encoding: {str(e)}")
            continue
    
    if df is None:
        print(f"Could not read file {csv_path} with any of the attempted encodings")
        return
    
    # Get total number of rows
    total_rows = len(df)
    print(f"Total rows: {total_rows:,}")
    
    # Analyze each column
    print("\nColumn Analysis:")
    print("-" * 50)
    print(f"{'Column Name':<30} {'Null Count':<15} {'Null Percentage':<15}")
    print("-" * 50)
    
    for column in df.columns:
        null_count = df[column].isnull().sum()
        null_percentage = (null_count / total_rows) * 100
        print(f"{column:<30} {null_count:<15,} {null_percentage:.2f}%")

def main():
    # Directory containing CSV files
    csv_dir = Path("../../integratedCSVs")
    
    # Get all CSV files in the directory
    csv_files = list(csv_dir.glob("*.csv"))
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    
    # Analyze each CSV file
    for csv_file in csv_files:
        try:
            analyze_csv_nulls(csv_file)
        except Exception as e:
            print(f"Error analyzing file {csv_file}: {str(e)}")
            continue

if __name__ == "__main__":
    main() 