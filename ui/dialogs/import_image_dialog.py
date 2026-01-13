"""Import image dialog."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QDialogButtonBox, QDoubleSpinBox,
    QRadioButton, QButtonGroup, QFileDialog
)
from PyQt6.QtCore import Qt


class ImportImageDialog(QDialog):
    """Dialog for importing images."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Image")
        self.setModal(True)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Select image file:"))
        self.file_edit = QLineEdit()
        self.file_edit.setReadOnly(True)
        file_layout.addWidget(self.file_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Zaborization parameters
        layout.addWidget(QLabel("Zaborization Parameters:"))
        
        # Connectivity
        connectivity_layout = QHBoxLayout()
        connectivity_layout.addWidget(QLabel("Connectivity:"))
        self.connectivity_group = QButtonGroup()
        self.connectivity_4 = QRadioButton("4")
        self.connectivity_8 = QRadioButton("8")
        self.connectivity_8.setChecked(True)
        self.connectivity_group.addButton(self.connectivity_4, 4)
        self.connectivity_group.addButton(self.connectivity_8, 8)
        connectivity_layout.addWidget(self.connectivity_4)
        connectivity_layout.addWidget(self.connectivity_8)
        layout.addLayout(connectivity_layout)
        
        # Threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Threshold:"))
        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setMinimum(0.0)
        self.threshold_spin.setMaximum(1.0)
        self.threshold_spin.setSingleStep(0.1)
        self.threshold_spin.setValue(0.5)
        threshold_layout.addWidget(self.threshold_spin)
        layout.addLayout(threshold_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _browse_file(self):
        """Browse for image file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if filepath:
            self.file_edit.setText(filepath)
    
    def get_values(self):
        """Get dialog values."""
        return {
            "filepath": self.file_edit.text(),
            "connectivity": self.connectivity_group.checkedId(),
            "threshold": self.threshold_spin.value()
        }

