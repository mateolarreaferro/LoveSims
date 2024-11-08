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
        self.date_logs = []

    def set_date_context(self, context):
        self.date_context = context
        print(f"Date context set to: {self.date_context}")

    def run_date(self, agent, responses=5):
        """
        Conducts a multi-response conversation between the user agent (Joon) and a date agent.

        Args:
        - agent: The agent for the date.
        - responses: Number of conversational exchanges in the date.
        """
        print(f"Starting date with {agent.name}")
        conversation_context = f"You are on a {self.date_context}. You are dating {agent.name}."
        system_prompt_user = self._create_date_prompt(self.user_agent, agent)
        system_prompt_agent = self._create_date_prompt(agent, self.user_agent)

        for i in range(responses):
            # Joon's message (user agent's perspective)
            user_message = f"(Response {i+1}) Describe your interaction on this date: {self.date_context}"
            user_response = self.generate_response(system_prompt_user, conversation_context + f"\n{self.user_agent.name}: {user_message}")
            print(f"{self.user_agent.name} (Response {i+1}): {user_response}")
            self.log_date(agent, f"{self.user_agent.name}: {user_response}", i+1)
            conversation_context += f"\n{self.user_agent.name}: {user_response}"

            # Date agent's response
            agent_response = self.generate_response(system_prompt_agent, conversation_context)
            print(f"{agent.name} (Response {i+1}): {agent_response}")
            self.log_date(agent, f"{agent.name}: {agent_response}", i+1)
            conversation_context += f"\n{agent.name}: {agent_response}"

    def generate_response(self, system_prompt, conversation_context):
        """
        Generates a response from the agent based on the system prompt and current conversation context.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conversation_context},
        ]
        response = gen_oai(messages)
        return response

    def _create_date_prompt(self, agent, other_agent):
        return f"""
        You are {agent.name}, {agent.persona}. You are on a date with {other_agent.name}. 
        Respond in character as {agent.name}, with short, conversational responses. 
        Context: {self.date_context}.
        """
    
    def log_date(self, agent, response, response_number):
        log_entry = f"Date with {agent.name} - Response {response_number}:\n{response}\n"
        self.date_logs.append(log_entry)

    def get_log(self):
        return "\n".join(self.date_logs)

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
        game.run_date(agent, responses=5)  # Set responses to define length of interaction

    print("Returning date logs")
    return jsonify({"date_logs": game.get_log()})

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
        return send_file(buffer, as_attachment=True, download_name='game_log.md', mimetype='text/markdown')
    else:
        print("No game log available for download")
        return jsonify({"error": "No game log available"}), 400

if __name__ == "__main__":
    app.run(debug=True)
