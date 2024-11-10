from threading import Thread

import numpy as np
from dateutil import parser
from flask import Blueprint, jsonify, request
from mongoengine import DateTimeField, Document, IntField, StringField

from app.models import Tab
from app.models.Tab import MutedInfo
from GPTPrompts import categorize_urls

user_routes = Blueprint("user_routes", __name__)

from collections import defaultdict
from datetime import datetime, timedelta
from urllib.parse import urlparse

from bson import ObjectId

from app.models import Tab

user_routes = Blueprint("user_routes", __name__)

import os

import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler


# Function to calculate category durations
def calculate_category_durations(user_id):
    # Define the categories in the desired order
    categories = [
        "Social Media",
        "News",
        "Shopping",
        "Entertainment",
        "Education",
        "Productivity",
        "Communication",
        "Finance",
        "Search Engines",
        "Health & Fitness",
        "Real Estate",
        "Travel & Navigation",
        "Technology & Gadgets",
        "Lifestyle",
        "Government & Legal",
        "Job Search",
        "DIY & Hobbies",
        "Automotive",
        "Gaming",
        "Other",
    ]

    # Query all tabs for the given user_id
    user_tabs = Tab.objects(userEmail=user_id)

    # Group by tabId to find the minimum and maximum timestamps for each tab
    tab_durations = {}
    for tab in user_tabs:
        tab_id = tab.tabId
        # Ensure timeStamp is a datetime object
        if isinstance(tab.timeStamp, str):
            tab.timeStamp = parser.isoparse(tab.timeStamp)

        if tab_id not in tab_durations:
            tab_durations[tab_id] = {
                "min": tab.timeStamp,
                "max": tab.timeStamp,
                "category": tab.category,
            }
        else:
            if tab.timeStamp < tab_durations[tab_id]["min"]:
                tab_durations[tab_id]["min"] = tab.timeStamp
            if tab.timeStamp > tab_durations[tab_id]["max"]:
                tab_durations[tab_id]["max"] = tab.timeStamp

    # Calculate duration for each tab and aggregate by category
    category_durations = {category: timedelta(seconds=0) for category in categories}
    for tab_id, times in tab_durations.items():
        duration = times["max"] - times["min"]
        category = times["category"] or "Other"
        if category in category_durations:
            category_durations[category] += duration

    return category_durations


# Function to vectorize and scale category durations
def vectorize_category_durations(category_durations):
    # Convert durations to seconds for scaling
    category_durations_seconds = np.array(
        [d.total_seconds() for d in category_durations.values()]
    )

    # Perform standard scaling
    scaler = StandardScaler()
    category_durations_scaled = scaler.fit_transform(
        category_durations_seconds.reshape(-1, 1)
    )

    # Convert to a dictionary for return
    categories = list(category_durations.keys())
    category_durations_scaled_dict = dict(
        zip(categories, category_durations_scaled.flatten())
    )

    return category_durations_scaled_dict


# Main function to aggregate user activity
def aggregate_user_activity(user_id):
    category_durations = calculate_category_durations(user_id)

    # Convert timedelta durations to seconds for JSON serialization
    category_durations_json = {
        category: duration.total_seconds()
        for category, duration in category_durations.items()
    }

    return category_durations_json


@user_routes.route("/user_activity_summary/<string:user_id>", methods=["GET"])
def user_activity_summary(user_id):
    try:
        # Define the past week date range
        print(user_id)

        # Aggregate data
        category_durations = aggregate_user_activity(user_id)

        print(category_durations)

        # Prepare response
        response = category_durations

        return jsonify(response), 200

    except Exception as e:
        print(f"Error in user_activity_summary: {e}")
        return (
            jsonify(
                {
                    "error": "An error occurred while processing the request",
                    "details": str(e),
                }
            ),
            500,
        )


