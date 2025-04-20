import pandas as pd
from pymongo import MongoClient

def csv_to_mongodb(file_path, db_name, collection_name):
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = MongoClient('localhost', 27017)
        
        # Create/Get database
        db = client[db_name]
        collection = db[collection_name]
        
        # Load Excel file into DataFrame
        print(f"Reading Excel file: {file_path}")
        df = pd.read_excel(file_path)
        print(f"Number of rows in Excel: {len(df)}")
        
        # Convert DataFrame to dictionary
        data_dict = df.to_dict("records")
        
        # Clear existing data
        collection.delete_many({})
        print("Cleared existing data from collection")
        
        # Insert new data
        result = collection.insert_many(data_dict)
        print(f"Inserted {len(result.inserted_ids)} documents")
        
        # Verify insertion
        count = collection.count_documents({})
        print(f"\nTotal documents in collection: {count}")
        
        # Print first document as verification
        first_doc = collection.find_one()
        print("\nFirst document in MongoDB:")
        print(first_doc)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    file_path = 'oss_dataset_features.xlsx'
    database_name = 'sustainable_brands'
    collection_name = 'brands'
    
    csv_to_mongodb(file_path, database_name, collection_name) 