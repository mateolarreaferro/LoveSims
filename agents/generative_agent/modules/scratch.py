class Scratch: 
  def __init__(self, scratch=None): 
    self.name = ""
    self.age_group = ""
    self.gender = ""
    self.grow_up_location = ""
    self.most_time_activity = ""
    self.important_value = ""
    self.closest_personality = ""
    self.social_context_action = ""
    self.infinite_money_use = ""
    self.favorite_hobby = ""
    self.political_affiliation = ""
    self.places_lived = ""
    self.important_relationship = ""
    self.childhood_description = ""
    self.mbti_type = ""
    self.five_year_goal = ""
    self.biggest_fear = ""
    self.childhood_trauma = ""
    self.intrusive_thoughts_frequency = ""
    self.meaningful_event = ""
    self.cultural_tension_experience = ""
    self.problem_solving_approach = ""
    self.religious_beliefs = ""
    self.prized_possession = ""
    self.career_aspiration = ""
    self.difficult_situation_method = ""
    self.friend_valued_trait = ""
    self.way_spend_100_dollars = ""
    self.family_income_level = ""
    self.ethnicity = ""
    self.primary_language = ""
    
    self.political_ideology = ""
    self.political_party = ""
    self.education = ""
    self.race = ""
    self.extraversion = 0.0
    self.agreeableness = 0.0
    self.conscientiousness = 0.0
    self.neuroticism = 0.0
    self.openness = 0.0
    self.fact_sheet = ""
    self.speech_pattern = ""
    self.self_description = ""
    self.private_self_description = ""

    if scratch: 
      self.name = scratch["name"]
      self.age_group = scratch["age_group"]
      self.gender = scratch["gender"]
      self.grow_up_location = scratch["grow_up_location"]
      self.most_time_activity = scratch["most_time_activity"]
      self.important_value = scratch["important_value"]
      self.closest_personality = scratch["closest_personality"]
      self.social_context_action = scratch["social_context_action"]
      self.infinite_money_use = scratch["infinite_money_use"]
      self.favorite_hobby = scratch["favorite_hobby"]
      self.political_affiliation = scratch["political_affiliation"]
      self.places_lived = scratch["places_lived"]
      self.important_relationship = scratch["important_relationship"]
      self.childhood_description = scratch["childhood_description"]
      self.mbti_type = scratch["mbti_type"]
      self.five_year_goal = scratch["five_year_goal"]
      self.biggest_fear = scratch["biggest_fear"]
      self.childhood_trauma = scratch["childhood_trauma"]
      self.intrusive_thoughts_frequency = scratch["intrusive_thoughts_frequency"]
      self.meaningful_event = scratch["meaningful_event"]
      self.cultural_tension_experience = scratch["cultural_tension_experience"]
      self.problem_solving_approach = scratch["problem_solving_approach"]
      self.religious_beliefs = scratch["religious_beliefs"]
      self.prized_possession = scratch["prized_possession"]
      self.career_aspiration = scratch["career_aspiration"]
      self.difficult_situation_method = scratch["difficult_situation_method"]
      self.friend_valued_trait = scratch["friend_valued_trait"]
      self.way_spend_100_dollars = scratch["way_spend_100_dollars"]
      self.family_income_level = scratch["family_income_level"]
      self.ethnicity = scratch["ethnicity"]
      self.primary_language = scratch["primary_language"]
      self.political_ideology = scratch["political_ideology"]
      self.political_party = scratch["political_party"]
      self.education = scratch["education"]
      self.race = scratch["race"]

      self.extraversion = float(scratch["extraversion"])
      self.agreeableness = float(scratch["agreeableness"])
      self.conscientiousness = float(scratch["conscientiousness"])
      self.neuroticism = float(scratch["neuroticism"])
      self.openness = float(scratch["openness"])

      self.fact_sheet = scratch["fact_sheet"]
      self.speech_pattern = scratch["speech_pattern"]
      self.self_description = scratch["self_description"]
      self.private_self_description = scratch["private_self_description"]


  def package(self): 
    """
    Packaging the agent's scratch memory for saving. 

    Parameters:
      None
    Returns: 
      packaged dictionary
    """
    curr_package = {}
    curr_package["name"] = self.name
    curr_package["age_group"] = self.age_group
    curr_package["gender"] = self.gender
    curr_package["grow_up_location"] = self.grow_up_location
    curr_package["most_time_activity"] = self.most_time_activity
    curr_package["important_value"] = self.important_value
    curr_package["closest_personality"] = self.closest_personality
    curr_package["social_context_action"] = self.social_context_action
    curr_package["infinite_money_use"] = self.infinite_money_use
    curr_package["favorite_hobby"] = self.favorite_hobby
    curr_package["political_affiliation"] = self.political_affiliation
    curr_package["places_lived"] = self.places_lived
    curr_package["important_relationship"] = self.important_relationship
    curr_package["childhood_description"] = self.childhood_description
    curr_package["mbti_type"] = self.mbti_type
    curr_package["five_year_goal"] = self.five_year_goal
    curr_package["biggest_fear"] = self.biggest_fear
    curr_package["childhood_trauma"] = self.childhood_trauma
    curr_package["intrusive_thoughts_frequency"] = self.intrusive_thoughts_frequency
    curr_package["meaningful_event"] = self.meaningful_event
    curr_package["cultural_tension_experience"] = self.cultural_tension_experience
    curr_package["problem_solving_approach"] = self.problem_solving_approach
    curr_package["religious_beliefs"] = self.religious_beliefs
    curr_package["prized_possession"] = self.prized_possession
    curr_package["career_aspiration"] = self.career_aspiration
    curr_package["difficult_situation_method"] = self.difficult_situation_method
    curr_package["friend_valued_trait"] = self.friend_valued_trait
    curr_package["way_spend_100_dollars"] = self.way_spend_100_dollars
    curr_package["family_income_level"] = self.family_income_level
    curr_package["ethnicity"] = self.ethnicity
    curr_package["primary_language"] = self.primary_language
    curr_package["political_ideology"] = self.political_ideology
    curr_package["political_party"] = self.political_party
    curr_package["education"] = self.education
    curr_package["race"] = self.race
    
    curr_package["extraversion"] = self.extraversion
    curr_package["agreeableness"] = self.agreeableness
    curr_package["conscientiousness"] = self.conscientiousness
    curr_package["neuroticism"] = self.neuroticism
    curr_package["openness"] = self.openness

    curr_package["fact_sheet"] = self.fact_sheet
    curr_package["speech_pattern"] = self.speech_pattern
    curr_package["self_description"] = self.self_description
    curr_package["private_self_description"] = self.private_self_description

    return curr_package


  def get_fullname(self):
    return f"{self.name}" 
