# Specyfikacja Interfejsu Użytkownika

## Framework GUI

**Rekomendacja:** PyQt6 lub PySide6

## Główne Okno Aplikacji

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar                                                    │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│ Toolbar  │              Canvas (Workspace View)            │
│          │                                                   │
│          │                                                   │
├──────────┼──────────────────────────────────────────────────┤
│          │                                                   │
│ Layers   │              Properties Panel                    │
│ Panel    │                                                   │
│          │                                                   │
├──────────┴──────────────────────────────────────────────────┤
│ Status Bar                                                  │
└─────────────────────────────────────────────────────────────┘
```

### Komponenty

#### 1. Menu Bar

**File Menu:**
- New Workspace (Ctrl+N)
- Open Workspace (Ctrl+O)
- Save Workspace (Ctrl+S)
- Save Workspace As (Ctrl+Shift+S)
- Import Image (Ctrl+I)
- Export Image (Ctrl+E)
- Exit (Ctrl+Q)

**Edit Menu:**
- Undo (Ctrl+Z)
- Redo (Ctrl+Y)
- Clear Workspace (Ctrl+Delete)

**View Menu:**
- Zoom In (Ctrl++)
- Zoom Out (Ctrl+-)
- Reset Zoom (Ctrl+0)
- Show Grid (Toggle)
- Show Features Overlay (Toggle)
- Show Skeleton Overlay (Toggle)

**Tools Menu:**
- Brush Tool (B)
- Eraser Tool (E)
- Flood Tool (F)
- Trash Tool (T)

**Biometric Menu:**
- Run Preprocessing
- Run Zaborization
- Run Skeletonization
- Run Crossinizer
- Generate Features Vector
- Select Skeletonization Algorithm...

**Help Menu:**
- User Guide
- About

#### 2. Toolbar

Ikony dla najczęściej używanych narzędzi:
- New, Open, Save
- Undo, Redo
- Brush, Eraser, Flood, Trash
- Zoom controls
- Layer visibility toggles

#### 3. Canvas (Workspace View)

**Funkcjonalności:**
- Wyświetlanie TILEMAP
- Renderowanie wszystkich LAYER
- Interakcja myszką (kliknięcie, przeciąganie)
- Zoom (scroll wheel, Ctrl+scroll)
- Pan (przeciąganie prawym przyciskiem myszy lub Space+drag)
- Podświetlanie FEATURES (opcjonalna nakładka)
- Podświetlanie SKELETOR (opcjonalna nakładka)
- Wskaźnik kursora (pokazuje współrzędne TILE CELL)

**Renderowanie:**
- Każdy TILE renderowany jako kwadrat/kafel
- Kolory zależne od typu TILE
- FUNCTIONAL TILE jako ikony
- Grid lines (opcjonalnie)
- BERLIN WALL jako czerwona ramka

#### 4. Layers Panel

**Funkcjonalności:**
- Lista wszystkich LAYER
- Przełączanie widoczności (checkbox)
- Przełączanie edytowalności (lock icon)
- Zmiana kolejności warstw (drag & drop)
- Dodawanie nowej warstwy (+)
- Usuwanie warstwy (-)
- Zmiana nazwy warstwy (double-click)
- Wskaźnik aktywnej warstwy (highlight)

**Wygląd:**
```
Layers
├─ [👁] [🔓] Background Layer
├─ [👁] [🔒] Terrain Layer (active)
└─ [  ] [🔓] Objects Layer
```

#### 5. Properties Panel

**Zakładki:**

**Tool Properties:**
- Wybór TILE z TILE LIST
- Wybór FUNCTIONAL TILE z FUNCTIONAL TILE LIST
- Rozmiar pędzla (brush size)
- Rotacja (dla BRUSH TOOL)

**Workspace Properties:**
- Nazwa WORKSPACE
- Autor
- Rozmiar (width x height)
- BERLIN WALL bounds (read-only, auto-detected)

**Biometric Properties:**
- Parametry PREPROCESSING
- Wybór algorytmu skeletonizATOR
- Parametry ZABORIZATION
- Wyniki (FEATURES VECTOR, statystyki)

**Template Properties:**
- Lista OBJECTS TEMPLATE
- Podgląd wybranego szablonu
- Przycisk "Place Template"

#### 6. Status Bar

**Informacje:**
- Pozycja kursora (X, Y)
- Aktywne narzędzie
- Aktywna warstwa
- Rozmiar WORKSPACE
- Status operacji (np. "Processing...", "Ready")

## Dialogi

### 1. New Workspace Dialog

```
┌─────────────────────────────┐
│ Create New Workspace        │
├─────────────────────────────┤
│ Name: [_______________]     │
│ Author: [_______________]   │
│                             │
│ Width:  [100]  tiles        │
│ Height: [100]  tiles          │
│                             │
│ Tile Size: [32] pixels      │
│                             │
│         [Cancel] [Create]   │
└─────────────────────────────┘
```

### 2. Import Image Dialog

```
┌─────────────────────────────┐
│ Import Image                │
├─────────────────────────────┤
│ Select image file:          │
│ [Browse...] image.png       │
│                             │
│ Zaborization Parameters:    │
│ Connectivity: ( ) 4  (•) 8  │
│ Threshold: [0.5]            │
│                             │
│ Preview: [Image preview]    │
│                             │
│         [Cancel] [Import]   │
└─────────────────────────────┘
```

### 3. Skeletonization Algorithm Selection

```
┌─────────────────────────────┐
│ Select Algorithm            │
├─────────────────────────────┤
│ Algorithm:                  │
│ (•) Zhang-Suen              │
│ ( ) Hildritch               │
│                             │
│         [Cancel] [Apply]    │
└─────────────────────────────┘
```

### 4. Features Vector Display

```
┌─────────────────────────────┐
│ Features Vector             │
├─────────────────────────────┤
│ Endpoints: 15               │
│ Bifurcations: 8             │
│ Crossings: 3                │
│                             │
│ Density: 0.026 features/tile│
│                             │
│ Vector: [15, 8, 3, 0.026]  │
│                             │
│              [Close]        │
└─────────────────────────────┘
```

## Interakcje

### Mysz

**Lewy przycisk:**
- BRUSH TOOL: Umieszcza TILE w pozycji kursora
- ERASER TOOL: Usuwa MAP OBJECT w pozycji kursora
- FLOOD TOOL: Wypełnia region od pozycji kursora
- TRASH TOOL: Umieszcza FUNCTIONAL TILE w pozycji kursora

**Prawy przycisk:**
- Pan (przesuwanie widoku)
- Context menu (opcjonalnie)

**Scroll:**
- Zoom in/out (z Ctrl)
- Scroll canvas (bez Ctrl)

**Przeciąganie:**
- BRUSH TOOL: Rysuje ciągłą linię TILE
- Pan: Przesuwa widok

### Klawiatura

**Skróty:**
- `B` - BRUSH TOOL
- `E` - ERASER TOOL
- `F` - FLOOD TOOL
- `T` - TRASH TOOL
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+S` - Save
- `Ctrl+O` - Open
- `Ctrl+N` - New
- `Ctrl+I` - Import Image
- `Ctrl++` - Zoom In
- `Ctrl+-` - Zoom Out
- `Ctrl+0` - Reset Zoom
- `Space` - Pan mode (hold)
- `Delete` - Delete selected (jeśli implementowane)

