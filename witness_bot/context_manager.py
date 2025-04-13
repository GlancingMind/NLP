import re
from collections import defaultdict

class ContextManager:
    def __init__(self):
        self.user_statements = []
        self.bot_responses = []
        self.facts = defaultdict(str)  # Store extracted facts about the witness/incident
        self.mentioned_topics = set()  # Track mentioned topics to avoid repetition
        
    def add_user_statement(self, statement):
        """Add a user statement to the conversation history"""
        self.user_statements.append(statement)
        self._extract_facts(statement)
        
    def add_bot_response(self, response):
        """Add a bot response to the conversation history"""
        self.bot_responses.append(response)
        
    def get_recent_user_statements(self, count=3):
        """Get the most recent user statements"""
        return self.user_statements[-count:] if self.user_statements else []
        
    def get_recent_bot_responses(self, count=3):
        """Get the most recent bot responses"""
        return self.bot_responses[-count:] if self.bot_responses else []
        
    def add_fact(self, key, value):
        """Explicitly add a fact to the context"""
        self.facts[key] = value
        self.mentioned_topics.add(key)
        
    def get_fact(self, key):
        """Retrieve a stored fact"""
        return self.facts.get(key, "")
        
    def _extract_facts(self, statement):
        """Extract potential facts from user statements"""
        # Try to extract time information
        time_match = re.search(r'at (\d+[:.]\d+|noon|midnight|dawn|dusk)', statement.lower())
        if time_match:
            self.facts['time'] = time_match.group(1)
            self.mentioned_topics.add('time')
            
        # Try to extract location information
        location_match = re.search(r'at (the |a )?([\w\s]+) (street|avenue|road|park|building|store|shop)', statement.lower())
        if location_match:
            self.facts['location'] = location_match.group(2) + " " + location_match.group(3)
            self.mentioned_topics.add('location')
            
        # Try to extract person descriptions
        person_match = re.search(r'(man|woman|person|individual) (was |looked |appeared )?([\w\s]+)', statement.lower())
        if person_match:
            self.facts['person_description'] = person_match.group(3)
            self.mentioned_topics.add('person')
            
        # Try to extract event type
        event_match = re.search(r'(robbery|theft|assault|attack|shooting|murder|crime)', statement.lower())
        if event_match:
            self.facts['event_type'] = event_match.group(1)
            self.mentioned_topics.add('event')
    
    def get_transcript_summary(self):
        """Generate a simple summary of the conversation"""
        if not self.user_statements:
            return "No interview data recorded."
            
        summary = []
        
        # Add known facts
        if self.facts:
            summary.append("EXTRACTED INFORMATION:")
            for key, value in self.facts.items():
                if value:  # Only include non-empty values
                    summary.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        # Add conversation statistics
        summary.append(f"\nINTERVIEW STATISTICS:")
        summary.append(f"- Total witness statements: {len(self.user_statements)}")
        summary.append(f"- Total questions asked: {len(self.bot_responses)}")
        
        # Calculate average statement length as a simple metric
        if self.user_statements:
            avg_length = sum(len(stmt.split()) for stmt in self.user_statements) / len(self.user_statements)
            summary.append(f"- Average statement length: {avg_length:.1f} words")
        
        # Add topics mentioned
        if self.mentioned_topics:
            summary.append(f"- Topics covered: {', '.join(self.mentioned_topics)}")
        
        return "\n".join(summary)
