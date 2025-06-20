from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Dict, List, Optional
import json
import os
from config import (
    MODEL_CONFIGS,
    DEFAULT_MODEL,
    GENRES,
    BASIC_ACTIONS,
    CORE_MECHANICS,
    MEMORY_TYPES
)
import logging

# Set up logging to a file for background/non-game output
logging.basicConfig(filename='ai_dungeon.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class GameEngine:
    def __init__(self, genre: str):
        self.genre = genre
        # Game state
        self.current_scene = self._get_initial_scene()
        self.memory = {key: {} for key in MEMORY_TYPES.keys()}
        self.active_quests = []
        self.completed_quests = []

    def _get_initial_scene(self) -> str:
        """Generate the initial scene based on genre."""
        genre_info = GENRES.get(self.genre, GENRES["fantasy"])
        return genre_info["initial_scene"]

    def _identify_action_type(self, player_action: str) -> str:
        """Identify the type of action the player is attempting."""
        action = player_action.lower()
        
        for mechanic_type, mechanic_info in CORE_MECHANICS.items():
            for example in mechanic_info["examples"]:
                if example in action:
                    return mechanic_type
        
        # Default to the first matching word
        for mechanic_type in CORE_MECHANICS.keys():
            if mechanic_type in action:
                return mechanic_type
                
        return "unknown"

    def _update_memory(self, action_type: str, action: str, response: str):
        """Update the game's memory system based on the action and response."""
        if action_type == "talk":
            self.memory["npc_interactions"][action] = response
        elif action_type == "move":
            self.memory["location_discovery"][action] = response
        elif action_type == "use":
            self.memory["item_usage"][action] = response

    def generate_response(self, player_action: str, context: dict) -> str:
        """Generate an AI response based on player action and context using local model + few-shot prompting (stub)."""
        # TODO: Integrate with Ollama/Llama.cpp local model here
        # For now, return a simple response
        action_type = self._identify_action_type(player_action)
        response = BASIC_ACTIONS.get(action_type, "You attempt to perform that action.")
        self._update_memory(action_type, player_action, response)
        return response

    def update_game_state(self, new_scene: str, quest_update: dict = None):
        """Update the game state with new information."""
        self.current_scene = new_scene
        if quest_update:
            self.memory["quest_progress"].update(quest_update)

    def get_game_state(self) -> dict:
        """Get the current game state."""
        return {
            "current_scene": self.current_scene,
            "memory": self.memory,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests
        } 