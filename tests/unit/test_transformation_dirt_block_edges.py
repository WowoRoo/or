"""Tests for dirt block edges growing grass."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_block_edges_should_grow_grass():
    """Test that edges of a dirt block should grow grass even without adjacent grass."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a 3x3 block of dirt
    # D D D
    # D D D
    # D D D
    for dx in range(3):
        for dy in range(3):
            dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(dirt)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, dirt)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Center dirt (6,6) should NOT transform (it's surrounded)
    center_dirt = workspace.tilemap.get_cell(6, 6).map_object
    assert center_dirt and center_dirt.tile_type == TileType.DIRT
    
    # Edges should transform to grass (they have free space on one side)
    # Top edge
    top_edge = workspace.tilemap.get_cell(6, 5).map_object
    # Bottom edge
    bottom_edge = workspace.tilemap.get_cell(6, 7).map_object
    # Left edge
    left_edge = workspace.tilemap.get_cell(5, 6).map_object
    # Right edge
    right_edge = workspace.tilemap.get_cell(7, 6).map_object
    
    # At least some edges should transform
    edges_transformed = sum([
        top_edge and top_edge.tile_type == TileType.GRASS,
        bottom_edge and bottom_edge.tile_type == TileType.GRASS,
        left_edge and left_edge.tile_type == TileType.GRASS,
        right_edge and right_edge.tile_type == TileType.GRASS,
    ])
    assert edges_transformed > 0, "At least one edge should transform to grass"


def test_dirt_block_corners_should_grow_grass():
    """Test that corners of a dirt block should grow grass."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a 3x3 block of dirt
    for dx in range(3):
        for dy in range(3):
            dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(dirt)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, dirt)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Corners should transform to grass (they have free space on two sides)
    # Top-left corner
    top_left = workspace.tilemap.get_cell(5, 5).map_object
    # Top-right corner
    top_right = workspace.tilemap.get_cell(7, 5).map_object
    # Bottom-left corner
    bottom_left = workspace.tilemap.get_cell(5, 7).map_object
    # Bottom-right corner
    bottom_right = workspace.tilemap.get_cell(7, 7).map_object
    
    # At least some corners should transform
    corners_transformed = sum([
        top_left and top_left.tile_type == TileType.GRASS,
        top_right and top_right.tile_type == TileType.GRASS,
        bottom_left and bottom_left.tile_type == TileType.GRASS,
        bottom_right and bottom_right.tile_type == TileType.GRASS,
    ])
    assert corners_transformed > 0, "At least one corner should transform to grass"

