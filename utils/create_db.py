from pymongo import MongoClient
import pandas as pd

def create_db(client : MongoClient) -> pd.DataFrame:
    test_db = client["test"]
    test_collection = test_db["tabs"]

    # Query all data from the test collection
    test_cursor = test_collection.find()

    # Convert cursor to list of dictionaries, then to DataFrame
    test_df = pd.DataFrame(list(test_cursor))

    # Drop MongoDB's default '_id' field if not needed
    if '_id' in test_df.columns:
        test_df = test_df.drop('_id', axis=1)
    
    return test_df