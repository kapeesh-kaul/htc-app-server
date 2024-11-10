from pymongo import MongoClient
import pandas as pd
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

def vectorize(df: pd.DataFrame, userEmail: str) -> pd.Series:
    # Convert the 'timeStamp' column to datetime
    df = df[df['userEmail'] == userEmail]
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])

    # Calculate the duration each tab was open
    tab_durations = df.groupby('tabId')['timeStamp'].agg(['min', 'max'])
    tab_durations['duration'] = tab_durations['max'] - tab_durations['min']

    # Merge tab_durations with the original DataFrame to get the category information
    merged_df = tab_durations.merge(df[['tabId', 'category']], left_index=True, right_on='tabId')

    # Group by category and sum the durations
    category_durations = merged_df.groupby('category')['duration'].sum()
    # Define the fixed category order
    categories = [
        "Social Media", "News", "Shopping", "Entertainment", "Education", 
        "Productivity", "Communication", "Finance", "Search Engines", 
        "Health & Fitness", "Real Estate", "Travel & Navigation", 
        "Technology & Gadgets", "Lifestyle", "Government & Legal", 
        "Job Search", "DIY & Hobbies", "Automotive", "Gaming", "Other"
    ]

    # Initialize a Series with zeros for all categories
    category_durations = pd.Series(pd.to_timedelta(0, unit='s'), index=categories)

    # Update the Series with the actual durations
    actual_durations = merged_df.groupby('category')['duration'].sum()
    for category, duration in actual_durations.items():
        if category in category_durations:
            category_durations[category] = duration

    # Convert the duration to total seconds for scaling
    category_durations_seconds = category_durations.dt.total_seconds()

    # Perform standard scaling
    scaler = StandardScaler()
    category_durations_scaled = scaler.fit_transform(category_durations_seconds.values.reshape(-1, 1))

    # Convert the scaled values back to a pandas Series
    category_durations_scaled_series = pd.Series(category_durations_scaled.flatten(), index=category_durations.index)

    return category_durations_scaled_series.values




if __name__ == "__main__":
    
    # Connect to MongoDB
    client = MongoClient(
        os.getenv("MONGO_URI")
    )  # replace with your MongoDB URI

    from create_db import create_db

    test_df = create_db(client) # Load the test DataFrame

    print(vectorize(test_df, test_df['userEmail'].iloc[0]))