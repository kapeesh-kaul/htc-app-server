
# HTC App Server API Guide

This repository provides information on the API endpoints available for moderation, pronoun processing, chat analysis, and URL categorization.

## API Endpoints

### 1. Community Guidelines Verification Endpoint

- **URL:** `/openai/verify_community_guidelines`
- **Method:** POST
- **Content-Type:** application/json

**Input Format**

```json
{
    "text": [
        "This is the first message.",
        "This message might contain inappropriate content."
    ]
}
```

**Output Format**

```json
{
    "analysis_timestamp": "2023-10-21T10:10:00Z",
    "total_messages_analyzed": 2,
    "assessments": {
        "1": {
            "message_id": "1",
            "content": "This is the first message.",
            "assessment": {
                "is_inappropriate": false,
                "flags": [],
                "feedback": "This message complies with community guidelines."
            },
            "timestamp": "2023-10-21T10:00:00Z"
        },
        "2": {
            "message_id": "2",
            "content": "This message might contain inappropriate content.",
            "assessment": {
                "is_inappropriate": true,
                "flags": ["Sensitive Topics"],
                "feedback": "This message discusses sensitive topics."
            },
            "timestamp": "2023-10-21T10:05:00Z"
        }
    }
}
```

**JavaScript Example**

```javascript
const data = {
    text: [
        "This is the first message.",
        "This message might contain inappropriate content."
    ]
};

fetch("http://https://htc-app-server.vercel.app/openai/verify_community_guidelines", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log("Response:", data))
.catch(error => console.error("Error:", error));
```

### 2. Pronoun Processing Endpoint

- **URL:** `/openai/process_pronouns`
- **Method:** POST

**Input Format**

```json
{
    "message_input": {
        "messageId": "123",
        "content": "They are working on their project.",
        "timestamp": "2023-10-21T10:00:00Z",
        "mentions": {
            "user123": {
                "startIndex": 0,
                "endIndex": 4
            }
        }
    },
    "users": {
        "user123": {
            "userId": "user123",
            "username": "Alex",
            "pronouns": {
                "subject": "they",
                "object": "them",
                "possessive": "their",
                "reflexive": "themselves"
            }
        }
    }
}
```

**Output Format**

```json
{
    "original": {
        "content": "They are working on their project.",
        "mentions": ["user123"]
    },
    "processed": {
        "content": "Alex is working on Alex's project.",
        "replacements": [
            {
                "original": "They",
                "replaced": "Alex",
                "position": 0,
                "userId": "user123"
            },
            {
                "original": "their",
                "replaced": "Alex's",
                "position": 21,
                "userId": "user123"
            }
        ]
    },
    "users": {
        "user123": {
            "userId": "user123",
            "username": "Alex",
            "pronouns": {
                "subject": "they",
                "object": "them",
                "possessive": "their",
                "reflexive": "themselves"
            }
        }
    },
    "timestamp": "2023-10-21T10:00:00Z"
}
```

**JavaScript Example**

```javascript
const data = {
    message_input: {
        messageId: "123",
        content: "They are working on their project.",
        timestamp: "2023-10-21T10:00:00Z",
        mentions: {
            "user123": {
                startIndex: 0,
                endIndex: 4
            }
        }
    },
    users: {
        user123: {
            userId: "user123",
            username: "Alex",
            pronouns: {
                subject: "they",
                object: "them",
                possessive: "their",
                reflexive: "themselves"
            }
        }
    }
};

fetch("http://https://htc-app-server.vercel.app/openai/process_pronouns", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log("Response:", data))
.catch(error => console.error("Error:", error));
```

### 3. Chat Moderation Endpoint

- **URL:** `/openai/moderate_chat`
- **Method:** POST

... (and so on for each endpoint)

For the complete code, download the file.

---

