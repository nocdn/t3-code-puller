import json
from google import genai
from google.genai import types
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Gemini client with your API key
gemini_api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

def analyze_youtube_video(youtube_url):
    """
    Analyze a YouTube video using Gemini models.

    Args:
        youtube_url (str): URL of the YouTube video to analyze
        prompt_text (str): The instruction for what to do with the video

    Returns:
        str: The generated response from Gemini
    """
    try:
        # Create a file data part with the YouTube URL
        youtube_part = types.Part(
            file_data=types.FileData(file_uri=youtube_url)
        )

        # Create a text part with the prompt
        text_part = types.Part(text="""what is the t3 chat promo code in this video? output in just a dictionary (not in a code block, just a dictionary as the message. THIS IS VERY IMPORTANT: ONLY OUTPUT THE DICTIONARY AS THE MESSAGE, NOT A JSON CODE BLOCK OR ANYTHING, JUST THE DICTIONARY AS THE TEXT) with keys of \"code\", \"count\" (being how many customers can use the code), and a key for \"notes\" if there is any other information. if it doesn't exist, output code: none""")

        # Combine parts into content
        content = types.Content(parts=[youtube_part, text_part])

        # Generate content using Gemini 2.0 Flash
        response = client.models.generate_content(
            model='models/gemini-2.0-flash',
            contents=content,
            config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000
            )
        )

        parsed_string = json.loads(str(response.text))
        return parsed_string

    except Exception as e:
        return f"An error occurred: {str(e)}"


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
            "chat_id": chat_id,
            "text": message
        }
    response = requests.post(url, data=payload)
    return response.json()

def main():
    youtube_url = input("Enter YouTube URL: ")
    print("\nAnalyzing video, please wait...\n")
    result = analyze_youtube_video(youtube_url)
    print(result)

    telegram_message=f"""{result['code']}"""
    print("telegram_message:", telegram_message)
    print(type(telegram_message))

    BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    send_telegram_message(BOT_TOKEN, CHAT_ID, telegram_message)


if __name__ == "__main__":
    main()
