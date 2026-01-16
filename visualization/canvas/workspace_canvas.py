"""Workspace canvas widget."""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from domain.entities.workspace import Workspace
from domain.value_objects.point import Point
from editing.tools.base_tool import BaseTool


class WorkspaceCanvas(QWidget):
    """Canvas for displaying and editing workspace."""
    
    def __init__(self, workspace: Workspace, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self.active_tool: BaseTool = None
        self.zoom_level = 1.0
        self.pan_offset = QPoint(0, 0)
        self.tile_size = 32
        self.show_grid = True
        self.show_features = False
        self.show_skeleton = False
        self.last_pan_pos = None
        self.last_click_pos = None
        self.is_dragging = False
        self.skeleton_result = None
        self.crossinizer_result = None
        self.template_preview_position = None  # Point for template preview
        self.template_preview_template = None  # ObjectsTemplate for preview
        self.template_preview_color = None  # (r, g, b) for preview coloring
        self.template_preview_scale = 1.0  # Scale factor for preview
        
        self.setMinimumSize(400, 300)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def set_active_tool(self, tool: BaseTool) -> None:
        """Set active tool."""
        self.active_tool = tool
    
    def focusOutEvent(self, event):
        """Handle focus loss - deactivate template tool if active."""
        from editing.tools.template_tool import TemplateTool
        from domain.enums.tool_type import ToolType
        
        if isinstance(self.active_tool, TemplateTool):
            # Find tool manager and switch to brush tool
            widget = self.parent()
            while widget:
                if hasattr(widget, 'tool_manager'):
                    widget.tool_manager.set_active_tool(ToolType.BRUSH)
                    self.update()
                    break
                widget = widget.parent()
        
        super().focusOutEvent(event)
    
    def paintEvent(self, event):
        """Paint workspace."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Apply zoom and pan
        painter.translate(self.pan_offset)
        painter.scale(self.zoom_level, self.zoom_level)
        
        # Draw grid
        if self.show_grid:
            self._draw_grid(painter)
        
        # Draw workspace
        if self.workspace:
            self._draw_workspace(painter)
        
        # Draw overlays
        if self.show_skeleton:
            self._draw_skeleton(painter)
        if self.show_features:
            self._draw_features(painter)
        
        # Draw template preview
        if self.template_preview_template and self.template_preview_position:
            self._draw_template_preview(painter)
    
    def _draw_grid(self, painter: QPainter) -> None:
        """Draw grid."""
        if not self.workspace:
            return
        
        pen = QPen(QColor(100, 100, 100), 1)
        painter.setPen(pen)
        
        for x in range(0, self.workspace.tilemap.width + 1):
            x_pos = x * self.tile_size
            painter.drawLine(x_pos, 0, x_pos, self.workspace.tilemap.height * self.tile_size)
        
        for y in range(0, self.workspace.tilemap.height + 1):
            y_pos = y * self.tile_size
            painter.drawLine(0, y_pos, self.workspace.tilemap.width * self.tile_size, y_pos)
    
    def _draw_workspace(self, painter: QPainter) -> None:
        """Draw workspace tiles."""
        if not self.workspace:
            return
        
        # Draw tiles
        for layer in self.workspace.layers:
            if not layer.visible:
                continue
            
            for obj in layer.get_map_objects():
                x = obj.position.x * self.tile_size
                y = obj.position.y * self.tile_size
                
                # Get color based on type
                color = self._get_object_color(obj)
                painter.fillRect(x, y, self.tile_size, self.tile_size, QColor(*color))
        
        # Draw Berlin Wall
        if self.workspace.berlin_wall:
            bw = self.workspace.berlin_wall
            pen = QPen(QColor(255, 0, 0), 2)  # Red border
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            x1 = bw.min_x * self.tile_size
            y1 = bw.min_y * self.tile_size
            width = (bw.max_x - bw.min_x + 1) * self.tile_size
            height = (bw.max_y - bw.min_y + 1) * self.tile_size
            
            painter.drawRect(x1, y1, width, height)
    
    def _get_object_color(self, obj) -> tuple:
        """Get color for object."""
        from domain.entities.tile import Tile
        from domain.entities.functional_tile import FunctionalTile
        from domain.enums.tile_type import TileType
        from domain.enums.functional_tile_type import FunctionalTileType
        
        if isinstance(obj, Tile):
            # Use custom color if set, otherwise use default
            if hasattr(obj, 'custom_color') and obj.custom_color:
                return obj.custom_color
            
            colors = {
                TileType.GRASS: (34, 139, 34),      # Green
                TileType.STONE: (128, 128, 128),    # Gray
                TileType.WATER: (0, 0, 255),        # Blue
                TileType.DIRT: (139, 69, 19),       # Brown
                TileType.SAND: (238, 203, 173),     # Beige
                TileType.SNOW: (255, 250, 250),     # White
                TileType.LAVA: (255, 69, 0),        # Red-orange
            }
            return colors.get(obj.tile_type, (200, 200, 200))
        elif isinstance(obj, FunctionalTile):
            colors = {
                FunctionalTileType.PLAYER_START: (255, 0, 0),      # Red
                FunctionalTileType.ENEMY: (255, 165, 0),           # Orange
                FunctionalTileType.CHECKPOINT: (0, 255, 0),        # Green
                FunctionalTileType.COIN: (255, 215, 0),            # Gold
                FunctionalTileType.POWERUP: (255, 0, 255),         # Magenta
                FunctionalTileType.EXIT: (0, 255, 255),            # Cyan
            }
            return colors.get(obj.functional_tile_type, (255, 255, 0))
        
        return (200, 200, 200)
    
    def _draw_skeleton(self, painter: QPainter) -> None:
        """Draw skeleton overlay."""
        if not self.skeleton_result:
            return
        
        painter.setPen(QPen(QColor(255, 255, 0), 1))  # Yellow lines
        bitmap = self.skeleton_result.skeleton_bitmap
        
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                if bitmap.get_pixel(x, y):
                    screen_x = x * self.tile_size
                    screen_y = y * self.tile_size
                    painter.drawPoint(screen_x + self.tile_size // 2, screen_y + self.tile_size // 2)
    
    def _draw_features(self, painter: QPainter) -> None:
        """Draw features overlay."""
        if not self.crossinizer_result:
            return
        
        # Draw endpoints (green)
        painter.setPen(QPen(QColor(0, 255, 0), 3))
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        for point in self.crossinizer_result.endpoints:
            screen_x = point.x * self.tile_size + self.tile_size // 2
            screen_y = point.y * self.tile_size + self.tile_size // 2
            painter.drawEllipse(screen_x - 3, screen_y - 3, 6, 6)
        
        # Draw bifurcations (blue)
        painter.setPen(QPen(QColor(0, 0, 255), 3))
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        for point in self.crossinizer_result.bifurcations:
            screen_x = point.x * self.tile_size + self.tile_size // 2
            screen_y = point.y * self.tile_size + self.tile_size // 2
            painter.drawEllipse(screen_x - 3, screen_y - 3, 6, 6)
        
        # Draw crossings (red)
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        for point in self.crossinizer_result.crossings:
            screen_x = point.x * self.tile_size + self.tile_size // 2
            screen_y = point.y * self.tile_size + self.tile_size // 2
            painter.drawEllipse(screen_x - 3, screen_y - 3, 6, 6)
        
        # Draw connections (thin lines)
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        for start, end in self.crossinizer_result.connections:
            start_x = start.x * self.tile_size + self.tile_size // 2
            start_y = start.y * self.tile_size + self.tile_size // 2
            end_x = end.x * self.tile_size + self.tile_size // 2
            end_y = end.y * self.tile_size + self.tile_size // 2
            painter.drawLine(start_x, start_y, end_x, end_y)
    
    def mousePressEvent(self, event):
        """Handle mouse press."""
        if event.button() == Qt.MouseButton.LeftButton and self.active_tool:
            point = self._screen_to_world(event.pos())
            if point:
                self.last_click_pos = point
                self.is_dragging = False
                # Don't call on_click yet - wait to see if it's a click or drag
        elif event.button() == Qt.MouseButton.RightButton:
            self.last_pan_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move."""
        if event.buttons() & Qt.MouseButton.RightButton:
            # Pan
            delta = event.pos() - self.last_pan_pos
            self.pan_offset += delta
            self.last_pan_pos = event.pos()
            self.update()
        elif event.buttons() & Qt.MouseButton.LeftButton and self.active_tool:
            # Drag
            point = self._screen_to_world(event.pos())
            if point and self.last_click_pos:
                if not self.is_dragging:
                    # First move - start drag operation
                    self.is_dragging = True
                    if hasattr(self.active_tool, 'on_drag_start'):
                        self.active_tool.on_drag_start(self.last_click_pos)
                
                # Continue drag
                self.active_tool.on_drag(self.last_click_pos, point)
                self.update()
                # Update parent window status bar if available
                self._update_parent_status()
                self.last_click_pos = point
        else:
            # Update template preview on mouse move (without button pressed)
            # Only if mouse is actually over the canvas
            if self.rect().contains(event.pos()):
                point = self._screen_to_world(event.pos())
                if point and self.active_tool:
                    from editing.tools.template_tool import TemplateTool
                    if isinstance(self.active_tool, TemplateTool) and self.active_tool.template:
                        self.template_preview_position = point
                        self.template_preview_template = self.active_tool.template
                        self.template_preview_color = self.active_tool.template_color
                        self.template_preview_scale = self.active_tool.scale
                        self.update()
                    else:
                        if self.template_preview_template:
                            self.template_preview_template = None
                            self.template_preview_position = None
                            self.update()
            else:
                # Mouse left canvas - clear preview
                if self.template_preview_template:
                    self.template_preview_template = None
                    self.template_preview_position = None
                    self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.MouseButton.LeftButton and self.active_tool:
            if not self.is_dragging and self.last_click_pos:
                # It was a click, not a drag - execute on_click now
                self.active_tool.on_click(self.last_click_pos)
                self.update()
                # Update parent window status bar if available
                self._update_parent_status()
            elif self.is_dragging:
                # End drag operation
                if hasattr(self.active_tool, 'on_drag_end'):
                    self.active_tool.on_drag_end()
                self.is_dragging = False
            self.last_click_pos = None
    
    def _update_parent_status(self):
        """Update parent window status bar if available."""
        widget = self.parent()
        while widget:
            if hasattr(widget, '_update_status_bar'):
                widget._update_status_bar()
                break
            widget = widget.parent()
    
    def wheelEvent(self, event):
        """Handle mouse wheel for zoom."""
        delta = event.angleDelta().y() / 120.0
        zoom_factor = 1.1 if delta > 0 else 0.9
        self.zoom_level *= zoom_factor
        self.zoom_level = max(0.1, min(5.0, self.zoom_level))
        self.update()
    
    def _screen_to_world(self, screen_pos: QPoint) -> Point:
        """Convert screen coordinates to world coordinates."""
        if not self.workspace:
            return None
        
        # Account for pan and zoom
        world_x = (screen_pos.x() - self.pan_offset.x()) / self.zoom_level
        world_y = (screen_pos.y() - self.pan_offset.y()) / self.zoom_level
        
        # Convert to tile coordinates
        tile_x = int(world_x / self.tile_size)
        tile_y = int(world_y / self.tile_size)
        
        if self.workspace.tilemap.is_valid_coordinate(tile_x, tile_y):
            return Point(tile_x, tile_y)
        return None
    
    def _draw_template_preview(self, painter: QPainter) -> None:
        """Draw template preview with opacity (centered)."""
        if not self.template_preview_template or not self.template_preview_position:
            return
        
        # Get template center
        template_center = self.template_preview_template.get_center()
        
        # Calculate offset from template center to position
        offset = Point(
            self.template_preview_position.x - template_center.x,
            self.template_preview_position.y - template_center.y
        )
        
        # Set opacity for preview
        painter.setOpacity(0.5)  # 50% opacity
        
        # Use dictionary to track positions and count votes for each position
        from collections import defaultdict
        
        position_votes = defaultdict(lambda: {'tiles': defaultdict(int), 'functional': defaultdict(int)})
        
        # Collect tiles from template with scaling (count votes for each position)
        for rel_pos, tile_type in self.template_preview_template.layout.tiles:
            # Apply scaling - scale relative position from center
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.template_preview_scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.template_preview_scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            
            if not self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                continue
            
            # Count vote for this tile type at this position
            position_votes[(abs_pos.x, abs_pos.y)]['tiles'][tile_type] += 1
        
        # Collect functional tiles from template with scaling
        for rel_pos, func_tile_type in self.template_preview_template.layout.functional_tiles:
            # Apply scaling - scale relative position from center
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.template_preview_scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.template_preview_scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            
            if not self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                continue
            
            # Count vote for this functional tile type at this position
            position_votes[(abs_pos.x, abs_pos.y)]['functional'][func_tile_type] += 1
        
        # Determine which tile/functional tile to draw at each position (most votes wins)
        tiles_to_draw = {}
        for pos, votes in position_votes.items():
            # Functional tiles take priority over regular tiles
            if votes['functional']:
                # Get functional tile type with most votes
                func_tile_type = max(votes['functional'].items(), key=lambda x: x[1])[0]
                tiles_to_draw[pos] = (func_tile_type, True)
            elif votes['tiles']:
                # Get tile type with most votes
                tile_type = max(votes['tiles'].items(), key=lambda x: x[1])[0]
                tiles_to_draw[pos] = (tile_type, False)
        
        # Draw all tiles (each position only once)
        for (pos_x, pos_y), (tile_or_func_type, is_functional) in tiles_to_draw.items():
            x = pos_x * self.tile_size
            y = pos_y * self.tile_size
            
            # Get color
            if is_functional:
                # Use default color for functional tiles
                from domain.enums.functional_tile_type import FunctionalTileType
                colors = {
                    FunctionalTileType.PLAYER_START: (255, 0, 0),
                    FunctionalTileType.ENEMY: (255, 165, 0),
                    FunctionalTileType.CHECKPOINT: (0, 255, 0),
                    FunctionalTileType.COIN: (255, 215, 0),
                    FunctionalTileType.POWERUP: (255, 0, 255),
                    FunctionalTileType.EXIT: (0, 255, 255),
                }
                default_color = colors.get(tile_or_func_type, (255, 255, 0))
                color = QColor(*default_color)
            else:
                # Get color - use template color if set, otherwise default
                if self.template_preview_color:
                    color = QColor(*self.template_preview_color)
                else:
                    # Use default color for tile type
                    from domain.enums.tile_type import TileType
                    colors = {
                        TileType.GRASS: (34, 139, 34),
                        TileType.STONE: (128, 128, 128),
                        TileType.WATER: (0, 0, 255),
                        TileType.DIRT: (139, 69, 19),
                        TileType.SAND: (238, 203, 173),
                        TileType.SNOW: (255, 250, 250),
                        TileType.LAVA: (255, 69, 0),
                    }
                    default_color = colors.get(tile_or_func_type, (200, 200, 200))
                    color = QColor(*default_color)
            
            painter.fillRect(x, y, self.tile_size, self.tile_size, color)
        
        # Reset opacity
        painter.setOpacity(1.0)
        """Draw preview using tile position scaling (original method)."""
        # Get template center
        template_center = self.template_preview_template.get_center()
        
        # Calculate offset from template center to position
        offset = Point(
            self.template_preview_position.x - template_center.x,
            self.template_preview_position.y - template_center.y
        )
        
        # Use dictionary to track positions and count votes for each position
        from collections import defaultdict
        
        position_votes = defaultdict(lambda: {'tiles': defaultdict(int), 'functional': defaultdict(int)})
        
        # Collect tiles from template with scaling (count votes for each position)
        for rel_pos, tile_type in self.template_preview_template.layout.tiles:
            # Apply scaling - scale relative position from center
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.template_preview_scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.template_preview_scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            
            if not self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                continue
            
            # Count vote for this tile type at this position
            position_votes[(abs_pos.x, abs_pos.y)]['tiles'][tile_type] += 1
        
        # Collect functional tiles from template with scaling
        for rel_pos, func_tile_type in self.template_preview_template.layout.functional_tiles:
            # Apply scaling - scale relative position from center
            scaled_rel_x = int((rel_pos.x - template_center.x) * self.template_preview_scale + template_center.x)
            scaled_rel_y = int((rel_pos.y - template_center.y) * self.template_preview_scale + template_center.y)
            scaled_rel_pos = Point(scaled_rel_x, scaled_rel_y)
            
            abs_pos = Point(scaled_rel_pos.x + offset.x, scaled_rel_pos.y + offset.y)
            
            if not self.workspace.tilemap.is_valid_coordinate(abs_pos.x, abs_pos.y):
                continue
            
            # Count vote for this functional tile type at this position
            position_votes[(abs_pos.x, abs_pos.y)]['functional'][func_tile_type] += 1
        
        # Determine which tile/functional tile to draw at each position (most votes wins)
        tiles_to_draw = {}
        for pos, votes in position_votes.items():
            # Functional tiles take priority over regular tiles
            if votes['functional']:
                # Get functional tile type with most votes
                func_tile_type = max(votes['functional'].items(), key=lambda x: x[1])[0]
                tiles_to_draw[pos] = (func_tile_type, True)
            elif votes['tiles']:
                # Get tile type with most votes
                tile_type = max(votes['tiles'].items(), key=lambda x: x[1])[0]
                tiles_to_draw[pos] = (tile_type, False)
        
        # Draw all tiles (each position only once)
        for (pos_x, pos_y), (tile_or_func_type, is_functional) in tiles_to_draw.items():
            x = pos_x * self.tile_size
            y = pos_y * self.tile_size
            
            # Get color
            if is_functional:
                # Use default color for functional tiles
                from domain.enums.functional_tile_type import FunctionalTileType
                colors = {
                    FunctionalTileType.PLAYER_START: (255, 0, 0),
                    FunctionalTileType.ENEMY: (255, 165, 0),
                    FunctionalTileType.CHECKPOINT: (0, 255, 0),
                    FunctionalTileType.COIN: (255, 215, 0),
                    FunctionalTileType.POWERUP: (255, 0, 255),
                    FunctionalTileType.EXIT: (0, 255, 255),
                }
                default_color = colors.get(tile_or_func_type, (255, 255, 0))
                color = QColor(*default_color)
            else:
                # Get color - use template color if set, otherwise default
                if self.template_preview_color:
                    color = QColor(*self.template_preview_color)
                else:
                    # Use default color for tile type
                    from domain.enums.tile_type import TileType
                    colors = {
                        TileType.GRASS: (34, 139, 34),
                        TileType.STONE: (128, 128, 128),
                        TileType.WATER: (0, 0, 255),
                        TileType.DIRT: (139, 69, 19),
                        TileType.SAND: (238, 203, 173),
                        TileType.SNOW: (255, 250, 250),
                        TileType.LAVA: (255, 69, 0),
                    }
                    default_color = colors.get(tile_or_func_type, (200, 200, 200))
                    color = QColor(*default_color)
            
            painter.fillRect(x, y, self.tile_size, self.tile_size, color)

