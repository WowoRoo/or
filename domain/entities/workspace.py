"""Workspace root entity."""

from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime
from domain.entities.tilemap import Tilemap
from domain.entities.layer import Layer
from domain.value_objects.workspace_metadata import WorkspaceMetadata
from domain.value_objects.berlin_wall import BerlinWall
from domain.value_objects.features_vector import FeaturesVector
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.entities.objects_template import ObjectsTemplate


class Workspace:
    """Root entity representing entire editable level."""
    
    def __init__(
        self,
        metadata: WorkspaceMetadata,
        tilemap: Tilemap,
        berlin_wall: BerlinWall,
        tile_list_reference: TileListReference,
        functional_tile_list_reference: FunctionalTileListReference
    ):
        self.id: UUID = uuid4()
        self.metadata: WorkspaceMetadata = metadata
        self.tilemap: Tilemap = tilemap
        self.berlin_wall: BerlinWall = berlin_wall
        self.layers: List[Layer] = []
        self.active_layer_id: Optional[UUID] = None
        self.features_vector: Optional[FeaturesVector] = None
        self.workspace_bitmap: Optional[WorkspaceBitmap] = None
        self.templates: List[ObjectsTemplate] = []
        self.tile_list_reference: TileListReference = tile_list_reference
        self.functional_tile_list_reference: FunctionalTileListReference = functional_tile_list_reference
    
    @staticmethod
    def create_new(
        name: str,
        author: str,
        width: int,
        height: int,
        tile_list_reference: TileListReference,
        functional_tile_list_reference: FunctionalTileListReference
    ) -> 'Workspace':
        """Create new workspace."""
        metadata = WorkspaceMetadata(
            name=name,
            author=author,
            created_at=datetime.now(),
            modified_at=datetime.now(),
            width=width,
            height=height
        )
        tilemap = Tilemap(width, height)
        berlin_wall = BerlinWall(0, 0, width - 1, height - 1)
        
        workspace = Workspace(
            metadata=metadata,
            tilemap=tilemap,
            berlin_wall=berlin_wall,
            tile_list_reference=tile_list_reference,
            functional_tile_list_reference=functional_tile_list_reference
        )
        
        # Create default layer
        from domain.enums.layer_type import LayerType
        default_layer = Layer(
            name="Default Layer",
            layer_type=LayerType.TILE_LAYER,
            tile_list_reference=tile_list_reference,
            functional_tile_list_reference=functional_tile_list_reference
        )
        workspace.add_layer(default_layer)
        # Set first layer as active
        workspace.active_layer_id = default_layer.id
        
        return workspace
    
    def add_layer(self, layer: Layer) -> None:
        """Add layer to workspace."""
        self.layers.append(layer)
    
    def remove_layer(self, layer_id: UUID) -> None:
        """Remove layer from workspace and clear its objects from tilemap."""
        # Find layer to remove
        layer_to_remove = next((l for l in self.layers if l.id == layer_id), None)
        if not layer_to_remove:
            return
        
        # Clear all objects from this layer in tilemap
        for obj in layer_to_remove.get_map_objects():
            cell = self.tilemap.get_cell(obj.position.x, obj.position.y)
            if cell and cell.map_object and cell.map_object.id == obj.id:
                cell.map_object = None
        
        # Remove layer
        self.layers = [l for l in self.layers if l.id != layer_id]
        
        # If removed layer was active, set first available layer as active
        if self.active_layer_id == layer_id:
            if self.layers:
                self.active_layer_id = self.layers[0].id
            else:
                self.active_layer_id = None
    
    def get_active_layer(self) -> Optional[Layer]:
        """Get active layer by ID, or first visible and editable layer as fallback."""
        # If active_layer_id is set, try to find that layer
        if self.active_layer_id:
            for layer in self.layers:
                if layer.id == self.active_layer_id and layer.visible and layer.editable:
                    return layer
        
        # Fallback to first visible and editable layer
        for layer in self.layers:
            if layer.visible and layer.editable:
                # Set it as active if not set
                if not self.active_layer_id:
                    self.active_layer_id = layer.id
                return layer
        return None
    
    def detect_berlin_wall(self) -> None:
        """Detect and update Berlin wall bounds."""
        # Find bounds of all placed objects
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        
        for layer in self.layers:
            for obj in layer.get_map_objects():
                x, y = obj.position.x, obj.position.y
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
        
        # If no objects, use full tilemap
        if min_x == float('inf'):
            min_x, min_y = 0, 0
            max_x, max_y = self.tilemap.width - 1, self.tilemap.height - 1
        
        self.berlin_wall = BerlinWall(int(min_x), int(min_y), int(max_x), int(max_y))
    
    def add_template(self, template: ObjectsTemplate) -> None:
        """Add template to workspace."""
        self.templates.append(template)
    
    def get_template(self, template_id: UUID) -> Optional[ObjectsTemplate]:
        """Get template by ID."""
        for template in self.templates:
            if template.id == template_id:
                return template
        return None
    
    def get_all_templates(self) -> List[ObjectsTemplate]:
        """Get all templates."""
        return self.templates.copy()

