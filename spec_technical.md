# Specyfikacja Techniczna

## Wymagania Techniczne

### Język Programowania
- **Python 3.10+** (zalecane 3.11 lub nowsze)

### Framework GUI
- **PyQt6** lub **tkinter** (dla prostoty) lub **PySide6**
- **Rekomendacja:** PyQt6/PySide6 dla lepszej funkcjonalności i wyglądu

### Biblioteki Zewnętrzne

#### Wymagane
- **numpy** - Operacje na macierzach i obrazach (tylko dla podstawowych operacji, nie dla algorytmów biometrycznych)
- **Pillow (PIL)** - Obsługa obrazów RGB (import/eksport)
- **PyQt6** lub **PySide6** - Interfejs graficzny

#### Opcjonalne (dla lepszego UX)
- **matplotlib** - Wizualizacja wykresów (dla FEATURES VECTOR)
- **json** - Serializacja WORKSPACE (standardowa biblioteka)
- **pickle** - Alternatywna serializacja (standardowa biblioteka)

### Ograniczenia

⚠️ **WAŻNE:** Algorytmy biometryczne muszą być zaimplementowane **bez użycia dodatkowych bibliotek** (oprócz numpy dla podstawowych operacji na macierzach).

Dozwolone:
- Standardowa biblioteka Pythona
- numpy (tylko podstawowe operacje: array, indexing, podstawowe operacje matematyczne)
- Własna implementacja algorytmów

Niedozwolone dla algorytmów biometrycznych:
- scikit-image
- OpenCV
- scipy
- Inne biblioteki do przetwarzania obrazów

## Struktura Zależności

### requirements.txt
```
numpy>=1.24.0
Pillow>=10.0.0
PyQt6>=6.5.0
# Opcjonalnie:
# matplotlib>=3.7.0
```

## Architektura Techniczna

### Obsługa Asynchroniczności

**Opcja 1: threading**
- `threading.Thread` dla długotrwałych operacji
- `queue.Queue` dla komunikacji między wątkami

**Opcja 2: asyncio**
- `asyncio` dla operacji asynchronicznych
- `QThread` (PyQt6) dla integracji z GUI

**Rekomendacja:** Kombinacja `QThread` (PyQt6) + `queue.Queue` dla najlepszej integracji z GUI.

### Format Danych

#### WORKSPACE
- **Format zapisu:** JSON lub własny format binarny
- **Struktura:**
  ```json
  {
    "metadata": {
      "name": "string",
      "author": "string",
      "width": "int",
      "height": "int"
    },
    "berlin_wall": {
      "min_x": "int",
      "min_y": "int",
      "max_x": "int",
      "max_y": "int"
    },
    "layers": [...],
    "tilemap": {...}
  }
  ```

#### Obrazy
- **Format wejściowy:** PNG, JPEG, BMP (RGB)
- **Format wyjściowy:** PNG (dla eksportu)

#### WORKSPACE BITMAP
- **Format:** numpy.ndarray (dtype=bool lub uint8)
- **Reprezentacja:** Binaryzacja (0 = BACKGROUND, 1 = FOREGROUND)

## Wydajność

### Optymalizacje
- **Lazy loading** dla dużych WORKSPACE
- **Viewport culling** - renderowanie tylko widocznej części
- **Caching** wyników algorytmów biometrycznych
- **Incremental updates** - aktualizacja tylko zmienionych obszarów

### Limity
- **Maksymalny rozmiar WORKSPACE:** 10000x10000 komórek (konfigurowalne)
- **Maksymalna liczba warstw:** 10 (konfigurowalne)
- **Timeout dla algorytmów:** 30 sekund (konfigurowalne)

## Konfiguracja

### Plik konfiguracyjny (config.json)
```json
{
  "workspace": {
    "max_width": 10000,
    "max_height": 10000,
    "default_width": 100,
    "default_height": 100,
    "default_tile_size": 32
  },
  "biometric": {
    "algorithm_timeout": 30,
    "preprocessing_enabled": true,
    "skeletonization_algorithm": "zhang_suen"
  },
  "ui": {
    "theme": "dark",
    "auto_save_interval": 300
  }
}
```

## Testowanie

### Framework testowy
- **pytest** - Framework testowy
- **unittest.mock** - Mockowanie zależności

### Pokrycie testami
- **Unit tests** dla algorytmów biometrycznych (wymagane)
- **Integration tests** dla głównych przepływów
- **UI tests** (opcjonalnie)

## Środowisko Deweloperskie

### IDE
- **Visual Studio Code** z rozszerzeniami Python
- **PyCharm** (Community Edition)

### Narzędzia
- **black** - Formatowanie kodu
- **flake8** lub **pylint** - Linting
- **mypy** - Type checking (opcjonalnie)

### Git
- **.gitignore** powinien zawierać:
  - `__pycache__/`
  - `*.pyc`
  - `.venv/`
  - `venv/`
  - `*.workspace` (pliki robocze)
  - `.pytest_cache/`

## Deployment

### Wymagania systemowe
- **OS:** Linux, Windows, macOS
- **RAM:** Minimum 4GB (zalecane 8GB)
- **Dysk:** 100MB wolnego miejsca

### Instalacja
```bash
pip install -r requirements.txt
python main.py
```

## Rozszerzalność

### Plugin System (opcjonalnie)
- Możliwość dodawania nowych algorytmów skeletonizATOR
- Możliwość dodawania nowych typów TILE
- Możliwość dodawania nowych narzędzi


