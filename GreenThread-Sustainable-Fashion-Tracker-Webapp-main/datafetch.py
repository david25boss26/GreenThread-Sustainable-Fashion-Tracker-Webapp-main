import pandas as pd
from pymongo import MongoClient

def csv_to_mongodb(file_path, db_name, collection_name):
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = MongoClient('localhost', 27017)
        
        # Print available databases
        print("Available databases:", client.list_database_names())
        
        db = client[db_name]
        collection = db[collection_name]
        
        # Print available collections
        print(f"Collections in {db_name}:", db.list_collection_names())

        # Load Excel file into DataFrame
        print(f"Reading Excel file: {file_path}")
        data = pd.read_excel(file_path)
        print(f"Number of rows in Excel: {len(data)}")
        
        # Print first few rows of data
        print("\nFirst few rows of Excel data:")
        print(data.head())

        # Convert DataFrame to dictionary and insert into MongoDB
        data_dict = data.to_dict("records")
        
        # Clear existing data (optional)
        collection.delete_many({})
        
        # Insert new data
        result = collection.insert_many(data_dict)
        
        # Verify insertion
        count = collection.count_documents({})
        print(f"\nSuccessfully inserted {count} documents")
        
        # Print first document as verification
        first_doc = collection.find_one()
        print("\nFirst document in MongoDB:")
        print(first_doc)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Update these values with your actual file path and database details
    file_path = 'oss_dataset_features.xlsx'  # Your Excel file path
    database_name = 'your_database'         # Your database name
    collection_name = 'your_collection'     # Your collection name
    
    csv_to_mongodb(file_path, database_name, collection_name)