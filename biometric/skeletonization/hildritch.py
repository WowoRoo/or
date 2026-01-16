"""Hildritch skeletonization algorithm."""

import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap


def hildritch(bitmap: WorkspaceBitmap) -> WorkspaceBitmap:
    """Apply Hildritch thinning algorithm.
    
    Hildritch skeletonizes pixels with value 1 (foreground in algorithm terms).
    Input bitmap should have 1 = pixels to skeletonize, 0 = background.
    """
    # Convert to uint8 for processing
    skeleton = bitmap.data.copy().astype(np.uint8)
    
    # Ensure we're working with 0/1 values
    skeleton = (skeleton > 0).astype(np.uint8)
    
    changed = True
    iteration = 0
    max_iterations = 1000
    
    while changed and iteration < max_iterations:
        changed = False
        iteration += 1
        
        to_remove = []
        for y in range(1, skeleton.shape[0] - 1):
            for x in range(1, skeleton.shape[1] - 1):
                if skeleton[y, x] == 1:  # Pixel to skeletonize
                    if _hildritch_conditions(skeleton, x, y):
                        to_remove.append((x, y))
        
        for x, y in to_remove:
            skeleton[y, x] = 0
            changed = True
    
    return WorkspaceBitmap(skeleton.astype(bool), bitmap.width, bitmap.height)


def _hildritch_conditions(skeleton: np.ndarray, x: int, y: int) -> bool:
    """Check Hildritch conditions for pixel removal."""
    # Get 8-neighborhood
    p2 = skeleton[y-1, x] if y > 0 else 0
    p3 = skeleton[y-1, x+1] if (y > 0 and x+1 < skeleton.shape[1]) else 0
    p4 = skeleton[y, x+1] if x+1 < skeleton.shape[1] else 0
    p5 = skeleton[y+1, x+1] if (y+1 < skeleton.shape[0] and x+1 < skeleton.shape[1]) else 0
    p6 = skeleton[y+1, x] if y+1 < skeleton.shape[0] else 0
    p7 = skeleton[y+1, x-1] if (y+1 < skeleton.shape[0] and x > 0) else 0
    p8 = skeleton[y, x-1] if x > 0 else 0
    p9 = skeleton[y-1, x-1] if (y > 0 and x > 0) else 0
    
    neighbors = [p2, p3, p4, p5, p6, p7, p8, p9]
    B = sum(neighbors)  # Number of 1-neighbors
    
    # Count 0->1 transitions
    transitions = 0
    for i in range(8):
        if neighbors[i] == 0 and neighbors[(i+1) % 8] == 1:
            transitions += 1
    
    # Hildritch conditions:
    # 1. 2 <= B <= 6
    # 2. A = 1 (exactly one transition)
    # 3. At least one of p2, p4, p6 is 0
    # 4. At least one of p4, p6, p8 is 0
    
    condition_1 = 2 <= B <= 6
    condition_2 = transitions == 1
    condition_3 = (p2 == 0 or p4 == 0 or p6 == 0)
    condition_4 = (p4 == 0 or p6 == 0 or p8 == 0)
    
    return condition_1 and condition_2 and condition_3 and condition_4