## Real-time Preview

### Wymagania

- Aktualizacje w czasie rzeczywistym podczas edycji
- Asynchroniczne przetwarzanie algorytmów biometrycznych
- Wskaźnik postępu dla długotrwałych operacji

### Wskaźnik Postępu

Dla długotrwałych operacji (skeletonizATOR, ZABORIZATION):
```
┌─────────────────────────────┐
│ Processing...               │
├─────────────────────────────┤
│ Running skeletonization... │
│ ████████████░░░░░░░░ 60%   │
│                             │
│              [Cancel]       │
└─────────────────────────────┘
```

## Wizualizacja Overlay

### Features Overlay

- **Endpoints:** Zielone kropki
- **Bifurcations:** Niebieskie kropki
- **Crossings:** Czerwone kropki
- **Connections:** Cienkie linie między punktami

### Skeleton Overlay

- **Skeleton lines:** Cienkie białe/żółte linie
- **Opacity:** Konfigurowalna (0-100%)

## Responsywność

- GUI nie powinno zamrażać się podczas długotrwałych operacji
- Wykorzystanie wątków/asynchroniczności
- Aktualizacje UI przez sygnały/sygnały Qt

## Motywy

- **Light Theme** (domyślny)
- **Dark Theme** (opcjonalnie)

## Accessibility

- Tooltips dla wszystkich przycisków
- Opisy w status barze
- Keyboard shortcuts dla wszystkich operacji
- Wskaźniki wizualne dla aktywnego narzędzia


