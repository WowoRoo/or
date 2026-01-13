"""Composite command for grouping multiple commands."""

from typing import List
from editing.commands.command import Command


class CompositeCommand(Command):
    """Command that groups multiple commands into one undoable operation."""
    
    def __init__(self, commands: List[Command]):
        self.commands = commands
    
    def execute(self) -> None:
        """Execute all commands in order."""
        for command in self.commands:
            command.execute()
    
    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for command in reversed(self.commands):
            command.undo()


