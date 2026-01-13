"""Tests for dirt transformation at corners."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_square_corners_should_grow():
    """Test that dirt at corners of a square should grow if grass is adjacent."""
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
    
    # Place grass on the right side of the square (same row as bottom corners)
    grass_right = Tile(TileType.GRASS, workspace.tilemap.get_cell(8, 7).position, layer.id)
    layer.add_map_object(grass_right)
    workspace.tilemap.set_cell(8, 7, grass_right)
    
    # Place grass on the left side of the square (same row as bottom corners)
    grass_left = Tile(TileType.GRASS, workspace.tilemap.get_cell(4, 7).position, layer.id)
    layer.add_map_object(grass_left)
    workspace.tilemap.set_cell(4, 7, grass_left)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Bottom corners (5,7) and (7,7) should transform because they have grass on sides
    # Check bottom-left corner
    bottom_left_corner = workspace.tilemap.get_cell(5, 7).map_object
    # Check bottom-right corner
    bottom_right_corner = workspace.tilemap.get_cell(7, 7).map_object
    
    # At least one corner should transform
    assert (bottom_left_corner and bottom_left_corner.tile_type == TileType.GRASS) or \
           (bottom_right_corner and bottom_right_corner.tile_type == TileType.GRASS)


def test_dirt_corner_with_grass_diagonal():
    """Test that dirt corner with grass on diagonal should grow."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Place dirt at bottom-left corner of a square
    dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5, 7).position, layer.id)
    layer.add_map_object(dirt)
    workspace.tilemap.set_cell(5, 7, dirt)
    
    # Place grass on top-right diagonal (should allow growth)
    grass = Tile(TileType.GRASS, workspace.tilemap.get_cell(6, 6).position, layer.id)
    layer.add_map_object(grass)
    workspace.tilemap.set_cell(6, 6, grass)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Dirt should transform (grass is on top-right diagonal)
    assert dirt.tile_type == TileType.GRASS

