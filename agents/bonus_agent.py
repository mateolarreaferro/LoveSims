from typing import List, Tuple, Dict, Any

from simulation_engine.gpt_structure import gpt_request_messages
from cs222_assignment_1_bonus.environment import BakingEnvironment


class Agent:
  relevant_memories = ""
  step_count = 0
  steps = []
  
  def __init__(self, name: str, description: str):
    self.name, self.description = name, description
    self.message_history = []
    self.env = BakingEnvironment(self)

  def perceive(self) -> None:
    env_description = f"""
      Current baking environment:
      Available ingredients:
      {', '.join(self.env.ingredients.keys())}
      Ingredients added: 
      {', '.join(ing for ing, data in self.env.ingredients.items() if data['current'] > 0)}
      Available tools: 
      {', '.join(self.env.tools.keys())}
      Tools in use: 
      {', '.join(tool for tool, data in self.env.tools.items() if data['used'])}"""

    self.message_history.append({
      "role": "user",
      "content": env_description
    })

  def call_gpt(self, memories, all=True) -> str:
    """
    This function call gpt api to retrieve relevant info for cake making from the memory.
    """
    prompt = f"""
    Input: {memories}
    From the input, modify the cooking steps of a vanilla cake by adding the specific ingredients in the vanilla cake recipe. 
    Output format: the modified cooking steps from the input with ingredients info to bake a vanilla cake. 
    
    "1. step 1
    2. step 2
    3. step 3
    ......"
    
    """
    response = gpt_request_messages(
      messages=[{"role": "system", "content": prompt}])
    return response
  
  def retrieve(self) -> str:
    """
    TODO
    In the agent's memories, there is a recipe for a cake buried amongst
    information about other topics. 

    Come up with a way to retrieve the relevant text from the agent's memory,
    without modifying the text file and minimizing the number of irrelevant
    information retrieved.

    Return the retrieved recipe (ingredients and steps) as a string.
    """
    if Agent.relevant_memories == "":
      memories = open(f"cs222_assignment_1_bonus/{self.name}/memory/cake.txt", 'r').read().split("\n\n")
      relevant_memories = self.call_gpt(memories)
      # print("relevant memories retrieved!")
      # print(relevant_memories)
      Agent.relevant_memories = relevant_memories
    return Agent.relevant_memories
  
  # The Most Basic Way to do it :)
  # def retrieve(self):
  #   memories = open(f"cs222_assignment_1_bonus/{self.name}/memory/cake.txt", 'r').read().split("\n\n")
  #   mems = [m for m in memories if "cake" in m and "cakewalk" not in m]
  #   print("RETRIEVED: " + str(mems))
  #   return mems
    
  def act(self) -> str:
    persona = f"""
    You are {self.name}. {self.description} You are baking a cake right now.
    You remember the recipe for the cake:
    {self.retrieve()}

    Speak in character, no asterisks. Take only one action at a time.
    """
    response = gpt_request_messages(
      messages=[{"role": "system", "content": persona}] + self.message_history)
    #print("message history", self.message_history)
    return response

  def reflect(self, response: str) -> None:
    self.message_history.append({"role": "assistant", "content": response})

  def baking_step(self) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    self.perceive()
    action = self.act()
    self.reflect(action)
    attempted, executed, feedbacks = self.env.process_action(action)
    return action, attempted, executed, feedbacks