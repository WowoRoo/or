"""Command for placing a template."""

from typing import List, Optional, Tuple
from domain.value_objects.point import Point
from domain.entities.tile import Tile
from domain.entities.functional_tile import FunctionalTile
from domain.entities.workspace import Workspace
from domain.entities.objects_template import ObjectsTemplate
from editing.commands.command import Command


class PlaceTemplateCommand(Command):
    """Command for placing a template at a position."""
    
    def __init__(
        self,
        workspace: Workspace,
        template: ObjectsTemplate,
        position: Point,
        template_color: Optional[Tuple[int, int, int]] = None,
        scale: float = 1.0
    ):
        self.workspace = workspace
        self.template = template
        self.position = position
        self.template_color = template_color  # (r, g, b) for coloring tiles
        self.scale = scale  # Scale factor (0.1 to 1.0)
        self.placed_tiles: List[str] = []  # List of tile IDs
        self.placed_functional_tiles: List[str] = []  # List of functional tile IDs
        self.previous_objects: List[Tuple[Point, object]] = []  # List of (point, object) tuples
    
    def execute(self) -> None:
        """Place template at position (centered)."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Get template center
        template_center = self.template.get_center()
        
        # Calculate offset from template center to position
        offset = Point(
            self.position.x - template_center.x,
            self.position.y - template_center.y
        )
        
        # Use dictionary to track positions and count votes for each position
        from collections import defaultdict
        from domain.enums.tile_type import TileType
        from domain.enums.functional_tile_type import FunctionalTileType
        
        position_votes = defaultdict(lambda: {'tiles': defaultdict(int), 'functional': defaultdict(int)})
        
        # Collect tiles from template with scaling (count votes for each position)
        for rel_pos, tile_type in self.template.layout.tiles:
            # Apply scaling - scale relative position from center
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            
            if not self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                continue
            
            # Count vote for this tile type at this position
            position_votes[(abs_pos.x, abs_pos.y)]['tiles'][tile_type] += 1
        
        # Collect functional tiles from template with scaling
        for rel_pos, func_tile_type in self.template.layout.functional_tiles:
            # Apply scaling - scale relative position from center
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            
            if not self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                continue
            
            # Count vote for this functional tile type at this position
            position_votes[(abs_pos.x, abs_pos.y)]['functional'][func_tile_type] += 1
        
        # Determine which tile/functional tile to place at each position (most votes wins)
        tiles_to_place = {}
        for pos, votes in position_votes.items():
            # Functional tiles take priority over regular tiles
            if votes['functional']:
                # Get functional tile type with most votes
                func_tile_type = max(votes['functional'].items(), key=lambda x: x[1])[0]
                tiles_to_place[pos] = (func_tile_type, True)
            elif votes['tiles']:
                # Get tile type with most votes
                tile_type = max(votes['tiles'].items(), key=lambda x: x[1])[0]
                tiles_to_place[pos] = (tile_type, False)
        
        # Place all tiles (each position only once)
        for (pos_x, pos_y), (tile_or_func_type, is_functional) in tiles_to_place.items():
            abs_pos = Point(pos_x, pos_y)
            
            cell = self.workspace.tilemap.get_cell(abs_pos.x, abs_pos.y)
            if not cell:
                continue
            
            # Save previous object
            if cell.map_object:
                self.previous_objects.append((abs_pos, cell.map_object))
                active_layer.remove_map_object(cell.map_object.id)
            
            # Create and place tile or functional tile
            if is_functional:
                func_tile = FunctionalTile(tile_or_func_type, abs_pos, active_layer.id)
                self.placed_functional_tiles.append(func_tile.id)
                active_layer.add_map_object(func_tile)
                self.workspace.tilemap.set_cell(abs_pos.x, abs_pos.y, func_tile)
            else:
                tile = Tile(tile_or_func_type, abs_pos, active_layer.id)
                self.placed_tiles.append(tile.id)
                active_layer.add_map_object(tile)
                self.workspace.tilemap.set_cell(abs_pos.x, abs_pos.y, tile)
    
    def undo(self) -> None:
        """Remove placed template and restore previous objects."""
        active_layer = self.workspace.get_active_layer()
        if not active_layer:
            return
        
        # Remove all placed tiles
        for tile_id in self.placed_tiles:
            active_layer.remove_map_object(tile_id)
        
        # Remove all placed functional tiles
        for func_tile_id in self.placed_functional_tiles:
            active_layer.remove_map_object(func_tile_id)
        
        # Clear cells (using same scaling as in execute)
        positions_to_clear = set()
        template_center = self.template.get_center()
        offset = Point(
            self.position.x - template_center.x,
            self.position.y - template_center.y
        )
        
        for rel_pos, _ in self.template.layout.tiles:
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            if self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                positions_to_clear.add((abs_pos.x, abs_pos.y))
        
        for rel_pos, _ in self.template.layout.functional_tiles:
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            if self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                positions_to_clear.add((abs_pos.x, abs_pos.y))
        
        # Clear all unique positions
        for pos_x, pos_y in positions_to_clear:
            cell = self.workspace.tilemap.get_cell(pos_x, pos_y)
            if cell:
                cell.map_object = None
        
        # Restore previous objects
        for point, obj in self.previous_objects:
            active_layer.add_map_object(obj)
            self.workspace.tilemap.set_cell(point.x, point.y, obj)

