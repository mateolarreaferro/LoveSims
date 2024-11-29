import os
import random
import io
from flask import Flask, render_template, jsonify, request, send_file, Response
from agents import agent_list  # Ensure this file exists with proper agent data
from llm_utils import *  # Ensure llm_utils.py is correctly set up

class Agent:
    def __init__(self, name, persona):
        self.name = name
        self.persona = persona
        self.messages = []

class Game:
    def __init__(self, user_agent, agents, date_duration=10):
        self.user_agent = Agent(user_agent["name"], user_agent["persona"])
        self.agents = agents
        self.date_context = ""
        self.date_transcript = []
        self.date_duration = date_duration

    def set_date_context(self, context):
        self.date_context = context
        print(f"Date context set to: {self.date_context}")

    def run_date(self, agent, responses=None):
        if responses is None:
            responses = self.date_duration
        print(f"Starting date with {agent.name}")
        conversation_history = []
        self.log_date(agent, f"Date with {agent.name}:\n", 0)

        for i in range(responses):
            # Determine the stage of the date
            if i < responses * 0.2:
                stage = "greeting"
            elif i < responses * 0.8:
                stage = "conversation"
            else:
                stage = "goodbye"

            # Decide whose turn it is
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
        ]
        if conversation_context.strip():
            messages.append({"role": "user", "content": conversation_context})
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
        self.date_transcript.append({"agent": agent.name, "response": response, "number": response_number})
        return {"agent": agent.name, "response": response, "number": response_number}

    def get_log(self):
        return "\n".join([msg["response"] for msg in self.date_transcript])

def init_game(user_agent_name, date_context, date_duration):
    print(user_agent_name)
    print(agent_list)
    user_agent = next(agent for agent in agent_list if agent["name"] == user_agent_name)
    other_agents = [Agent(agent_data["name"], agent_data["persona"]) for agent_data in agent_list if agent_data["name"] != user_agent_name]
    game = Game(user_agent, other_agents, date_duration)
    game.set_date_context(date_context)
    return game

app = Flask(__name__)
game = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_dates', methods=['POST'])
def start_dates():
    global game
    data = request.json
    user_agent_name = data['name']
    date_context = data['context']
    date_duration = int(data.get('duration', 10))  # Default to 10 if not provided

    game = init_game(user_agent_name, date_context, date_duration)
    print(f"Game initialized with agent: {user_agent_name}, context: {date_context}, duration: {date_duration}")
    return jsonify({"status": "success"})

@app.route('/stream')
def stream():
    def generate():
        while True:
            if not hasattr(stream, 'queue'):
                stream.queue = []
            if stream.queue:
                data = stream.queue.pop(0)
                yield f"data: {json.dumps(data)}\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/run_dates', methods=['POST'])
def run_dates():
    global game
    if not game:
        print("No game initialized")
        return jsonify({"error": "No game initialized"}), 400

    def run_dates_async():
        for agent in game.agents:
            print(f"Running date with {agent.name}")
            for i in range(game.date_duration):
                # Determine the stage of the date
                if i < game.date_duration * 0.2:
                    stage = "greeting"
                elif i < game.date_duration * 0.8:
                    stage = "conversation"
                else:
                    stage = "goodbye"

                # Decide whose turn it is
                if i % 2 == 0:
                    current_agent = game.user_agent
                    other_agent = agent
                else:
                    current_agent = agent
                    other_agent = game.user_agent

                # Update system prompt to include the current stage
                system_prompt = game._create_date_prompt(current_agent, other_agent, stage)
                conversation_context = '\n'.join([msg["response"] for msg in game.date_transcript[-10:]])
                
                # Generate response
                response = game.generate_response(system_prompt, conversation_context)
                print(f"{current_agent.name} (Response {i+1}): {response}")
                
                # Log and stream the response
                response_data = game.log_date(agent, f"{current_agent.name}: {response}", i+1)
                if not hasattr(stream, 'queue'):
                    stream.queue = []
                stream.queue.append(response_data)

        return jsonify({"status": "completed"})

    return run_dates_async()

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
