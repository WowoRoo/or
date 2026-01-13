"""New workspace dialog."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSpinBox, QPushButton, QDialogButtonBox
)


class NewWorkspaceDialog(QDialog):
    """Dialog for creating new workspace."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Workspace")
        self.setModal(True)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setText("New Workspace")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Author
        author_layout = QHBoxLayout()
        author_layout.addWidget(QLabel("Author:"))
        self.author_edit = QLineEdit()
        self.author_edit.setText("User")
        author_layout.addWidget(self.author_edit)
        layout.addLayout(author_layout)
        
        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(10)
        self.width_spin.setMaximum(10000)
        self.width_spin.setValue(100)
        width_layout.addWidget(self.width_spin)
        width_layout.addWidget(QLabel("tiles"))
        layout.addLayout(width_layout)
        
        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(10)
        self.height_spin.setMaximum(10000)
        self.height_spin.setValue(100)
        height_layout.addWidget(self.height_spin)
        height_layout.addWidget(QLabel("tiles"))
        layout.addLayout(height_layout)
        
        # Tile Size
        tile_size_layout = QHBoxLayout()
        tile_size_layout.addWidget(QLabel("Tile Size:"))
        self.tile_size_spin = QSpinBox()
        self.tile_size_spin.setMinimum(8)
        self.tile_size_spin.setMaximum(128)
        self.tile_size_spin.setValue(32)
        tile_size_layout.addWidget(self.tile_size_spin)
        tile_size_layout.addWidget(QLabel("pixels"))
        layout.addLayout(tile_size_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_values(self):
        """Get dialog values."""
        return {
            "name": self.name_edit.text(),
            "author": self.author_edit.text(),
            "width": self.width_spin.value(),
            "height": self.height_spin.value(),
            "tile_size": self.tile_size_spin.value()
        }

