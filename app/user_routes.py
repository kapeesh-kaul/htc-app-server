from datetime import datetime

from flask import Blueprint, jsonify, request

from app.models import Tab
from app.models.Tab import MutedInfo

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/publish_tabs_snapshot", methods=["POST"])
def store_tabs_snapshot():
    try:
        data = request.json
        tabs_data = data.get("tabs", [])
        user_token = data.get("userToken")
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        # Loop through each tab and store it in MongoDB
        for tab_data in tabs_data:
            tab = Tab(
                userEmail=user_token,
                id=tab_data.get("id"),
                url=tab_data.get("url"),
                title=tab_data.get("title"),
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
                lastAccessed=tab_data.get("lastAccessed"),
                mutedInfo=MutedInfo(
                    muted=tab_data.get("mutedInfo", {}).get("muted", False)
                ),
                pinned=tab_data.get("pinned", False),
                selected=tab_data.get("selected", False),
                status=tab_data.get("status", "unloaded"),
                width=tab_data.get("width", 0),
                windowId=tab_data.get("windowId"),
            )
            tab.save()

        return jsonify({"message": "Tabs snapshot stored successfully"}), 201

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
