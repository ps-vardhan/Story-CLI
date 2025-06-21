from typing import Dict, List, Optional
import json
import os
from config import (
    MAIN_GENRES,
    SUB_GENRES,
    DEFAULT_MAIN_GENRE,
    DEFAULT_SUB_GENRE,
    BASIC_ACTIONS,
    CORE_MECHANICS,
    MEMORY_TYPES,
    STORY_SETTINGS
)
import logging
from story_buffer import StoryBuffer
from llm_interface import LLMInterface

# Set up logging to a file for background/non-game output
logging.basicConfig(filename='story_cli.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class GameEngine:
    def __init__(self, main_genre: str, sub_genre: str):
        self.main_genre = main_genre
        self.sub_genre = sub_genre
        self.genre_combination = f"{main_genre}_{sub_genre}"
        
        # Initialize systems
        self.story_buffer = StoryBuffer()
        self.llm_interface = LLMInterface()
        
        # Game state
        self.current_scene = ""
        self.memory = {key: {} for key in MEMORY_TYPES.keys()}
        self.active_quests = []
        self.completed_quests = []
        self.player_stats = {
            "health": 100,
            "strength": 10,
            "intelligence": 10,
            "charisma": 10
        }
        
        # Initialize the story
        self._initialize_story()

    def _initialize_story(self):
        """Initialize the story with an opening scene."""
        try:
            # Generate initial scene using LLM
            initial_scene = self.llm_interface.generate_initial_scene(self.main_genre, self.sub_genre)
            self.current_scene = initial_scene
            
            # Add to story buffer
            self.story_buffer.add_story_segment(initial_scene, "story")
            
            logging.info(f"Story initialized for {self.genre_combination}")
            
        except Exception as e:
            logging.error(f"Failed to initialize story: {e}")
            # Fallback scene
            self.current_scene = f"You find yourself in a {self.sub_genre} world, ready for {self.main_genre}."
            self.story_buffer.add_story_segment(self.current_scene, "story")

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
        elif action_type == "investigate":
            self.memory["clues_found"][action] = response

    def generate_response(self, player_action: str, context: dict = None) -> str:
        """Generate an AI response based on player action and context using LLM."""
        try:
            # Add player action to buffer
            self.story_buffer.add_player_action(player_action)
            
            # Get context for LLM
            llm_context = ""
            if self.story_buffer.should_inject_context():
                llm_context = self.story_buffer.get_context_for_llm()
            
            # Create prompt based on action type
            action_type = self._identify_action_type(player_action)
            prompt = self._create_action_prompt(player_action, action_type)
            
            # Generate response using LLM
            response = self.llm_interface.generate_story_continuation(prompt, llm_context)
            
            # Add response to buffer
            self.story_buffer.add_ai_response(response)
            
            # Update memory
            self._update_memory(action_type, player_action, response)
            
            # Update current scene
            self.current_scene = response
            
            return response
            
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            # Fallback response
            fallback = BASIC_ACTIONS.get(action_type, "You attempt to perform that action.")
            self.story_buffer.add_ai_response(fallback)
            return fallback

    def _create_action_prompt(self, player_action: str, action_type: str) -> str:
        """Create a prompt for the LLM based on the player's action."""
        genre_context = f"{self.main_genre} story in a {self.sub_genre} setting"
        
        if action_type == "move":
            return f"In this {genre_context}, the player {player_action}. Describe what happens next in 2-3 sentences."
        elif action_type == "talk":
            return f"In this {genre_context}, the player {player_action}. Describe the response or conversation in 2-3 sentences."
        elif action_type == "fight":
            return f"In this {genre_context}, the player {player_action}. Describe the combat or conflict in 2-3 sentences."
        elif action_type == "use":
            return f"In this {genre_context}, the player {player_action}. Describe the result in 2-3 sentences."
        elif action_type == "investigate":
            return f"In this {genre_context}, the player {player_action}. Describe what they discover in 2-3 sentences."
        else:
            return f"In this {genre_context}, the player {player_action}. Continue the story in 2-3 sentences."

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
            "completed_quests": self.completed_quests,
            "player_stats": self.player_stats,
            "story_buffer_stats": self.story_buffer.get_stats()
        }
    
    def get_recent_story_chunks(self, num_chunks: Optional[int] = None) -> List[str]:
        """Get recent story chunks for display."""
        return self.story_buffer.get_recent_story_chunks(num_chunks)
    
    def get_story_summary(self) -> str:
        """Get a summary of the story so far."""
        return self.story_buffer.get_story_summary()
    
    def save_game(self, filename: str = "saved_game.json"):
        """Save the current game state."""
        game_data = {
            "main_genre": self.main_genre,
            "sub_genre": self.sub_genre,
            "current_scene": self.current_scene,
            "memory": self.memory,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "player_stats": self.player_stats
        }
        
        with open(filename, 'w') as f:
            json.dump(game_data, f, indent=2)
        
        # Also save story buffer
        self.story_buffer.save_story("saved_story.json")
    
    def load_game(self, filename: str = "saved_game.json"):
        """Load a saved game state."""
        try:
            with open(filename, 'r') as f:
                game_data = json.load(f)
            
            self.main_genre = game_data.get("main_genre", self.main_genre)
            self.sub_genre = game_data.get("sub_genre", self.sub_genre)
            self.current_scene = game_data.get("current_scene", self.current_scene)
            self.memory = game_data.get("memory", self.memory)
            self.active_quests = game_data.get("active_quests", self.active_quests)
            self.completed_quests = game_data.get("completed_quests", self.completed_quests)
            self.player_stats = game_data.get("player_stats", self.player_stats)
            
            # Load story buffer
            self.story_buffer.load_story("saved_story.json")
            
        except FileNotFoundError:
            logging.warning(f"Save file {filename} not found")
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in save file {filename}") 