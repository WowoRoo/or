"""Tests for tile transformation."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_to_grass_with_free_space_above():
    """Test that dirt transforms to grass when has free space above AND grass on side."""
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
    
    # Place grass on the right (required for transformation)
    grass_tile = Tile(TileType.GRASS, workspace.tilemap.get_cell(6, 5).position, layer.id)
    layer.add_map_object(grass_tile)
    workspace.tilemap.set_cell(6, 5, grass_tile)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    assert count > 0
    assert dirt_tile.tile_type == TileType.GRASS


def test_lava_water_to_stone():
    """Test that lava touching water transforms to stone."""
    tile_list_ref = TileListReference(list(TileType))
    func_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
    
    workspace = Workspace.create_new(
        "Test", "User", 10, 10,
        tile_list_ref, func_tile_list_ref
    )
    
    layer = workspace.get_active_layer()
    
    # Place lava tile
    lava_tile = Tile(TileType.LAVA, workspace.tilemap.get_cell(5, 5).position, layer.id)
    layer.add_map_object(lava_tile)
    workspace.tilemap.set_cell(5, 5, lava_tile)
    
    # Place water tile next to it
    water_tile = Tile(TileType.WATER, workspace.tilemap.get_cell(6, 5).position, layer.id)
    layer.add_map_object(water_tile)
    workspace.tilemap.set_cell(6, 5, water_tile)
    
    service = TransformationService(SegmentationService())
    count = service.apply_transformations(workspace)
    
    assert count > 0
    # Either lava or water should transform to stone
    assert (lava_tile.tile_type == TileType.STONE or 
            water_tile.tile_type == TileType.STONE)

