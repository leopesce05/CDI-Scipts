import pandas as pd
from pathlib import Path

def load_csv_with_encoding(file_path):
    """Try to load a CSV file with different encodings"""
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
            print(f"Successfully loaded {file_path} with {encoding} encoding")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error loading {file_path} with {encoding} encoding: {str(e)}")
            continue
    
    raise Exception(f"Could not load {file_path} with any of the attempted encodings")

def verify_books():
    """Verify that all books in ratings.csv exist in books.csv"""
    print("Loading files...")
    
    try:
        books_df = load_csv_with_encoding("../../integratedCSVs/books.csv")
        ratings_df = load_csv_with_encoding("../../integratedCSVs/ratings.csv")
    except Exception as e:
        print(f"Error loading files: {str(e)}")
        return
    
    # Get unique book IDs from both files
    books_ids = set(books_df['Id'].unique())
    ratings_book_ids = set(ratings_df['Id'].unique())
    
    # Find books in ratings that don't exist in books
    missing_books = ratings_book_ids - books_ids
    
    # Print statistics
    print("\nVerification Results:")
    print("-" * 50)
    print(f"Total unique books in books.csv: {len(books_ids):,}")
    print(f"Total unique books in ratings.csv: {len(ratings_book_ids):,}")
    print(f"Number of books in ratings not found in books: {len(missing_books):,}")
    
    if missing_books:
        print("\nMissing books details:")
        print("-" * 50)
        # Get sample of missing books with their ratings count
        missing_books_sample = list(missing_books)[:10]  # Show first 10 for example
        for book_id in missing_books_sample:
            ratings_count = len(ratings_df[ratings_df['Id'] == book_id])
            print(f"Book ID: {book_id} - Appears in {ratings_count:,} ratings")
        
        if len(missing_books) > 10:
            print(f"\n... and {len(missing_books) - 10} more missing books")
        
        # Save missing books to a CSV file
        missing_books_df = ratings_df[ratings_df['Id'].isin(missing_books)]
        missing_books_df.to_csv('missing_books_in_ratings.csv', index=False)
        print("\nDetails of missing books have been saved to 'missing_books_in_ratings.csv'")
    else:
        print("\nAll books in ratings.csv exist in books.csv!")

if __name__ == "__main__":
    verify_books() 