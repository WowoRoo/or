# Specyfikacja Modeli Danych

## Domain Entities

### 1. WORKSPACE (Root Entity)

```python
class Workspace:
    id: UUID
    metadata: WorkspaceMetadata
    tilemap: Tilemap
    berlin_wall: BerlinWall
    layers: List[Layer]
    features_vector: Optional[FeaturesVector]
    workspace_bitmap: Optional[WorkspaceBitmap]
    
    def create_new(width: int, height: int) -> Workspace
    def save(path: str) -> None
    def load(path: str) -> Workspace
    def add_layer(layer: Layer) -> None
    def remove_layer(layer_id: UUID) -> None
    def get_active_layer() -> Layer
    def detect_berlin_wall() -> None
```

### 2. TILEMAP (Entity)

```python
class Tilemap:
    width: int
    height: int
    cells: Dict[Tuple[int, int], TileCell]
    
    def get_cell(x: int, y: int) -> Optional[TileCell]
    def set_cell(x: int, y: int, map_object: Optional[MapObject]) -> None
    def get_region(x: int, y: int) -> Region
    def is_valid_coordinate(x: int, y: int) -> bool
    def to_bitmap() -> WorkspaceBitmap
```

### 3. LAYER (Entity)

```python
class Layer:
    id: UUID
    name: str
    visible: bool
    editable: bool
    layer_type: LayerType  # TILE_LAYER, FUNCTIONAL_TILE_LAYER
    map_objects: List[MapObject]
    tile_list_reference: TileListReference
    functional_tile_list_reference: FunctionalTileListReference
    
    def add_map_object(map_object: MapObject) -> None
    def remove_map_object(map_object_id: UUID) -> None
    def get_map_objects() -> List[MapObject]
```

### 4. MAP OBJECT (Entity)

```python
class MapObject:
    id: UUID
    position: Point
    layer_id: UUID
    
    # Abstract base class
    def get_type() -> MapObjectType
```

### 5. TILE (Entity, extends MapObject)

```python
class Tile(MapObject):
    tile_type: TileType
    rotation: float  # 0-360 degrees
    direction: Optional[Direction]  # From CROSSINIZER
    
    def __init__(tile_type: TileType, position: Point, rotation: float = 0.0)
```

### 6. FUNCTIONAL TILE (Entity, extends MapObject)

```python
class FunctionalTile(MapObject):
    functional_tile_type: FunctionalTileType
    
    def __init__(functional_tile_type: FunctionalTileType, position: Point)
```

### 7. OBJECTS TEMPLATE (Entity)

```python
class ObjectsTemplate:
    id: UUID
    name: str
    layout: TemplateLayout
    origin_point: Point
    
    def apply_to_tilemap(tilemap: Tilemap, position: Point) -> None
    def save(path: str) -> None
    def load(path: str) -> ObjectsTemplate
```

### 8. Biometric Processing Session (Entity)

```python
class BiometricProcessingSession:
    id: UUID
    workspace_id: UUID
    preprocessing_parameters: PreprocessingParameters
    zaborization_result: Optional[ZaborizationResult]
    skeleton_result: Optional[SkeletonResult]
    crossinizer_result: Optional[CrossinizerResult]
    detected_features: List[Feature]
    features_vector: Optional[FeaturesVector]
    
    def run_preprocessing(workspace_bitmap: WorkspaceBitmap) -> None
    def run_zaborization(workspace_bitmap: WorkspaceBitmap) -> None
    def run_skeletonization(algorithm: SkeletonizationAlgorithm) -> None
    def run_crossinizer(skeleton: SkeletonResult) -> None
    def detect_features() -> None
    def generate_features_vector() -> None
```

## Value Objects

### 1. WorkspaceMetadata

```python
@dataclass(frozen=True)
class WorkspaceMetadata:
    name: str
    author: str
    created_at: datetime
    modified_at: datetime
    width: int
    height: int
```

### 2. BerlinWall

```python
@dataclass(frozen=True)
class BerlinWall:
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    
    def contains(x: int, y: int) -> bool
    def get_bounds() -> Tuple[int, int, int, int]
```

### 3. Point

```python
@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def distance_to(other: Point) -> float
    def __add__(other: Point) -> Point
```

### 4. TileCell

```python
@dataclass
class TileCell:
    position: Point
    map_object: Optional[MapObject]
    
    def is_empty() -> bool
    def clear() -> None
```

### 5. Region

```python
@dataclass(frozen=True)
class Region:
    cells: Set[Point]
    
    def contains(point: Point) -> bool
    def get_bounds() -> Tuple[int, int, int, int]
    def get_size() -> int
```

### 6. TemplateLayout

