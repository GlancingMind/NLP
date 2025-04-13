import re
import random

# Base patterns for matching user input
PATTERNS = [
    # Personal details patterns
    (r'my name is (\w+)', [
        "Thank you, {0}. Could you tell me about what you witnessed?", 
        "Nice to meet you, {0}. What brings you here today?",
        "Hello {0}, I appreciate you coming in. Can you share what happened?"
    ]),
    (r"i'?m (\w+)", [
        "Thank you, {0}. Could you tell me what you observed?",
        "Hello {0}, please share what you witnessed."
    ]),
    
    # Event description patterns
    (r'(robbery|theft|assault|attack|crime|shooting|fight)', [
        "Could you describe the {0} in more detail?",
        "What did you notice during the {0}?",
        "Tell me more about this {0}. What exactly did you see?"
    ]),
    
    # Witnessed action patterns
    (r'i (saw|witnessed|observed) (.*)', [
        "Can you elaborate on what you {0} regarding {1}?",
        "When you {0} {1}, where exactly were you standing?",
        "What details do you remember most clearly about {1}?"
    ]),
    
    # Location patterns
    (r'(at|in|near) (the |a )?([\w\s]+)', [
        "What else did you notice while you were {0} {2}?",
        "Could you describe the surroundings {0} {2}?",
        "How many people were present {0} {2}?"
    ]),
    
    # Time patterns
    (r'(at|around|about) (\d+[:.]\d+|noon|midnight|dawn|dusk|morning|evening|night)', [
        "What exactly occurred {0} {1}?",
        "What did you observe {0} {1}?",
        "How was the visibility {0} {1}?"
    ]),
    
    # Person description patterns
    (r'(man|woman|person|guy|individual|suspect) (was|is|had|with) (.*)', [
        "Could you describe this person's appearance in more detail?",
        "Did you notice any distinctive features about this {0}?",
        "Would you recognize this {0} if you saw them again?"
    ]),
    
    # Emotion patterns
    (r'(scared|afraid|nervous|worried|anxious|terrified)', [
        "It's normal to feel {0}. Take your time. What else do you remember?",
        "I understand this is difficult. When you felt {0}, what did you observe?",
        "Many witnesses feel {0} in these situations. What happened next?"
    ]),
    
    # Fallback patterns for generic inputs
    (r'.*', [
        "Could you elaborate on that?", 
        "What else do you remember about the incident?", 
        "Please continue...", 
        "How did you feel when that happened?",
        "What happened next?",
        "Can you describe that in more detail?"
    ])
]

# Formal and informal response variations
REFLECTIVE_PROMPTS = {
    'formal': [
        "Could you tell me more about that?",
        "Please elaborate on what you just mentioned.",
        "What other details do you recall about this?",
        "How did you proceed after that?",
        "Could you describe that in more detail?"
    ],
    'informal': [
        "Can you tell me more about that?",
        "What else do you remember?",
        "And then what happened?",
        "How did that make you feel?",
        "Anything else you noticed?"
    ]
}

def get_response(user_input, context, formal=True, name=None):
    """Generate a response based on the user's input and conversation context"""
    style = 'formal' if formal else 'informal'
    
    # Personalize with name if available
    name_prefix = f"{name}, " if name else ""
    
    # Check if the input is too short or vague
    if len(user_input.split()) < 3:
        return f"{name_prefix}could you provide more details please?"
    
    # Check if we're repeating ourselves too much
    recent_responses = context.get_recent_bot_responses(3)
    user_statements = context.get_recent_user_statements(3)
    
    # Check for repeated user statements
    if user_input in user_statements:
        return f"{name_prefix}I notice you've mentioned that before. Is there anything else you can add?"
    
    # Extract key facts from context for potential use in response
    context_facts = {
        "location": context.get_fact("location"),
        "time": context.get_fact("time"),
        "person_description": context.get_fact("person_description")
    }
    
    # Try to match patterns
    for pattern, responses in PATTERNS:
        match = re.search(pattern, user_input.lower())
        if match:
            # Format the response with captured groups
            response_template = random.choice(responses)
            try:
                # Replace placeholders with matched groups
                response = response_template.format(*match.groups())
                
                # Add name to response occasionally (50% chance if name is known)
                if name and random.random() > 0.5:
                    response = f"{name}, {response[0].lower() + response[1:]}"
                
                # Reference previously mentioned facts occasionally
                for fact_key, fact_value in context_facts.items():
                    if fact_value and random.random() > 0.7:  # 30% chance to reference a known fact
                        if fact_key == "location" and "location" not in response.lower():
                            response += f" Was this still at {fact_value}?"
                        elif fact_key == "time" and "time" not in response.lower():
                            response += f" Was this still around {fact_value}?"
                
            except IndexError:
                # If formatting fails, use the template as is
                response = response_template
                
            # Avoid repeating the exact same response
            if response in recent_responses:
                # Add a reflective prompt instead
                base_prompt = random.choice(REFLECTIVE_PROMPTS[style])
                response = f"{name_prefix}{base_prompt}"
                
            return response
    
    # Default response if no pattern matches (shouldn't typically reach here due to catch-all pattern)
    base_prompt = random.choice(REFLECTIVE_PROMPTS[style])
    return f"{name_prefix}{base_prompt}"
