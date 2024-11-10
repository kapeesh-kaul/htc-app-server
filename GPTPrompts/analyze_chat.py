from openai import OpenAI
import json
from typing import Dict, Any, List
import os

# Set up your OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

def parse_analysis(prompt: str, content: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content.strip()

def analyze_chat(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    analysis_chat_prompt = """
    **Input TypeScript Interface:**
    \`\`\`typescript
    interface IssueContext {
      message_id: string;
      context: string;
      timestamp: string;
    }

    interface Issue {
      category: string;
      keyword: string;
      occurrence_count: number;
      first_mentioned: string;
      last_mentioned: string;
      mentioned_by: string[];
      priority_score: number;
      sample_contexts: IssueContext[];
    }

    interface ChatAnalysis {
      analysis_timestamp: string;
      total_messages_analyzed: number;
      issues: {
        [key: string]: Issue;
      };
    }

    export default ChatAnalysis;
    \`\`\`

    **Messages Sample:**
    \`\`\`
    [Group chat message history goes here]
    \`\`\`

    **Analysis Requirements:**
    You are an expert chat analyzer. Your task is to analyze the group chat messages and identify:
    1. Common issues and bugs reported
    2. Feature requests and suggestions
    3. Questions and support needs
    4. Priority levels of issues
    5. User engagement patterns

    **Important Considerations:**
    * **Output structure:** Ensure that the output strictly follows the output typescript interface (ChatAnalysis).
    * **Non-omittance:** Ensure that all relevant issues from the chat are captured and categorized appropriately.
    * **Output format:** Ensure to output only JSON and nothing else.

    The analysis should focus on identifying patterns, recurring issues, and priority items that need attention.
    """

    # Combine messages into JSON format for the API call
    content = json.dumps({
        "messages": messages
    }, indent=2)

    # Pass the prompt and content to parse_analysis
    parsed_response = parse_analysis(analysis_chat_prompt, content)
    
    # Clean and parse the response
    return json.loads(parsed_response.strip("```json\n").strip("```"))

# Example usage
if __name__ == "__main__":
    # Example chat messages for analysis
    messages = [
        {
            "message_id": "1",
            "context": "I keep encountering a bug when trying to save my work.",
            "timestamp": "2023-10-21T10:00:00Z"
        },
        {
            "message_id": "2",
            "context": "Is there a way to enable dark mode?",
            "timestamp": "2023-10-21T10:05:00Z"
        },
        {
            "message_id": "3",
            "context": "The save button is not responsive sometimes.",
            "timestamp": "2023-10-21T10:07:00Z"
        },
        {
            "message_id": "4",
            "context": "I’d like a feature that allows for automatic backups.",
            "timestamp": "2023-10-21T10:10:00Z"
        }
    ]

    result = analyze_chat(messages)
    print(json.dumps(result, indent=2))
