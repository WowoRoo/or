"""Zhang-Suen skeletonization algorithm."""

import numpy as np
from domain.value_objects.workspace_bitmap import WorkspaceBitmap


def zhang_suen(bitmap: WorkspaceBitmap) -> WorkspaceBitmap:
    """Apply Zhang-Suen thinning algorithm.
    
    Zhang-Suen skeletonizes pixels with value 1 (foreground in algorithm terms).
    Input bitmap should have 1 = pixels to skeletonize, 0 = background.
    """
    # Convert to uint8 for processing
    skeleton = bitmap.data.copy().astype(np.uint8)
    
    # Ensure we're working with 0/1 values
    skeleton = (skeleton > 0).astype(np.uint8)
    
    # Zhang-Suen works on 1 = foreground (pixels to skeletonize), 0 = background
    changed = True
    iteration = 0
    max_iterations = 1000
    
    while changed and iteration < max_iterations:
        changed = False
        iteration += 1
        
        # Subiteration 1
        to_remove_1 = []
        for y in range(1, skeleton.shape[0] - 1):
            for x in range(1, skeleton.shape[1] - 1):
                if skeleton[y, x] == 1:  # Pixel to skeletonize
                    if _zhang_suen_condition_1(skeleton, x, y) and _zhang_suen_condition_2(skeleton, x, y):
                        to_remove_1.append((x, y))
        
        for x, y in to_remove_1:
            skeleton[y, x] = 0
            changed = True
        
        # Subiteration 2
        to_remove_2 = []
        for y in range(1, skeleton.shape[0] - 1):
            for x in range(1, skeleton.shape[1] - 1):
                if skeleton[y, x] == 1:  # Pixel to skeletonize
                    if _zhang_suen_condition_3(skeleton, x, y) and _zhang_suen_condition_2(skeleton, x, y):
                        to_remove_2.append((x, y))
        
        for x, y in to_remove_2:
            skeleton[y, x] = 0
            changed = True
    
    return WorkspaceBitmap(skeleton.astype(bool), bitmap.width, bitmap.height)


def _zhang_suen_condition_1(skeleton: np.ndarray, x: int, y: int) -> bool:
    """Check Zhang-Suen condition 1 for subiteration 1.
    Condition: (p2 * p4 * p6 == 0) AND (p4 * p6 * p8 == 0)
    """
    # Get 8-neighborhood
    p2 = skeleton[y-1, x] if y > 0 else 0
    p3 = skeleton[y-1, x+1] if (y > 0 and x+1 < skeleton.shape[1]) else 0
    p4 = skeleton[y, x+1] if x+1 < skeleton.shape[1] else 0
    p5 = skeleton[y+1, x+1] if (y+1 < skeleton.shape[0] and x+1 < skeleton.shape[1]) else 0
    p6 = skeleton[y+1, x] if y+1 < skeleton.shape[0] else 0
    p7 = skeleton[y+1, x-1] if (y+1 < skeleton.shape[0] and x > 0) else 0
    p8 = skeleton[y, x-1] if x > 0 else 0
    p9 = skeleton[y-1, x-1] if (y > 0 and x > 0) else 0
    
    # Condition 1: p2 * p4 * p6 = 0 (at least one is background)
    # Condition 2: p4 * p6 * p8 = 0 (at least one is background)
    return (p2 * p4 * p6 == 0) and (p4 * p6 * p8 == 0)


def _zhang_suen_condition_2(skeleton: np.ndarray, x: int, y: int) -> bool:
    """Check Zhang-Suen condition 2 (common for both subiterations)."""
    # Get 8-neighborhood
    p2 = skeleton[y-1, x] if y > 0 else 0
    p3 = skeleton[y-1, x+1] if (y > 0 and x+1 < skeleton.shape[1]) else 0
    p4 = skeleton[y, x+1] if x+1 < skeleton.shape[1] else 0
    p5 = skeleton[y+1, x+1] if (y+1 < skeleton.shape[0] and x+1 < skeleton.shape[1]) else 0
    p6 = skeleton[y+1, x] if y+1 < skeleton.shape[0] else 0
    p7 = skeleton[y+1, x-1] if (y+1 < skeleton.shape[0] and x > 0) else 0
    p8 = skeleton[y, x-1] if x > 0 else 0
    p9 = skeleton[y-1, x-1] if (y > 0 and x > 0) else 0
    
    # Count neighbors
    neighbors = [p2, p3, p4, p5, p6, p7, p8, p9]
    B = sum(neighbors)  # Number of 1-neighbors
    
    # Count 0->1 transitions
    transitions = 0
    for i in range(8):
        if neighbors[i] == 0 and neighbors[(i+1) % 8] == 1:
            transitions += 1
    
    # Condition: 2 <= B <= 6 and A = 1
    return 2 <= B <= 6 and transitions == 1


def _zhang_suen_condition_3(skeleton: np.ndarray, x: int, y: int) -> bool:
    """Check Zhang-Suen condition 3 for subiteration 2.
    Condition: (p2 * p4 * p8 == 0) AND (p2 * p6 * p8 == 0)
    """
    # Get 8-neighborhood
    p2 = skeleton[y-1, x] if y > 0 else 0
    p3 = skeleton[y-1, x+1] if (y > 0 and x+1 < skeleton.shape[1]) else 0
    p4 = skeleton[y, x+1] if x+1 < skeleton.shape[1] else 0
    p5 = skeleton[y+1, x+1] if (y+1 < skeleton.shape[0] and x+1 < skeleton.shape[1]) else 0
    p6 = skeleton[y+1, x] if y+1 < skeleton.shape[0] else 0
    p7 = skeleton[y+1, x-1] if (y+1 < skeleton.shape[0] and x > 0) else 0
    p8 = skeleton[y, x-1] if x > 0 else 0
    p9 = skeleton[y-1, x-1] if (y > 0 and x > 0) else 0
    
    # Condition 1: p2 * p4 * p8 = 0 (at least one is background)
    # Condition 2: p2 * p6 * p8 = 0 (at least one is background)
    return (p2 * p4 * p8 == 0) and (p2 * p6 * p8 == 0)

