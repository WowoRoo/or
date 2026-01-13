"""Layers panel widget."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QCheckBox, QLabel
)
from PyQt6.QtCore import Qt as QtCore
from PyQt6.QtCore import Qt
from domain.entities.workspace import Workspace
from domain.entities.layer import Layer
from uuid import UUID


class LayersPanel(QWidget):
    """Panel for managing layers."""
    
    def __init__(self, workspace: Workspace, parent=None):
        super().__init__(parent)
        self.workspace = workspace
        self.active_layer_id: UUID = None
        self._setup_ui()
        self._update_layers()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Layers")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Layers list
        self.layers_list = QListWidget()
        self.layers_list.itemChanged.connect(self._on_layer_changed)
        self.layers_list.itemDoubleClicked.connect(self._on_layer_double_clicked)
        self.layers_list.itemClicked.connect(self._on_layer_clicked)
        layout.addWidget(self.layers_list)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        add_button = QPushButton("+ Add Layer")
        add_button.clicked.connect(self._add_layer)
        button_layout.addWidget(add_button)
        
        remove_button = QPushButton("- Remove Layer")
        remove_button.clicked.connect(self._remove_layer)
        button_layout.addWidget(remove_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def _update_layers(self):
        """Update layers list."""
        self.layers_list.clear()
        
        if not self.workspace:
            return
        
        # Sync active_layer_id from workspace
        if self.workspace.active_layer_id:
            self.active_layer_id = self.workspace.active_layer_id
        
        for layer in self.workspace.layers:
            # Create item without text (text will be in widget)
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, layer.id)
            
            # Create widget with checkbox and label
            widget = QWidget()
            widget_layout = QHBoxLayout(widget)
            widget_layout.setContentsMargins(4, 2, 4, 2)
            widget_layout.setSpacing(8)
            
            # Add visibility checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(layer.visible)
            checkbox.stateChanged.connect(
                lambda state, l=layer: self._toggle_visibility(l, state == Qt.CheckState.Checked.value)
            )
            # Store item reference for checkbox clicks - select item when checkbox area is clicked
            def on_checkbox_click(e, it=item):
                # Select item when checkbox is clicked
                self.layers_list.setCurrentItem(it)
                # Let default checkbox behavior happen
                QCheckBox.mousePressEvent(checkbox, e)
            checkbox.mousePressEvent = on_checkbox_click
            widget_layout.addWidget(checkbox)
            
            # Add label with layer name
            label = QLabel(layer.name)
            label.setWordWrap(False)
            # Make label clickable to select item
            label.mousePressEvent = lambda e, it=item: self._select_item(it)
            widget_layout.addWidget(label)
            widget_layout.addStretch()
            
            # Mark active layer
            if layer.id == self.active_layer_id:
                item.setBackground(Qt.GlobalColor.lightGray)
                # Also set as selected and current
                item.setSelected(True)
                self.layers_list.setCurrentItem(item)
            
            self.layers_list.addItem(item)
            self.layers_list.setItemWidget(item, widget)
            
            # Make the whole widget clickable to select the item
            def make_widget_clickable(w, it=item):
                def mousePressEvent(e):
                    # Select item when widget is clicked
                    self.layers_list.setCurrentItem(it)
                    it.setSelected(True)
                    # Also set as active layer
                    layer_id = it.data(Qt.ItemDataRole.UserRole)
                    if layer_id and self.workspace:
                        self.workspace.active_layer_id = layer_id
                        self.set_active_layer(layer_id)
                    # Call parent mousePressEvent
                    QWidget.mousePressEvent(w, e)
                w.mousePressEvent = mousePressEvent
            
            make_widget_clickable(widget)
    
    def _toggle_visibility(self, layer: Layer, visible: bool):
        """Toggle layer visibility."""
        layer.visible = visible
        # Find main window and update canvas
        widget = self.parent()
        while widget:
            if hasattr(widget, 'canvas'):
                widget.canvas.update()
                break
            widget = widget.parent()
    
    def _on_layer_changed(self, item: QListWidgetItem):
        """Handle layer item changed."""
        pass
    
    def _select_item(self, item: QListWidgetItem):
        """Select item in list."""
        self.layers_list.setCurrentItem(item)
        self._on_layer_clicked(item)
    
    def _on_layer_clicked(self, item: QListWidgetItem):
        """Handle layer click - set as active layer."""
        layer_id = item.data(Qt.ItemDataRole.UserRole)
        if layer_id and self.workspace:
            # Set in workspace first
            self.workspace.active_layer_id = layer_id
            # Then update UI
            self.set_active_layer(layer_id)
    
    def _on_layer_double_clicked(self, item: QListWidgetItem):
        """Handle layer double click (rename)."""
        # Simple rename - could be improved with dialog
        layer_id = item.data(Qt.ItemDataRole.UserRole)
        layer = next((l for l in self.workspace.layers if l.id == layer_id), None)
        if layer:
            from PyQt6.QtWidgets import QInputDialog
            new_name, ok = QInputDialog.getText(self, "Rename Layer", "Layer name:", text=layer.name)
            if ok and new_name:
                layer.name = new_name
                self._update_layers()
    
    def _add_layer(self):
        """Add new layer."""
        if not self.workspace:
            return
        
        from domain.enums.layer_type import LayerType
        new_layer = Layer(
            name=f"Layer {len(self.workspace.layers) + 1}",
            layer_type=LayerType.TILE_LAYER,
            tile_list_reference=self.workspace.tile_list_reference,
            functional_tile_list_reference=self.workspace.functional_tile_list_reference
        )
        self.workspace.add_layer(new_layer)
        # Set new layer as active
        self.workspace.active_layer_id = new_layer.id
        self._update_layers()
    
    def _remove_layer(self):
        """Remove selected layer."""
        if not self.workspace:
            return
        
        # Use active layer as primary source
        layer_id = None
        
        # First try to get from selected item
        current_item = self.layers_list.currentItem()
        if current_item:
            layer_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        # If no selected item, try selectedItems
        if not layer_id:
            selected_items = self.layers_list.selectedItems()
            if selected_items:
                layer_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        
        # If still no layer_id, use active layer
        if not layer_id and self.workspace.active_layer_id:
            layer_id = self.workspace.active_layer_id
        
        if not layer_id:
            return
            
        if len(self.workspace.layers) <= 1:  # Don't remove last layer
            return
        
        try:
            self.workspace.remove_layer(layer_id)
            self._update_layers()
            
            # Update canvas to reflect changes
            widget = self.parent()
            while widget:
                if hasattr(widget, 'canvas'):
                    widget.canvas.update()
                    break
                widget = widget.parent()
        except Exception as e:
            import traceback
            print(f"Error removing layer: {e}")
            traceback.print_exc()
    
    def set_active_layer(self, layer_id: UUID):
        """Set active layer."""
        self.active_layer_id = layer_id
        self._update_layers()
    
    def set_workspace(self, workspace: Workspace):
        """Update workspace."""
        self.workspace = workspace
        self._update_layers()

