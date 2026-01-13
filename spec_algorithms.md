# Specyfikacja Algorytmów Biometrycznych

## Ogólne Wymagania

⚠️ **WAŻNE:** Wszystkie algorytmy biometryczne muszą być zaimplementowane **bez użycia dodatkowych bibliotek** (oprócz numpy dla podstawowych operacji na macierzach).

Dozwolone:
- Standardowa biblioteka Pythona
- numpy (tylko podstawowe operacje: array, indexing, podstawowe operacje matematyczne)

## 1. PREPROCESSING

### Cel
Przygotowanie obrazu/TILEMAP do analizy biometrycznej poprzez usunięcie szumu, filtrację i binaryzację.

### Wejście
- `WorkspaceBitmap` (numpy.ndarray, dtype=uint8 lub bool)
- `PreprocessingParameters`

### Wyjście
- `WorkspaceBitmap` (przetworzony, dtype=bool)

### Operacje

#### 1.1 Binaryzacja
- Konwersja obrazu RGB/grayscale na binarny (0/1)
- Metoda: Thresholding (progowanie)
- Parametr: `binaryzation_threshold` (0.0-1.0)

#### 1.2 Usuwanie szumu
- **Median Filter** (własna implementacja)
- Rozmiar okna: `filter_size` (np. 3x3, 5x5)
- Usuwa pojedyncze piksele szumu

#### 1.3 Filtracja
- **Gaussian Blur** (własna implementacja) - opcjonalnie
- **Morphological Operations** (opening, closing) - opcjonalnie

### Implementacja

```python
class PreprocessingService:
    def preprocess(
        self, 
        bitmap: WorkspaceBitmap, 
        parameters: PreprocessingParameters
    ) -> WorkspaceBitmap:
        # 1. Binaryzacja
        binary = self._binaryze(bitmap, parameters.binaryzation_threshold)
        
        # 2. Usuwanie szumu (jeśli włączone)
        if parameters.noise_removal_enabled:
            binary = self._remove_noise(binary, parameters.noise_removal_threshold)
        
        # 3. Filtracja (jeśli włączona)
        if parameters.filtering_enabled:
            binary = self._apply_filter(binary, parameters.filter_type, parameters.filter_size)
        
        return WorkspaceBitmap(binary, bitmap.width, bitmap.height)
    
    def _binaryze(self, bitmap: WorkspaceBitmap, threshold: float) -> numpy.ndarray:
        # Własna implementacja binaryzacji
        pass
    
    def _remove_noise(self, bitmap: numpy.ndarray, threshold: float) -> numpy.ndarray:
        # Własna implementacja median filter
        pass
    
    def _apply_filter(self, bitmap: numpy.ndarray, filter_type: str, size: int) -> numpy.ndarray:
        # Własna implementacja filtracji
        pass
```

## 2. ZABORIZATION (Segmentation)

### Cel
Dzielenie regionu na podobszary na podstawie typu TILE lub rozdzielania obiektu od tła na obrazie.

### Wejście
- `WorkspaceBitmap` lub obraz RGB
- Parametry segmentacji (opcjonalne)

### Wyjście
- `ZaborizationResult` zawierający:
  - Lista regionów FOREGROUND
  - Lista regionów BACKGROUND
  - Mapa segmentacji

### Algorytmy

#### 2.1 Flood Fill Segmentation
- Rozpoczyna od punktu startowego
- Wypełnia spójny obszar o podobnych wartościach
- Używa 4-connectivity lub 8-connectivity

#### 2.2 Region Growing
- Rozpoczyna od seed points
- Rozszerza region na podstawie podobieństwa pikseli
- Parametr: threshold podobieństwa

### Implementacja

```python
class SegmentationService:
    def segment(self, bitmap: WorkspaceBitmap) -> ZaborizationResult:
        # Wykryj FOREGROUND i BACKGROUND
        foreground_regions = self._find_foreground_regions(bitmap)
        background_regions = self._find_background_regions(bitmap)
        
        return ZaborizationResult(
            foreground_regions=foreground_regions,
            background_regions=background_regions,
            segmentation_map=self._create_segmentation_map(foreground_regions, background_regions)
        )
    
    def _find_foreground_regions(self, bitmap: WorkspaceBitmap) -> List[Region]:
        # Własna implementacja flood fill / region growing
        pass
    
    def _find_background_regions(self, bitmap: WorkspaceBitmap) -> List[Region]:
        # Własna implementacja
        pass
```

