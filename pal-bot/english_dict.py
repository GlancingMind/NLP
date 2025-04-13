from enum import Enum

class Category(Enum):
    SUBJECTS = "subjects"
    VERBS = "verbs"
    OBJECTS = "objects"
    ADJECTIVES = "adjectives"

class EnglishDictionary:
    def __init__(self):
        self.subjects = [
            "I", "he", "she", "we", "they", "it", "my", "you", "someone", "everyone", "nobody",
            "people", "children", "parents", "students", "teachers", "animals", "friends", "neighbors"
        ]
        self.verbs = [
            "am", "is", "are", "feel", "like", "love", "hate", "remember", "think", "makes",
            "want", "say", "see", "need", "know", "believe", "run", "walk", "write", "read",
            "speak", "listen", "eat", "drink", "play", "work", "sleep", "study", "help", "create"
        ]
        self.objects = [
            "school", "homework", "sports", "friends", "movies", "books", "death", "life",
            "food", "music", "family", "phone", "internet", "job", "car", "house", "garden",
            "computer", "game", "city", "country", "ocean", "mountain", "river", "forest", "sky"
        ]
        self.adjectives = [
            "happy", "sad", "angry", "bored", "lonely", "excited", "tired", "confused",
            "frustrated", "nervous", "anxious", "thrilled", "beautiful", "ugly", "strong",
            "weak", "fast", "slow", "smart", "kind", "brave", "funny", "serious", "friendly"
        ]

    def lookup(self, category: Category):
        """
        Lookup words by category.

        :param category: The category to look up (Category Enum).
        :return: List of words in the specified category or an empty list if the category is invalid.
        """
        return getattr(self, category.value, [])