#!/usr/bin/env python3

import os
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.table import Table
from colorama import init
from dotenv import load_dotenv
from game_engine import GameEngine
from config import (
    GAME_TITLE,
    DEFAULT_MAIN_GENRE,
    DEFAULT_SUB_GENRE,
    INITIAL_HEALTH,
    INITIAL_STRENGTH,
    INITIAL_INTELLIGENCE,
    INITIAL_CHARISMA,
    MAIN_GENRES,
    SUB_GENRES,
    STORY_SETTINGS
)

# Initialize colorama for Windows compatibility
init()

class Game:
    def __init__(self):
        self.console = Console()
        self.running = True
        self.current_scene = None
        self.player = None
        self.main_genre = None
        self.sub_genre = None
        self.engine = None

    def initialize_game(self):
        """Initialize the game and set up the player."""
        self.console.print(Panel.fit(
            f"[bold blue]{GAME_TITLE}[/bold blue]\n"
            "An interactive text-based adventure game powered by AI.",
            title=GAME_TITLE
        ))
        
        # Choose main genre
        self.console.print("\n[bold]Choose your main genre:[/bold]")
        main_genre_choices = list(MAIN_GENRES.keys())
        
        for i, genre_key in enumerate(main_genre_choices, 1):
            genre_info = MAIN_GENRES[genre_key]
            color = genre_info.get("color", "white")
            self.console.print(f"[{color}]{i}. {genre_info['name']}: {genre_info['description']}[/{color}]")
            
        self.main_genre = Prompt.ask(
            "\nChoose your main genre",
            choices=main_genre_choices,
            default=DEFAULT_MAIN_GENRE
        )
        
        # Choose sub-genre
        self.console.print(f"\n[bold]Choose your {MAIN_GENRES[self.main_genre]['name']} sub-genre:[/bold]")
        sub_genre_choices = list(SUB_GENRES.keys())
        
        for i, sub_genre_key in enumerate(sub_genre_choices, 1):
            sub_genre_info = SUB_GENRES[sub_genre_key]
            color = sub_genre_info.get("color", "white")
            self.console.print(f"[{color}]{i}. {sub_genre_info['name']}: {sub_genre_info['description']}[/{color}]")
            
        self.sub_genre = Prompt.ask(
            f"\nChoose your {MAIN_GENRES[self.main_genre]['name']} sub-genre",
            choices=sub_genre_choices,
            default=DEFAULT_SUB_GENRE
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
        self.console.print(f"\n[green]Initializing {MAIN_GENRES[self.main_genre]['name']} story in {SUB_GENRES[self.sub_genre]['name']} setting...[/green]")
        self.engine = GameEngine(self.main_genre, self.sub_genre)
        
        self.console.print(f"\n[green]Welcome, {self.player['name']}![/green]")
        self.console.print(f"Genre: {MAIN_GENRES[self.main_genre]['name']} - {SUB_GENRES[self.sub_genre]['name']}\n")
        
        # Display initial scene
        self.display_story_chunks()

    def display_story_chunks(self):
        """Display recent story chunks in a formatted way."""
        chunks = self.engine.get_recent_story_chunks()
        
        if chunks:
            self.console.print(Panel(
                "\n".join(chunks),
                title="[bold]Story[/bold]",
                border_style="blue"
            ))
        else:
            self.console.print(Panel(
                "The story begins...",
                title="[bold]Story[/bold]",
                border_style="blue"
            ))

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
        
        elif command == "save":
            self.engine.save_game()
            return "Game saved successfully!"
        
        elif command == "load":
            self.engine.load_game()
            self.display_story_chunks()
            return "Game loaded successfully!"
        
        elif command == "summary":
            return self.engine.get_story_summary()
        
        # Process game actions
        return self.process_game_action(command)

    def process_game_action(self, action):
        """Process game actions and generate AI response."""
        # Generate AI response
        response = self.engine.generate_response(action)
        
        # Display the new story chunks
        self.display_story_chunks()
        
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
- Type any action to play (e.g., 'go north', 'attack the dragon', 'search the room')
- 'help': Show this help message
- 'inventory': Check your inventory
- 'stats': View your character stats
- 'save': Save your current game
- 'load': Load your saved game
- 'summary': Show story summary
- 'quit': Exit the game

Action examples:
- Movement: go north, walk to the door, enter building
- Interaction: talk to npc, ask about quest, greet guard
- Combat: attack enemy, defend yourself, use weapon
- Investigation: search room, examine body, look for clues
- Item usage: pick up key, use potion, examine map"""

    def run(self):
        """Main game loop."""
        self.initialize_game()
        
        while self.running:
            try:
                command = Prompt.ask("\n[bold]What would you like to do?[/bold]")
                response = self.process_command(command)
                
                if response and response != "Goodbye!":
                    # Don't display response for story chunks as they're shown above
                    if not response.startswith("Game") and not response.startswith("Your"):
                        self.console.print(Panel(response, title="[bold]Response[/bold]", border_style="green"))
                
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