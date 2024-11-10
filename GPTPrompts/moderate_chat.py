from openai import OpenAI
import json
from typing import Dict, Any, List
import os

# Set up your OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

def parse_moderation(prompt: str, content: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content.strip()

def moderate_chat(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    moderation_prompt = """
    **Input TypeScript Interface:**
    \`\`\`typescript
    interface MessageAssessment {
      message_id: string;
      content: string;
      assessment: {
        is_inappropriate: boolean;
        flags: string[];
        feedback: string;
      };
      timestamp: string;
    }

    interface ChatModeration {
      analysis_timestamp: string;
      total_messages_analyzed: number;
      assessments: {
        [key: string]: MessageAssessment;
      };
    }

    export default ChatModeration;
    \`\`\`

    **Messages Sample:**
    \`\`\`
    [Group chat message history goes here]
    \`\`\`

    **Assessment Guidelines:**
    Content moderation guidelines to check for:
    1. Disrespectful Language
    2. Hate Speech or Harassment
    3. Negative/Unconstructive Tone
    4. Sensitive Topics
    5. Spam/Self-Promotion
    6. Privacy Violations
    7. Off-Topic Content
    8. Cultural Insensitivity
    9. Trolling/Provocative Language

    **Important Considerations:**
    * **Output structure:** Ensure output follows the ChatModeration interface.
    * **Non-omittance:** Ensure all messages are properly assessed and categorized.
    * **Output format:** Ensure to output only JSON and nothing else.
    """

    # Combine messages into JSON format for the API call
    content = json.dumps({
        "messages": messages
    }, indent=2)

    # Pass the prompt and content to parse_moderation
    parsed_response = parse_moderation(moderation_prompt, content)
    
    # Clean and parse the response
    return json.loads(parsed_response.strip("```json\n").strip("```"))

# Example usage
if __name__ == "__main__":
    # Example messages for moderation
    messages = [
        {
            "message_id": "1",
            "content": "I don't like this topic.",
            "timestamp": "2023-10-21T10:00:00Z"
        },
        {
            "message_id": "2",
            "content": "That was really disrespectful.",
            "timestamp": "2023-10-21T10:05:00Z"
        }
    ]

    result = moderate_chat(messages)
    print(json.dumps(result, indent=2))
