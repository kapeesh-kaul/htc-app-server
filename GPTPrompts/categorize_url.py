from openai import OpenAI
import json
from typing import Dict, Any, List
import os

# Set up your OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

def parse_categorization(prompt: str, content: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content.strip()

def categorize_urls(urls: List[Dict[str, Any]]) -> Dict[str, Any]:
    categorization_prompt = """
    **Input TypeScript Interface:**
    \`\`\`typescript
    interface URLData {
      url: string;
      title: string;
      raw: string;
    }

    interface URLAssessment {
      url_id: string;
      content: URLData;
      assessment: {
        category: ("Social Media" | "News" | "Shopping" | "Entertainment" | "Education" | 
                  "Productivity" | "Communication" | "Finance" | "Search Engines" | 
                  "Health & Fitness" | "Real Estate" | "Travel & Navigation" | 
                  "Technology & Gadgets" | "Lifestyle" | "Government & Legal" | 
                  "Job Search" | "DIY & Hobbies" | "Automotive" | "Gaming" | "Other");
        keywords: string[];
        confidence_score: number;
      };
      timestamp: string;
    }

    interface URLCategorization {
      analysis_timestamp: string;
      total_urls_analyzed: number;
      assessments: {
        [key: string]: URLAssessment;
      };
    }

    export default URLCategorization;
    \`\`\`

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
    * **Output structure**: Ensure output follows the URLCategorization interface.
    * **Non-omittance**: Ensure all URLs are properly categorized.
    * **Output format**: Ensure to output only JSON and nothing else.
    """

    # Combine URLs into JSON format for the API call
    content = json.dumps({
        "urls": urls
    }, indent=2)

    # Pass the prompt and content to parse_categorization
    parsed_response = parse_categorization(categorization_prompt, content)
    
    # Clean and parse the response
    return json.loads(parsed_response.strip("```json\n").strip("```"))

# Example usage
if __name__ == "__main__":
    # Example URLs for categorization
    urls = [
        {
            "url_id": "1",
            "content": {
                "url": "https://www.example.com/news/tech-updates",
                "title": "Latest Tech News and Updates",
                "raw": "Get the latest updates on technology, gadgets, and more..."
            },
            "timestamp": "2023-10-21T10:00:00Z"
        },
        {
            "url_id": "2",
            "content": {
                "url": "https://www.example.com/fitness/workout-tips",
                "title": "Top Workout Tips for Beginners",
                "raw": "Discover effective workout routines and fitness advice for all levels."
            },
            "timestamp": "2023-10-21T10:05:00Z"
        }
    ]

    result = categorize_urls(urls)
    print(json.dumps(result, indent=2))
