from mongoengine import Document, ListField, StringField, ValidationError

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


class Urls(Document):
    url = StringField(required=True, unique=True)  # URL should be unique
    rawText = StringField()  # Raw text data associated with the URL
    topic = StringField(
        required=True, choices=CATEGORIES
    )  # Restricted to predefined categories

    meta = {"collection": "urls"}  # Specify the collection name in MongoDB

    # Optional: Custom validation for the topic field
    def clean(self):
        if self.topic not in CATEGORIES:
            raise ValidationError(
                f"Topic must be one of the following categories: {CATEGORIES}"
            )
