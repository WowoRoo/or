"""Tests for grass to dirt transformation in interior of blocks."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_grass_interior_should_become_dirt():
    """Test that grass in interior of a block (surrounded on all sides) transforms to dirt."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a 3x3 block of grass
    # G G G
    # G G G
    # G G G
    for dx in range(3):
        for dy in range(3):
            grass = Tile(TileType.GRASS, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(grass)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, grass)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Center grass (6,6) should transform to dirt (it's surrounded on all sides)
    center_grass = workspace.tilemap.get_cell(6, 6).map_object
    assert center_grass and center_grass.tile_type == TileType.DIRT
    
    # Edges should remain grass
    # Top-left corner
    top_left = workspace.tilemap.get_cell(5, 5).map_object
    # Top edge
    top_edge = workspace.tilemap.get_cell(6, 5).map_object
    # Left edge
    left_edge = workspace.tilemap.get_cell(5, 6).map_object
    
    assert top_left and top_left.tile_type == TileType.GRASS
    assert top_edge and top_edge.tile_type == TileType.GRASS
    assert left_edge and left_edge.tile_type == TileType.GRASS


def test_grass_with_free_space_should_not_become_dirt():
    """Test that grass with free space (not surrounded) does NOT transform to dirt."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Place single grass tile (not surrounded)
    grass_tile = Tile(TileType.GRASS, workspace.tilemap.get_cell(5, 5).position, layer.id)
    layer.add_map_object(grass_tile)
    workspace.tilemap.set_cell(5, 5, grass_tile)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Grass should NOT transform (it's not surrounded)
    assert grass_tile.tile_type == TileType.GRASS


def test_grass_edges_should_remain_grass():
    """Test that grass on edges of a block (not fully surrounded) remains grass."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Create a 3x3 block of grass
    for dx in range(3):
        for dy in range(3):
            grass = Tile(TileType.GRASS, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
            layer.add_map_object(grass)
            workspace.tilemap.set_cell(5 + dx, 5 + dy, grass)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # All edge tiles should remain grass
    # Top row
    for dx in range(3):
        edge = workspace.tilemap.get_cell(5 + dx, 5).map_object
        assert edge and edge.tile_type == TileType.GRASS
    
    # Bottom row
    for dx in range(3):
        edge = workspace.tilemap.get_cell(5 + dx, 7).map_object
        assert edge and edge.tile_type == TileType.GRASS
    
    # Left column
    for dy in range(3):
        edge = workspace.tilemap.get_cell(5, 5 + dy).map_object
        assert edge and edge.tile_type == TileType.GRASS
    
    # Right column
    for dy in range(3):
        edge = workspace.tilemap.get_cell(7, 5 + dy).map_object
        assert edge and edge.tile_type == TileType.GRASS

