"""Tests for dirt transformation when surrounded."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_surrounded_should_not_transform():
    """Test that dirt surrounded on all sides does NOT transform to grass."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Place dirt tile in center
    center_dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5, 5).position, layer.id)
    layer.add_map_object(center_dirt)
    workspace.tilemap.set_cell(5, 5, center_dirt)
    
    # Surround it with dirt on all sides
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # left, right, top, bottom
        dirt = Tile(TileType.DIRT, workspace.tilemap.get_cell(5 + dx, 5 + dy).position, layer.id)
        layer.add_map_object(dirt)
        workspace.tilemap.set_cell(5 + dx, 5 + dy, dirt)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Center dirt should NOT transform (it's surrounded)
    assert center_dirt.tile_type == TileType.DIRT


def test_dirt_with_grass_on_side_should_transform():
    """Test that dirt with grass on left, right, or top transforms to grass."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Place dirt tile
    dirt_tile = Tile(TileType.DIRT, workspace.tilemap.get_cell(5, 5).position, layer.id)
    layer.add_map_object(dirt_tile)
    workspace.tilemap.set_cell(5, 5, dirt_tile)
    
    # Place grass on the right
    grass_tile = Tile(TileType.GRASS, workspace.tilemap.get_cell(6, 5).position, layer.id)
    layer.add_map_object(grass_tile)
    workspace.tilemap.set_cell(6, 5, grass_tile)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Dirt should transform to grass (has grass on the right)
    assert dirt_tile.tile_type == TileType.GRASS


def test_dirt_with_grass_only_below_should_not_transform():
    """Test that dirt with grass only below does NOT transform."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Place dirt tile
    dirt_tile = Tile(TileType.DIRT, workspace.tilemap.get_cell(5, 5).position, layer.id)
    layer.add_map_object(dirt_tile)
    workspace.tilemap.set_cell(5, 5, dirt_tile)
    
    # Place grass only below (should NOT transform)
    grass_tile = Tile(TileType.GRASS, workspace.tilemap.get_cell(5, 6).position, layer.id)
    layer.add_map_object(grass_tile)
    workspace.tilemap.set_cell(5, 6, grass_tile)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    # Dirt should NOT transform (grass is only below, not on sides or top)
    assert dirt_tile.tile_type == TileType.DIRT

