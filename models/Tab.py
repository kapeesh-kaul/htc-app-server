from mongoengine import (
    BooleanField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    StringField,
)


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

    meta = {"collection": "tabs"}
