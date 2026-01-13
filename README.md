# Biometric Level Editor

Edytor poziomów platformowych z algorytmami biometrycznymi.

## Wymagania

- Python 3.10+
- PyQt6
- numpy
- Pillow

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python main.py
```

## Struktura Projektu

Projekt zaimplementowany zgodnie z Domain-Driven Design (DDD) z podziałem na Bounded Contexts:

- **Editing Context** - zarządzanie workspace, narzędzia edycji
- **Biometric Context** - algorytmy biometryczne (preprocessing, zaborization, skeletonization, crossinizer)
- **Prefab Context** - zarządzanie szablonami obiektów
- **Visualization Context** - wizualizacja workspace i wyników biometrycznych

## Algorytmy Biometryczne

Wszystkie algorytmy biometryczne zaimplementowane bez użycia dodatkowych bibliotek (tylko standardowa biblioteka Pythona + numpy):

- **PREPROCESSING** - binaryzacja, usuwanie szumu, filtracja
- **ZABORIZATION** - segmentacja (flood fill, region growing)
- **skeletonizATOR** - dwa algorytmy: Zhang-Suen i Hildritch
- **CROSSINIZER** - wykrywanie końcówek, rozgałęzień, skrzyżowań
- **FEATURES Detection** - detekcja cech biometrycznych
- **FEATURES VECTOR** - generowanie wektora cech

## Testy

```bash
pytest tests/
```

## Licencja

Projekt edukacyjny.

