import os
import random
import io
from flask import Flask, render_template, jsonify, request, send_file
from agents import agent_list  # Ensure this file exists with proper agent data
from llm_utils import gen_oai  # Ensure gen_oai is correctly imported and implemented

class Agent:
    def __init__(self, name, persona):
        self.name = name
        self.persona = persona

class DatingSimulation:
    def __init__(self, user_agent, agents, date_context, date_duration=10):
        self.user_agent = Agent(user_agent["name"], user_agent["persona"])
        self.agents = agents  # List of Agent objects
        self.date_context = date_context
        self.date_duration = date_duration
        self.current_agent_index = 0  # Index of current agent
        self.current_conversation_stage = 0  # Number of messages exchanged
        self.conversation_history = []
        self.date_transcript = []
        self.current_agent = None  # Track the current agent

    def get_next_message(self):
        if self.current_agent_index >= len(self.agents):
            return None, None, None  # All dates are over

        if self.current_conversation_stage == 0:
            # Start of new date
            self.current_agent = self.agents[self.current_agent_index]
            agent = self.current_agent
            print(f"Starting date with {agent.name}")
            self.date_transcript.append(f"Date with {agent.name}:\n")
            self.current_conversation_stage += 1  # Move to the next stage
            return "System", f"Date with {agent.name}", True

        if self.current_conversation_stage > self.date_duration:
            # Date with current agent is over, move to next agent
            self.current_agent_index += 1
            if self.current_agent_index >= len(self.agents):
                print("All dates completed.")
                return None, None, None  # All dates are over
            else:
                # Prepare for next date
                self.current_conversation_stage = 0
                self.conversation_history = []
                return self.get_next_message()  # Start next date

        # Proceed with conversation
        if self.current_conversation_stage <= self.date_duration:
            # Determine the stage
            if self.current_conversation_stage <= self.date_duration * 0.2:
                stage = "greeting"
            elif self.current_conversation_stage <= self.date_duration * 0.8:
                stage = "conversation"
            else:
                stage = "goodbye"

            # Decide whose turn it is
            if self.current_conversation_stage % 2 == 1:
                current_agent = self.user_agent
                other_agent = self.current_agent
            else:
                current_agent = self.current_agent
                other_agent = self.user_agent

            system_prompt = self._create_date_prompt(current_agent, other_agent, stage)
            conversation_history_text = '\n'.join(self.conversation_history)

            # Generate response
            response = self.generate_response(system_prompt, conversation_history_text)

            # Debug statements
            print(f"System Prompt:\n{system_prompt}")
            print(f"Conversation History:\n{conversation_history_text}")
            print(f"{current_agent.name}'s Response: {response}\n")

            if not response:
                response = "..."

            self.conversation_history.append(f"{current_agent.name}: {response.strip()}")
            self.date_transcript.append(f"{current_agent.name}: {response.strip()}\n")
            self.current_conversation_stage += 1

            return current_agent.name, response.strip(), False

    def generate_response(self, system_prompt, conversation_context):
        """
        Generates a response from the agent based on the system prompt and current conversation context.
        """
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        if conversation_context.strip():
            messages.append({"role": "user", "content": conversation_context})
        try:
            response = gen_oai(messages)
            return response.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return "..."

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

    def get_log(self):
        return "\n".join(self.date_transcript)

def init_simulation(user_agent_name, date_context, date_duration, date_mode='all', date_agent_name=None):
    user_agent = next((agent for agent in agent_list if agent["name"] == user_agent_name), None)
    if not user_agent:
        raise ValueError(f"User agent '{user_agent_name}' not found in agent list.")

    if date_mode == 'one' and date_agent_name:
        # Only date with selected agent
        other_agents = [Agent(agent_data["name"], agent_data["persona"]) for agent_data in agent_list if agent_data["name"] == date_agent_name]
        if not other_agents:
            raise ValueError(f"Date agent '{date_agent_name}' not found in agent list.")
    else:
        # Date with all other agents
        other_agents = [Agent(agent_data["name"], agent_data["persona"]) for agent_data in agent_list if agent_data["name"] != user_agent_name]
    simulation = DatingSimulation(user_agent, other_agents, date_context, date_duration)
    # No need to call start_next_date here, as get_next_message will handle it
    return simulation

app = Flask(__name__)
simulation = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_dates', methods=['POST'])
def start_dates():
    global simulation
    data = request.json
    user_agent_name = data['name']
    date_context = data['context']
    date_duration = int(data.get('duration', 10))  # Default to 10 if not provided
    date_mode = data.get('date_mode', 'all')
    date_agent_name = data.get('date_agent_name', None)

    try:
        simulation = init_simulation(user_agent_name, date_context, date_duration, date_mode, date_agent_name)
        print(f"Simulation initialized with agent: {user_agent_name}, context: {date_context}, duration: {date_duration}, date_mode: {date_mode}, date_agent_name: {date_agent_name}")
        return jsonify({"status": "success"})
    except ValueError as e:
        print(f"Error initializing simulation: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/next_message', methods=['POST'])
def next_message():
    global simulation
    if not simulation:
        return jsonify({"error": "No simulation initialized"}), 400

    agent_name, message, date_started = simulation.get_next_message()
    if agent_name is None:
        # All dates completed
        return jsonify({"finished": True})
    else:
        return jsonify({
            "agent_name": agent_name,
            "message": message,
            "date_started": date_started,
        })

@app.route('/reset', methods=['POST'])
def reset_simulation():
    global simulation
    simulation = None
    print("Simulation reset")
    return jsonify({"status": "reset"})

@app.route('/download_log', methods=['GET'])
def download_log():
    if simulation:
        log_content = simulation.get_log()
        buffer = io.BytesIO()
        buffer.write(log_content.encode('utf-8'))
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='date_transcript.md', mimetype='text/markdown')
    else:
        print("No date transcript available for download")
        return jsonify({"error": "No date transcript available"}), 400

if __name__ == "__main__":
    app.run(debug=True)
