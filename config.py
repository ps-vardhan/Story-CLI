"""
Configuration settings for the AI Dungeon CLI game.
"""

# Game Configuration
GAME_TITLE = "AI Dungeon CLI"
DEFAULT_GENRE = "fantasy"

# Game Settings
INITIAL_HEALTH = 100
INITIAL_STRENGTH = 10
INITIAL_INTELLIGENCE = 10
INITIAL_CHARISMA = 10

# Available Genres
GENRES = {
    "fantasy": {
        "name": "Fantasy",
        "description": "A world of magic, dragons, and medieval adventure",
        "initial_scene": "You find yourself in a medieval tavern. The air is thick with the smell of mead and wood smoke."
    },
    "scifi": {
        "name": "Science Fiction",
        "description": "A futuristic world of space travel and advanced technology",
        "initial_scene": "You wake up in a cryogenic pod aboard a spaceship. The ship's AI announces your revival."
    },
    "horror": {
        "name": "Horror",
        "description": "A world of mystery, fear, and supernatural elements",
        "initial_scene": "You stand in an abandoned mansion. The floorboards creak beneath your feet."
    },
    "modern": {
        "name": "Modern",
        "description": "A contemporary world of everyday life and adventure",
        "initial_scene": "You're in a bustling city street. People rush past you, lost in their own worlds."
    },
    "apocalyptic": {
        "name": "Apocalyptic",
        "description": "A world after civilization's collapse, where survival is the ultimate goal",
        "initial_scene": "You emerge from your shelter into a desolate wasteland. The ruins of civilization stretch before you."
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "description": "A high-tech, low-life future where corporations rule and technology is everywhere",
        "initial_scene": "Neon lights flicker through the rain as you navigate the crowded streets of the megacity."
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
    }
}

# Basic Actions
BASIC_ACTIONS = {
    "move": "You move in that direction.",
    "talk": "You attempt to communicate.",
    "fight": "You prepare for combat.",
    "use": "You interact with the item."
}

# Memory System
MEMORY_TYPES = {
    "npc_interactions": {},
    "quest_progress": {},
    "location_discovery": {},
    "item_usage": {}
} 