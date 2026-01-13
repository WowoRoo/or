"""Workspace serializer."""

import json
from typing import Dict, Any
from domain.entities.workspace import Workspace
from domain.entities.layer import Layer
from domain.entities.tile import Tile
from domain.entities.functional_tile import FunctionalTile


class WorkspaceSerializer:
    """Serializer for workspace to JSON."""
    
    def serialize(self, workspace: Workspace) -> Dict[str, Any]:
        """Serialize workspace to dictionary."""
        return {
            "metadata": {
                "name": workspace.metadata.name,
                "author": workspace.metadata.author,
                "created_at": workspace.metadata.created_at.isoformat(),
                "modified_at": workspace.metadata.modified_at.isoformat(),
                "width": workspace.metadata.width,
                "height": workspace.metadata.height
            },
            "berlin_wall": {
                "min_x": workspace.berlin_wall.min_x,
                "min_y": workspace.berlin_wall.min_y,
                "max_x": workspace.berlin_wall.max_x,
                "max_y": workspace.berlin_wall.max_y
            },
            "layers": [self._serialize_layer(layer) for layer in workspace.layers],
            "tilemap": {
                "width": workspace.tilemap.width,
                "height": workspace.tilemap.height
            }
        }
    
    def _serialize_layer(self, layer: Layer) -> Dict[str, Any]:
        """Serialize layer."""
        return {
            "id": str(layer.id),
            "name": layer.name,
            "visible": layer.visible,
            "editable": layer.editable,
            "layer_type": layer.layer_type.value,
            "map_objects": [self._serialize_map_object(obj) for obj in layer.get_map_objects()]
        }
    
    def _serialize_map_object(self, obj) -> Dict[str, Any]:
        """Serialize map object."""
        base = {
            "id": str(obj.id),
            "position": {"x": obj.position.x, "y": obj.position.y},
            "layer_id": str(obj.layer_id)
        }
        
        if isinstance(obj, Tile):
            base["type"] = "tile"
            base["tile_type"] = obj.tile_type.value
            base["rotation"] = obj.rotation
        elif isinstance(obj, FunctionalTile):
            base["type"] = "functional_tile"
            base["functional_tile_type"] = obj.functional_tile_type.value
        
        return base
    
    def save_to_file(self, workspace: Workspace, filepath: str) -> None:
        """Save workspace to file."""
        data = self.serialize(workspace)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

