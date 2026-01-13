"""Tests for dirt transformation at bottom edge of large blocks."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_large_block_bottom_edge_should_not_grow():
    """Test that dirt at bottom edge of a large block (5x5) should NOT grow grass."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 20, 20,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a 5x5 block of dirt
    # D D D D D
    # D D D D D
    # D D D D D
    # D D D D D
    # D D D D D
    for dx in range(5):
        for dy in range(5):
            dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(dirt)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, dirt)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Bottom edge should NOT transform (only has free space below)
    # Check all bottom edge tiles
    for x in range(5, 10):
        bottom_tile = workspace.tilemap.get_cell(x, 9).map_object
        assert bottom_tile and bottom_tile.tile_type == TileType.DIRT, \
            f"Bottom edge tile at ({x},9) should remain DIRT, but is {bottom_tile.tile_type if bottom_tile else 'None'}"
    
    # Top edge should transform (has free space above)
    for x in range(5, 10):
        top_tile = workspace.tilemap.get_cell(x, 5).map_object
        assert top_tile and top_tile.tile_type == TileType.GRASS, \
            f"Top edge tile at ({x},5) should be GRASS, but is {top_tile.tile_type if top_tile else 'None'}"
    
    # Left edge should transform (has free space on left)
    # But NOT the bottom-left corner (5,9) - it's part of bottom edge
    for y in range(5, 9):  # Exclude bottom row (y=9)
        left_tile = workspace.tilemap.get_cell(5, y).map_object
        assert left_tile and left_tile.tile_type == TileType.GRASS, \
            f"Left edge tile at (5,{y}) should be GRASS, but is {left_tile.tile_type if left_tile else 'None'}"
    
    # Right edge should transform (has free space on right)
    # But NOT the bottom-right corner (9,9) - it's part of bottom edge
    for y in range(5, 9):  # Exclude bottom row (y=9)
        right_tile = workspace.tilemap.get_cell(9, y).map_object
        assert right_tile and right_tile.tile_type == TileType.GRASS, \
            f"Right edge tile at (9,{y}) should be GRASS, but is {right_tile.tile_type if right_tile else 'None'}"


def test_dirt_large_block_bottom_edge_with_grass_should_not_grow():
    """Test that dirt at bottom edge of a large block should NOT grow even with grass on sides."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 20, 20,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a 5x5 block of dirt
    for dx in range(5):
        for dy in range(5):
            dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(dirt)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, dirt)
    
    # Place grass on the right side of the square (same row as bottom edge)
    grass_right = Tile(TileType.GRASS, workspace.tilemap.get_cell(10, 9).position, layer.id)
    layer.add_map_object(grass_right)
    workspace.tilemap.set_cell(10, 9, grass_right)
    
    # Place grass on the left side of the square (same row as bottom edge)
    grass_left = Tile(TileType.GRASS, workspace.tilemap.get_cell(4, 9).position, layer.id)
    layer.add_map_object(grass_left)
    workspace.tilemap.set_cell(4, 9, grass_left)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Bottom edge center tiles should NOT transform (they're part of square, not corners)
    # Only corners might transform, but center should not
    for x in range(6, 9):  # Center tiles (not corners)
        bottom_tile = workspace.tilemap.get_cell(x, 9).map_object
        assert bottom_tile and bottom_tile.tile_type == TileType.DIRT, \
            f"Bottom edge center tile at ({x},9) should remain DIRT, but is {bottom_tile.tile_type if bottom_tile else 'None'}"

