# Specyfikacja Architektury Systemu

## Przegląd

System edytora poziomów platformowych z algorytmami biometrycznymi, zaimplementowany w Pythonie z graficznym interfejsem użytkownika.

## Architektura Ogólna

System oparty na **Domain-Driven Design (DDD)** z podziałem na **Bounded Contexts** i wykorzystaniem **Dependency Injection** dla **Inversion of Control**.

### Warstwy Architektury

1. **Presentation Layer** - Interfejs użytkownika (GUI)
2. **Application Layer** - Orkiestracja, koordynacja między kontekstami
3. **Domain Layer** - Logika biznesowa, agregaty, encje, value objects
4. **Infrastructure Layer** - Persystencja, zewnętrzne biblioteki

## Bounded Contexts

### 1. Editing Context

**Odpowiedzialność:** Edycja i przechowywanie WORKSPACE

**Moduły:**
- `editing/workspace/` - Zarządzanie WORKSPACE
- `editing/tilemap/` - Zarządzanie TILEMAP
- `editing/layers/` - Zarządzanie LAYER
- `editing/tools/` - Narzędzia edycji (BRUSH, ERASER, FLOOD, TRASH)
- `editing/commands/` - Wzorzec Command dla undo/redo
- `editing/persistence/` - Zapis/odczyt WORKSPACE

**Kluczowe komponenty:**
- `WorkspaceService` - Główna logika WORKSPACE
- `TilemapService` - Operacje na TILEMAP
- `LayerManager` - Zarządzanie warstwami
- `ToolManager` - Zarządzanie narzędziami
- `CommandHistory` - Historia operacji (undo/redo)

### 2. Biometric Context

**Odpowiedzialność:** Algorytmy biometryczne do analizy TILEMAP i obrazów

**Moduły:**
- `biometric/preprocessing/` - PREPROCESSING
- `biometric/segmentation/` - ZABORIZATION
- `biometric/skeletonization/` - skeletonizATOR (min. 2 algorytmy)
- `biometric/crossinizer/` - CROSSINIZER
- `biometric/features/` - Detekcja FEATURES
- `biometric/vectorization/` - Generowanie FEATURES VECTOR
- `biometric/conversion/` - Konwersja do WORKSPACE BITMAP

**Kluczowe komponenty:**
- `BiometricProcessor` - Główny procesor algorytmów
- `PreprocessingService` - Przygotowanie danych
- `SegmentationService` - ZABORIZATION
- `SkeletonizationService` - skeletonizATOR (strategia dla różnych algorytmów)
- `CrossinizerService` - CROSSINIZER
- `FeatureDetector` - Detekcja FEATURES
- `VectorGenerator` - Generowanie FEATURES VECTOR

**Wymaganie:** Algorytmy biometryczne implementowane bez użycia dodatkowych bibliotek (tylko standardowa biblioteka Pythona + numpy dla operacji na macierzach).

### 3. Prefab Context

**Odpowiedzialność:** Tworzenie i zarządzanie OBJECTS TEMPLATE

**Moduły:**
- `prefab/template/` - Definicje OBJECTS TEMPLATE
- `prefab/importer/` - Import obrazów RGB
- `prefab/converter/` - Konwersja obrazów na OBJECTS TEMPLATE

**Kluczowe komponenty:**
- `TemplateManager` - Zarządzanie szablonami
- `ImageImporter` - Import obrazów
- `TemplateConverter` - Konwersja obrazów na szablony

### 4. Visualization Context

**Odpowiedzialność:** Wizualizacja WORKSPACE i wyników biometrycznych

**Moduły:**
- `visualization/canvas/` - Główny canvas do rysowania
- `visualization/renderers/` - Renderery dla różnych typów obiektów
- `visualization/overlays/` - Nakładki (FEATURES, SKELETOR)
- `visualization/async/` - Asynchroniczne aktualizacje

**Kluczowe komponenty:**
- `WorkspaceRenderer` - Renderowanie WORKSPACE
- `LayerRenderer` - Renderowanie warstw
- `FeatureOverlay` - Nakładka z FEATURES
- `SkeletonOverlay` - Nakładka z SKELETOR
- `AsyncUpdateManager` - Zarządzanie asynchronicznymi aktualizacjami

## Dependency Injection

System wykorzystuje **Dependency Injection** dla luźnego sprzężenia komponentów.

**Struktura:**
- `core/di/container.py` - Kontener DI
- `core/di/providers.py` - Dostawcy zależności
- `core/di/modules.py` - Moduły konfiguracyjne dla każdego Bounded Context

## Event-Driven Architecture

System wykorzystuje **Domain Events** do komunikacji między komponentami.

**Struktura:**
- `core/events/event_bus.py` - Szyna zdarzeń
- `core/events/event_handlers.py` - Obsługa zdarzeń
- `core/events/domain_events.py` - Definicje zdarzeń domenowych

## Wzorce Projektowe

1. **Command Pattern** - Dla undo/redo operacji
2. **Strategy Pattern** - Dla różnych algorytmów skeletonizATOR
3. **Observer Pattern** - Dla Domain Events
4. **Factory Pattern** - Dla tworzenia obiektów domenowych
5. **Repository Pattern** - Dla persystencji (opcjonalnie)
6. **Service Layer Pattern** - Dla logiki biznesowej

## Komunikacja między Kontekstami

- **Editing ↔ Biometric:** Editing Context wywołuje Biometric Context do analizy
- **Editing ↔ Prefab:** Prefab Context tworzy OBJECTS TEMPLATE dla Editing Context
- **Editing ↔ Visualization:** Visualization Context subskrybuje zdarzenia z Editing Context
- **Biometric ↔ Visualization:** Biometric Context emituje zdarzenia z wynikami dla Visualization Context

## Threading i Asynchroniczność

- Długotrwałe operacje (algorytmy biometryczne) wykonywane asynchronicznie
- GUI pozostaje responsywne podczas przetwarzania
- Wykorzystanie `asyncio` lub `threading` dla operacji w tle
- Aktualizacje UI przez kolejki zdarzeń


