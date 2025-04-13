import re
import random
from english_dict import EnglishDictionary, Category
import time

class PalChatbot:
    def __init__(self):
        self.running = True
        self.debug = True
        self.dictionary = EnglishDictionary()  # Initialize EnglishDictionary

    def say(self, text):
        """
        Print the text to the console.
        """
        print(f"Pal: {text}")

    def ask(self, prompt=""):
        """
        Print the text to the console and return user input.
        """
        self.say(prompt)
        return input("You: ").strip()

    def extract_subject_verb_object(self, sentence):
        """
        Extract subject, verb, object, and adjective from a sentence using the EnglishDictionary.
        """
        words = sentence.lower().split()  # Convert to lower for case-insensitive matching
        subject, verb, obj, adj = None, None, None, None
        found_subject = False
        found_verb = False
        found_obj = False
        i = 0
        while i < len(words):
            word = words[i]
            # Check for "the" + known object pattern first
            if word == "the" and i + 1 < len(words) and words[i+1] in self.dictionary.lookup(Category.OBJECTS) and not found_subject:
                subject = f"the {words[i+1]}"
                found_subject = True
                i += 1  # Skip the next word as it's part of the subject
            elif word in self.dictionary.lookup(Category.SUBJECTS) and not found_subject:
                subject = word
                found_subject = True
            elif word in self.dictionary.lookup(Category.VERBS) and found_subject and not found_verb:  # Verb usually follows subject
                verb = word
                found_verb = True
            elif word in self.dictionary.lookup(Category.OBJECTS) and found_verb and not found_obj and (subject is None or word != subject.split()[-1]):
                obj = word
                found_obj = True
            elif word in self.dictionary.lookup(Category.ADJECTIVES) and not adj:  # Adjective can appear anywhere
                adj = word
            i += 1

        # Fallback if strict order fails but components exist (excluding "the" check here)
        if not subject: subject = next((w for w in words if w in self.dictionary.lookup(Category.SUBJECTS)), None)
        if not verb: verb = next((w for w in words if w in self.dictionary.lookup(Category.VERBS)), None)
        if not obj: obj = next((w for w in words if w in self.dictionary.lookup(Category.OBJECTS) and (subject is None or w != subject.split()[-1])), None)
        if not adj: adj = next((w for w in words if w in self.dictionary.lookup(Category.ADJECTIVES)), None)

        # Debug output
        if self.debug:
            print(f"DEBUG: Detected - Subject: {subject}, Verb: {verb}, Object: {obj}, Adjective: {adj}")

        return subject, verb, obj, adj

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

    def normalize_text(self, text):
        """
        Normalize text by replacing shortforms with their long forms.
        """
        contractions = {
            "i'm": "I am",
            "you're": "you are",
            "he's": "he is",
            "she's": "she is",
            "it's": "it is",
            "we're": "we are",
            "they're": "they are",
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "didn't": "did not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "i've": "I have",
            "you've": "you have",
            "we've": "we have",
            "they've": "they have",
            "i'll": "I will",
            "you'll": "you will",
            "he'll": "he will",
            "she'll": "she will",
            "it'll": "it will",
            "we'll": "we will",
            "they'll": "they will",
            "i'd": "I would",
            "you'd": "you would",
            "he'd": "he would",
            "she'd": "she would",
            "we'd": "we would",
            "they'd": "they would",
        }
        for shortform, longform in contractions.items():
            text = re.sub(rf"\b{shortform}\b", longform, text, flags=re.IGNORECASE)
        return text

    def analyze_and_respond(self, text):
        # Normalize the input text
        text = self.normalize_text(text)

        # Split input into sentences and process the first meaningful one for dynamic response
        sentences = [s for s in re.split(r'[.!?]+\s*', text) if s.strip()]
        processed_dynamically = False
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Extract components from the sentence
            subject, verb, obj, adj = self.extract_subject_verb_object(sentence)

            # Try crafting a dynamic response (component-based)
            dynamic_response = self.craft_dynamic_response(sentence, subject, verb, obj, adj)

            if dynamic_response:
                self.ask(dynamic_response)
                processed_dynamically = True
                break # Respond based on the first sentence that yields a dynamic response

        if processed_dynamically:
            return True

        # If no dynamic response was generated, check keyword patterns
        return False # Signal that no specific response was found, fallback needed

    def introduce(self, max_introduction_attempts=2):
        """
        Introduce the chatbot and ask for the user's name.
        """
        name = None
        introduction_attempts = 0

        intoduction_patterns = [
            r"i[' ]?m (\w+)", # TODO: not necessary due to the normalization?
            r"i am (\w+)",
            r"you can call me (\w+)",
            r"my name is (\w+)",
            r"it's (\w+)",
            r"this is (\w+)",
            r"i am called (\w+)",
            r"they call me (\w+)",
            r"the name's (\w+)",
            r"^(\w+)$",
        ]

        user_response = self.ask("Hello! I'm Pal. What's your name?")
        while not name:
            introduction_attempts += 1

            for pattern in intoduction_patterns:
                match = re.search(pattern, user_response, re.IGNORECASE)
                if match:
                    name = match.group(1)
                    break

            if not name:
                user_response = self.ask(random.choice([
                    "Sorry, I couldn't catch your name. Could you please say it again?",
                    "Hmm, I missed that. What's your name again?",
                    "Oh, I didn't quite get that. Could you tell me your name once more?",
                    "My apologies, I didn't catch your name. Could you repeat it for me?"
                ]))
                print(f"DEBUG: User response: {user_response}")
                continue

            confirmation = self.ask(f"Did I get that right? Your name is {name}, correct?").lower()
            if confirmation not in ["yes", "y", "right", "correct", "true", "yeah"]:
                name = None
                if introduction_attempts > max_introduction_attempts:
                    return None
                user_response = self.ask(random.choice([
                    "Oh, I see. then tell me your name again, please.",
                    "Alright, then please repeat your name.",
                    "Upsi, then please share your name once more.",
                    "My apologies, I seem to have missed your name. Please say it again.",
                    "Oh, I see. then tell me your name again, please.",
                ]))

        return name

    def run(self):
        fallback_responses = [
            "Tell me more.",
            "I see, please continue.",
            "That's interesting, can you elaborate?",
            "Good, please go on.",
        ]

        name = self.introduce(max_introduction_attempts=2)

        if name:
            self.say(f"Nice to meet you, {name}! Let's get started. If you want to exit, just type 'exit'.")
        else:
            self.say(random.choice([
                "Oh boy... You know what? Let's just scratch the introduction and continue with conversation. If you want to exit, just type 'exit'.",
                "Oh no. :-( Let's just skip the formalities and dive into the conversation! If you want to exit, just type 'exit'.",
                "My apologies, that I couldn't get your name yet again. But no worries, let's move on to the important part! For your information. If you want to exit, just type 'exit'.",
            ]))

        user_input = self.ask("So... how are you doing today? :-)")
        while self.running:
            if user_input.lower() == "exit":
                self.running = False
                continue

            responded = self.analyze_and_respond(user_input)
            if not responded:
                self.ask(random.choice(fallback_responses))

if __name__ == "__main__":
    PalChatbot().run()