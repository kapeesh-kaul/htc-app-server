import json
import os
from typing import Any, Dict, List

from openai import OpenAI

# Set up your OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")


def parse_categorization(prompt: str, content: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content.strip()


def categorize_urls(urls: List[Dict[str, Any]]) -> Dict[str, Any]:
    categorization_prompt = """
    **Input TypeScript Interface:**
    \`\`\`typescript
    interface MutedInfo {
        muted: boolean;
    }

    interface Tab {
        userEmail: string;
        id: number;
        url: string;
        title?: string;
        active?: boolean;
        timeStamp: number;
        icon?: string;
        audible?: boolean;
        autoDiscardable?: boolean;
        discarded?: boolean;
        favIconUrl?: string;
        groupId?: number;
        height?: number;
        highlighted?: boolean;
        incognito?: boolean;
        index?: number;
        lastAccessed?: number;
        mutedInfo?: MutedInfo;
        pinned?: boolean;
        selected?: boolean;
        status?: "unloaded" | "loading" | "complete";
        width?: number;
        windowId?: number;
    }
    \`\`\`

    **Output Typescript interface**
    \`\`\`
    type Category = 
        "Social Media" |
        "News" |
        "Shopping" |
        "Entertainment" |
        "Education" |
        "Productivity" |
        "Communication" |
        "Finance" |
        "Search Engines" |
        "Health & Fitness" |
        "Real Estate" |
        "Travel & Navigation" |
        "Technology & Gadgets" |
        "Lifestyle" |
        "Government & Legal" |
        "Job Search" |
        "DIY & Hobbies" |
        "Automotive" |
        "Gaming" |
        "Other";

    interface MutedInfo {
        muted: boolean;
    }

    interface Tab {
        userEmail: string;
        id: number;
        url: string;
        title?: string;
        active?: boolean;
        timeStamp: number;
        icon?: string;
        audible?: boolean;
        autoDiscardable?: boolean;
        discarded?: boolean;
        favIconUrl?: string;
        groupId?: number;
        height?: number;
        highlighted?: boolean;
        incognito?: boolean;
        index?: number;
        lastAccessed?: number;
        mutedInfo?: MutedInfo;
        pinned?: boolean;
        selected?: boolean;
        status?: "unloaded" | "loading" | "complete";
        width?: number;
        windowId?: number;
        category: Category;  // New category field based on predefined categories
    }

    interface OutputResponse {
        tabs: [Tab]
    }
    \`\`\`

    You are a browser tab categorizer/classifier. Based on the input interface provided to you, 
    you are expected to categorize each tab that is provided to you into the Category type. Provide the output strictly in 
    JSON format with the additional field of category appended to the browser tabs. All other information should remain the same.

    **Assessment Guidelines:**
    Content categorization guidelines to check for:
    1. URL structure and domain
    2. Page title relevance
    3. Content keywords
    4. Site functionality
    5. User interaction patterns
    6. Content type and format
    7. Industry standards
    8. Common use cases
    9. Target audience

    **Important Considerations:**
    * **Keywords extraction**: Extract relevant keywords from title and content for better categorization.
    * **Output structure**: Ensure output follows the OutputResponse interface.
    * **Non-omittance**: Ensure all Tabs are properly categorized.
    * **Output format**: Ensure to output only JSON and nothing else.
    """

    # Combine URLs into JSON format for the API call
    content = json.dumps({"tabs": urls}, indent=2)

    # Pass the prompt and content to parse_categorization
    parsed_response = parse_categorization(categorization_prompt, content)

    # Clean and parse the response
    return json.loads(parsed_response.strip("```json\n").strip("```"))["tabs"]
