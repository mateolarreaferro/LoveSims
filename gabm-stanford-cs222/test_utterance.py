import sys
from typing import List, Optional, Dict
from generative_agent.modules.memory_stream import MemoryStream, ConceptNode
from generative_agent.modules.interaction import utterance
from generative_agent.modules.scratch import Scratch

# Test agent class with mock data for the agent's scratch attributes and memory
class TestAgent:
    def __init__(self):
        scratch_data = {
            "first_name": "Matthew",
            "last_name": "Jacobs",
            "age": 48,
            "sex": "Male",
            "census_division": "West South Central",
            "political_ideology": "Libertarian",
            "political_party": "Libertarian",
            "education": "Bachelor's degree in Business Administration",
            "race": "Caucasian",
            "ethnicity": "Non-Hispanic",
            "annual_income": 72000,
            "extraversion": 4.0,
            "agreeableness": 3.75,
            "conscientiousness": 3.9,
            "neuroticism": 2.8,
            "openness": 3.1,
            "address": "Austin, Texas",
            "fact_sheet": "{'childhood': 'Raised in rural Texas, grew up hunting and fishing with father.'}",
            "speech_pattern": "Matthew's speech is confident and assertive.",
            "self_description": "I’m Matthew Jacobs, a business owner from Texas.",
            "private_self_description": "I don't share much about my divorce and health concerns."
        }
        self.scratch = Scratch(scratch_data)

        self.memory_stream = MemoryStreamWithFallback(
            nodes=[
                ConceptNode({
                    "node_id": 0,
                    "node_type": "observation",
                    "content": "I sold a house last week.",
                    "importance": 3.0,
                    "created": 1,
                    "last_retrieved": 1,
                    "pointer_id": None
                }),
                ConceptNode({
                    "node_id": 1,
                    "node_type": "observation",
                    "content": "I went fishing with my friends.",
                    "importance": 1.0,
                    "created": 2,
                    "last_retrieved": 2,
                    "pointer_id": None
                })
            ],
            embeddings={
                "I sold a house last week.": [0.1, 0.2, 0.3],
                "I went fishing with my friends.": [0.2, 0.2, 0.5]
            }
        )

class MemoryStreamWithFallback(MemoryStream):
    def __init__(self, nodes: List[ConceptNode], embeddings: Dict[str, List[float]]):
        node_dicts = [node.package() for node in nodes]
        super().__init__(node_dicts, embeddings)

    def retrieve(self, focal_points: List[str], time_step: int, 
                 n_count: int = 10, curr_filter: str = "all", 
                 hp: List[float] = [0.5, 3, 0.5], stateless: bool = True, 
                 verbose: bool = False, record_json: Optional[str] = None) -> Dict[str, List['ConceptNode']]:
        """
        Override the retrieve method to add a fallback embedding.
        """
        fallback_embedding = [1.0, 1.0, 1.0]  # Use a valid non-zero fallback embedding

        for focal_pt in focal_points:
            if focal_pt not in self.embeddings:
                print(f"Warning: No embedding found for {focal_pt}. Using fallback embedding.")
                self.embeddings[focal_pt] = fallback_embedding

        return super().retrieve(focal_points, time_step, n_count, curr_filter, hp, stateless, verbose, record_json)

# Test function to simulate a dialogue and generate an utterance
def test_generate_utterance():
    agent = TestAgent()

    # Simulated dialogue and context
    dialogue = [
        ["User", "What have you been up to?"],
        ["Matthew Jacobs", "I’ve been working on my real estate business."]
    ]
    context = "Matthew is having a casual conversation with a potential client."

    # Add the agent's memory stream fallback
    agent.memory_stream = MemoryStreamWithFallback(agent.memory_stream.seq_nodes, agent.memory_stream.embeddings)

    # Generate an utterance
    generated_utterance = utterance(agent, dialogue, context)

    # Print the result
    print("\nGenerated Utterance:")
    print(generated_utterance)

if __name__ == "__main__":
    test_generate_utterance()
