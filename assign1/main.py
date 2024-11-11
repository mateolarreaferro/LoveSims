import csv
import json
from simulation_engine.settings import *
from simulation_engine.global_methods import *

from agent_bank.navigator import *
from generative_agent.generative_agent import * 

from cs222_assignment_1.memories.matthew_jacobs_memories import *
from cs222_assignment_1.questions.matthew_jacobs_questions import *


# Load memories into the agent and save
def build_agent():
    curr_agent = GenerativeAgent("SyntheticCS222_Base", "matthew_jacobs")
    for m in matthew_memories:
        curr_agent.remember(m)
    curr_agent.save("SyntheticCS222", "matthew_jacobs")


# Function to ask questions, store responses, and save memories
def interview_agent():
    curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
    
    # Question lists
    factual_questions = [
    "What business did you start after working for a larger firm?",
    "What political group did you join, and what beliefs did you strengthen through this association?",
    "How did the 2008 housing crisis impact your real estate business?",
    "How long were you married to your college girlfriend before you divorced?",
    "What role did you hold during high school that taught you leadership and responsibility?",
    "What degree did you earn from the University of Texas, and how did it shape your career?",
    "What personal challenge did you face during the COVID-19 pandemic?",
    "What health issue prompted you to focus more on your physical health?",
    "How did your relationship with your daughter change as she grew older?",
    "What was your long-time dream related to property ownership, and how did you fulfill it?"
    ]
    reflective_questions = [
    "How has your upbringing in rural Texas, learning to hunt and fish with your father, shaped your values and worldview?",
    "In what ways did your experience as captain of your high school football team influence your leadership style in your professional and personal life?",
    "How has your divorce and your evolving relationship with your daughter impacted your sense of responsibility and personal fulfillment?",
    "How have your libertarian beliefs influenced your approach to managing your real estate business and navigating financial challenges?",
    "How has your experience with failure, such as losing the election for local office, affected your sense of purpose and resilience?"
    ]

    # Create CSV and JSON files
    responses_csv_path = "cs222_assignment_1/report/matthew_jacobs/answers__matthew_jacobs.csv"
    memories_json_path = "cs222_assignment_1/report/matthew_jacobs/retrieved__matthew_jacobs.json"
    
    with open(responses_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Question", "Agent's Response"])

        retrieved_memories = {}

        # Asking factual questions
        for question in factual_questions:
            response = curr_agent.utterance([[f"User", question]])
            csv_writer.writerow([question, response])
            
            # Retrieve top 10 memories
            retrieved = curr_agent.memory_stream.retrieve([question], time_step=0, n_count=10, verbose=False)
            memories_list = [memory.content for memory in retrieved[question]]
            retrieved_memories[question] = memories_list
        
        # Asking reflective questions
        for question in reflective_questions:
            response = curr_agent.utterance([[f"User", question]])
            csv_writer.writerow([question, response])
            
            # Retrieve top 10 memories
            retrieved = curr_agent.memory_stream.retrieve([question], time_step=0, n_count=10, verbose=False)
            memories_list = [memory.content for memory in retrieved[question]]
            retrieved_memories[question] = memories_list

        # Save retrieved memories to a JSON file
        with open(memories_json_path, 'w') as json_file:
            json.dump(retrieved_memories, json_file, indent=4)


def chat_with_agent():
    curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
    chat_session(curr_agent, False)


def ask_agent_to_reflect():
    curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
    curr_agent.reflect("Reflect on your goal in life")

def chat_session(generative_agent, stateless=False): 
    print(f"Start chatting with {generative_agent.scratch.get_fullname()}.")
    print("Type 'bye' to exit.")
    print("")
    
    context = input("First, describe the context of this conversation: ")
    user_name = input("And what is your name: ")
    print("")
    
    curr_convo = []
    
    while True:
        if stateless: 
            curr_convo = []
        
        user_input = input("You: ").strip()
        curr_convo += [[user_name, user_input]]
        
        if user_input.lower() == "bye":
            print(generative_agent.utterance(curr_convo)) 
            break
        
        response = generative_agent.utterance(curr_convo)  
        curr_convo += [[generative_agent.scratch.get_fullname(), response]]
        print(f"{generative_agent.scratch.get_fullname()}: {response}")



def main():
    build_agent()           # Load and save the agent with memories
    interview_agent()       # Conduct the interview and store results
    chat_with_agent()       # Optional: Chat interactively with the agent
    ask_agent_to_reflect()  # Optional: Have the agent reflect on something


if __name__ == '__main__':
    main()