### Parametryzacja
- `connectivity` (4 lub 8)
- `similarity_threshold` (dla region growing)
- `min_region_size` (filtrowanie małych regionów)

## 3. skeletonizATOR (Skeletonization)

### Cel
Przekształcenie tła z TILEMAP w jednopikselowy szkielet.

### Wymaganie
**Minimum 2 różne algorytmy skeletonizacji** do porównania wyników.

### Wejście
- `WorkspaceBitmap` (binarny, BACKGROUND = 1, FOREGROUND = 0)

### Wyjście
- `SkeletonResult` zawierający:
  - `skeleton_bitmap` (WorkspaceBitmap)
  - `algorithm_used` (nazwa algorytmu)

### Algorytm 1: Zhang-Suen

**Opis:** Iteracyjny algorytm przerzedzania dla obrazów binarnych.

**Kroki:**
1. Iteracja 1: Usuwanie pikseli spełniających warunki (subiteration 1)
2. Iteracja 2: Usuwanie pikseli spełniających warunki (subiteration 2)
3. Powtarzaj aż brak zmian

**Warunki usuwania:**
- Piksel musi być czarny (1)
- 2 ≤ liczba sąsiadów ≤ 6
- Liczba przejść 0→1 w sąsiedztwie = 1
- Specyficzne warunki dla subiteration 1 i 2

### Algorytm 2: Hilditch

**Opis:** Alternatywny algorytm przerzedzania.

**Kroki:**
- Iteracyjne usuwanie pikseli brzegowych
- Zachowanie połączeń i końcówek

### Implementacja

```python
class SkeletonizationService:
    def skeletonize(
        self, 
        bitmap: WorkspaceBitmap, 
        algorithm: SkeletonizationAlgorithm
    ) -> SkeletonResult:
        if algorithm == SkeletonizationAlgorithm.ZHANG_SUEN:
            skeleton = self._zhang_suen(bitmap)
        elif algorithm == SkeletonizationAlgorithm.HILDRITCH:
            skeleton = self._hildritch(bitmap)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        return SkeletonResult(
            skeleton_bitmap=skeleton,
            algorithm_used=algorithm.value
        )
    
    def _zhang_suen(self, bitmap: WorkspaceBitmap) -> WorkspaceBitmap:
        # Własna implementacja algorytmu Zhang-Suen
        # Używa tylko numpy i standardowej biblioteki Pythona
        pass
    
    def _hildritch(self, bitmap: WorkspaceBitmap) -> WorkspaceBitmap:
        # Własna implementacja algorytmu Hildritch
        pass
```

## 4. CROSSINIZER

### Cel
Na podstawie przejść między sąsiadującymi obiektami określa końcówki, skrzyżowania i rozgałęzienia.

### Wejście
- `SkeletonResult` (skeleton bitmap)

### Wyjście
- `CrossinizerResult` zawierający:
  - Lista `endpoints` (końcówki)
  - Lista `bifurcations` (rozgałęzienia)
  - Lista `crossings` (skrzyżowania)
  - Lista `connections` (połączenia między punktami)

### Algorytm

#### Klasyfikacja punktów szkieletu:

1. **Endpoint (końcówka):**
   - Piksel z dokładnie 1 sąsiadem (w 8-connectivity)

2. **Bifurcation (rozgałęzienie):**
   - Piksel z 3 lub więcej sąsiadami
   - Wykrywa punkty rozgałęzienia struktury

3. **Crossing (skrzyżowanie):**
   - Piksel z 4 lub więcej sąsiadami
   - Wykrywa przecięcia linii

4. **Regular point (punkt regularny):**
   - Piksel z 2 sąsiadami
   - Część ciągłej linii

### Implementacja

