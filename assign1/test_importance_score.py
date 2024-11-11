import openai
import sys
import os

# Add the path to simulation_engine to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'simulation_engine'))

# Import the API key from settings.py
from settings import OPENAI_API_KEY

# Explicitly set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to test the OpenAI API with batch importance prompt
def test_batch_importance():
    prompt = """
    The following is a list of numbered observations. Each observation represents a piece of information that the AI needs to evaluate for its importance within a certain context. The goal is to provide an importance score between 0 and 100 for each observation, where 0 means the observation is not important, and 100 means the observation is extremely important. Consider the relevance, significance, and the overall impact of each observation when assigning the importance score.

    Observations:
    Item 1: "The system booted successfully."
    Item 2: "There was an error in the login sequence."
    Item 3: "The user updated the profile successfully."
    
    Return the scores as a JSON object in the following format:
    {
      "Item 1": <int importance score for item 1>,
      "Item 2": <int importance score for item 2>,
      "Item 3": <int importance score for item 3>
    }
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the appropriate GPT model for your project
            messages=[
                {"role": "system", "content": "You are an assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0
        )

        # Extract and print the response
        print("Batch Importance Test Result:")
        print(response.choices[0].message['content'])

    except Exception as e:
        print(f"Error during batch importance test: {e}")

# Function to test singular importance prompt
def test_singular_importance():
    prompt = """
    The following is a single observation. The AI needs to evaluate the importance of this observation and provide an importance score between 0 and 100, where 0 means the observation is not important, and 100 means the observation is extremely important. Consider the relevance, significance, and overall impact of the observation when assigning the importance score.

    Observation:
    "There was an error in the login sequence."

    Return the score as a JSON object in the following format:
    {
      "Item  1": <int importance score>
    }
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the appropriate GPT model for your project
            messages=[
                {"role": "system", "content": "You are an assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0
        )

        # Extract and print the response
        print("Singular Importance Test Result:")
        print(response.choices[0].message['content'])

    except Exception as e:
        print(f"Error during singular importance test: {e}")


if __name__ == "__main__":
    print("Testing Batch Importance Prompt...")
    test_batch_importance()

    print("\nTesting Singular Importance Prompt...")
    test_singular_importance()
