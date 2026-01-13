"""Tests for dirt transformation at bottom edge."""

import pytest
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.entities.tile import Tile
from editing.tile_transformation.transformation_service import TransformationService
from biometric.segmentation.segmentation_service import SegmentationService


def test_dirt_bottom_edge_should_not_grow():
    """Test that dirt at bottom edge of a block should NOT grow grass."""
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
    
    # Bottom edge center (6,7) should NOT transform (only has free space below)
    bottom_center = workspace.tilemap.get_cell(6, 7).map_object
    assert bottom_center and bottom_center.tile_type == TileType.DIRT
    
    # Top edge should transform (has free space above)
    top_edge = workspace.tilemap.get_cell(6, 5).map_object
    assert top_edge and top_edge.tile_type == TileType.GRASS
    
    # Left edge should transform (has free space on left)
    left_edge = workspace.tilemap.get_cell(5, 6).map_object
    assert left_edge and left_edge.tile_type == TileType.GRASS
    
    # Right edge should transform (has free space on right)
    right_edge = workspace.tilemap.get_cell(7, 6).map_object
    assert right_edge and right_edge.tile_type == TileType.GRASS

