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

def verify_users():
    """Verify that all users in ratings.csv exist in users.csv"""
    print("Loading files...")
    
    try:
        users_df = load_csv_with_encoding("../../integratedCSVs/users.csv")
        ratings_df = load_csv_with_encoding("../../integratedCSVs/ratings.csv")
    except Exception as e:
        print(f"Error loading files: {str(e)}")
        return
    
    # Get unique user IDs from both files
    users_ids = set(users_df['User_id'].unique())
    ratings_user_ids = set(ratings_df['User_id'].unique())
    
    # Find users in ratings that don't exist in users
    missing_users = ratings_user_ids - users_ids
    
    # Print statistics
    print("\nVerification Results:")
    print("-" * 50)
    print(f"Total unique users in users.csv: {len(users_ids):,}")
    print(f"Total unique users in ratings.csv: {len(ratings_user_ids):,}")
    print(f"Number of users in ratings not found in users: {len(missing_users):,}")
    
    if missing_users:
        print("\nMissing users details:")
        print("-" * 50)
        # Get sample of missing users with their ratings count
        missing_users_sample = list(missing_users)[:10]  # Show first 10 for example
        for user_id in missing_users_sample:
            ratings_count = len(ratings_df[ratings_df['User_id'] == user_id])
            print(f"User ID: {user_id} - Appears in {ratings_count:,} ratings")
        
        if len(missing_users) > 10:
            print(f"\n... and {len(missing_users) - 10} more missing users")
        
        # Save missing users to a CSV file
        missing_users_df = ratings_df[ratings_df['User_id'].isin(missing_users)]
        missing_users_df.to_csv('missing_users_in_ratings.csv', index=False)
        print("\nDetails of missing users have been saved to 'missing_users_in_ratings.csv'")
    else:
        print("\nAll users in ratings.csv exist in users.csv!")

if __name__ == "__main__":
    verify_users() 