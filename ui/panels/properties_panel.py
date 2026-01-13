"""Properties panel widget."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, QLineEdit,
    QSpinBox, QComboBox, QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from domain.entities.workspace import Workspace
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm


class PropertiesPanel(QWidget):
    """Panel for displaying and editing properties."""
    
    def __init__(self, workspace: Workspace, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Properties")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tool Properties tab
        tool_tab = self._create_tool_properties_tab()
        self.tabs.addTab(tool_tab, "Tool")
        
        # Workspace Properties tab
        workspace_tab = self._create_workspace_properties_tab()
        self.tabs.addTab(workspace_tab, "Workspace")
        
        # Biometric Properties tab
        biometric_tab = self._create_biometric_properties_tab()
        self.tabs.addTab(biometric_tab, "Biometric")
        
        layout.addWidget(self.tabs)
        layout.addStretch()
    
    def _create_tool_properties_tab(self) -> QWidget:
        """Create tool properties tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Combined tile/functional tile selection
        layout.addWidget(QLabel("Object Type:"))
        self.object_combo = QComboBox()
        
        # Use QStandardItemModel for better control
        model = QStandardItemModel()
        
        # Add separator for tiles (disabled, non-selectable)
        separator1 = QStandardItem("--- Tiles ---")
        separator1.setEnabled(False)
        model.appendRow(separator1)
        
        # Add all tile types
        for tile_type in TileType:
            item = QStandardItem(f"Tile: {tile_type.value}")
            item.setData(("tile", tile_type), Qt.ItemDataRole.UserRole)
            model.appendRow(item)
        
        # Add separator for functional tiles (disabled, non-selectable)
        separator2 = QStandardItem("--- Functional Tiles ---")
        separator2.setEnabled(False)
        model.appendRow(separator2)
        
        # Add all functional tile types
        for func_tile_type in FunctionalTileType:
            item = QStandardItem(f"Functional: {func_tile_type.value}")
            item.setData(("functional", func_tile_type), Qt.ItemDataRole.UserRole)
            model.appendRow(item)
        
        self.object_combo.setModel(model)
        
        # Set default selection to first tile (skip separator at index 0)
        if model.rowCount() > 1:
            self.object_combo.setCurrentIndex(1)
        
        # Connect to update tools
        self.object_combo.currentIndexChanged.connect(self._on_object_selected)
        layout.addWidget(self.object_combo)
        
        layout.addStretch()
        return widget
    
    def _on_object_selected(self, index):
        """Handle object selection change."""
        # Get item from model
        model = self.object_combo.model()
        item = model.item(index)
        
        if not item or not item.isEnabled():
            # Skip separators - select next valid item
            if index < model.rowCount() - 1:
                # Find next enabled item
                for i in range(index + 1, model.rowCount()):
                    next_item = model.item(i)
                    if next_item and next_item.isEnabled():
                        self.object_combo.setCurrentIndex(i)
                        return
            return
        
        data = item.data(Qt.ItemDataRole.UserRole)
        if data is None:
            return
        
        # Find main window and update tools
        widget = self.parent()
        while widget:
            if hasattr(widget, 'tool_manager') and widget.tool_manager:
                obj_type, obj_enum = data
                if obj_type == "tile":
                    # Update brush tool
                    if hasattr(widget.tool_manager, 'brush_tool'):
                        widget.tool_manager.brush_tool.tile_type = obj_enum
                    # Update flood tool
                    if hasattr(widget.tool_manager, 'flood_tool'):
                        widget.tool_manager.flood_tool.tile_type = obj_enum
                elif obj_type == "functional":
                    # Update trash tool
                    if hasattr(widget.tool_manager, 'trash_tool'):
                        widget.tool_manager.trash_tool.functional_tile_type = obj_enum
                break
            widget = widget.parent()
    
    def _create_workspace_properties_tab(self) -> QWidget:
        """Create workspace properties tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Name
        layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.workspace.metadata.name if self.workspace else "")
        layout.addWidget(self.name_edit)
        
        # Author
        layout.addWidget(QLabel("Author:"))
        self.author_edit = QLineEdit()
        self.author_edit.setText(self.workspace.metadata.author if self.workspace else "")
        layout.addWidget(self.author_edit)
        
        # Size
        layout.addWidget(QLabel("Size:"))
        size_label = QLabel()
        if self.workspace:
            size_label.setText(f"{self.workspace.metadata.width} x {self.workspace.metadata.height}")
        layout.addWidget(size_label)
        
        # Berlin Wall
        layout.addWidget(QLabel("Berlin Wall:"))
        bw_label = QLabel()
        if self.workspace:
            bw = self.workspace.berlin_wall
            bw_label.setText(f"({bw.min_x}, {bw.min_y}) - ({bw.max_x}, {bw.max_y})")
        layout.addWidget(bw_label)
        
        layout.addStretch()
        return widget
    
    def _create_biometric_properties_tab(self) -> QWidget:
        """Create biometric properties tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Algorithm selection
        layout.addWidget(QLabel("Skeletonization Algorithm:"))
        self.algorithm_combo = QComboBox()
        for algo in SkeletonizationAlgorithm:
            self.algorithm_combo.addItem(algo.value, algo)
        layout.addWidget(self.algorithm_combo)
        
        # Features Vector display
        layout.addWidget(QLabel("Features Vector:"))
        self.features_text = QTextEdit()
        self.features_text.setReadOnly(True)
        layout.addWidget(self.features_text)
        
        layout.addStretch()
        return widget
    
    def set_workspace(self, workspace: Workspace):
        """Update workspace."""
        self.workspace = workspace
        # Update UI elements
        if self.workspace:
            self.name_edit.setText(self.workspace.metadata.name)
            self.author_edit.setText(self.workspace.metadata.author)
            
            # Update features vector if available
            if self.workspace.features_vector:
                from domain.enums.feature_type import FeatureType
                fv = self.workspace.features_vector
                text = f"Endpoints: {fv.feature_counts.get(FeatureType.ENDPOINT, 0)}\n"
                text += f"Bifurcations: {fv.feature_counts.get(FeatureType.BIFURCATION, 0)}\n"
                text += f"Crossings: {fv.feature_counts.get(FeatureType.CROSSING, 0)}\n"
                text += f"Total: {fv.total_features}\n"
                text += f"Vector: {fv.vector.tolist()}"
                self.features_text.setText(text)

