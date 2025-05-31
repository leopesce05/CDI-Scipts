import pandas as pd
import os
from pathlib import Path

def analyze_csv_nulls(csv_path):
    """Analyze null values and data types in a CSV file and return statistics."""
    print(f"\nAnalyzing file: {csv_path}")
    
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=encoding, low_memory=False)
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
    print("-" * 100)
    print(f"{'Column Name':<30} {'Data Type':<15} {'Null Count':<15} {'Null %':<10} {'Unique Values':<15} {'Sample Values'}")
    print("-" * 100)
    
    for column in df.columns:
        # Basic statistics
        null_count = df[column].isnull().sum()
        null_percentage = (null_count / total_rows) * 100
        data_type = str(df[column].dtype)
        unique_count = df[column].nunique()
        
        # Get sample values (non-null)
        sample_values = df[column].dropna().head(3).tolist()
        sample_str = str(sample_values)[:50] + "..." if len(str(sample_values)) > 50 else str(sample_values)
        
        # Print column analysis
        print(f"{column:<30} {data_type:<15} {null_count:<15,} {null_percentage:>6.2f}% {unique_count:<15,} {sample_str}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("-" * 50)
    print(f"Total Columns: {len(df.columns)}")
    print(f"Total Rows: {total_rows:,}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Print columns with high null percentage
    high_null_cols = [col for col in df.columns if df[col].isnull().mean() > 0.5]
    if high_null_cols:
        print("\nColumns with more than 50% null values:")
        for col in high_null_cols:
            null_percentage = (df[col].isnull().sum() / total_rows) * 100
            print(f"- {col}: {null_percentage:.2f}% null")

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