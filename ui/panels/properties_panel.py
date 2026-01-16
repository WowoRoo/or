"""Properties panel widget."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit,
    QSpinBox, QComboBox, QPushButton, QTextEdit, QListWidget, QColorDialog,
    QDoubleSpinBox, QSlider
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor
from domain.entities.workspace import Workspace
from domain.entities.objects_template import ObjectsTemplate
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm
from domain.value_objects.point import Point


class TemplatePreviewWidget(QWidget):
    """Widget for displaying template preview."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.template: ObjectsTemplate = None
        self.zoom_level = 1.0  # Zoom level (0.1 to 5.0)
        self.setMinimumSize(200, 200)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enable focus for wheel events
    
    def set_template(self, template: ObjectsTemplate) -> None:
        """Set template to preview."""
        self.template = template
        self.zoom_level = 1.0  # Reset zoom when template changes
        self.update()  # Trigger repaint
    
    def wheelEvent(self, event):
        """Handle mouse wheel for zoom."""
        if not self.template:
            return
        
        # Zoom in/out based on wheel delta
        delta = event.angleDelta().y()
        zoom_factor = 1.1 if delta > 0 else 0.9
        self.zoom_level = max(0.1, min(5.0, self.zoom_level * zoom_factor))
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Paint template preview."""
        if not self.template:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate bounds
        all_points = [t[0] for t in self.template.layout.tiles] + [t[0] for t in self.template.layout.functional_tiles]
        if not all_points:
            return
        
        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        # Calculate base tile size to fit in widget
        widget_width = self.width() - 20
        widget_height = self.height() - 20
        base_tile_size = min(widget_width // max(width, 1), widget_height // max(height, 1), 20)
        base_tile_size = max(2, base_tile_size)  # Minimum 2 pixels
        
        # Apply zoom
        tile_size = int(base_tile_size * self.zoom_level)
        tile_size = max(1, tile_size)  # Minimum 1 pixel
        
        # Calculate offset to center
        total_width = width * tile_size
        total_height = height * tile_size
        offset_x = (widget_width - total_width) // 2 + 10
        offset_y = (widget_height - total_height) // 2 + 10
        
        # Draw background
        painter.fillRect(0, 0, self.width(), self.height(), QColor(240, 240, 240))
        
        # Draw tiles
        for rel_pos, tile_type in self.template.layout.tiles:
            x = (rel_pos.x - min_x) * tile_size + offset_x
            y = (rel_pos.y - min_y) * tile_size + offset_y
            
            colors = {
                TileType.GRASS: (34, 139, 34),
                TileType.STONE: (128, 128, 128),
                TileType.WATER: (0, 0, 255),
                TileType.DIRT: (139, 69, 19),
                TileType.SAND: (238, 203, 173),
                TileType.SNOW: (255, 250, 250),
                TileType.LAVA: (255, 69, 0),
            }
            color = QColor(*colors.get(tile_type, (200, 200, 200)))
            painter.fillRect(x, y, tile_size, tile_size, color)
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(x, y, tile_size, tile_size)
        
        # Draw functional tiles
        for rel_pos, func_tile_type in self.template.layout.functional_tiles:
            x = (rel_pos.x - min_x) * tile_size + offset_x
            y = (rel_pos.y - min_y) * tile_size + offset_y
            
            colors = {
                FunctionalTileType.PLAYER_START: (255, 0, 0),
                FunctionalTileType.ENEMY: (255, 165, 0),
                FunctionalTileType.CHECKPOINT: (0, 255, 0),
                FunctionalTileType.COIN: (255, 215, 0),
                FunctionalTileType.POWERUP: (255, 0, 255),
                FunctionalTileType.EXIT: (0, 255, 255),
            }
            color = QColor(*colors.get(func_tile_type, (255, 255, 0)))
            painter.fillRect(x, y, tile_size, tile_size, color)
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(x, y, tile_size, tile_size)


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
        self.tabs.currentChanged.connect(self._on_tab_changed)
        
        # Tool Properties tab
        tool_tab = self._create_tool_properties_tab()
        self.tabs.addTab(tool_tab, "Tool")
        
        # Workspace Properties tab
        workspace_tab = self._create_workspace_properties_tab()
        self.tabs.addTab(workspace_tab, "Workspace")
        
        # Biometric Properties tab
        biometric_tab = self._create_biometric_properties_tab()
        self.tabs.addTab(biometric_tab, "Biometric")
        
        # Template Properties tab
        template_tab = self._create_template_properties_tab()
        self.tabs.addTab(template_tab, "Templates")
        
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
            
            # Update template list
            self._update_template_list()
    
    def _create_template_properties_tab(self) -> QWidget:
        """Create template properties tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Template list
        layout.addWidget(QLabel("Available Templates:"))
        self.template_list = QListWidget()
        self.template_list.itemSelectionChanged.connect(self._on_template_selected)
        layout.addWidget(self.template_list)
        
        # Template name editor
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Template Name:"))
        self.template_name_edit = QLineEdit()
        self.template_name_edit.setEnabled(False)
        self.template_name_edit.editingFinished.connect(self._on_template_name_changed)
        name_layout.addWidget(self.template_name_edit)
        layout.addLayout(name_layout)
        
        # Template preview (mini visual preview)
        layout.addWidget(QLabel("Template Preview:"))
        self.template_preview_widget = TemplatePreviewWidget()
        self.template_preview_widget.setMinimumHeight(200)
        self.template_preview_widget.setMaximumHeight(200)
        layout.addWidget(self.template_preview_widget)
        
        # Template info (text)
        self.template_info = QTextEdit()
        self.template_info.setReadOnly(True)
        self.template_info.setMaximumHeight(100)
        layout.addWidget(self.template_info)
        
        # Color picker
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Template Color:"))
        self.template_color_btn = QPushButton("Choose Color")
        self.template_color_btn.clicked.connect(self._on_choose_color)
        self.template_color = None  # (r, g, b)
        color_layout.addWidget(self.template_color_btn)
        self.template_color_preview = QLabel()
        self.template_color_preview.setMinimumSize(30, 30)
        self.template_color_preview.setStyleSheet("background-color: white; border: 1px solid black;")
        color_layout.addWidget(self.template_color_preview)
        layout.addLayout(color_layout)
        
        # Scale control
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Scale:"))
        self.template_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.template_scale_slider.setMinimum(10)  # 0.1 * 100
        self.template_scale_slider.setMaximum(100)  # 1.0 * 100
        self.template_scale_slider.setValue(100)  # Default 1.0
        self.template_scale_slider.valueChanged.connect(self._on_scale_changed)
        scale_layout.addWidget(self.template_scale_slider)
        self.template_scale_label = QLabel("1.00")
        self.template_scale_label.setMinimumWidth(40)
        scale_layout.addWidget(self.template_scale_label)
        layout.addLayout(scale_layout)
        
        # Place template button (now activates template tool)
        self.place_template_btn = QPushButton("Activate Template Tool")
        self.place_template_btn.setEnabled(False)
        self.place_template_btn.clicked.connect(self._on_activate_template_tool)
        layout.addWidget(self.place_template_btn)
        
        layout.addStretch()
        return widget
    
    def _on_template_selected(self):
        """Handle template selection change."""
        selected_items = self.template_list.selectedItems()
        if not selected_items:
            self.place_template_btn.setEnabled(False)
            self.template_name_edit.setEnabled(False)
            self.template_name_edit.clear()
            self.template_preview_widget.set_template(None)
            self.template_info.clear()
            return
        
        template = selected_items[0].data(Qt.ItemDataRole.UserRole)
        if not template:
            self.place_template_btn.setEnabled(False)
            self.template_name_edit.setEnabled(False)
            return
        
        # Update name editor
        self.template_name_edit.setEnabled(True)
        self.template_name_edit.setText(template.name)
        self.template_name_edit.setProperty("template", template)  # Store template reference
        
        # Update visual preview
        self.template_preview_widget.set_template(template)
        
        # Update info text
        info_text = f"Tiles: {len(template.layout.tiles)}\n"
        info_text += f"Functional Tiles: {len(template.layout.functional_tiles)}\n"
        info_text += f"Origin: ({template.origin_point.x}, {template.origin_point.y})\n"
        
        # Show bounds
        if template.layout.tiles or template.layout.functional_tiles:
            all_points = [t[0] for t in template.layout.tiles] + [t[0] for t in template.layout.functional_tiles]
            if all_points:
                min_x = min(p.x for p in all_points)
                max_x = max(p.x for p in all_points)
                min_y = min(p.y for p in all_points)
                max_y = max(p.y for p in all_points)
                info_text += f"Bounds: ({min_x}, {min_y}) to ({max_x}, {max_y})\n"
                info_text += f"Size: {max_x - min_x + 1} x {max_y - min_y + 1}"
        
        self.template_info.setText(info_text)
        self.place_template_btn.setEnabled(True)
    
    def _on_template_name_changed(self):
        """Handle template name change."""
        template = self.template_name_edit.property("template")
        if template:
            new_name = self.template_name_edit.text().strip()
            if new_name and new_name != template.name:
                template.name = new_name
                # Update list item text
                selected_items = self.template_list.selectedItems()
                if selected_items:
                    selected_items[0].setText(new_name)
    
    def _on_choose_color(self):
        """Handle color picker button click."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.template_color = (color.red(), color.green(), color.blue())
            self.template_color_preview.setStyleSheet(
                f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); "
                "border: 1px solid black;"
            )
            # Update template tool if active
            self._update_template_tool()
    
    def _on_scale_changed(self, value: int):
        """Handle scale slider change."""
        scale = value / 100.0
        self.template_scale_label.setText(f"{scale:.2f}")
        # Update template tool if active
        self._update_template_tool_scale(scale)
    
    def _on_activate_template_tool(self):
        """Activate template tool with selected template."""
        selected_items = self.template_list.selectedItems()
        if not selected_items:
            return
        
        template = selected_items[0].data(Qt.ItemDataRole.UserRole)
        if not template or not self.workspace:
            return
        
        # Find main window to access tool manager
        widget = self.parent()  # QSplitter
        if widget:
            widget = widget.parent()  # MainWindow
        
        if widget and hasattr(widget, 'tool_manager') and hasattr(widget, 'canvas'):
            from domain.enums.tool_type import ToolType
            from editing.tools.template_tool import TemplateTool
            
            # Set template tool as active
            widget.tool_manager.set_active_tool(ToolType.TEMPLATE)
            
            # Set template, color and scale in tool
            if isinstance(widget.tool_manager.template_tool, TemplateTool):
                scale = self.template_scale_slider.value() / 100.0
                widget.tool_manager.template_tool.set_template(template)
                widget.tool_manager.template_tool.set_template_color(self.template_color)
                widget.tool_manager.template_tool.set_scale(scale)
            
            # Update canvas
            widget.canvas.set_active_tool(widget.tool_manager.get_active_tool())
            widget.canvas.update()
    
    def _on_tab_changed(self, index: int):
        """Handle tab change - deactivate template tool if leaving Templates tab."""
        # Get tab name
        tab_name = self.tabs.tabText(index)
        if tab_name != "Templates":
            # Deactivate template tool
            self._deactivate_template_tool()
    
    def _deactivate_template_tool(self):
        """Deactivate template tool."""
        widget = self.parent()  # QSplitter
        if widget:
            widget = widget.parent()  # MainWindow
        
        if widget and hasattr(widget, 'tool_manager'):
            from editing.tools.template_tool import TemplateTool
            from domain.enums.tool_type import ToolType
            
            # If template tool is active, switch to default tool (brush)
            if isinstance(widget.tool_manager.get_active_tool(), TemplateTool):
                widget.tool_manager.set_active_tool(ToolType.BRUSH)
                if hasattr(widget, 'canvas'):
                    widget.canvas.update()
    
    def _update_template_tool(self):
        """Update template tool with current color."""
        widget = self.parent()  # QSplitter
        if widget:
            widget = widget.parent()  # MainWindow
        
        if widget and hasattr(widget, 'tool_manager'):
            from editing.tools.template_tool import TemplateTool
            if isinstance(widget.tool_manager.get_active_tool(), TemplateTool):
                widget.tool_manager.template_tool.set_template_color(self.template_color)
                if hasattr(widget, 'canvas'):
                    widget.canvas.update()
    
    def _update_template_tool_scale(self, scale: float):
        """Update template tool with current scale."""
        widget = self.parent()  # QSplitter
        if widget:
            widget = widget.parent()  # MainWindow
        
        if widget and hasattr(widget, 'tool_manager'):
            from editing.tools.template_tool import TemplateTool
            if isinstance(widget.tool_manager.get_active_tool(), TemplateTool):
                widget.tool_manager.template_tool.set_scale(scale)
                if hasattr(widget, 'canvas'):
                    widget.canvas.update()
    
    
    def _update_template_list(self):
        """Update template list from workspace."""
        self.template_list.clear()
        if not self.workspace:
            return
        
        for template in self.workspace.get_all_templates():
            from PyQt6.QtWidgets import QListWidgetItem
            list_item = QListWidgetItem(template.name)
            list_item.setData(Qt.ItemDataRole.UserRole, template)
            self.template_list.addItem(list_item)

