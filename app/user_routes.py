from threading import Thread

from flask import Blueprint, jsonify, request

from app.models import Tab
from app.models.Tab import MutedInfo
from GPTPrompts import categorize_urls

user_routes = Blueprint("user_routes", __name__)

from collections import defaultdict
from datetime import datetime, timedelta

from bson import ObjectId

from app.models import Tab

user_routes = Blueprint("user_routes", __name__)


def aggregate_user_activity(user_id, past_week):
    # Initialize structures to store category and daily screen time
    category_time = defaultdict(float)
    daily_screen_time = defaultdict(float)

    # Iterate through each day of the past week
    for day in past_week:
        # Convert start and end times to Unix timestamps
        start_timestamp = day["start"].timestamp()
        end_timestamp = day["end"].timestamp()

        # Query tabs for the specified user and time range
        tabs = Tab.objects(
            userEmail=user_id,
            timeStamp__gte=start_timestamp,
            timeStamp__lt=end_timestamp,
        )

        # Iterate through tabs to compute category and daily time
        for tab in tabs:
            category = tab.category
            default_view_time = (
                10 * 60
            )  # Assume 10 minutes (600 seconds) per tab as an example

            # Aggregate time spent on each category
            category_time[category] += default_view_time

            # Aggregate daily screen time
            daily_screen_time[day["name"]] += default_view_time

    return category_time, daily_screen_time


@user_routes.route("/user_activity_summary/<string:user_id>", methods=["GET"])
def user_activity_summary(user_id):
    try:
        # Define the past week date range
        today = datetime.now()
        past_week = [
            {
                "name": (today - timedelta(days=i)).strftime("%A"),
                "start": (today - timedelta(days=i)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                ),
                "end": (today - timedelta(days=i)).replace(
                    hour=23, minute=59, second=59, microsecond=999999
                ),
            }
            for i in range(7)
        ]

        # Aggregate data
        category_time, daily_screen_time = aggregate_user_activity(user_id, past_week)

        # Prepare response
        response = {
            "category_time": dict(category_time),
            "daily_screen_time": dict(daily_screen_time),
        }

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


# def categorize_and_store_tabs(tabs_data, user_token, timestamp):
#     try:
#         # Directly categorize tabs using the provided function
#         for i, tab in enumerate(tabs_data):
#             del tab["content"]

#         categorized_tabs = categorize_urls(tabs_data)
#         # categorized_tabs = []
#         print(categorized_tabs)

#         # Loop through each categorized tab and store it in MongoDB
#         for i, tab_data in enumerate(categorized_tabs):
#             if not isinstance(tab_data, dict):
#                 print(f"Skipping invalid tab data format: {tab_data}")
#                 continue

#             # Get category from categorized data
#             category = tab_data.get("category", "Other")

#             # Handle mutedInfo, ensuring it's correctly structured
#             muted_info_data = tab_data.get("mutedInfo")
#             if isinstance(muted_info_data, list) and len(muted_info_data) > 0:
#                 muted = muted_info_data[0] if muted_info_data[0] is not None else False
#             else:
#                 muted = False

#             # Save the tab with categorization to the Tab collection
#             tab = Tab(
#                 userEmail=user_token,
#                 tabId=tab_data.get("id", 0),  # Default id to 0 if missing
#                 url=tab_data.get("url", ""),
#                 title=tab_data.get("title", ""),
#                 active=tab_data.get("active", False),
#                 timeStamp=timestamp,
#                 icon=tab_data.get("favIconUrl", ""),
#                 audible=tab_data.get("audible", False),
#                 autoDiscardable=tab_data.get("autoDiscardable", True),
#                 discarded=tab_data.get("discarded", False),
#                 favIconUrl=tab_data.get("favIconUrl", ""),
#                 groupId=tab_data.get("groupId", -1),
#                 height=tab_data.get("height", 0),
#                 highlighted=tab_data.get("highlighted", False),
#                 incognito=tab_data.get("incognito", False),
#                 index=tab_data.get("index", 0),
#                 lastAccessed=tab_data.get("lastAccessed", 0),
#                 mutedInfo=MutedInfo(muted=muted),
#                 pinned=tab_data.get("pinned", False),
#                 selected=tab_data.get("selected", False),
#                 status=tab_data.get("status", "unloaded"),
#                 width=tab_data.get("width", 0),
#                 windowId=tab_data.get("windowId", 0),
#                 category=category,
#             )
#             tab.save()

#         print("Background task completed: All tabs categorized and stored.")
#     except Exception as e:
#         print(f"Error in background task: {e}")

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
    