```python
@dataclass(frozen=True)
class TemplateLayout:
    tiles: List[Tuple[Point, TileType]]  # Relative positions
    functional_tiles: List[Tuple[Point, FunctionalTileType]]
    
    def get_bounds() -> Tuple[int, int, int, int]
```

### 7. WorkspaceBitmap

```python
@dataclass(frozen=True)
class WorkspaceBitmap:
    data: numpy.ndarray  # dtype=bool or uint8, shape=(height, width)
    width: int
    height: int
    
    def get_pixel(x: int, y: int) -> bool
    def set_pixel(x: int, y: int, value: bool) -> None
    def to_image() -> PIL.Image
```

### 8. SkeletonResult (SKELETOR)

```python
@dataclass(frozen=True)
class SkeletonResult:
    skeleton_bitmap: WorkspaceBitmap
    algorithm_used: str
    
    def get_skeleton_points() -> List[Point]
```

### 9. ZaborizationResult

```python
@dataclass(frozen=True)
class ZaborizationResult:
    foreground_regions: List[Region]
    background_regions: List[Region]
    segmentation_map: numpy.ndarray  # Map of region IDs
    
    def get_foreground_mask() -> WorkspaceBitmap
    def get_background_mask() -> WorkspaceBitmap
```

### 10. CrossinizerResult

```python
@dataclass(frozen=True)
class CrossinizerResult:
    endpoints: List[Point]
    bifurcations: List[Point]
    crossings: List[Point]
    connections: List[Tuple[Point, Point]]  # Connections between points
    
    def get_feature_at(point: Point) -> Optional[FeatureType]
```

### 11. Feature

```python
@dataclass(frozen=True)
class Feature:
    position: Point
    feature_type: FeatureType  # ENDPOINT, BIFURCATION, CROSSING
    confidence: float  # 0.0-1.0
    
    def __eq__(self, other) -> bool
```

### 12. FeaturesVector

```python
@dataclass(frozen=True)
class FeaturesVector:
    vector: numpy.ndarray  # 1D array of features
    feature_counts: Dict[FeatureType, int]
    total_features: int
    
    def to_array() -> numpy.ndarray
    def distance_to(other: FeaturesVector) -> float
```

### 13. PreprocessingParameters

```python
@dataclass(frozen=True)
class PreprocessingParameters:
    noise_removal_enabled: bool
    noise_removal_threshold: float
    filtering_enabled: bool
    filter_type: str  # "gaussian", "median", etc.
    filter_size: int
    binaryzation_threshold: float
```

### 14. TileListReference

```python
@dataclass(frozen=True)
class TileListReference:
    tile_types: List[TileType]
    
    def get_tile_type(name: str) -> Optional[TileType]
```

### 15. FunctionalTileListReference

```python
@dataclass(frozen=True)
class FunctionalTileListReference:
    functional_tile_types: List[FunctionalTileType]
    
    def get_functional_tile_type(name: str) -> Optional[FunctionalTileType]
```

## Enums

### LayerType

```python
class LayerType(Enum):
    TILE_LAYER = "tile_layer"
    FUNCTIONAL_TILE_LAYER = "functional_tile_layer"
```

### MapObjectType

```python
class MapObjectType(Enum):
    TILE = "tile"
    FUNCTIONAL_TILE = "functional_tile"
```

### TileType

```python
class TileType(Enum):
    GRASS = "grass"
    STONE = "stone"
    WATER = "water"
    # ... więcej typów
```

### FunctionalTileType

```python
class FunctionalTileType(Enum):
    PLAYER_START = "player_start"
    ENEMY = "enemy"
    CHECKPOINT = "checkpoint"
    # ... więcej typów
```

### FeatureType

```python
class FeatureType(Enum):
    ENDPOINT = "endpoint"
    BIFURCATION = "bifurcation"
    CROSSING = "crossing"
```

### ToolType

```python
class ToolType(Enum):
    BRUSH = "brush"
    ERASER = "eraser"
    FLOOD = "flood"
    TRASH = "trash"
```

### SkeletonizationAlgorithm

```python
class SkeletonizationAlgorithm(Enum):
    ZHANG_SUEN = "zhang_suen"
    HILDRITCH = "hildritch"
    # Minimum 2 algorytmy wymagane
```

## Relacje

- **WORKSPACE** zawiera wiele **LAYER**
- **WORKSPACE** zawiera jeden **TILEMAP**
- **LAYER** zawiera wiele **MAP OBJECT**
- **MAP OBJECT** może być **TILE** lub **FUNCTIONAL TILE**
- **WORKSPACE** może mieć jeden **Biometric Processing Session**
- **OBJECTS TEMPLATE** zawiera wiele **TILE** w **TemplateLayout**