# Function to calculate URL durations
def calculate_url_durations(user_id):
    # Query all tabs for the given user_id
    user_tabs = Tab.objects(userEmail=user_id)

    # Group by tabId to find the minimum and maximum timestamps for each URL
    url_durations = {}
    for tab in user_tabs:
        tab_id = tab.tabId
        url = tab.url
        favicon_url = tab.favIconUrl  # Assuming Tab has a field faviconUrl

        # Ensure timeStamp is a datetime object
        if isinstance(tab.timeStamp, str):
            tab.timeStamp = parser.isoparse(tab.timeStamp)

        if tab_id not in url_durations:
            url_durations[tab_id] = {
                "min": tab.timeStamp,
                "max": tab.timeStamp,
                "url": url,
                "favicons": {favicon_url},
            }
        else:
            if tab.timeStamp < url_durations[tab_id]["min"]:
                url_durations[tab_id]["min"] = tab.timeStamp
            if tab.timeStamp > url_durations[tab_id]["max"]:
                url_durations[tab_id]["max"] = tab.timeStamp
            url_durations[tab_id]["favicons"].add(favicon_url)

    # Calculate duration for each URL
    url_duration_dict = defaultdict(
        lambda: {"duration": timedelta(), "favicons": set()}
    )
    for tab_id, times in url_durations.items():
        duration = times["max"] - times["min"]
        url = times["url"]
        url_duration_dict[url]["duration"] += duration
        url_duration_dict[url]["favicons"].update(times["favicons"])

    return url_duration_dict


# Function to calculate domain durations from URL durations
def calculate_domain_durations(url_durations):
    domain_durations = defaultdict(lambda: {"duration": timedelta(), "favicons": set()})

    for url, data in url_durations.items():
        domain = urlparse(url).netloc
        domain_durations[domain]["duration"] += data["duration"]
        domain_durations[domain]["favicons"].update(data["favicons"])

    # Sort by descending duration
    sorted_domain_durations = sorted(
        domain_durations.items(), key=lambda x: x[1]["duration"], reverse=True
    )

    # Convert to list of dictionaries for JSON serialization
    domain_durations_list = [
        {
            "domain": domain,
            "duration": data["duration"].total_seconds(),
            "favUrls": list(data["favicons"]),
        }
        for domain, data in sorted_domain_durations
    ]

    return domain_durations_list


# Function to aggregate user activity for domain durations
def aggregate_user_domain_activity(user_id):
    url_durations = calculate_url_durations(user_id)
    domain_durations = calculate_domain_durations(url_durations)
    return domain_durations


@user_routes.route("/user_domain_summary/<string:user_id>", methods=["GET"])
def user_domain_summary(user_id):
    try:
        # Aggregate data
        domain_durations = aggregate_user_domain_activity(user_id)

        # Prepare response
        response = domain_durations

        return jsonify(response), 200

    except Exception as e:
        print(f"Error in user_domain_summary: {e}")
        return (
            jsonify(
                {
                    "error": "An error occurred while processing the request",
                    "details": str(e),
                }
            ),
            500,
        )


# Domain to Category Mapping Dictionary
domain_category_mapping = {
    "github.com": "Productivity",
    "youtube.com": "Entertainment",
    "docs.google.com": "Productivity",
    "outlook.office365.com": "Communication",
    "netflix.com": "Entertainment",
    "linkedin.com": "Job Search",
    "peopleclick.com": "Job Search",
    "successfactors.eu": "Job Search",
    "celestica.com": "Job Search",
    "myworkdayjobs.com": "Job Search",
    "greenhouse.io": "Job Search",
    "lever.co": "Job Search",
    "seismic.com": "Job Search",
    "trendmicro.wd3.myworkdayjobs.com": "Job Search",
    "tcenergy.wd3.myworkdayjobs.com": "Job Search",
    "serpapi.com": "Productivity",
    "open.spotify.com": "Entertainment",
    "andrew.cmu.edu": "Education",
    "urcourses.uregina.ca": "Education",
    "developer.chrome.com": "Technology & Gadgets",
    "google.com": "Search Engines",
    "store.steampowered.com": "Gaming",
    "localhost": "Other",
    "ui.shadcn.com": "Productivity",
    "chrome://newtab": "Other",
    "mongoosejs.com": "Technology & Gadgets",
    "docs.python.org": "Technology & Gadgets",
    "stackoverflow.com": "Productivity",
    "mongodb.com": "Technology & Gadgets",
    "chrome://extensions": "Other",
}


