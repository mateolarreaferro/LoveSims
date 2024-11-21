from simulation_engine.settings import *
from simulation_engine.global_methods import *

from agent_bank.navigator import *
from generative_agent.generative_agent import * 

from cs222_assignment_1.memories.jasmine_carter_memories import *
from cs222_assignment_1.memories.matthew_jacobs_memories import *
from cs222_assignment_1.questions.jasmine_carter_questions import *
from cs222_assignment_1.questions.matthew_jacobs_questions import *

from agent_bank.memories.Yuki import *

import csv

factual_questions = [
    "What is your earliest memory?",
    "Where did you spend most of your childhood?",
    "What significant experience in primary school influenced your desire to study abroad?",
    "Which high schools did you attend, and where were they located?",
    "What is your major at Stanford University, and what does it focus on?",
    "What minor are you pursuing, and for how many years have you been studying this subject?",
    "What clubs or activities related to Japanese culture have you participated in at Stanford?",
    "What daily routine do you follow, including your morning and evening activities?",
    "Which qualities do you value most in other people, according to your personal values?",
    "If you didn’t have to work, what creative activity would you focus on and why?"
]


reflective_questions = [
    "What experiences in your life have shaped who you are today?",
    "How has your view on the world changed over the years?",
    "What challenges have you faced that have taught you the most about yourself?",
    "What decisions in your life do you feel proud of, and why?",
    "How do you define success for yourself, and has that definition evolved?",
    "What is the biggest lesson you’ve learned from failure?",
    "How do you handle uncertainty, and has your approach to it changed over time?",
    "What are the values that guide your life, and how do you ensure you stay true to them?",
    "How do you balance your personal passions with practical responsibilities?",
    "What legacy do you hope to leave behind, and how are you working toward it?"
]



"""
This function ask a bunch of questions at the same time,
and store the response in a csv file.
"""
def interview(generative_agent, stateless=False): 
  curr_convo = []
  with open("./interview_results.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    for i in range(len(factual_questions)):
      question = factual_questions[i]
      if stateless: curr_convo = []
      curr_convo += [["charlotte", question]]
      response = generative_agent.utterance(curr_convo) 
      
      print(question)
      print(f"{generative_agent.scratch.get_fullname()}: {response}")
      print()
      writer.writerow([question, response])
      
    for i in range(len(reflective_questions)):
      question = reflective_questions[i]
      if stateless: curr_convo = []
      curr_convo += [["charlotte", question]]
      response = generative_agent.utterance(curr_convo) 
      
      print(question)
      print(f"{generative_agent.scratch.get_fullname()}: {response}")
      print()
      writer.writerow([question, response])

"""
Original chat session function
"""
def chat_session(generative_agent, stateless=False): 
  print (f"Start chatting with {generative_agent.scratch.get_fullname()}.")
  print ("Type 'bye' to exit.")
  print ("")

  context = input("First, describe the context of this conversation: ")
  user_name = input("And what is your name: ")
  print ("")

  curr_convo = []

  while True: 
    if stateless: curr_convo = []

    user_input = input("You: ").strip()
    curr_convo += [[user_name, user_input]]

    if user_input.lower() == "bye":
      print(generative_agent.utterance(curr_convo)) 
      break

    response = generative_agent.utterance(curr_convo)  
    curr_convo += [[generative_agent.scratch.get_fullname(), response]]
    print(f"{generative_agent.scratch.get_fullname()}: {response}")


def mass_interview(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "Yuki")
  interview(curr_agent, True)


def build_agent(): 
  curr_agent = GenerativeAgent("SyntheticCS222_Base", "Yuki")
  for m in Yuki_memory: 
    curr_agent.remember(m)
  curr_agent.save("SyntheticCS222", "Yuki")


def interview_agent(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "Yuki")
  chat_session(curr_agent, True)


def chat_with_agent(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
  chat_session(curr_agent, False)


def ask_agent_to_reflect(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
  curr_agent.reflect("Reflect on your goal in life")


def main(): 
  # build_agent()
  interview_agent()
  # chat_with_agent()
  # ask_agent_to_reflect()


if __name__ == '__main__':
  # main()
  mass_interview()
  # interview_agent()
  

































