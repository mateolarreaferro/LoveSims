import openai
import sys
import os

# Add the path to simulation_engine to the Python path
sys.path.append('./simulation_engine')

# Import the API key from settings.py
from settings import OPENAI_API_KEY, DEBUG

# Function to test the OpenAI API
def test_openai_api():
    try:
        # Set up the OpenAI API key
        openai.api_key = OPENAI_API_KEY

        # Make a test API call using the ChatCompletion endpoint (adjust model if necessary)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or use the model you're working with
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of the United States?"},
            ]
        )

        # Print the response
        print("API test successful. Response:")
        print(response['choices'][0]['message']['content'].strip())

    except Exception as e:
        print(f"API test failed: {e}")

if __name__ == "__main__":
    if DEBUG:
        print("Testing OpenAI API...")
    test_openai_api()
