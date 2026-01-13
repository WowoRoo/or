"""Workspace loader."""

import json
from typing import Dict, Any
from domain.entities.workspace import Workspace
from domain.value_objects.workspace_metadata import WorkspaceMetadata
from domain.value_objects.berlin_wall import BerlinWall
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.enums.layer_type import LayerType
from domain.value_objects.point import Point
from datetime import datetime


class WorkspaceLoader:
    """Loader for workspace from JSON."""
    
    def load_from_file(
        self,
        filepath: str,
        tile_list_reference: TileListReference,
        functional_tile_list_reference: FunctionalTileListReference
    ) -> Workspace:
        """Load workspace from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return self.deserialize(data, tile_list_reference, functional_tile_list_reference)
    
    def deserialize(
        self,
        data: Dict[str, Any],
        tile_list_reference: TileListReference,
        functional_tile_list_reference: FunctionalTileListReference
    ) -> Workspace:
        """Deserialize workspace from dictionary."""
        from domain.entities.tilemap import Tilemap
        from domain.entities.layer import Layer
        from domain.entities.tile import Tile
        from domain.entities.functional_tile import FunctionalTile
        from uuid import UUID
        
        # Create metadata
        metadata = WorkspaceMetadata(
            name=data["metadata"]["name"],
            author=data["metadata"]["author"],
            created_at=datetime.fromisoformat(data["metadata"]["created_at"]),
            modified_at=datetime.fromisoformat(data["metadata"]["modified_at"]),
            width=data["metadata"]["width"],
            height=data["metadata"]["height"]
        )
        
        # Create tilemap
        tilemap = Tilemap(data["tilemap"]["width"], data["tilemap"]["height"])
        
        # Create Berlin wall
        bw_data = data["berlin_wall"]
        berlin_wall = BerlinWall(
            bw_data["min_x"], bw_data["min_y"],
            bw_data["max_x"], bw_data["max_y"]
        )
        
        # Create workspace
        workspace = Workspace(
            metadata=metadata,
            tilemap=tilemap,
            berlin_wall=berlin_wall,
            tile_list_reference=tile_list_reference,
            functional_tile_list_reference=functional_tile_list_reference
        )
        
        # Load layers
        for layer_data in data["layers"]:
            layer = Layer(
                name=layer_data["name"],
                layer_type=LayerType(layer_data["layer_type"]),
                tile_list_reference=tile_list_reference,
                functional_tile_list_reference=functional_tile_list_reference
            )
            layer.id = UUID(layer_data["id"])
            layer.visible = layer_data["visible"]
            layer.editable = layer_data["editable"]
            
            # Load map objects
            for obj_data in layer_data["map_objects"]:
                position = Point(obj_data["position"]["x"], obj_data["position"]["y"])
                layer_id = UUID(obj_data["layer_id"])
                
                if obj_data["type"] == "tile":
                    tile_type = TileType(obj_data["tile_type"])
                    tile = Tile(tile_type, position, layer_id, obj_data.get("rotation", 0.0))
                    tile.id = UUID(obj_data["id"])
                    layer.add_map_object(tile)
                    workspace.tilemap.set_cell(position.x, position.y, tile)
                elif obj_data["type"] == "functional_tile":
                    func_tile_type = FunctionalTileType(obj_data["functional_tile_type"])
                    func_tile = FunctionalTile(func_tile_type, position, layer_id)
                    func_tile.id = UUID(obj_data["id"])
                    layer.add_map_object(func_tile)
                    workspace.tilemap.set_cell(position.x, position.y, func_tile)
            
            workspace.add_layer(layer)
        
        return workspace

