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
  curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
  interview(curr_agent, True)


def build_agent(): 
  curr_agent = GenerativeAgent("SyntheticCS222_Base", "Yuki")
  for m in Yuki_memories: 
    curr_agent.remember(m)
  curr_agent.save("SyntheticCS222", "Yuki")


def interview_agent(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
  chat_session(curr_agent, True)


def chat_with_agent(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
  chat_session(curr_agent, False)


def ask_agent_to_reflect(): 
  curr_agent = GenerativeAgent("SyntheticCS222", "matthew_jacobs")
  curr_agent.reflect("Reflect on your goal in life")


def main(): 
  build_agent()
  interview_agent()
  chat_with_agent()
  ask_agent_to_reflect()


if __name__ == '__main__':
  main()
  # mass_interview()
  # interview_agent()
  

































