#!/usr/bin/env python3

import os
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from colorama import init
from dotenv import load_dotenv
from game_engine import GameEngine
from config import (
    GAME_TITLE,
    DEFAULT_GENRE,
    DEFAULT_MODE,
    INITIAL_HEALTH,
    INITIAL_STRENGTH,
    INITIAL_INTELLIGENCE,
    INITIAL_CHARISMA,
    GENRES,
    GAME_MODES
)

# Initialize colorama for Windows compatibility
init()

# Initialize Rich console
console = Console()

class Game:
    def __init__(self):
        self.console = Console()
        self.running = True
        self.current_scene = None
        self.player = None
        self.game_mode = None
        self.genre = None
        self.engine = None

    def initialize_game(self):
        """Initialize the game and set up the player."""
        self.console.print(Panel.fit(
            f"[bold blue]{GAME_TITLE}[/bold blue]\n"
            "An interactive text-based adventure game powered by AI.",
            title=GAME_TITLE
        ))
        
        # Choose game mode
        mode_choices = list(GAME_MODES.keys())
        mode_descriptions = [f"{GAME_MODES[mode]['name']}: {GAME_MODES[mode]['description']}" 
                           for mode in mode_choices]
        
        self.console.print("\n[bold]Available Game Modes:[/bold]")
        for desc in mode_descriptions:
            self.console.print(f"- {desc}")
            
        self.game_mode = Prompt.ask(
            "\nChoose your game mode",
            choices=mode_choices,
            default=DEFAULT_MODE
        )
        
        # Choose genre
        genre_choices = list(GENRES.keys())
        genre_descriptions = [f"{GENRES[genre]['name']}: {GENRES[genre]['description']}" 
                            for genre in genre_choices]
        
        self.console.print("\n[bold]Available Genres:[/bold]")
        for desc in genre_descriptions:
            self.console.print(f"- {desc}")
            
        self.genre = Prompt.ask(
            "\nChoose your genre",
            choices=genre_choices,
            default=DEFAULT_GENRE
        )
        
        # Initialize player
        self.player = {
            "name": Prompt.ask("Enter your character's name"),
            "health": INITIAL_HEALTH,
            "inventory": [],
            "stats": {
                "strength": INITIAL_STRENGTH,
                "intelligence": INITIAL_INTELLIGENCE,
                "charisma": INITIAL_CHARISMA
            }
        }
        
        # Initialize game engine
        self.engine = GameEngine(self.genre, self.game_mode)
        self.current_scene = self.engine.current_scene
        
        self.console.print(f"\n[green]Welcome, {self.player['name']}![/green]")
        self.console.print(f"Genre: {GENRES[self.genre]['name']}")
        self.console.print(f"Mode: {GAME_MODES[self.game_mode]['name']}\n")
        
        # Display initial scene
        self.console.print(Panel(self.current_scene, title="Scene"))

    def process_command(self, command):
        """Process player commands."""
        command = command.lower().strip()
        
        if command == "quit":
            self.running = False
            return "Goodbye!"
        
        elif command == "help":
            return self.get_help_text()
        
        elif command == "inventory":
            return self.show_inventory()
        
        elif command == "stats":
            return self.show_stats()
        
        # Process game actions
        return self.process_game_action(command)

    def process_game_action(self, action):
        """Process game actions and generate AI response."""
        # Get current game state
        game_state = self.engine.get_game_state()
        
        # Generate AI response
        response = self.engine.generate_response(action, game_state)
        
        # Update game state
        self.engine.update_game_state(response)
        self.current_scene = response
        
        return response

    def show_inventory(self):
        """Display player's inventory."""
        if not self.player["inventory"]:
            return "Your inventory is empty."
        
        items = "\n".join(f"- {item}" for item in self.player["inventory"])
        return f"Your inventory:\n{items}"

    def show_stats(self):
        """Display player's stats."""
        stats = self.player["stats"]
        return f"""Your stats:
Health: {self.player['health']}
Strength: {stats['strength']}
Intelligence: {stats['intelligence']}
Charisma: {stats['charisma']}"""

    def get_help_text(self):
        """Return help text for available commands."""
        return """Available commands:
- Type any action to play (e.g., 'go north', 'attack the dragon')
- 'help': Show this help message
- 'inventory': Check your inventory
- 'stats': View your character stats
- 'quit': Exit the game"""

    def run(self):
        """Main game loop."""
        self.initialize_game()
        
        while self.running:
            try:
                command = Prompt.ask("\nWhat would you like to do?")
                response = self.process_command(command)
                self.console.print(Panel(response, title="Response"))
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Game interrupted. Use 'quit' to exit properly.[/yellow]")
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")

def main():
    # Load environment variables
    load_dotenv()
    
    # Create and run game
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 