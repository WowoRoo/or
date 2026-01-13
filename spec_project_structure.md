# Struktura Projektu

## Organizacja Katalogów

```
biometria/
├── main.py                          # Punkt wejściowy aplikacji
├── requirements.txt                 # Zależności Python
├── config.json                      # Konfiguracja aplikacji
├── README.md                        # Dokumentacja projektu
├── .gitignore                       # Pliki ignorowane przez Git
│
├── core/                            # Rdzeń systemu
│   ├── __init__.py
│   ├── di/                          # Dependency Injection
│   │   ├── __init__.py
│   │   ├── container.py             # Kontener DI
│   │   ├── providers.py             # Dostawcy zależności
│   │   └── modules.py               # Moduły konfiguracyjne
│   │
│   ├── events/                      # Event System
│   │   ├── __init__.py
│   │   ├── event_bus.py             # Szyna zdarzeń
│   │   ├── event_handlers.py        # Obsługa zdarzeń
│   │   └── domain_events.py         # Definicje zdarzeń domenowych
│   │
│   └── exceptions/                  # Wyjątki domenowe
│       ├── __init__.py
│       ├── workspace_exceptions.py
│       └── biometric_exceptions.py
│
├── domain/                          # Warstwa domenowa
│   ├── __init__.py
│   │
│   ├── entities/                    # Encje domenowe
│   │   ├── __init__.py
│   │   ├── workspace.py             # WORKSPACE
│   │   ├── tilemap.py                # TILEMAP
│   │   ├── layer.py                  # LAYER
│   │   ├── map_object.py             # MAP OBJECT (base)
│   │   ├── tile.py                   # TILE
│   │   ├── functional_tile.py        # FUNCTIONAL TILE
│   │   ├── objects_template.py       # OBJECTS TEMPLATE
│   │   └── biometric_session.py      # Biometric Processing Session
│   │
│   ├── value_objects/               # Value Objects
│   │   ├── __init__.py
│   │   ├── point.py                  # Point
│   │   ├── region.py                 # Region
│   │   ├── workspace_metadata.py     # WorkspaceMetadata
│   │   ├── berlin_wall.py            # BerlinWall
│   │   ├── tile_cell.py              # TileCell
│   │   ├── template_layout.py        # TemplateLayout
│   │   ├── workspace_bitmap.py       # WorkspaceBitmap
│   │   ├── skeleton_result.py        # SkeletonResult
│   │   ├── zaborization_result.py    # ZaborizationResult
│   │   ├── crossinizer_result.py     # CrossinizerResult
│   │   ├── feature.py                 # Feature
│   │   ├── features_vector.py        # FeaturesVector
│   │   ├── preprocessing_parameters.py
│   │   └── references.py             # TileListReference, etc.
│   │
│   └── enums/                       # Enumeracje
│       ├── __init__.py
│       ├── layer_type.py
│       ├── map_object_type.py
│       ├── tile_type.py
│       ├── functional_tile_type.py
│       ├── feature_type.py
│       ├── tool_type.py
│       └── skeletonization_algorithm.py
│
├── editing/                         # Bounded Context: Editing
│   ├── __init__.py
│   │
│   ├── workspace/                   # Zarządzanie WORKSPACE
│   │   ├── __init__.py
│   │   ├── workspace_service.py     # WorkspaceService
│   │   └── workspace_repository.py  # Persystencja (opcjonalnie)
│   │
│   ├── tilemap/                     # Zarządzanie TILEMAP
│   │   ├── __init__.py
│   │   └── tilemap_service.py       # TilemapService
│   │
│   ├── layers/                      # Zarządzanie LAYER
│   │   ├── __init__.py
│   │   └── layer_manager.py         # LayerManager
│   │
│   ├── tools/                       # Narzędzia edycji
│   │   ├── __init__.py
│   │   ├── tool_manager.py          # ToolManager
│   │   ├── base_tool.py             # BaseTool (abstract)
│   │   ├── brush_tool.py            # BRUSH TOOL
│   │   ├── eraser_tool.py           # ERASER TOOL
│   │   ├── flood_tool.py            # FLOOD TOOL
│   │   └── trash_tool.py            # TRASH TOOL
│   │
│   ├── commands/                    # Command Pattern (undo/redo)
│   │   ├── __init__.py
│   │   ├── command.py                # BaseCommand
│   │   ├── place_tile_command.py
│   │   ├── erase_object_command.py
│   │   ├── fill_region_command.py
│   │   └── command_history.py       # CommandHistory
│   │
│   └── persistence/                 # Zapis/odczyt
│       ├── __init__.py
│       ├── workspace_serializer.py  # Serializacja WORKSPACE
│       └── workspace_loader.py      # Ładowanie WORKSPACE
│
├── biometric/                       # Bounded Context: Biometric
│   ├── __init__.py
│   │
│   ├── preprocessing/               # PREPROCESSING
│   │   ├── __init__.py
│   │   └── preprocessing_service.py
│   │
│   ├── segmentation/               # ZABORIZATION
│   │   ├── __init__.py
│   │   └── segmentation_service.py
│   │
│   ├── skeletonization/            # skeletonizATOR
│   │   ├── __init__.py
│   │   ├── skeletonization_service.py
│   │   ├── zhang_suen.py           # Algorytm Zhang-Suen
│   │   └── hildritch.py             # Algorytm Hildritch
│   │
│   ├── crossinizer/                # CROSSINIZER
│   │   ├── __init__.py
│   │   └── crossinizer_service.py
│   │
│   ├── features/                   # FEATURES
│   │   ├── __init__.py
│   │   └── feature_detector.py
│   │
│   ├── vectorization/              # FEATURES VECTOR
│   │   ├── __init__.py
│   │   └── vector_generator.py
│   │
│   ├── conversion/                 # Konwersja do WORKSPACE BITMAP
│   │   ├── __init__.py
│   │   └── bitmap_converter.py
│   │
│   └── processor/                  # Główny procesor
│       ├── __init__.py
│       └── biometric_processor.py  # BiometricProcessor
│
├── prefab/                         # Bounded Context: Prefab
│   ├── __init__.py
│   │
│   ├── template/                   # OBJECTS TEMPLATE
│   │   ├── __init__.py
│   │   └── template_manager.py     # TemplateManager
│   │
│   ├── importer/                   # Import obrazów
│   │   ├── __init__.py
│   │   └── image_importer.py       # ImageImporter
│   │
│   └── converter/                  # Konwersja obrazów
│       ├── __init__.py
│       └── template_converter.py   # TemplateConverter
│
├── visualization/                  # Bounded Context: Visualization
│   ├── __init__.py
│   │
│   ├── canvas/                     # Główny canvas
│   │   ├── __init__.py
│   │   └── workspace_canvas.py     # WorkspaceCanvas (QWidget)
│   │
│   ├── renderers/                  # Renderery
│   │   ├── __init__.py
│   │   ├── workspace_renderer.py   # WorkspaceRenderer
│   │   ├── layer_renderer.py       # LayerRenderer
│   │   └── tile_renderer.py        # TileRenderer
│   │
│   ├── overlays/                   # Nakładki
│   │   ├── __init__.py
│   │   ├── feature_overlay.py      # FeatureOverlay
│   │   └── skeleton_overlay.py     # SkeletonOverlay
│   │
│   └── async/                      # Asynchroniczne aktualizacje
│       ├── __init__.py
│       └── async_update_manager.py  # AsyncUpdateManager
│
├── ui/                             # Warstwa prezentacji (GUI)
│   ├── __init__.py
│   │
│   ├── main_window.py              # Główne okno aplikacji (QMainWindow)
│   ├── menu_bar.py                 # Menu bar
│   ├── toolbar.py                  # Toolbar
│   ├── status_bar.py               # Status bar
│   │
│   ├── panels/                     # Panele boczne
│   │   ├── __init__.py
│   │   ├── layers_panel.py         # Layers Panel
│   │   └── properties_panel.py     # Properties Panel
│   │
│   ├── dialogs/                    # Dialogi
│   │   ├── __init__.py
│   │   ├── new_workspace_dialog.py
│   │   ├── import_image_dialog.py
│   │   ├── algorithm_selection_dialog.py
│   │   └── features_vector_dialog.py
│   │
│   └── widgets/                    # Widgety pomocnicze
│       ├── __init__.py
│       ├── tile_list_widget.py     # TILE LIST widget
│       └── template_list_widget.py # OBJECTS TEMPLATE LIST widget
│
├── tests/                          # Testy
│   ├── __init__.py
│   │
│   ├── unit/                       # Testy jednostkowe
│   │   ├── __init__.py
│   │   ├── test_preprocessing.py
│   │   ├── test_segmentation.py
│   │   ├── test_skeletonization.py
│   │   ├── test_crossinizer.py
│   │   └── test_features.py
│   │
│   ├── integration/                # Testy integracyjne
│   │   ├── __init__.py
│   │   ├── test_workspace_flow.py
│   │   └── test_biometric_pipeline.py
│   │
│   └── fixtures/                   # Fixtures testowe
│       ├── __init__.py
│       └── test_bitmaps.py
│
└── utils/                          # Narzędzia pomocnicze
    ├── __init__.py
    ├── image_utils.py              # Pomocnicze funkcje do obrazów
    └── math_utils.py               # Pomocnicze funkcje matematyczne
```

