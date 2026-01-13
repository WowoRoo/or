# Specyfikacja Projektu - Przegląd

Ten katalog zawiera szczegółowe specyfikacje techniczne dla projektu edytora poziomów platformowych z algorytmami biometrycznymi.

## Pliki Specyfikacji

### 1. `spec_architecture.md`
**Architektura systemu**
- Przegląd architektury opartej na DDD
- Bounded Contexts i ich odpowiedzialności
- Dependency Injection
- Event-Driven Architecture
- Wzorce projektowe
- Komunikacja między kontekstami

### 2. `spec_technical.md`
**Wymagania techniczne**
- Język programowania (Python 3.10+)
- Framework GUI (PyQt6/PySide6)
- Biblioteki zewnętrzne
- Ograniczenia (algorytmy bez dodatkowych bibliotek)
- Format danych
- Wydajność i optymalizacje
- Konfiguracja
- Testowanie
- Środowisko deweloperskie

### 3. `spec_data_models.md`
**Modele danych domenowych**
- Domain Entities (WORKSPACE, TILEMAP, LAYER, etc.)
- Value Objects (Point, Region, WorkspaceBitmap, etc.)
- Enumeracje (LayerType, TileType, FeatureType, etc.)
- Relacje między obiektami
- Interfejsy i metody

### 4. `spec_algorithms.md`
**Specyfikacja algorytmów biometrycznych**
- PREPROCESSING (binaryzacja, usuwanie szumu, filtracja)
- ZABORIZATION (segmentacja, flood fill, region growing)
- skeletonizATOR (Zhang-Suen, Hildritch - minimum 2 algorytmy)
- CROSSINIZER (wykrywanie końcówek, rozgałęzień, skrzyżowań)
- FEATURES Detection
- FEATURES VECTOR Generation
- Testowanie algorytmów

### 5. `spec_ui.md`
**Specyfikacja interfejsu użytkownika**
- Framework GUI (PyQt6)
- Layout głównego okna
- Komponenty UI (Menu, Toolbar, Canvas, Panele)
- Dialogi
- Interakcje (mysz, klawiatura)
- Real-time preview
- Wizualizacja overlay (FEATURES, SKELETOR)
- Responsywność

### 6. `spec_project_structure.md`
**Struktura projektu**
- Organizacja katalogów
- Struktura modułów
- Pliki konfiguracyjne
- Punkt wejściowy
- Konwencje nazewnictwa
- Zależności między modułami

## Jak korzystać z tych specyfikacji

1. **Zacznij od `spec_architecture.md`** - zrozum ogólną architekturę systemu
2. **Przeczytaj `spec_technical.md`** - poznaj wymagania techniczne i ograniczenia
3. **Zapoznaj się z `spec_data_models.md`** - zrozum strukturę danych
4. **Przeanalizuj `spec_algorithms.md`** - szczegóły implementacji algorytmów
5. **Zobacz `spec_ui.md`** - wymagania dotyczące interfejsu
6. **Użyj `spec_project_structure.md`** - jako przewodnik przy tworzeniu struktury projektu

## Kluczowe Wymagania

### ⚠️ Ważne Ograniczenia

**Algorytmy biometryczne muszą być zaimplementowane bez użycia dodatkowych bibliotek:**
- ✅ Dozwolone: standardowa biblioteka Pythona, numpy (podstawowe operacje)
- ❌ Niedozwolone: scikit-image, OpenCV, scipy, inne biblioteki do przetwarzania obrazów

### Wymagane Funkcjonalności

#### Major User Stories (3 punkty każdy)
1. Import obrazu RGB i ZABORIZATION
2. skeletonizATOR na BACKGROUND
3. Automatyczne zastosowanie CROSSINIZER do BRUSH TOOL
4. FLOOD TOOL z ZABORIZATION
5. PREPROCESSING
6. skeletonizATOR na TILE
7. Testowanie ZABORIZATION niezależnie

#### Standard User Stories (2 punkty każdy)
1. Tworzenie WORKSPACE
2. Zapis/ładowanie WORKSPACE
3. Parametryzacja ZABORIZATION
4. Minimum 2 algorytmy skeletonizATOR
5. Umieszczanie OBJECTS TEMPLATE
6. Konwersja do WORKSPACE BITMAP
7. Automatyczne ładowanie domyślnego WORKSPACE
8. Real-time preview
9. Asynchroniczne zadania
10. Dependency Injection
11. Unit tests algorytmów

#### Minor User Stories (1 punkt każdy)
- Podstawowe narzędzia (BRUSH, ERASER, FLOOD, TRASH)
- Przełączanie LAYER
- Tworzenie i wyświetlanie FEATURES VECTOR
- Przyjazny interfejs
- TILE LIST i FUNCTIONAL TILE LIST
- Podświetlanie FEATURES
- Undo/redo
- Automatyczne wykrywanie BERLIN WALL
- Automatyczna adnotacja FEATURES
- Synchronizacja danych w czasie rzeczywistym

## Technologie

- **Język:** Python 3.10+
- **GUI:** PyQt6 lub PySide6
- **Biblioteki:** numpy, Pillow
- **Testy:** pytest
- **Architektura:** Domain-Driven Design (DDD)
- **DI:** Własna implementacja Dependency Injection

## Następne Kroki

1. Stwórz strukturę katalogów zgodnie z `spec_project_structure.md`
2. Zaimplementuj modele domenowe z `spec_data_models.md`
3. Zaimplementuj algorytmy biometryczne z `spec_algorithms.md`
4. Stwórz interfejs użytkownika zgodnie z `spec_ui.md`
5. Połącz wszystko zgodnie z `spec_architecture.md`

## Uwagi

- Wszystkie specyfikacje są szczegółowe, ale mogą wymagać doprecyzowania podczas implementacji
- Algorytmy biometryczne są najważniejszą częścią projektu - skup się na ich poprawności
- GUI powinno być responsywne - używaj asynchroniczności dla długotrwałych operacji
- Testy jednostkowe są wymagane dla algorytmów biometrycznych


