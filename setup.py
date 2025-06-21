#!/usr/bin/env python3
"""
Story-CLI Setup Script
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import logging

class GameSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_dir = self.project_root / "config"
        
    def print_status(self, message):
        print(f"[SETUP] {message}")
        
    def run_command(self, command, cwd=None):
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.print_status(f"Error running: {command}")
                self.print_status(f"Error: {result.stderr}")
                return False
            return True
        except Exception as e:
            self.print_status(f"Exception running {command}: {e}")
            return False
    
    def install_python_dependencies(self):
        self.print_status("Installing Python dependencies...")
        
        if not self.run_command("pip install -r requirements.txt"):
            self.print_status("Failed to install Python dependencies")
            return False
            
        self.print_status("Python dependencies installed successfully")
        return True
    
    def check_ollama(self):
        self.print_status("Checking Ollama installation...")
        
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                self.print_status("Ollama is available")
                return True
            else:
                self.print_status("Ollama not found. Please install Ollama first.")
                return False
        except Exception as e:
            self.print_status(f"Ollama check failed: {e}")
            self.print_status("Please install Ollama from https://ollama.ai")
            return False
    
    def pull_model(self):
        self.print_status("Pulling Ollama model...")
        
        try:
            result = subprocess.run(
                ["ollama", "pull", "llama2:7b-chat"],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                self.print_status("Ollama model pulled successfully")
                return True
            else:
                self.print_status(f"Failed to pull model: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_status("Model pull timed out. Please try again.")
            return False
        except Exception as e:
            self.print_status(f"Failed to pull model: {e}")
            return False
    
    def create_config_files(self):
        self.print_status("Creating configuration files...")
        
        self.config_dir.mkdir(exist_ok=True)
        
        game_config = {
            "ollama_model": "llama2:7b-chat",
            "context_length": 1024,
            "max_tokens": 100,
            "temperature": 0.8,
            "story_chunk_size": 3,
            "context_injection_interval": 5
        }
        
        config_file = self.config_dir / "game_config.json"
        with open(config_file, 'w') as f:
            json.dump(game_config, f, indent=2)
        
        self.print_status("Configuration files created")
        return True
    
    def create_genre_prompts(self):
        self.print_status("Creating genre prompt templates...")
        
        genre_prompts = {
            "mystery": {
                "fantasy": "Create a mysterious crime story in a magical fantasy world where the hero is the culprit. Include magical elements, enchanted objects, and mystical creatures.",
                "horror": "Create a mysterious crime story in a horror setting where the hero is the culprit. Include supernatural elements, dark atmosphere, and psychological terror.",
                "scifi": "Create a mysterious crime story in a futuristic sci-fi world where the hero is the culprit. Include advanced technology, space elements, and cyberpunk themes.",
                "modern": "Create a mysterious crime story in modern day settings where the hero is the culprit. Include contemporary technology, urban settings, and realistic scenarios.",
                "cosmic": "Create a mysterious crime story with cosmic horror elements where the hero is the culprit. Include eldritch beings, cosmic entities, and reality-bending elements."
            },
            "adventure": {
                "fantasy": "Create an epic adventure story in a magical fantasy world. Include quests, magical creatures, enchanted items, and heroic challenges.",
                "horror": "Create an adventure story in a horror setting. Include survival challenges, supernatural threats, and dark exploration.",
                "scifi": "Create an adventure story in a futuristic sci-fi world. Include space exploration, advanced technology, and alien encounters.",
                "modern": "Create an adventure story in modern day settings. Include contemporary challenges, urban exploration, and real-world excitement.",
                "cosmic": "Create an adventure story with cosmic elements. Include space exploration, cosmic phenomena, and interdimensional travel."
            },
            "action": {
                "fantasy": "Create an action-packed story in a magical fantasy world. Include epic battles, magical combat, and heroic feats.",
                "horror": "Create an action story in a horror setting. Include intense survival action, supernatural combat, and thrilling escapes.",
                "scifi": "Create an action story in a futuristic sci-fi world. Include high-tech combat, space battles, and futuristic action sequences.",
                "modern": "Create an action story in modern day settings. Include contemporary action, realistic combat, and modern-day excitement.",
                "cosmic": "Create an action story with cosmic elements. Include cosmic battles, reality-warping action, and interdimensional combat."
            }
        }
        
        prompts_file = self.config_dir / "genre_prompts.json"
        with open(prompts_file, 'w') as f:
            json.dump(genre_prompts, f, indent=2)
        
        self.print_status("Genre prompt templates created")
        return True
    
    def cleanup_unwanted_files(self):
        self.print_status("Cleaning up unwanted files...")
        
        unwanted_items = [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            ".tox",
            ".mypy_cache",
            ".ruff_cache",
            ".DS_Store",
            "Thumbs.db"
        ]
        
        for item in unwanted_items:
            if "*" in item:
                import glob
                for file_path in glob.glob(item):
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        self.print_status(f"Could not remove {file_path}: {e}")
            else:
                item_path = self.project_root / item
                if item_path.exists():
                    try:
                        if item_path.is_file():
                            item_path.unlink()
                        elif item_path.is_dir():
                            shutil.rmtree(item_path)
                    except Exception as e:
                        self.print_status(f"Could not remove {item}: {e}")
        
        self.print_status("Cleanup completed")
        return True
    
    def run_setup(self):
        self.print_status("Starting Story-CLI setup...")
        self.print_status("System detected: 7.5GB RAM, Intel i5-1035G1 CPU")
        self.print_status("Optimizing for your system specifications...")
        
        # Install Python dependencies
        if not self.install_python_dependencies():
            return False
        
        # Check Ollama
        if not self.check_ollama():
            return False
        
        # Pull model
        if not self.pull_model():
            return False
        
        # Create configuration files
        if not self.create_config_files():
            return False
        
        # Create genre prompts
        if not self.create_genre_prompts():
            return False
        
        # Cleanup
        self.cleanup_unwanted_files()
        
        self.print_status("Setup completed successfully!")
        self.print_status("You can now run the game with: python main.py")
        return True

def main():
    setup = GameSetup()
    success = setup.run_setup()
    
    if success:
        print("\n[SUCCESS] Story-CLI is ready to play!")
        print("Run 'python main.py' to start the game.")
    else:
        print("\n[ERROR] Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
