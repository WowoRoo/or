"""Tests for dirt transformation at bottom edge of square."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_square_bottom_edge_should_not_grow():
    """Test that dirt at bottom edge of a square should NOT grow even with grass on sides."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a square of dirt (3x3)
    #  D D D
    #  D D D
    #  D D D
    for dx in range(3):
        for dy in range(3):
            dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(dirt)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, dirt)
    
    # Place grass on the right side of the square (same row as bottom edge)
    grass_right = Tile(TileType.GRASS, workspace.tilemap.get_cell(8, 7).position, layer.id)
    layer.add_map_object(grass_right)
    workspace.tilemap.set_cell(8, 7, grass_right)
    
    # Place grass on the left side of the square (same row as bottom edge)
    grass_left = Tile(TileType.GRASS, workspace.tilemap.get_cell(4, 7).position, layer.id)
    layer.add_map_object(grass_left)
    workspace.tilemap.set_cell(4, 7, grass_left)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Bottom edge center (6,7) should NOT transform (it's part of square, not a corner)
    bottom_center = workspace.tilemap.get_cell(6, 7).map_object
    assert bottom_center and bottom_center.tile_type == TileType.DIRT
    
    # Only corners should transform, not the entire bottom edge
    # Bottom-left corner (5,7) - should transform (corner)
    bottom_left_corner = workspace.tilemap.get_cell(5, 7).map_object
    # Bottom-right corner (7,7) - should transform (corner)
    bottom_right_corner = workspace.tilemap.get_cell(7, 7).map_object
    
    # At least one corner should transform, but center should not
    assert (bottom_left_corner and bottom_left_corner.tile_type == TileType.GRASS) or \
           (bottom_right_corner and bottom_right_corner.tile_type == TileType.GRASS)
    assert bottom_center.tile_type == TileType.DIRT

