import os
import random
import io
from flask import Flask, render_template, jsonify, request, send_file
from agents import agent_list
from llm_utils import *

class Agent:
    def __init__(self, name, persona):
        self.name = name
        self.persona = persona
        self.messages = []

class Game:
    def __init__(self, user_agent, agents):
        self.user_agent = Agent(user_agent["name"], user_agent["persona"])
        self.agents = agents
        self.date_context = ""
        self.date_transcript = []

    def set_date_context(self, context):
        self.date_context = context
        print(f"Date context set to: {self.date_context}")

    def run_date(self, agent, responses=10):
        """
        Conducts a multi-response conversation between the user agent and a date agent.
        """
        print(f"Starting date with {agent.name}")
        conversation_history = []  # List of messages without speaker names
        self.log_date(agent, f"Date with {agent.name}:\n", 0)  # Log the start of the date

        for i in range(responses):
            # Determine the stage of the date
            if i < 2:
                stage = "greeting"
            elif i < 8:
                stage = "conversation"
            else:
                stage = "goodbye"

            # It's the user agent's turn if i % 2 == 0
            if i % 2 == 0:
                current_agent = self.user_agent
                other_agent = agent
            else:
                current_agent = agent
                other_agent = self.user_agent

            # Update system prompt to include the current stage
            system_prompt = self._create_date_prompt(current_agent, other_agent, stage)

            # Construct conversation context without speaker names
            conversation_context = '\n'.join(conversation_history)

            # Generate response
            response = self.generate_response(system_prompt, conversation_context)
            print(f"{current_agent.name} (Response {i+1}): {response}")

            # Append to conversation history without the speaker's name
            conversation_history.append(response.strip())

            # Log the response with speaker's name
            self.log_date(agent, f"{current_agent.name}: {response}", i+1)

    def generate_response(self, system_prompt, conversation_context):
        """
        Generates a response from the agent based on the system prompt and current conversation context.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conversation_context},
        ]
        response = gen_oai(messages)
        return response.strip()

    def _create_date_prompt(self, agent, other_agent, stage):
        return f"""
        You are {agent.name}, {agent.persona}. You are on a date with {other_agent.name}.
        The date should follow this structure: start with a greeting, then progress from light to deeper conversation topics, and end with a goodbye.
        You are currently in the {stage} stage of the date.
        Respond in character as {agent.name}, with short, conversational responses appropriate for the current stage of the date.
        Do not include your name or any prefixes or labels in your responses.
        Only output what you would say as {agent.name}.
        Context: {self.date_context}.
        """

    def log_date(self, agent, response, response_number):
        if response_number == 0:
            # Start a new date transcript
            self.date_transcript.append(response)
        else:
            self.date_transcript.append(f"{response}\n")

    def get_log(self):
        return "\n".join(self.date_transcript)

def init_game(user_agent_name, date_context):
    user_agent = next(agent for agent in agent_list if agent["name"] == user_agent_name)
    other_agents = [Agent(agent_data["name"], agent_data["persona"]) for agent_data in agent_list if agent_data["name"] != user_agent_name]
    game = Game(user_agent, other_agents)
    game.set_date_context(date_context)
    return game

app = Flask(__name__)
game = None
original_agent_count = len(agent_list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_dates', methods=['POST'])
def start_dates():
    global game
    data = request.json
    user_agent_name = data['name']
    date_context = data['context']
    
    game = init_game(user_agent_name, date_context)
    print(f"Game initialized with agent: {user_agent_name} and context: {date_context}")
    return jsonify({"status": "success"})

@app.route('/run_dates', methods=['POST'])
def run_dates():
    global game
    if not game:
        print("No game initialized")
        return jsonify({"error": "No game initialized"}), 400

    print("Running dates with each agent")
    for agent in game.agents:
        print(f"Running date with {agent.name}")
        game.run_date(agent, responses=10)  # Set responses to define length of interaction

    print("Returning date transcripts")
    return jsonify({"date_transcript": game.get_log()})

@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = None
    print("Game reset")
    return jsonify({"status": "reset"})

@app.route('/download_log', methods=['GET'])
def download_log():
    if game:
        log_content = game.get_log()
        buffer = io.BytesIO()
        buffer.write(log_content.encode('utf-8'))
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='date_transcript.md', mimetype='text/markdown')
    else:
        print("No date transcript available for download")
        return jsonify({"error": "No date transcript available"}), 400

if __name__ == "__main__":
    app.run(debug=True)
