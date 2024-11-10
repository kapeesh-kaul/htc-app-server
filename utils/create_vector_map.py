import pandas as pd
from typing import Dict, Any
from vectorize import vectorize
from create_db import create_db
from pymongo import MongoClient
import os

def create_vector_map(client : MongoClient) -> Dict[str, Any]:
    db = create_db(client) 
    
    vector_map = {}
    for user in db.userEmail.unique():
        vector_map[user] = vectorize(db, user)
    return vector_map

if __name__ == "__main__":
    client = MongoClient(
        os.getenv("MONGO_URI")
    )
    vector_map = create_vector_map(client)
    print(vector_map)