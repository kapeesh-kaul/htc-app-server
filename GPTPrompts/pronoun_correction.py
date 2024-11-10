from openai import OpenAI
import json
from typing import Dict, Any, List
import os

# Set up your OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

def parse_pronouns(prompt: str, content: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content.strip()

def process_pronouns(message_input: Dict[str, Any], users: Dict[str, Any]) -> Dict[str, Any]:
    pronoun_processor_prompt = """
    **Input TypeScript Interface:**
    \`\`\`typescript
    interface UserPronoun {
      userId: string;
      username: string;
      pronouns: {
        subject: string;
        object: string;
        possessive: string;
        reflexive: string;
      };
    }

    interface MessageInput {
      messageId: string;
      content: string;
      timestamp: string;
      mentions: {
        [userId: string]: {
          startIndex: number;
          endIndex: number;
        };
      };
    }

    interface ProcessedMessage {
      original: {
        content: string;
        mentions: string[];
      };
      processed: {
        content: string;
        replacements: Array<{
          original: string;
          replaced: string;
          position: number;
          userId: string;
        }>;
      };
      users: {
        [userId: string]: UserPronoun;
      };
      timestamp: string;
    }

    export default ProcessedMessage;
    \`\`\`

    **Processing Requirements:**
    You are a pronoun-aware message processor. Your task is to:
    1. Identify and replace only standalone pronouns (subject, object, possessive, and reflexive forms) based on each specific user's mentioned preferences.
    2. Avoid altering possessive pronouns that are part of other words (e.g., "yours").
    3. Track all changes made to the message with accurate position recording.
    4. Preserve the original message and mentions.
    5. Make sure the grammer (is and are) and context are maintained after replacement.
    6. understand the context of the message and identify the person and replace pronouns accordingly.

    **Important Considerations:**
    * **Output structure:** Ensure that the output strictly follows the ProcessedMessage interface.
    * **Non-omittance:** Ensure all standalone pronouns are correctly identified and replaced.
    * **Output format:** Ensure to output only JSON and nothing else.

    The processor should focus on:
    1. Accurate identification and replacement of standalone pronouns.
    2. Make sure grammar (is and are) and context are maintained after replacement.
    3. Correct replacement based on user preferences.
    4. Maintaining message context and readability without altering unintended words.
    5. Proper tracking of all changes made.
    """

    # Combine input for the prompt
    content = json.dumps({
        "message_input": message_input,
        "users": users
    }, indent=2)

    # Pass the prompt and content to parse_pronouns
    parsed_response = parse_pronouns(pronoun_processor_prompt, content)
    
    # Clean and parse the response
    return json.loads(parsed_response.strip("```json\n").strip("```"))

if __name__ == "__main__":
    message_input = {
        "messageId": "123",
        "content": "They are working on their project.",
        "timestamp": "2023-10-21T10:00:00Z",
        "mentions": {
            "user123": {
                "startIndex": 0,
                "endIndex": 4
            }
        }
    }

    users = {
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

    result = process_pronouns(message_input, users)
    print(json.dumps(result, indent=2))

