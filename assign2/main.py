import os
import random
import io
from flask import Flask, render_template, jsonify, request, send_file, Response
from flask_cors import CORS
from agents import agent_list  # Ensure this file exists with proper agent data
from llm_utils import *  # Ensure llm_utils.py is correctly set up

class Agent:
    def __init__(self, name, persona):
        self.name = name
        self.persona = persona
        self.messages = []

class Game:
    def __init__(self, date_duration=10):
        self.agents = []
        self.date_context = ""
        self.date_transcript = []
        self.date_duration = date_duration
        self.current_pairs = []

    def add_agents(self, agent_names):
        self.agents = [Agent(name, next(a["persona"] for a in agent_list if a["name"] == name)) 
                      for name in agent_names]

    def set_date_context(self, context):
        self.date_context = context
        print(f"Date context set to: {self.date_context}")

    def set_pairs(self, mode, selected_agents):
        if mode == "one-to-one":
            self.current_pairs = [(selected_agents[0], selected_agents[1])]
        elif mode == "one-to-all":
            main_agent = selected_agents[0]
            other_agents = [a["name"] for a in agent_list if a["name"] != main_agent]
            self.current_pairs = [(main_agent, other) for other in other_agents]
        else:  # all-pairs
            all_agents = [a["name"] for a in agent_list]
            self.current_pairs = [(a1, a2) 
                                for i, a1 in enumerate(all_agents) 
                                for a2 in all_agents[i+1:]]

    def run_dates(self):
        for agent1_name, agent2_name in self.current_pairs:
            agent1 = Agent(agent1_name, next(a["persona"] for a in agent_list if a["name"] == agent1_name))
            agent2 = Agent(agent2_name, next(a["persona"] for a in agent_list if a["name"] == agent2_name))
            
            # Log the start of the date
            date_start = f"Date between {agent1_name} and {agent2_name}:"
            response_data = {"agent": "System", "response": date_start, "number": 0}
            if not hasattr(stream, 'queue'):
                stream.queue = []
            stream.queue.append(response_data)
            
            for i in range(self.date_duration):
                # Determine the stage of the date
                if i < self.date_duration * 0.2:
                    stage = "greeting"
                elif i < self.date_duration * 0.8:
                    stage = "conversation"
                else:
                    stage = "goodbye"

                # Alternate between agents
                if i % 2 == 0:
                    current_agent = agent1
                    other_agent = agent2
                else:
                    current_agent = agent2
                    other_agent = agent1

                # Generate and stream the response
                system_prompt = self._create_date_prompt(current_agent, other_agent, stage)
                conversation_context = '\n'.join([msg["response"] for msg in self.date_transcript[-10:]])
                response = self.generate_response(system_prompt, conversation_context)
                
                response_data = self.log_date(current_agent, f"{current_agent.name}: {response}", i+1)
                if not hasattr(stream, 'queue'):
                    stream.queue = []
                stream.queue.append(response_data)

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

app = Flask(__name__)
CORS(app)
game = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_dates', methods=['POST'])
def start_dates():
    global game
    data = request.get_json()
    
    mode = data.get('mode')
    selected_agents = data.get('agents')
    date_context = data.get('dateContext', '')
    date_duration = data.get('dateDuration', 10)

    game = Game(date_duration=date_duration)
    
    if mode != 'all-pairs':
        game.set_date_context(date_context)
    
    game.set_pairs(mode, selected_agents)
    
    print(f"Game initialized with mode: {mode}, agents: {selected_agents}, context: {date_context}, duration: {date_duration}")
    return jsonify({"status": "success"})

@app.route('/run_dates', methods=['POST'])
def run_dates():
    global game
    if not game:
        print("No game initialized")
        return jsonify({"error": "No game initialized"}), 400

    def run_dates_async():
        game.run_dates()
        return jsonify({"status": "completed"})

    return run_dates_async()

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
