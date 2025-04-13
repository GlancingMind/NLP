import re
import time
from response_patterns import get_response
from context_manager import ContextManager

class WitnessInterviewBot:
    def __init__(self, formal=True):
        self.formal = formal
        self.context = ContextManager()
        self.name = None
        
    def greet(self):
        print("""
            =============================
            NYPD Witness Interview System
            =============================
        """)

        greeting = "Hello, I'm Officer Davis. I'll be taking your statement today." if self.formal else "Hi there, I'm Officer Davis. I'm here to talk about what you saw."
        print(f"{greeting}")

        print("Please take your time and share as many details as you can remember.")
        print("You can end this interview anytime by typing 'exit' or 'quit'.")
        print("=============================")

    def process_input(self, user_input):
        # Check for exit command
        if user_input.lower() in ['exit', 'quit', 'end', 'stop']:
            return None
        
        # Save input to context
        self.context.add_user_statement(user_input)
        
        # Extract name if not already known
        if not self.name:
            # Enhanced name extraction with multiple patterns
            name_patterns = [
                r'my name is (\w+)',
                r"i'm (\w+)",
                r"i am (\w+)",
                r"(\w+) (is )?my name"
            ]
            
            for pattern in name_patterns:
                name_match = re.search(pattern, user_input.lower())
                if name_match:
                    self.name = name_match.group(1).capitalize()
                    self.context.add_fact("name", self.name)
                    break
        
        # Get appropriate response based on input and context
        response = get_response(user_input, self.context, formal=self.formal, name=self.name)
        
        # Add slight delay for natural feel
        time.sleep(0.5)
        
        # Save response to context
        self.context.add_bot_response(response)
        
        return response
    
    def run(self):
        self.greet()
        
        while True:
            user_input = input("\nYou: ").strip()
            response = self.process_input(user_input)
            
            if response is None:
                print("\nThank you for your statement. This concludes our interview.")
                if self.context.get_transcript_summary():
                    print("\nInterview Summary:")
                    print(self.context.get_transcript_summary())
                break
                
            print(f"\nOfficer Davis: {response}")

if __name__ == "__main__":
    print("Initializing witness interview system...")
    print("Select interview style:")
    print("1. Formal")
    print("2. Informal")
    
    style_choice = input("Enter your choice (1/2): ").strip()
    formal = True if style_choice != "2" else False
    
    bot = WitnessInterviewBot(formal=formal)
    bot.run()
