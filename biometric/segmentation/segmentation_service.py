"""Segmentation service (Zaborization)."""

from typing import List
import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap
from domain.value_objects.zaborization_result import ZaborizationResult
from domain.value_objects.region import Region
from domain.value_objects.point import Point


class SegmentationService:
    """Service for segmentation (zaborization)."""
    
    def segment(
        self,
        bitmap: WorkspaceBitmap,
        connectivity: int = 8,
        similarity_threshold: float = 0.5,
        min_region_size: int = 1
    ) -> ZaborizationResult:
        """Segment bitmap into regions."""
        foreground_regions = self._find_foreground_regions(
            bitmap, connectivity, similarity_threshold, min_region_size
        )
        background_regions = self._find_background_regions(
            bitmap, connectivity, similarity_threshold, min_region_size
        )
        
        # Create segmentation map
        segmentation_map = self._create_segmentation_map(
            bitmap, foreground_regions, background_regions, connectivity
        )
        
        return ZaborizationResult(
            foreground_regions=foreground_regions,
            background_regions=background_regions,
            segmentation_map=segmentation_map
        )
    
    def _find_foreground_regions(
        self,
        bitmap: WorkspaceBitmap,
        connectivity: int,
        threshold: float,
        min_size: int
    ) -> List[Region]:
        """Find foreground regions using flood fill.
        Foreground = False (0) in bitmap = tiles.
        """
        visited = np.zeros((bitmap.height, bitmap.width), dtype=bool)
        regions = []
        
        # Visit all pixels to find foreground regions
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                # FOREGROUND = False (0) in bitmap
                pixel_value = bitmap.get_pixel(x, y)
                if not visited[y, x] and not pixel_value:  # Foreground pixel
                    region = self._flood_fill(
                        bitmap, Point(x, y), visited, connectivity, False
                    )
                    if len(region.cells) >= min_size:
                        regions.append(region)
        
        return regions
    
    def _find_background_regions(
        self,
        bitmap: WorkspaceBitmap,
        connectivity: int,
        threshold: float,
        min_size: int
    ) -> List[Region]:
        """Find background regions using flood fill.
        Background = True (1) in bitmap = empty cells or functional tiles.
        """
        visited = np.zeros((bitmap.height, bitmap.width), dtype=bool)
        regions = []
        
        # Visit all pixels to find background regions
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                if not visited[y, x] and bitmap.get_pixel(x, y):  # BACKGROUND = True (1)
                    region = self._flood_fill(
                        bitmap, Point(x, y), visited, connectivity, True
                    )
                    if len(region.cells) >= min_size:
                        regions.append(region)
        
        return regions
    
    def _flood_fill(
        self,
        bitmap: WorkspaceBitmap,
        start: Point,
        visited: np.ndarray,
        connectivity: int,
        target_value: bool
    ) -> Region:
        """Flood fill algorithm."""
        cells = set()
        stack = [start]
        
        if connectivity == 4:
            neighbors = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
        else:  # 8-connectivity
            neighbors = [
                Point(-1, -1), Point(0, -1), Point(1, -1),
                Point(-1, 0), Point(1, 0),
                Point(-1, 1), Point(0, 1), Point(1, 1)
            ]
        
        while stack:
            point = stack.pop()
            x, y = point.x, point.y
            
            if not bitmap.is_valid_coordinate(x, y):
                continue
            
            if visited[y, x]:
                continue
            
            if bitmap.get_pixel(x, y) != target_value:
                continue
            
            visited[y, x] = True
            cells.add(point)
            
            # Add neighbors
            for offset in neighbors:
                neighbor = point + offset
                if (bitmap.is_valid_coordinate(neighbor.x, neighbor.y) and
                    not visited[neighbor.y, neighbor.x] and
                    bitmap.get_pixel(neighbor.x, neighbor.y) == target_value):
                    stack.append(neighbor)
        
        return Region(cells)
    
    def _flood_fill_unclassified(
        self,
        bitmap: WorkspaceBitmap,
        start: Point,
        visited: np.ndarray,
        connectivity: int,
        target_value: bool
    ) -> Region:
        """Flood fill for unclassified pixels (similar to _flood_fill but for unclassified areas)."""
        cells = set()
        stack = [start]
        
        if connectivity == 4:
            neighbors = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
        else:  # 8-connectivity
            neighbors = [
                Point(-1, -1), Point(0, -1), Point(1, -1),
                Point(-1, 0), Point(1, 0),
                Point(-1, 1), Point(0, 1), Point(1, 1)
            ]
        
        while stack:
            point = stack.pop()
            x, y = point.x, point.y
            
            if not bitmap.is_valid_coordinate(x, y):
                continue
            
            if visited[y, x]:
                continue
            
            if bitmap.get_pixel(x, y) != target_value:
                continue
            
            visited[y, x] = True
            cells.add(point)
            
            # Add neighbors
            for offset in neighbors:
                neighbor = point + offset
                if (bitmap.is_valid_coordinate(neighbor.x, neighbor.y) and
                    not visited[neighbor.y, neighbor.x] and
                    bitmap.get_pixel(neighbor.x, neighbor.y) == target_value):
                    stack.append(neighbor)
        
        return Region(cells)
    
    def _create_segmentation_map(
        self,
        bitmap: WorkspaceBitmap,
        foreground_regions: List[Region],
        background_regions: List[Region],
        connectivity: int = 8
    ) -> np.ndarray:
        """Create segmentation map with region IDs.
        Ensures all pixels are classified - unclassified pixels are assigned based on bitmap value.
        """
        segmentation_map = np.zeros((bitmap.height, bitmap.width), dtype=np.int32)
        region_id = 1
        
        # Mark foreground regions (positive IDs)
        for region in foreground_regions:
            for point in region.cells:
                segmentation_map[point.y, point.x] = region_id
            region_id += 1
        
        # Mark background regions (negative IDs)
        bg_region_id = 1
        for region in background_regions:
            for point in region.cells:
                segmentation_map[point.y, point.x] = -bg_region_id
            bg_region_id += 1
        
        # Ensure all pixels are classified - assign unclassified pixels based on bitmap value
        # Create sets of classified pixels for faster lookup
        classified_foreground = set()
        for region in foreground_regions:
            classified_foreground.update(region.cells)
        
        classified_background = set()
        for region in background_regions:
            classified_background.update(region.cells)
        
        # Assign unclassified pixels - group them into regions using flood fill
        unclassified_visited = np.zeros((bitmap.height, bitmap.width), dtype=bool)
        next_bg_id = bg_region_id
        next_fg_id = region_id
        
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                point = Point(x, y)
                if point not in classified_foreground and point not in classified_background:
                    if not unclassified_visited[y, x]:
                        # Start new region for unclassified pixels
                        pixel_value = bitmap.get_pixel(x, y)
                        # Use flood fill to group connected unclassified pixels
                        unclassified_region = self._flood_fill_unclassified(
                            bitmap, point, unclassified_visited, connectivity, pixel_value
                        )
                        # Assign region ID based on pixel value
                        if pixel_value:
                            # Background - assign negative ID
                            for p in unclassified_region.cells:
                                segmentation_map[p.y, p.x] = -next_bg_id
                            next_bg_id += 1
                        else:
                            # Foreground - assign positive ID
                            for p in unclassified_region.cells:
                                segmentation_map[p.y, p.x] = next_fg_id
                            next_fg_id += 1
        
        return segmentation_map

