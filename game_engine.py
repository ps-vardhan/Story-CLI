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
    def __init__(self, genre: str, game_mode: str, model_name: str = DEFAULT_MODEL):
        self.genre = genre
        self.game_mode = game_mode
        self.model_name = model_name
        self.model_config = MODEL_CONFIGS[model_name]
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.initialize_ai()
        
        # Game state
        self.current_scene = self._get_initial_scene()
        self.memory = {key: {} for key in MEMORY_TYPES.keys()}
        self.active_quests = []
        self.completed_quests = []

    def initialize_ai(self):
        """Initialize the AI model and tokenizer with support for finetuned models."""
        try:
            model_path = self.model_config["finetune_path"] if self.model_config["is_finetuned"] else self.model_config["name"]
            
            # Try to load finetuned model if specified
            if self.model_config["is_finetuned"] and os.path.exists(model_path):
                logging.info(f"Loading finetuned model from {model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForCausalLM.from_pretrained(model_path)
            else:
                logging.info(f"Loading base model {self.model_config['name']}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_config["name"])
                self.model = AutoModelForCausalLM.from_pretrained(self.model_config["name"])
            
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer
            )
        except Exception as e:
            logging.error(f"Error initializing AI model: {str(e)}")
            logging.info("Falling back to simple response generation")
            self.generator = None

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

    def generate_response(self, player_action: str, context: Dict) -> str:
        """Generate an AI response based on player action and context."""
        if self.generator is None:
            return self._generate_simple_response(player_action)

        # Identify the type of action
        action_type = self._identify_action_type(player_action)
        
        # Prepare the prompt with memory context
        prompt = self._prepare_prompt(player_action, context, action_type)
        
        try:
            # Generate response with model-specific parameters
            response = self.generator(
                prompt,
                max_length=self.model_config["max_length"],
                num_return_sequences=1,
                temperature=self.model_config["temperature"],
                top_p=self.model_config["top_p"],
                pad_token_id=self.tokenizer.eos_token_id
            )[0]["generated_text"]
            
            # Clean up the response
            response = self._clean_response(response, prompt)
            
            # Update memory
            self._update_memory(action_type, player_action, response)
            
            return response
            
        except Exception as e:
            logging.error(f"Error generating AI response: {str(e)}")
            return self._generate_simple_response(player_action)

    def _prepare_prompt(self, player_action: str, context: Dict, action_type: str) -> str:
        """Prepare the prompt for the AI model with memory context."""
        genre_info = GENRES.get(self.genre, GENRES["fantasy"])
        base_prompt = f"You are a {genre_info['name']} world narrator. The scene is: "
        current_scene = context.get("current_scene", self.current_scene)
        
        # Add memory context
        memory_context = ""
        if self.memory["npc_interactions"]:
            memory_context += "\nPrevious interactions: " + ", ".join(self.memory["npc_interactions"].keys())
        if self.memory["location_discovery"]:
            memory_context += "\nKnown locations: " + ", ".join(self.memory["location_discovery"].keys())
        
        # Format prompt based on model type
        if self.model_name == "distilgpt2":
            # DistilGPT2 works better with more concise prompts
            return f"{base_prompt}{current_scene}\nAction ({action_type}): {player_action}\nResponse:"
        else:
            # GPT2 can handle more detailed prompts
            return f"{base_prompt}{current_scene}{memory_context}\nPlayer action ({action_type}): {player_action}\nNarrator:"

    def _clean_response(self, response: str, prompt: str) -> str:
        """Clean up the AI-generated response."""
        # Remove the prompt from the response
        response = response[len(prompt):].strip()
        
        # Remove any incomplete sentences
        if response and response[-1] not in ".!?":
            response = response.rsplit(".", 1)[0] + "."
            
        return response

    def _generate_simple_response(self, player_action: str) -> str:
        """Generate a simple response when AI model is not available."""
        action_type = self._identify_action_type(player_action)
        return BASIC_ACTIONS.get(action_type, "You attempt to perform that action.")

    def update_game_state(self, new_scene: str, quest_update: Dict = None):
        """Update the game state with new information."""
        self.current_scene = new_scene
        if quest_update:
            self.memory["quest_progress"].update(quest_update)

    def get_game_state(self) -> Dict:
        """Get the current game state."""
        return {
            "current_scene": self.current_scene,
            "memory": self.memory,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests
        } 