```python
class CrossinizerService:
    def analyze(self, skeleton: SkeletonResult) -> CrossinizerResult:
        endpoints = []
        bifurcations = []
        crossings = []
        connections = []
        
        bitmap = skeleton.skeleton_bitmap
        
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                if bitmap.get_pixel(x, y):
                    neighbors = self._count_neighbors(bitmap, x, y)
                    point = Point(x, y)
                    
                    if neighbors == 1:
                        endpoints.append(point)
                    elif neighbors == 3:
                        bifurcations.append(point)
                    elif neighbors >= 4:
                        crossings.append(point)
                    # neighbors == 2 to regular point
        
        # Znajdź połączenia między punktami
        connections = self._find_connections(bitmap, endpoints, bifurcations, crossings)
        
        return CrossinizerResult(
            endpoints=endpoints,
            bifurcations=bifurcations,
            crossings=crossings,
            connections=connections
        )
    
    def _count_neighbors(self, bitmap: WorkspaceBitmap, x: int, y: int) -> int:
        # Liczy sąsiadów w 8-connectivity
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if bitmap.is_valid_coordinate(nx, ny) and bitmap.get_pixel(nx, ny):
                    count += 1
        return count
    
    def _find_connections(self, bitmap, endpoints, bifurcations, crossings):
        # Znajdź ścieżki między punktami specjalnymi
        pass
```

## 5. FEATURES Detection

### Cel
Wykrywanie charakterystycznych cech SKELETOR oraz punktów sklasyfikowanych przez CROSSINIZER.

### Wejście
- `CrossinizerResult`
- `SkeletonResult`

### Wyjście
- Lista `Feature` (pozycja, typ, confidence)

### Implementacja

```python
class FeatureDetector:
    def detect_features(
        self, 
        crossinizer_result: CrossinizerResult,
        skeleton: SkeletonResult
    ) -> List[Feature]:
        features = []
        
        # Konwertuj wyniki CROSSINIZER na FEATURES
        for endpoint in crossinizer_result.endpoints:
            features.append(Feature(
                position=endpoint,
                feature_type=FeatureType.ENDPOINT,
                confidence=1.0
            ))
        
        for bifurcation in crossinizer_result.bifurcations:
            features.append(Feature(
                position=bifurcation,
                feature_type=FeatureType.BIFURCATION,
                confidence=1.0
            ))
        
        for crossing in crossinizer_result.crossings:
            features.append(Feature(
                position=crossing,
                feature_type=FeatureType.CROSSING,
                confidence=1.0
            ))
        
        return features
```

## 6. FEATURES VECTOR Generation

### Cel
Numeryczna reprezentacja wszystkich FEATURES z danego obrazu lub TILEMAP.

### Wejście
- Lista `Feature`

### Wyjście
- `FeaturesVector` (numpy.ndarray)

### Metoda

**Prosty wektor cech:**
- Liczba endpointów
- Liczba bifurcations
- Liczba crossings
- Gęstość features (na jednostkę powierzchni)
- Rozkład przestrzenny (histogram pozycji)

```python
class VectorGenerator:
    def generate(self, features: List[Feature], workspace: Workspace) -> FeaturesVector:
        # Policz features według typu
        feature_counts = {
            FeatureType.ENDPOINT: 0,
            FeatureType.BIFURCATION: 0,
            FeatureType.CROSSING: 0
        }
        
        for feature in features:
            feature_counts[feature.feature_type] += 1
        
        # Oblicz gęstość
        area = workspace.metadata.width * workspace.metadata.height
        density = len(features) / area if area > 0 else 0
        
        # Stwórz wektor
        vector = numpy.array([
            feature_counts[FeatureType.ENDPOINT],
            feature_counts[FeatureType.BIFURCATION],
            feature_counts[FeatureType.CROSSING],
            density,
            # ... więcej cech
        ])
        
        return FeaturesVector(
            vector=vector,
            feature_counts=feature_counts,
            total_features=len(features)
        )
```

## Testowanie Algorytmów

### Unit Tests

Każdy algorytm powinien mieć testy jednostkowe:

```python
def test_zhang_suen_skeletonization():
    # Test na prostym kształcie
    input_bitmap = create_test_bitmap()
    result = skeletonization_service.skeletonize(input_bitmap, SkeletonizationAlgorithm.ZHANG_SUEN)
    assert result.skeleton_bitmap is not None
    assert result.algorithm_used == "zhang_suen"

def test_crossinizer_detects_endpoints():
    skeleton = create_test_skeleton()
    result = crossinizer_service.analyze(skeleton)
    assert len(result.endpoints) > 0
```

### Test Cases

1. **Prosty kształt** - linia prosta (powinna dać 2 endpoints)
2. **Y-shape** - powinna dać 1 bifurcation, 3 endpoints
3. **X-shape** - powinna dać 1 crossing, 4 endpoints
4. **Koło** - powinna dać 0 endpoints (zamknięty kształt)