## Pliki Konfiguracyjne

### requirements.txt
```
numpy>=1.24.0
Pillow>=10.0.0
PyQt6>=6.5.0
pytest>=7.4.0
```

### config.json
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

### .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
*.workspace
*.workspace.bak
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

## Punkt Wejściowy

### main.py
```python
#!/usr/bin/env python3
"""
Biometric Level Editor - Main Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication
from core.di.container import DIContainer
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Initialize DI Container
    container = DIContainer()
    container.configure()
    
    # Create and show main window
    main_window = container.resolve(MainWindow)
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

## Konwencje Nazewnictwa

- **Klasy:** PascalCase (np. `WorkspaceService`)
- **Funkcje/Metody:** snake_case (np. `create_workspace`)
- **Zmienne:** snake_case (np. `tile_map`)
- **Stałe:** UPPER_SNAKE_CASE (np. `MAX_WORKSPACE_SIZE`)
- **Pliki:** snake_case (np. `workspace_service.py`)
- **Moduły:** snake_case (np. `editing/workspace/`)

## Zależności między Modułami

```
ui/ → visualization/ → domain/
ui/ → editing/ → domain/
ui/ → biometric/ → domain/
ui/ → prefab/ → domain/

editing/ → domain/
biometric/ → domain/
prefab/ → domain/
visualization/ → domain/

core/ → (używane przez wszystkie)
```

## Notatki

- Każdy moduł powinien mieć `__init__.py`
- Importy powinny być względne w obrębie pakietu
- Zależności zewnętrzne tylko w `requirements.txt`
- Testy powinny być równoległe do struktury kodu źródłowego


