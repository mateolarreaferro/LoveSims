"""
Prompts and formats for different types of evaluations in LoveSims
"""

# Format specifications for different evaluation types
SELF_REFLECTION_FORMAT = """{
    "satisfactionScore": "Score from 0-100 indicating overall satisfaction with the interaction",
    "lengthFeedback": "One of: 'Too short', 'Just right', 'Too long'",
    "attributeRatings": {
        "Attractiveness": "Score 0-100 on how attracted you felt",
        "Sincerity": "Score 0-100 on how sincere they seemed",
        "Intelligence": "Score 0-100 on how intelligent they appeared",
        "Fun": "Score 0-100 on how fun the interaction was",
        "Ambition": "Score 0-100 on how ambitious they seemed",
        "SharedInterests": "Score 0-100 on level of shared interests"
    },
    "decision": "Answer 'yes' or 'no': Would you want to see this person again?",
    "analysis": "Brief analysis of the interaction and compatibility"
}"""

TRANSCRIPT_ANALYSIS_FORMAT = """{
    "analysis": "Detailed analysis of the interaction and compatibility",
    "compatibilityScore": "Overall compatibility score from 0-100",
    "attributeSimilarity": {
        "Attractiveness": "Score 0-100 on similarity in attractiveness levels",
        "Sincerity": "Score 0-100 on similarity in sincerity levels",
        "Intelligence": "Score 0-100 on similarity in intelligence levels",
        "Fun": "Score 0-100 on similarity in fun/playfulness",
        "Ambition": "Score 0-100 on similarity in ambition levels",
        "SharedInterests": "Score 0-100 on overlap in interests"
    },
    "decision": "Answer 'yes' or 'no': Should these two people see each other again?",
    "keyFactors": "List of 3-5 key factors affecting compatibility"
}"""

PROFILE_ANALYSIS_FORMAT = """{
    "analysis": "Detailed analysis of potential compatibility based on profiles",
    "compatibilityScore": "Overall compatibility score from 0-100",
    "attributeSimilarity": {
        "Attractiveness": "Score 0-100 on compatibility in attractiveness preferences",
        "Sincerity": "Score 0-100 on alignment in sincerity/authenticity",
        "Intelligence": "Score 0-100 on intellectual compatibility",
        "Fun": "Score 0-100 on similarity in approach to fun/entertainment",
        "Ambition": "Score 0-100 on alignment in ambition/goals",
        "SharedInterests": "Score 0-100 on overlap in interests/hobbies"
    },
    "decision": "Answer 'yes' or 'no': Should these two people see each other again?",
    "keyFactors": "List of 3-5 key factors affecting compatibility"
}"""

def get_self_reflection_prompt(agent_name, agent_profile, memories, other_agent, context, transcript):
    return f"""You are {agent_name}. Based on your profile:
{agent_profile}

And your memories:
{memories}

You just had a conversation with {other_agent} in the context: {context}

Here's the transcript:
{transcript}

Please reflect on this interaction by providing:
1. A satisfaction score (0-100). Be critical and honest - not every interaction is perfect. Consider:
   - How well did you connect?
   - Were there any awkward moments or misunderstandings?
   - Did they match your preferences and interests?
   - Would you want to meet them again?

2. Feedback on conversation length
3. Ratings (0-100) for different attributes, being specific to this interaction
4. A brief analysis of the interaction

Be brutally honest in your evaluation. Don't be afraid to give low scores if the interaction wasn't great."""

def get_transcript_analysis_prompt(agents, context, transcript):
    return f"""As a neutral third-party evaluator, analyze this conversation between {' and '.join(agents)}:

Context: {context}

Transcript:
{transcript}

Please analyze:
1. Overall compatibility (score 0-100)
2. Similarity in key attributes (each scored 0-100)
3. Key factors affecting compatibility
4. Provide a detailed analysis of their interaction

Focus on how well they connect and align in different areas."""

def get_profile_analysis_prompt(agent1, profile1, memories1, agent2, profile2, memories2):
    return f"""As a neutral third-party matchmaker, analyze the compatibility between these individuals based on their profiles and memories:

Person 1 ({agent1}):
Profile: {profile1}
Memories: {memories1}

Person 2 ({agent2}):
Profile: {profile2}
Memories: {memories2}

Please analyze:
1. Overall compatibility potential (score 0-100)
2. Similarity in key attributes (each scored 0-100)
3. Key factors affecting compatibility
4. Provide a detailed analysis of their potential match

Focus on long-term compatibility and alignment in values, goals, and personality traits."""
