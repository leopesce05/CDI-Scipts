import pandas as pd
from datetime import datetime
import os

def verify_book_ratings():
    try:
        # Read the CSV files with different encodings
        try:
            books_df = pd.read_csv('../../integratedCSVs/books.csv', encoding='utf-8')
        except UnicodeDecodeError:
            books_df = pd.read_csv('../../integratedCSVs/books.csv', encoding='latin1')
            
        try:
            ratings_df = pd.read_csv('../../integratedCSVs/ratings.csv', encoding='utf-8')
        except UnicodeDecodeError:
            ratings_df = pd.read_csv('../../integratedCSVs/ratings.csv', encoding='latin1')
        
        # Calculate average ratings from ratings.csv
        calculated_ratings = ratings_df.groupby('Id').agg({
            'review/score': ['mean', 'count']
        }).reset_index()
        
        # Rename columns for clarity
        calculated_ratings.columns = ['Id', 'calculated_avg_rating', 'rating_count']
        
        # Prepare books data
        books_data = books_df[['Id', 'ratingsCount']].copy()
        books_data['stored_avg_rating'] = books_df['ratingsCount']  # Asumiendo que ratingsCount es el promedio
        
        # Merge the data
        merged_df = pd.merge(
            books_data,
            calculated_ratings,
            on='Id',
            how='outer'
        )
        
        # Calculate differences
        merged_df['rating_difference'] = abs(merged_df['stored_avg_rating'] - merged_df['calculated_avg_rating'])
        merged_df['count_difference'] = abs(merged_df['ratingsCount'] - merged_df['rating_count'])
        
        # Filter for discrepancies
        discrepancies = merged_df[
            (merged_df['rating_difference'] > 0.01) |  # Allow small floating point differences
            (merged_df['count_difference'] > 0)
        ]
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"rating_verification_report_{timestamp}.csv"
        discrepancies.to_csv(report_filename, index=False, encoding='utf-8')
        
        print(f"\nVerification Report:")
        print(f"Total books checked: {len(merged_df)}")
        print(f"Books with discrepancies: {len(discrepancies)}")
        print(f"Report saved to: {report_filename}")
        
        if len(discrepancies) > 0:
            print("\nDetailed Analysis of Discrepancies:")
            print("\n1. Rating Differences:")
            print(f"   - Average difference: {discrepancies['rating_difference'].mean():.2f}")
            print(f"   - Maximum difference: {discrepancies['rating_difference'].max():.2f}")
            print(f"   - Minimum difference: {discrepancies['rating_difference'].min():.2f}")
            
            print("\n2. Count Differences:")
            print(f"   - Average difference: {discrepancies['count_difference'].mean():.2f}")
            print(f"   - Maximum difference: {discrepancies['count_difference'].max():.2f}")
            print(f"   - Minimum difference: {discrepancies['count_difference'].min():.2f}")
            
            print("\nSample of discrepancies (first 5):")
            sample = discrepancies[['Id', 'stored_avg_rating', 'calculated_avg_rating', 'ratingsCount', 'rating_count', 'rating_difference', 'count_difference']].head()
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            print(sample)
            
            # Additional analysis
            print("\n3. Books with highest rating differences:")
            top_rating_diff = discrepancies.nlargest(5, 'rating_difference')
            print(top_rating_diff[['Id', 'stored_avg_rating', 'calculated_avg_rating', 'rating_difference']])
            
            print("\n4. Books with highest count differences:")
            top_count_diff = discrepancies.nlargest(5, 'count_difference')
            print(top_count_diff[['Id', 'ratingsCount', 'rating_count', 'count_difference']])
        
    except Exception as e:
        print(f"Error processing files: {e}")
        print("Trying alternative encodings...")
        try:
            # Try with different encodings
            books_df = pd.read_csv('../../integratedCSVs/books.csv', encoding='cp1252')
            ratings_df = pd.read_csv('../../integratedCSVs/ratings.csv', encoding='cp1252')
            print("Successfully read files with cp1252 encoding")
        except Exception as e2:
            print(f"Failed with cp1252 encoding: {e2}")

if __name__ == "__main__":
    verify_book_ratings() 