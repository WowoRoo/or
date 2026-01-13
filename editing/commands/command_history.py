"""Command history for undo/redo."""

from typing import List
from editing.commands.command import Command


class CommandHistory:
    """History manager for undo/redo."""
    
    def __init__(self, max_history: int = 100):
        self.history: List[Command] = []
        self.current_index: int = -1
        self.max_history = max_history
    
    def execute(self, command: Command) -> None:
        """Execute command and add to history."""
        command.execute()
        
        # Remove any commands after current index (for redo)
        self.history = self.history[:self.current_index + 1]
        
        # Add new command
        self.history.append(command)
        self.current_index += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1
    
    def undo(self) -> bool:
        """Undo last command."""
        if self.current_index >= 0:
            self.history[self.current_index].undo()
            self.current_index -= 1
            return True
        return False
    
    def redo(self) -> bool:
        """Redo last undone command."""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.history[self.current_index].execute()
            return True
        return False
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.current_index >= 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.current_index < len(self.history) - 1
    
    def add_executed_command(self, command: Command) -> None:
        """Add an already executed command to history without executing it again."""
        # Remove any commands after current index (for redo)
        self.history = self.history[:self.current_index + 1]
        
        # Add new command
        self.history.append(command)
        self.current_index += 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1

