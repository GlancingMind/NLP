import re
import random

class PalChatbot:
    def __init__(self):
        self.running = True

        self.keyword_patterns = {
            # Generalized pattern for questions directed at the bot ("you")
            r"\b(how\s+are|what\s+about|and)\s+you\b\??|\bare\s+you\s+(ok|okay|alright|well|doing)\b\??": [
                "Thanks for asking about me! As a program, I don't have feelings, but I'm functioning well. How are you feeling today?",
                "That's kind of you to ask! I'm just a chatbot, but I'm ready to listen. What's on your mind?",
                "Thank you for checking in! I'm operating as expected. More importantly, how are you doing right now?",
                "I appreciate you asking about me! I'm here to focus on you, though. How are things with you?",
            ],
            r"\bsad\b": [
                "It sounds like you’re feeling sad. Would you like to talk more about that?",
                "I'm sorry you feel sad. Can you tell me what's bothering you?",
            ],
            r"\bhappy\b": [
                "You seem happy! That's wonderful. Care to share more?",
                "It's great to see you're feeling happy. What's making you smile today?",
            ],
            r"\bmother\b": [
                "Tell me more about your family. Do you have any particular memories in mind?",
                "What does your mother mean to you in your life?"
            ],
            r"\bfather\b": [
                "What's your relationship like with your father?",
                "How do you feel about your father?"
            ],
            r"\blonely\b": [
                "It can be tough to feel lonely. What's on your mind?",
                "Sometimes loneliness hurts. Would sharing help?"
            ],
            r"\bbored\b": [
                "What do you enjoy doing when you're bored?",
                "Being bored can be challenging. What usually interests you?"
            ],
            r"\bwhy\b": [
                "Why do you think that might be? Please elaborate.",
                "Can you explore further why that is so?"
            ],
            r"\bangry\b": [
                "It sounds like you're feeling quite angry. What's causing these strong feelings?",
                "Anger can be overwhelming. What's making you feel this way?"
            ],
            r"\bbecause\b": [
                "Is that the main reason you feel this way?",
                "Could you tell me more about why you feel that way?"
            ],
            r"\bI\s+don'?t\s+know\b": [
                "Sometimes it can be hard to understand our feelings. Can you tell me more?",
                "Not knowing is okay. What do you think might help you understand better?"
            ],
            r"\bremember\b": [
                "Do you often recall this memory? How does it impact you?",
                "That memory seems important. Could you describe it further?"
            ],
            r"\bfeel\b": [
                "Can you describe that feeling in more detail?",
                "What does that feeling bring up for you?"
            ],
            r"\bschool\b": [
                "School can be challenging. How are you coping with your studies?",
                "It sounds like school might be overwhelming. What's on your mind regarding your classes?",
                "Tell me more about your school experiences. What subjects interest you the most?",
                "School life has its ups and downs. How are you managing your workload?",
                "Is there something specific about school that’s affecting your mood?"
            ],
            r"\bhomework\b": [
                "Homework sometimes feels like too much. What aspect is causing you stress?",
                "Are you finding your homework challenging or just overwhelming?",
                "Tell me about your homework. Is there a particular subject giving you trouble?",
                "Homework can pile up quickly. How are you balancing it with your free time?",
                "Does homework stress you out, or are you finding it manageable?"
            ],
            r"\b(subjects|math|science|history|english|biology|chemistry|physics|literature|geography|art|music|physical education|computer science|economics|philosophy|psychology|social studies|languages|drama|coding)\b": [
                "How do you feel about your classes and subjects?",
                "Do any particular subjects excite you or make you anxious?",
                "Tell me more about your experience with your favorite subject.",
                "It seems your subjects affect your mood. Which one stands out most?",
                "Are there any subjects you look forward to or dread?"
            ],
            r"\bsports\b": [
                "Do you enjoy playing sports? Which one is your favorite?",
                "Sports can be a great outlet. What activities do you engage in?",
                "Tell me about your experience with sports. Are you part of any teams?",
                "How do you feel after a good workout or game?",
                "Is there a sport that helps you relieve stress or feel energized?"
            ],
            r"\bhobbies\b": [
                "Hobbies can be very fulfilling. What activities are you passionate about?",
                "It's great to have hobbies. What do you enjoy doing in your free time?",
                "Tell me more about your hobbies. How do they make you feel?",
                "Hobbies offer a creative escape. What are yours?",
                "How do your hobbies help you relax or express yourself?"
            ],
            r"\bfriends\b": [
                "Friends are important. How are your relationships these days?",
                "Do you feel supported by the people around you?",
                "Tell me more about your friendships. Are they a source of comfort?",
                "How have your interactions with friends influenced your mood lately?",
                "Is there something about your social life that you'd like to share?"
            ],
            r"\bmovies\b": [
                "Movies can be a great escape. Have you seen any good ones lately?",
                "What kind of movies do you enjoy, and why do they resonate with you?",
                "Tell me about a movie that has left an impression on you.",
                "Do movies help you process your feelings? What’s your favorite film?",
                "How do films influence your mood or spark your imagination?"
            ],
            r"\bbooks\b": [
                "Books can transport us to different worlds. What are you reading lately?",
                "Do you find solace in books? Tell me about your favorite one.",
                "Literature often reflects our inner thoughts. Which book has impacted you recently?",
                "How do books help you understand your feelings better?",
                "Is there a particular book that has offered you comfort or insight?"
            ],
            r"\bdeath\b": [
                "Death is a heavy topic. How are you processing these thoughts?",
                "Losing someone can be profoundly painful. Would you like to share your feelings?",
                "It's normal to be troubled by thoughts of death. Tell me more about how you feel.",
                "Such thoughts can be overwhelming. What specifically makes you think about death?",
                "Death touches us all in different ways. How has it affected your outlook on life?"
            ]
        }

        self.fallback_responses = [
            "Tell me more.",
            "I see, please continue.",
            "That's interesting, can you elaborate?",
            "Good, please go on.",
        ]

    def craft_dynamic_response(self, text, subject, verb, obj, adj):
        """
        Create a dynamic response using extracted components with more variety.
        """
        # Enhanced logic based on extracted components with multiple response options
        response_templates = []

        if adj and subject and verb and obj:
            response_templates = [
                f"It sounds like you're feeling {adj} regarding {subject} {verb} {obj}. Could you elaborate?",
                f"Feeling {adj} when {subject} {verb} {obj} seems significant. What's behind that?",
                f"Why do you associate feeling {adj} with {subject} {verb} {obj}?",
            ]
        elif adj and subject and verb: # e.g., "I am happy because..." (verb might be 'am')
             response_templates = [
                 f"Why do you feel {adj} when you say '{subject} {verb}'?",
                 f"What leads you to feel {adj} in that situation ({subject} {verb})?",
                 f"Tell me more about feeling {adj} when {subject} {verb}.",
             ]
        elif subject and verb and obj:
            response_templates = [
                f"Why do you think {subject} {verb} {obj}?",
                f"What comes to mind when you say '{subject} {verb} {obj}'?",
                f"Tell me more about {subject} {verb} {obj}.",
                f"How does '{subject} {verb} {obj}' make you feel?",
            ]
        elif adj and subject: # Handle cases like "I am sad", "I feel lonely"
             response_templates = [
                 f"Why do you feel {adj}?",
                 f"What makes you say you are {adj}?",
                 f"Tell me more about feeling {adj}.",
                 f"When did you start feeling {adj}?",
             ]
        elif subject and verb:
             response_templates = [
                 f"Can you elaborate on '{subject} {verb}'?",
                 f"What does '{subject} {verb}' mean to you?",
                 f"Tell me more about why {subject} {verb}.",
             ]
        elif verb and obj:
             response_templates = [
                 f"What makes '{verb} {obj}' significant to you?",
                 f"How do you feel about '{verb} {obj}'?",
                 f"Tell me more about '{verb} {obj}'.",
             ]
        elif adj: # Only adjective detected
             response_templates = [
                 f"Tell me more about feeling {adj}.",
                 f"You mentioned feeling {adj}. Can you expand on that?",
                 f"What's causing you to feel {adj}?",
             ]
        elif obj: # Only object detected (less common, but possible)
            response_templates = [
                f"You mentioned {obj}. How does that relate to how you're feeling?",
                f"What about {obj} is on your mind?",
                f"Tell me more concerning {obj}.",
            ]

        if response_templates:
            return random.choice(response_templates)

        # If no specific component combination matched well, return None
        return None

    def analyze_and_respond(self, text):
        # Split input into sentences and process the first meaningful one for dynamic response
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

        for pattern, responses in self.keyword_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                print(random.choice(responses))
                return True

        # If no patterns matched at all, use a fallback response and signal that no specific response was found
        return False 

    def run(self):
        print("Hello I'm Pal! I'm here to listen and help you with your feelings. Feel free to share what's on your mind.")
        print("If you want to exit, just type 'exit'.")
        while self.running:
            text = input("You: ")
            if text.strip().lower() == "exit":
                self.running = False
                continue
            responded = self.analyze_and_respond(text)
            if not responded:
                print("Pal: ", random.choice(self.fallback_responses))

if __name__ == "__main__":
    PalChatbot().run()