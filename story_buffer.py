"""
Story Buffer System for Story-CLI
Manages story context and provides output buffering for the LLM.
"""

import json
from typing import List, Dict, Optional
from pathlib import Path
import logging

class StoryBuffer:
    def __init__(self, config_path: str = "config/game_config.json"):
        """Initialize the story buffer with configuration."""
        self.story_segments = []
        self.context_window = []
        self.interaction_count = 0
        self.config = self._load_config(config_path)
        self.max_context_length = self.config.get("context_length", 1024)
        self.chunk_size = self.config.get("story_chunk_size", 3)
        self.injection_interval = self.config.get("context_injection_interval", 5)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Config file {config_path} not found, using defaults")
            return {
                "context_length": 1024,
                "story_chunk_size": 3,
                "context_injection_interval": 5
            }
    
    def add_story_segment(self, text: str, segment_type: str = "story"):
        """Add a new story segment to the buffer."""
        segment = {
            "text": text,
            "type": segment_type,
            "timestamp": len(self.story_segments)
        }
        self.story_segments.append(segment)
        self._update_context_window()
        
    def add_player_action(self, action: str):
        """Add a player action to the buffer."""
        self.add_story_segment(f"Player: {action}", "player_action")
        self.interaction_count += 1
        
    def add_ai_response(self, response: str):
        """Add an AI response to the buffer."""
        self.add_story_segment(f"AI: {response}", "ai_response")
        
    def _update_context_window(self):
        """Update the context window with recent story segments."""
        total_length = 0
        self.context_window = []
        
        for segment in reversed(self.story_segments):
            segment_length = len(segment["text"])
            if total_length + segment_length <= self.max_context_length:
                self.context_window.insert(0, segment)
                total_length += segment_length
            else:
                break
                
    def get_context_for_llm(self) -> str:
        """Get formatted context for the LLM."""
        if not self.context_window:
            return ""
            
        context_parts = []
        for segment in self.context_window:
            if segment["type"] == "story":
                context_parts.append(segment["text"])
            elif segment["type"] == "player_action":
                context_parts.append(f"Player: {segment['text']}")
            elif segment["type"] == "ai_response":
                context_parts.append(f"AI: {segment['text']}")
                
        return "\n".join(context_parts)
    
    def should_inject_context(self) -> bool:
        """Check if context should be injected based on interaction count."""
        return self.interaction_count % self.injection_interval == 0
    
    def get_recent_story_chunks(self, num_chunks: Optional[int] = None) -> List[str]:
        """Get recent story chunks for display."""
        if num_chunks is None:
            num_chunks = self.chunk_size
            
        story_segments = [seg for seg in self.story_segments if seg["type"] == "story"]
        return [seg["text"] for seg in story_segments[-num_chunks:]]
    
    def get_story_summary(self) -> str:
        """Get a summary of the story so far."""
        if not self.story_segments:
            return "No story has been generated yet."
            
        story_parts = [seg["text"] for seg in self.story_segments if seg["type"] == "story"]
        if not story_parts:
            return "No story content available."
            
        # Create a brief summary
        summary = " ".join(story_parts[-5:])  # Last 5 story segments
        if len(summary) > 500:
            summary = summary[:500] + "..."
            
        return summary
    
    def clear_buffer(self):
        """Clear the story buffer."""
        self.story_segments = []
        self.context_window = []
        self.interaction_count = 0
        
    def save_story(self, filename: str = "saved_story.json"):
        """Save the current story to a file."""
        story_data = {
            "segments": self.story_segments,
            "interaction_count": self.interaction_count,
            "summary": self.get_story_summary()
        }
        
        with open(filename, 'w') as f:
            json.dump(story_data, f, indent=2)
            
    def load_story(self, filename: str = "saved_story.json"):
        """Load a story from a file."""
        try:
            with open(filename, 'r') as f:
                story_data = json.load(f)
                
            self.story_segments = story_data.get("segments", [])
            self.interaction_count = story_data.get("interaction_count", 0)
            self._update_context_window()
            
        except FileNotFoundError:
            logging.warning(f"Story file {filename} not found")
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in story file {filename}")
            
    def get_stats(self) -> Dict:
        """Get statistics about the story buffer."""
        return {
            "total_segments": len(self.story_segments),
            "story_segments": len([s for s in self.story_segments if s["type"] == "story"]),
            "player_actions": len([s for s in self.story_segments if s["type"] == "player_action"]),
            "ai_responses": len([s for s in self.story_segments if s["type"] == "ai_response"]),
            "interaction_count": self.interaction_count,
            "context_window_size": len(self.context_window)
        } 