"""Service for automatic tile transformation based on neighbors using biometric algorithms."""

from typing import List, Optional, Tuple
from domain.entities.workspace import Workspace
from domain.entities.tilemap import Tilemap
from domain.entities.tile import Tile
from domain.entities.map_object import MapObject
from domain.enums.tile_type import TileType
from domain.value_objects.point import Point
from domain.enums.map_object_type import MapObjectType
from biometric.segmentation.segmentation_service import SegmentationService
from biometric.conversion.bitmap_converter import BitmapConverter
from domain.value_objects.region import Region


class TransformationService:
    """Service for transforming tiles based on neighbor rules using biometric segmentation."""
    
    def __init__(self, segmentation_service: SegmentationService = None):
        self.segmentation_service = segmentation_service or SegmentationService()
        self.bitmap_converter = BitmapConverter()
    
    def apply_transformations(self, workspace: Workspace) -> int:
        """Apply all transformation rules to workspace using biometric segmentation (zaborization)."""
        transformations_count = 0
        
        # Step 1: Use zaborization (segmentation) to detect regions
        # Convert workspace to bitmap for biometric analysis
        bitmap = self.bitmap_converter.convert_to_bitmap(workspace)
        
        # Step 2: Apply zaborization to segment workspace into regions
        segmentation_result = self.segmentation_service.segment(bitmap, connectivity=8)
        
        # Step 3: Analyze regions and apply transformations based on biometric analysis
        transformations_to_apply = []
        
        for layer in workspace.layers:
            if not layer.visible or not layer.editable:
                continue
            
            for obj in layer.get_map_objects():
                if not isinstance(obj, Tile):
                    continue
                
                # Use zaborization result to get region context
                x, y = obj.position.x, obj.position.y
                region_id = segmentation_result.segmentation_map[y, x] if (
                    y < segmentation_result.segmentation_map.shape[0] and
                    x < segmentation_result.segmentation_map.shape[1]
                ) else 0
                
                # Check transformation rules using both direct neighbors and region analysis
                new_tile_type = self._check_transformation_rules_with_segmentation(
                    workspace.tilemap, obj, layer, segmentation_result, region_id
                )
                
                if new_tile_type and new_tile_type != obj.tile_type:
                    transformations_to_apply.append((obj, new_tile_type))
        
        # Apply all transformations
        for obj, new_type in transformations_to_apply:
            obj.tile_type = new_type
            transformations_count += 1
        
        return transformations_count
    
    def _check_transformation_rules_with_segmentation(
        self,
        tilemap: Tilemap,
        tile: Tile,
        layer,
        segmentation_result,
        region_id: int
    ) -> Optional[TileType]:
        """Check if tile should be transformed based on rules using biometric segmentation."""
        x, y = tile.position.x, tile.position.y
        
        # Get adjacent regions using zaborization result
        adjacent_region_ids = self._get_adjacent_region_ids(x, y, segmentation_result)
        
        # Rule 1: Dirt -> Grass if has free space above AND grass is on left, right, or top
        # Rule 2: Dirt -> Grass if adjacent to grass blocks on left, right, or top (not bottom)
        # But NOT if surrounded on all sides or has something below
        
        if tile.tile_type == TileType.DIRT:
            # Check if dirt is surrounded on all sides (should NOT transform)
            if self._is_surrounded_on_all_sides(tilemap, x, y):
                return None  # Don't transform if completely surrounded
            
            # Check if has something above (is part of a square/block)
            has_something_above = not self._has_free_space_above(tilemap, x, y)
            
            if has_something_above:
                # If has something above, check if it's an edge (not fully surrounded)
                # But only transform if it has free space on top/left/right (NOT just bottom)
                if not self._is_surrounded_on_all_sides(tilemap, x, y):
                    # Check if has free space on top, left, or right (NOT bottom)
                    has_free_top = self._has_free_space_above(tilemap, x, y)
                    has_free_left = self._has_free_space_on_side(tilemap, x, y, -1, 0)  # Left
                    has_free_right = self._has_free_space_on_side(tilemap, x, y, 1, 0)   # Right
                    has_free_below = self._has_free_space_on_side(tilemap, x, y, 0, 1)  # Bottom
                    
                    # Check if has grass on left, right, or top (corners with grass should transform)
                    has_grass_on_sides = self._is_adjacent_to_grass_sides_or_top(tilemap, x, y, layer)
                    
                    # If has free space below AND no free space above, check if it's a corner with grass
                    # Bottom edge center should NOT transform, but corners with grass can transform
                    if has_free_below and not has_free_top:
                        if has_grass_on_sides:
                            # Check if it's a corner (has grass on one side, not both)
                            from domain.entities.tile import Tile
                            has_grass_left = False
                            has_grass_right = False
                            if tilemap.is_valid_coordinate(x - 1, y):
                                cell_left = tilemap.get_cell(x - 1, y)
                                if cell_left and cell_left.map_object and isinstance(cell_left.map_object, Tile):
                                    if cell_left.map_object.tile_type == TileType.GRASS:
                                        has_grass_left = True
                            if tilemap.is_valid_coordinate(x + 1, y):
                                cell_right = tilemap.get_cell(x + 1, y)
                                if cell_right and cell_right.map_object and isinstance(cell_right.map_object, Tile):
                                    if cell_right.map_object.tile_type == TileType.GRASS:
                                        has_grass_right = True
                            # Corner = has grass on one side (left XOR right), not both
                            is_corner = (has_grass_left and not has_grass_right) or (has_grass_right and not has_grass_left)
                            if is_corner:
                                # It's a corner with grass - transform
                                return TileType.GRASS
                        # Not a corner or no grass - don't transform (bottom edge)
                        return None
                    
                    # Transform if:
                    # 1. Has free space on top (top edge)
                    # 2. Has free space on left/right AND no free space below (left/right edges, not bottom)
                    if has_free_top:
                        # It's a top edge - transform to grass
                        return TileType.GRASS
                    if (has_free_left or has_free_right) and not has_free_below:
                        # It's a left/right edge (not bottom) - transform to grass
                        return TileType.GRASS
                # Fully surrounded or only has free space below - don't transform
                return None
            
            # If no something above (has free space above), dirt should transform to grass
            # But NOT if only has free space below (bottom edge should not transform)
            has_something_below = self._has_something_below(tilemap, x, y)
            has_free_below = self._has_free_space_on_side(tilemap, x, y, 0, 1)  # Bottom
            
            # If only has free space below (and not above), don't transform (bottom edge)
            if has_free_below and not self._has_free_space_above(tilemap, x, y):
                return None
            
            # If has something below (not free space), check if grass is on sides/top
            # BUT if has free space above AND is part of a block (has something on left/right), transform (top edge)
            if has_something_below:
                # Check if is part of a block (has something on left or right)
                has_something_left = not self._has_free_space_on_side(tilemap, x, y, -1, 0)
                has_something_right = not self._has_free_space_on_side(tilemap, x, y, 1, 0)
                is_part_of_block = has_something_left or has_something_right
                
                # If has free space above AND is part of a block, transform (top edge of block)
                if self._has_free_space_above(tilemap, x, y) and is_part_of_block:
                    return TileType.GRASS
                # No free space above or not part of block - check if grass is on sides/top
                has_grass_adjacent = self._is_adjacent_to_grass_sides_or_top(tilemap, x, y, layer)
                has_grass_in_regions = self._adjacent_regions_contain_grass_sides_or_top(tilemap, x, y, adjacent_region_ids, segmentation_result)
                if has_grass_adjacent or has_grass_in_regions:
                    # Has grass on sides/top - transform
                    return TileType.GRASS
                # Has something below but no grass on sides/top - don't transform
                return None
            
            # Has free space above and nothing below - transform to grass
            return TileType.GRASS
        
        # Rule 3: Lava + Water -> Stone (using region analysis)
        if tile.tile_type == TileType.LAVA:
            # Check direct neighbors
            if self._touches_water(tilemap, x, y, layer):
                return TileType.STONE
            # Check if adjacent regions contain water
            if self._adjacent_regions_contain_water(tilemap, adjacent_region_ids, segmentation_result):
                return TileType.STONE
        
        # Rule 4: Water + Lava -> Stone (using region analysis)
        if tile.tile_type == TileType.WATER:
            # Check direct neighbors
            if self._touches_lava(tilemap, x, y, layer):
                return TileType.STONE
            # Check if adjacent regions contain lava
            if self._adjacent_regions_contain_lava(tilemap, adjacent_region_ids, segmentation_result):
                return TileType.STONE
        
        # Rule 5: Grass -> Dirt if surrounded on all sides (interior of grass block)
        if tile.tile_type == TileType.GRASS:
            # Check if grass is surrounded on all sides (left, right, top, bottom)
            if self._is_surrounded_on_all_sides(tilemap, x, y):
                # Interior grass should become dirt
                return TileType.DIRT
        
        return None
    
    def _get_adjacent_region_ids(
        self,
        x: int,
        y: int,
        segmentation_result
    ) -> List[int]:
        """Get adjacent region IDs using zaborization segmentation map."""
        adjacent_regions = set()
        
        if (y >= segmentation_result.segmentation_map.shape[0] or
            x >= segmentation_result.segmentation_map.shape[1]):
            return []
        
        # Check 8-connectivity neighbors
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if (0 <= ny < segmentation_result.segmentation_map.shape[0] and
                    0 <= nx < segmentation_result.segmentation_map.shape[1]):
                    region_id = segmentation_result.segmentation_map[ny, nx]
                    if region_id != 0:
                        adjacent_regions.add(int(region_id))
        
        return list(adjacent_regions)
    
    def _adjacent_regions_contain_grass(
        self,
        tilemap: Tilemap,
        adjacent_region_ids: List[int],
        segmentation_result
    ) -> bool:
        """Check if adjacent regions contain grass tiles using segmentation."""
        # Check tiles in adjacent regions
        for region in segmentation_result.foreground_regions:
            for point in region.cells:
                cell = tilemap.get_cell(point.x, point.y)
                if cell and cell.map_object and isinstance(cell.map_object, Tile):
                    if cell.map_object.tile_type == TileType.GRASS:
                        # Check if this region is adjacent
                        region_id = segmentation_result.segmentation_map[point.y, point.x]
                        if region_id in adjacent_region_ids:
                            return True
        return False
    
    def _adjacent_regions_contain_water(
        self,
        tilemap: Tilemap,
        adjacent_region_ids: List[int],
        segmentation_result
    ) -> bool:
        """Check if adjacent regions contain water tiles using segmentation."""
        for region in segmentation_result.foreground_regions:
            for point in region.cells:
                cell = tilemap.get_cell(point.x, point.y)
                if cell and cell.map_object and isinstance(cell.map_object, Tile):
                    if cell.map_object.tile_type == TileType.WATER:
                        region_id = segmentation_result.segmentation_map[point.y, point.x]
                        if region_id in adjacent_region_ids:
                            return True
        return False
    
    def _adjacent_regions_contain_lava(
        self,
        tilemap: Tilemap,
        adjacent_region_ids: List[int],
        segmentation_result
    ) -> bool:
        """Check if adjacent regions contain lava tiles using segmentation."""
        for region in segmentation_result.foreground_regions:
            for point in region.cells:
                cell = tilemap.get_cell(point.x, point.y)
                if cell and cell.map_object and isinstance(cell.map_object, Tile):
                    if cell.map_object.tile_type == TileType.LAVA:
                        region_id = segmentation_result.segmentation_map[point.y, point.x]
                        if region_id in adjacent_region_ids:
                            return True
        return False
    
    def _has_free_space_above(self, tilemap: Tilemap, x: int, y: int) -> bool:
        """Check if there's free space above the tile."""
        if y <= 0:
            return True  # Top of map is considered free space
        
        cell_above = tilemap.get_cell(x, y - 1)
        return cell_above is None or cell_above.is_empty()
    
    def _has_something_below(self, tilemap: Tilemap, x: int, y: int) -> bool:
        """Check if there's something below the tile."""
        if y >= tilemap.height - 1:
            return False  # Bottom of map is considered empty
        
        cell_below = tilemap.get_cell(x, y + 1)
        return cell_below is not None and not cell_below.is_empty()
    
    def _has_free_space_on_side(self, tilemap: Tilemap, x: int, y: int, dx: int, dy: int) -> bool:
        """Check if there's free space on a specific side (dx, dy) of the tile."""
        nx, ny = x + dx, y + dy
        if not tilemap.is_valid_coordinate(nx, ny):
            return True  # Edge of map is considered free space
        
        cell = tilemap.get_cell(nx, ny)
        return cell is None or cell.is_empty()
    
    def _is_surrounded_on_all_sides(self, tilemap: Tilemap, x: int, y: int) -> bool:
        """Check if tile is surrounded on all sides (left, right, top, bottom)."""
        # Check all 4 sides
        sides = [
            (x - 1, y),  # Left
            (x + 1, y),  # Right
            (x, y - 1),  # Top
            (x, y + 1),  # Bottom
        ]
        
        for nx, ny in sides:
            if not tilemap.is_valid_coordinate(nx, ny):
                return False  # Not surrounded if at map edge
            
            cell = tilemap.get_cell(nx, ny)
            if not cell or cell.is_empty():
                return False  # Not surrounded if has empty space
        
        return True  # All sides have something
    
    def _is_corner_of_square(self, tilemap: Tilemap, x: int, y: int, layer) -> bool:
        """Check if tile is at a corner of a square (has something above and grass on one side)."""
        from domain.entities.tile import Tile
        
        # Check if has something above
        if self._has_free_space_above(tilemap, x, y):
            return False  # Not a corner if no something above
        
        # Check if has grass on left OR right side (not both, and not center)
        has_grass_left = False
        has_grass_right = False
        has_dirt_left = False
        has_dirt_right = False
        
        if tilemap.is_valid_coordinate(x - 1, y):
            cell_left = tilemap.get_cell(x - 1, y)
            if cell_left and cell_left.map_object:
                if isinstance(cell_left.map_object, Tile):
                    if cell_left.map_object.tile_type == TileType.GRASS:
                        has_grass_left = True
                    elif cell_left.map_object.tile_type == TileType.DIRT:
                        has_dirt_left = True
        
        if tilemap.is_valid_coordinate(x + 1, y):
            cell_right = tilemap.get_cell(x + 1, y)
            if cell_right and cell_right.map_object:
                if isinstance(cell_right.map_object, Tile):
                    if cell_right.map_object.tile_type == TileType.GRASS:
                        has_grass_right = True
                    elif cell_right.map_object.tile_type == TileType.DIRT:
                        has_dirt_right = True
        
        # Corner = has something above AND has grass on one side AND dirt on the other
        # OR has grass on one side and empty on the other
        return (has_grass_left and (has_dirt_right or not has_grass_right)) or \
               (has_grass_right and (has_dirt_left or not has_grass_left))
    
    def _is_adjacent_to_grass_sides_or_top(
        self,
        tilemap: Tilemap,
        x: int,
        y: int,
        layer
    ) -> bool:
        """Check if tile is adjacent to grass blocks on left, right, or top (not bottom)."""
        from domain.entities.tile import Tile
        
        # Check left, right, and top (NOT diagonal - that's checked separately)
        neighbors = [
            (x - 1, y),      # Left
            (x + 1, y),      # Right
            (x, y - 1),      # Top
        ]
        
        for nx, ny in neighbors:
            if not tilemap.is_valid_coordinate(nx, ny):
                continue
            
            cell = tilemap.get_cell(nx, ny)
            if cell and cell.map_object:
                if isinstance(cell.map_object, Tile):
                    if cell.map_object.tile_type == TileType.GRASS:
                        return True
        
        return False
    
    def _is_adjacent_to_grass_diagonal(
        self,
        tilemap: Tilemap,
        x: int,
        y: int,
        layer
    ) -> bool:
        """Check if tile is adjacent to grass blocks on diagonal corners (top-left, top-right)."""
        from domain.entities.tile import Tile
        
        # Check only diagonal corners (top-left, top-right)
        # This indicates a corner of a square
        neighbors = [
            (x - 1, y - 1),  # Top-left (diagonal)
            (x + 1, y - 1),  # Top-right (diagonal)
        ]
        
        for nx, ny in neighbors:
            if not tilemap.is_valid_coordinate(nx, ny):
                continue
            
            cell = tilemap.get_cell(nx, ny)
            if cell and cell.map_object:
                if isinstance(cell.map_object, Tile):
                    if cell.map_object.tile_type == TileType.GRASS:
                        return True
        
        return False
    
    def _adjacent_regions_contain_grass_sides_or_top(
        self,
        tilemap: Tilemap,
        x: int,
        y: int,
        adjacent_region_ids: List[int],
        segmentation_result
    ) -> bool:
        """Check if adjacent regions (left, right, top, diagonals) contain grass tiles."""
        # Check tiles in adjacent regions, including diagonal corners
        for region in segmentation_result.foreground_regions:
            for point in region.cells:
                # Check if point is on left, right, top, or diagonal corners (top-left, top-right)
                if not ((point.x == x - 1 and point.y == y) or      # Left
                        (point.x == x + 1 and point.y == y) or      # Right
                        (point.x == x and point.y == y - 1) or      # Top
                        (point.x == x - 1 and point.y == y - 1) or # Top-left
                        (point.x == x + 1 and point.y == y - 1)):   # Top-right
                    continue
                
                cell = tilemap.get_cell(point.x, point.y)
                if cell and cell.map_object and isinstance(cell.map_object, Tile):
                    if cell.map_object.tile_type == TileType.GRASS:
                        region_id = segmentation_result.segmentation_map[point.y, point.x]
                        if region_id in adjacent_region_ids:
                            return True
        return False
    
    def _touches_water(
        self,
        tilemap: Tilemap,
        x: int,
        y: int,
        layer
    ) -> bool:
        """Check if tile touches water (8-connectivity)."""
        from domain.entities.tile import Tile
        
        # Check 8-connectivity neighbors
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if not tilemap.is_valid_coordinate(nx, ny):
                    continue
                
                cell = tilemap.get_cell(nx, ny)
                if cell and cell.map_object:
                    if isinstance(cell.map_object, Tile):
                        if cell.map_object.tile_type == TileType.WATER:
                            return True
        
        return False
    
    def _touches_lava(
        self,
        tilemap: Tilemap,
        x: int,
        y: int,
        layer
    ) -> bool:
        """Check if tile touches lava (8-connectivity)."""
        from domain.entities.tile import Tile
        
        # Check 8-connectivity neighbors
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if not tilemap.is_valid_coordinate(nx, ny):
                    continue
                
                cell = tilemap.get_cell(nx, ny)
                if cell and cell.map_object:
                    if isinstance(cell.map_object, Tile):
                        if cell.map_object.tile_type == TileType.LAVA:
                            return True
        
        return False
    
    def apply_transformations_iterative(
        self,
        workspace: Workspace,
        max_iterations: int = 10
    ) -> int:
        """Apply transformations iteratively until no more changes."""
        total_transformations = 0
        
        for iteration in range(max_iterations):
            transformations = self.apply_transformations(workspace)
            total_transformations += transformations
            
            if transformations == 0:
                break  # No more transformations needed
        
        return total_transformations