def categorize_domain(url):
    """
    Categorizes a URL based on its domain by using a predefined domain-to-category mapping.

    Parameters:
    url (str): The URL to categorize.

    Returns:
    str: The category of the URL based on its domain.
    """
    from urllib.parse import urlparse

    # Extract the domain from the URL
    domain = urlparse(url).netloc
    # Remove any subdomains for simplified matching if necessary
    domain_main = ".".join(domain.split(".")[-2:])

    # Return the category based on the main domain or default to 'Other'
    return domain_category_mapping.get(domain_main, "Other")


def categorize_and_store_tabs(tabs_data, user_token, timestamp):
    try:
        # Remove "content" from each tab before categorization
        # for tab in tabs_data:
        #     tab.pop("content", None)
        #     print(tab["url"])

        # print(tabs_data)

        # Categorize tabs
        # categorized_tabs = categorize_urls(tabs_data)
        categorized_tabs = tabs_data
        print(categorized_tabs)

        # Prepare list for bulk insertion
        tab_documents = []

        # Loop through each categorized tab and prepare the document
        for tab_data in categorized_tabs:
            if not isinstance(tab_data, dict):
                print(f"Skipping invalid tab data format: {tab_data}")
                continue

            # Get category from categorized data
            category = tab_data.get("category", "Other")

            # Handle mutedInfo, ensuring it's correctly structured
            muted_info_data = tab_data.get("mutedInfo")
            if isinstance(muted_info_data, list) and len(muted_info_data) > 0:
                muted = muted_info_data[0] if muted_info_data[0] is not None else False
            else:
                muted = False

            # Create the Tab document instance
            tab = Tab(
                userEmail=user_token,
                tabId=tab_data.get("id", 0),
                url=tab_data.get("url", ""),
                title=tab_data.get("title", ""),
                active=tab_data.get("active", False),
                timeStamp=timestamp,
                icon=tab_data.get("favIconUrl", ""),
                audible=tab_data.get("audible", False),
                autoDiscardable=tab_data.get("autoDiscardable", True),
                discarded=tab_data.get("discarded", False),
                favIconUrl=tab_data.get("favIconUrl", ""),
                groupId=tab_data.get("groupId", -1),
                height=tab_data.get("height", 0),
                highlighted=tab_data.get("highlighted", False),
                incognito=tab_data.get("incognito", False),
                index=tab_data.get("index", 0),
                lastAccessed=tab_data.get("lastAccessed", 0),
                mutedInfo=MutedInfo(muted=muted),
                pinned=tab_data.get("pinned", False),
                selected=tab_data.get("selected", False),
                status=tab_data.get("status", "unloaded"),
                width=tab_data.get("width", 0),
                windowId=tab_data.get("windowId", 0),
                category=categorize_domain(
                    tab_data.get("url", ""),
                ),
            )
            tab_documents.append(tab)

        # Perform bulk insert
        if tab_documents:
            Tab.objects.insert(tab_documents)
            print("Bulk insert completed: All tabs categorized and stored.")

    except Exception as e:
        print(f"Error in background task: {e}")


@user_routes.route("/publish_tabs_snapshot", methods=["POST"])
def store_tabs_snapshot():
    try:
        data = request.json
        tabs_data = data.get("tabs", [])
        user_token = data.get("userToken")
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        # print(tabs_data[0].keys())
        # Run the background task in a separate thread
        thread = Thread(
            target=categorize_and_store_tabs, args=(tabs_data, user_token, timestamp)
        )
        thread.start()

        # Immediate acknowledgment response
        return jsonify({"message": "Tabs snapshot is being processed"}), 202

    except Exception as e:
        print(f"Error in store_tabs_snapshot: {e}")
        return (
            jsonify(
                {
                    "error": "An error occurred while processing the request",
                    "details": str(e),
                }
            ),
            500,
        )
    