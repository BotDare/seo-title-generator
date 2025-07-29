import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_user_input():
    print("What would you like to generate?")
    print("1. Blog")
    print("2. Article")
    
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            return "blog"
        elif choice == '2':
            return "article"
        else:
            print("Invalid input. Please type 1 or 2.")

def get_notes():
    print("\nEnter your notes or main ideas for the content. Press Enter twice when you're done:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def generate_title_and_description(content_type, notes):
    prompt = f"""You are a helpful SEO assistant. Generate an attention-grabbing, Google-search-friendly TITLE and a short, keyword-optimised DESCRIPTION for a {content_type}.

Notes:
{notes}

Format your answer like this:
Title: ...
Description: ...
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use gpt-4 if available and allowed
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

def main():
    content_type = get_user_input()
    notes = get_notes()
    print("\nGenerating SEO-friendly title and description...\n")
    result = generate_title_and_description(content_type, notes)
    print(result)

if __name__ == "__main__":
    main()
