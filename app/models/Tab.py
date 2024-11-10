from mongoengine import (
    BooleanField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    StringField,
)

# Define the allowed categories
CATEGORIES = [
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


class MutedInfo(EmbeddedDocument):
    muted = BooleanField(required=True)


class Tab(Document):
    userEmail = StringField(required=True)
    id = IntField(required=True, unique=True)
    url = StringField(required=True)
    title = StringField()
    active = BooleanField(default=False)
    timeStamp = FloatField(required=True)
    icon = StringField()
    audible = BooleanField(default=False)
    autoDiscardable = BooleanField(default=True)
    discarded = BooleanField(default=True)
    favIconUrl = StringField()
    groupId = IntField(default=-1)
    height = IntField(default=0)
    highlighted = BooleanField(default=False)
    incognito = BooleanField(default=False)
    index = IntField(default=0)
    lastAccessed = FloatField()
    mutedInfo = EmbeddedDocumentField(MutedInfo)
    pinned = BooleanField(default=False)
    selected = BooleanField(default=False)
    status = StringField(
        choices=["unloaded", "loading", "complete"], default="unloaded"
    )
    width = IntField(default=0)
    windowId = IntField()
    category = StringField(choices=CATEGORIES, default="Other")  # New category field

    meta = {"collection": "tabs"}
