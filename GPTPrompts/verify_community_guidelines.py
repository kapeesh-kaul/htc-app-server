from openai import OpenAI
import json
from typing import Dict, Any, List
import os

def parse_prompt(prompt: str, content: str) -> str:
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content.strip()


def verify_community_guidelines(text: List[str]) -> Dict[str, Any]:
    moderation_prompt = """
    **Input TypeScript Interface:**
    \`\`\`typescript
    interface MessageAssessment {
      message_id: string;
      content: string;
      assessment: {
        is_inappropriate: boolean;
        flags: ("Disrespectful Language" | "Hate Speech or Harassment" | "Negative/Unconstructive Tone" | "Sensitive Topics" | "Spam/Self-Promotion" | "Privacy Violations" | "Off-Topic Content" | "Cultural Insensitivity" | "Trolling/Provocative Language" | "API Guideline Violation")[];
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
    * **Flag API violations**: If the input violates API guidelines, add an "API Guideline Violation" flag to the `flags` array but do not throw an error.
    * **Output structure**: Ensure output follows the ChatModeration interface.
    * **Non-omittance**: Ensure all messages are properly assessed and categorized.
    * **Output format**: Ensure to output only JSON and nothing else.
    """
    
    # Join list elements into a single string for the API call
    content = "\n".join(text)
    
    # Pass the prompt and combined content to parse_prompt
    parsed_response = parse_prompt(moderation_prompt, content)
    
    # Clean and parse the response
    return json.loads(parsed_response.strip("```json\n").strip("```"))