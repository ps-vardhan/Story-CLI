"""
LLM Interface for Story-CLI
Handles communication with Ollama for story generation.
"""

import subprocess
import json
import tempfile
import os
from typing import Dict, List, Optional
from pathlib import Path
import logging

class LLMInterface:
    def __init__(self, config_path: str = "config/game_config.json"):
        """Initialize the LLM interface with configuration."""
        self.config = self._load_config(config_path)
        self.model_name = self.config.get("ollama_model", "llama2:7b-chat")
        self.temperature = self.config.get("temperature", 0.8)
        self.max_tokens = self.config.get("max_tokens", 100)  # Reduced for faster responses
        self.context_length = self.config.get("context_length", 1024)  # Reduced for memory efficiency
        
        # Validate Ollama is available
        if not self._validate_ollama():
            raise ValueError("Ollama not found or not working. Please install Ollama first.")
            
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Config file {config_path} not found, using defaults")
            return {
                "ollama_model": "llama2:7b-chat",
                "temperature": 0.8,
                "max_tokens": 100,  # Reduced for faster responses
                "context_length": 1024,  # Reduced for memory efficiency
            }
    
    def _validate_ollama(self) -> bool:
        """Validate that Ollama is available and working."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logging.error(f"Ollama validation failed: {e}")
            return False
    
    def generate_story_continuation(self, prompt: str, context: str = "") -> str:
        """Generate story continuation using Ollama."""
        try:
            # Prepare the full prompt with context
            full_prompt = self._prepare_prompt(prompt, context)
            
            # Build Ollama command (model name comes first, then prompt)
            cmd = [
                "ollama", "run",
                self.model_name,
                full_prompt
            ]
            
            # Run Ollama
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # Increased timeout for model loading and generation
            )
            
            if result.returncode != 0:
                logging.error(f"Ollama error: {result.stderr}")
                return "The story continues with an unexpected turn of events..."
            
            # Extract the generated continuation
            output = result.stdout.strip()
            continuation = self._extract_continuation(output, full_prompt)
            return continuation
                
        except subprocess.TimeoutExpired:
            logging.error("Ollama timed out")
            return "The story continues with a moment of suspense..."
        except Exception as e:
            logging.error(f"Error generating story: {e}")
            return "The story continues with an unexpected development..."
    
    def _prepare_prompt(self, prompt: str, context: str = "") -> str:
        """Prepare the full prompt for the LLM."""
        if context:
            full_prompt = f"""Context: {context}

Story Prompt: {prompt}

Continue the story in 2-3 sentences, maintaining the established tone and style:"""
        else:
            full_prompt = f"""Story Prompt: {prompt}

Begin the story in 2-3 sentences, setting the scene and atmosphere:"""
            
        return full_prompt
    
    def _extract_continuation(self, output: str, original_prompt: str) -> str:
        """Extract the story continuation from Ollama output."""
        # Remove the original prompt from the output
        if original_prompt in output:
            continuation = output.split(original_prompt)[-1].strip()
        else:
            continuation = output.strip()
        
        # Clean up the continuation
        continuation = continuation.replace("Context:", "").replace("Story Prompt:", "").strip()
        
        # Limit to reasonable length (reduced for faster responses)
        if len(continuation) > 300:
            continuation = continuation[:300] + "..."
            
        return continuation if continuation else "The story continues with an interesting development..."
    
    def generate_initial_scene(self, main_genre: str, sub_genre: str) -> str:
        """Generate an initial scene based on genre selection."""
        # Load genre prompts
        try:
            with open("config/genre_prompts.json", 'r') as f:
                genre_prompts = json.load(f)
                
            prompt = genre_prompts.get(main_genre, {}).get(sub_genre, 
                f"Create an engaging opening scene for a {main_genre} story in a {sub_genre} setting.")
                
        except FileNotFoundError:
            prompt = f"Create an engaging opening scene for a {main_genre} story in a {sub_genre} setting."
        
        return self.generate_story_continuation(prompt)
    
    def test_connection(self) -> bool:
        """Test if the LLM interface is working properly."""
        try:
            test_response = self.generate_story_continuation("Test prompt")
            return len(test_response) > 0
        except Exception as e:
            logging.error(f"LLM interface test failed: {e}")
            return False 