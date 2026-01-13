"""Transformation options dialog."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QPushButton, QDialogButtonBox, QTextEdit
)


class TransformationDialog(QDialog):
    """Dialog for transformation options."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tile Transformations")
        self.setModal(True)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        # Info text
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(150)
        info_text.setText(
            "Automatic tile transformations using biometric algorithms (Zaborization).\n\n"
            "Rules:\n"
            "• Dirt → Grass (if has free space above)\n"
            "• Dirt → Grass (if adjacent to grass blocks)\n"
            "• Lava + Water → Stone\n"
            "• Water + Lava → Stone\n\n"
            "Transformations use Zaborization to detect regions and analyze neighbor relationships."
        )
        layout.addWidget(info_text)
        
        # Max iterations
        iterations_layout = QHBoxLayout()
        iterations_layout.addWidget(QLabel("Max Iterations:"))
        self.iterations_spin = QSpinBox()
        self.iterations_spin.setMinimum(1)
        self.iterations_spin.setMaximum(50)
        self.iterations_spin.setValue(10)
        self.iterations_spin.setToolTip("Number of iterations to apply transformations")
        iterations_layout.addWidget(self.iterations_spin)
        layout.addLayout(iterations_layout)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_max_iterations(self) -> int:
        """Get max iterations value."""
        return self.iterations_spin.value()

