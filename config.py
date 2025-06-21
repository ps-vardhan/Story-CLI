"""
Configuration settings for the Story-CLI game.
"""

# Game Configuration
GAME_TITLE = "Story-CLI"
DEFAULT_MAIN_GENRE = "action"
DEFAULT_SUB_GENRE = "scifi"

# Game Settings
INITIAL_HEALTH = 100
INITIAL_STRENGTH = 10
INITIAL_INTELLIGENCE = 10
INITIAL_CHARISMA = 10

# Main Genres (3 main categories)
MAIN_GENRES = {
    "mystery": {
        "name": "Mystery",
        "description": "Solve puzzles and uncover secrets",
        "color": "blue"
    },
    "adventure": {
        "name": "Adventure", 
        "description": "Explore new worlds and face challenges",
        "color": "green"
    },
    "action": {
        "name": "Action",
        "description": "Fast-paced excitement and combat",
        "color": "red"
    }
}

# Sub Genres (5 sub-categories)
SUB_GENRES = {
    "fantasy": {
        "name": "Fantasy",
        "description": "Magical worlds and creatures",
        "color": "magenta"
    },
    "horror": {
        "name": "Horror",
        "description": "Fear and supernatural elements",
        "color": "dark_red"
    },
    "scifi": {
        "name": "Science Fiction",
        "description": "Futuristic technology and space",
        "color": "cyan"
    },
    "modern": {
        "name": "Modern",
        "description": "Present day settings",
        "color": "yellow"
    },
    "cosmic": {
        "name": "Cosmic",
        "description": "Cosmic horror and space mysteries",
        "color": "purple"
    }
}

# Core Game Mechanics
CORE_MECHANICS = {
    "move": {
        "name": "Move",
        "description": "Navigate through the world",
        "examples": ["go north", "walk to the door", "enter the building"]
    },
    "talk": {
        "name": "Talk",
        "description": "Interact with NPCs and the environment",
        "examples": ["speak to the merchant", "ask about the quest", "greet the guard"]
    },
    "fight": {
        "name": "Fight",
        "description": "Engage in combat",
        "examples": ["attack the enemy", "defend yourself", "use your weapon"]
    },
    "use": {
        "name": "Use Items",
        "description": "Interact with items and objects",
        "examples": ["pick up the key", "use the potion", "examine the map"]
    },
    "investigate": {
        "name": "Investigate",
        "description": "Search for clues and examine surroundings",
        "examples": ["search the room", "examine the body", "look for clues"]
    }
}

# Basic Actions
BASIC_ACTIONS = {
    "move": "You move in that direction.",
    "talk": "You attempt to communicate.",
    "fight": "You prepare for combat.",
    "use": "You interact with the item.",
    "investigate": "You search the area carefully."
}

# Memory System
MEMORY_TYPES = {
    "npc_interactions": {},
    "quest_progress": {},
    "location_discovery": {},
    "item_usage": {},
    "story_progress": {},
    "clues_found": {}
}

# Story Generation Settings
STORY_SETTINGS = {
    "chunk_size": 3,  # Number of lines to show at once
    "context_injection_interval": 5,  # Inject context every N interactions
    "max_response_length": 150,  # Maximum tokens per response
    "temperature": 0.8,  # Creativity level
    "top_p": 0.9  # Nucleus sampling parameter
} 