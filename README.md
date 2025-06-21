# Story-CLI

A text-based adventure game powered by AI. Create your own stories through natural language interaction with Ollama.

## Features

- **3 Main Genres**: Mystery, Adventure, Action
- **5 Sub-Genres**: Fantasy, Horror, Sci-Fi, Modern, Cosmic
- **Dynamic Story Generation**: AI-powered story creation using Ollama
- **Story Buffer System**: Intelligent context management for coherent storytelling
- **Chunked Story Display**: Stories shown 2-3 lines at a time for better pacing
- **Character Stats and Inventory System**
- **Rich text interface** with colors and formatting
- **Save/Load Game State**
- **Story Summary and Progress Tracking**

## Installation

### Prerequisites
- Python 3.8 or higher
- Ollama (for running the LLM)
- At least 8GB RAM (for running the LLM)

### Quick Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd story-cli
```

2. Install Ollama (if not already installed):
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

3. Run the setup script:
```bash
python setup.py
```

The setup script will:
- Install Python dependencies
- Check Ollama installation
- Pull the llama2:7b-chat model (~4GB)
- Create configuration files
- Set up genre-specific prompts

## Usage

### Starting the Game
```bash
python main.py
```

### Game Flow

1. **Genre Selection**: Choose from 3 main genres and 5 sub-genres
2. **Character Creation**: Enter your character's name
3. **Story Generation**: AI generates an opening scene based on your choices
4. **Interactive Storytelling**: Type actions in natural language

### Game Controls

- **Natural Language Actions**: Type any action (e.g., 'go north', 'attack the dragon', 'search the room')
- **Meta Commands**:
  - `help`: Show available commands
  - `quit`: Exit the game
  - `inventory`: Check your items
  - `stats`: View your character stats
  - `save`: Save your current game
  - `load`: Load your saved game
  - `summary`: Show story summary

### Action Examples

- **Movement**: `go north`, `walk to the door`, `enter building`
- **Interaction**: `talk to npc`, `ask about quest`, `greet guard`
- **Combat**: `attack enemy`, `defend yourself`, `use weapon`
- **Investigation**: `search room`, `examine body`, `look for clues`
- **Item Usage**: `pick up key`, `use potion`, `examine map`

## Genre Combinations

The game supports 15 unique genre combinations:

### Mystery Stories
- **Mystery + Fantasy**: Magical crime solving with enchanted clues
- **Mystery + Horror**: Supernatural investigations and dark secrets
- **Mystery + Sci-Fi**: Futuristic detective work with advanced technology
- **Mystery + Modern**: Contemporary crime solving in urban settings
- **Mystery + Cosmic**: Reality-bending mysteries with eldritch elements

### Adventure Stories
- **Adventure + Fantasy**: Epic quests in magical worlds
- **Adventure + Horror**: Survival challenges in terrifying environments
- **Adventure + Sci-Fi**: Space exploration and alien encounters
- **Adventure + Modern**: Real-world exploration and discovery
- **Adventure + Cosmic**: Interdimensional travel and cosmic phenomena

### Action Stories
- **Action + Fantasy**: Epic battles with magical combat
- **Action + Horror**: Intense survival action against supernatural threats
- **Action + Sci-Fi**: High-tech combat and space battles
- **Action + Modern**: Contemporary action and realistic combat
- **Action + Cosmic**: Reality-warping battles and interdimensional combat

## Technical Details

### Architecture
- **Game Engine**: Manages game state, player actions, and story progression
- **Ollama Interface**: Handles communication with Ollama for story generation
- **Story Buffer**: Manages context and provides coherent storytelling
- **Configuration System**: Handles genre prompts and game settings

### Files Structure
```
story-cli/
├── setup.py              # One-time setup script
├── main.py               # Main game entry point
├── game_engine.py        # Core game logic
├── llm_interface.py      # Ollama communication
├── story_buffer.py       # Context management
├── config.py             # Game configuration
├── requirements.txt      # Python dependencies
└── config/               # Configuration files
```

## Troubleshooting

### Common Issues

1. **Ollama not found**:
   - Install Ollama from https://ollama.ai
   - Ensure Ollama is running: `ollama serve`

2. **Model not found**:
   - Pull the model: `ollama pull llama2:7b-chat`
   - Check available models: `ollama list`

3. **Game runs slowly**:
   - The LLM requires significant computational resources
   - Consider using a smaller model or upgrading your hardware

4. **Story quality issues**:
   - The model quality depends on the Ollama model used
   - You can try different models: `ollama pull llama2:13b-chat`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Install Ollama and pull model: `ollama pull llama2:7b-chat`
6. Run setup: `python setup.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details. 