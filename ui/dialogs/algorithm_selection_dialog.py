"""Algorithm selection dialog."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QRadioButton, QButtonGroup, QDialogButtonBox
)
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm


class AlgorithmSelectionDialog(QDialog):
    """Dialog for selecting skeletonization algorithm."""
    
    def __init__(self, current_algorithm: SkeletonizationAlgorithm = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Algorithm")
        self.setModal(True)
        self._setup_ui(current_algorithm)
    
    def _setup_ui(self, current_algorithm):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Algorithm:"))
        
        self.algorithm_group = QButtonGroup()
        # Map button IDs to algorithms
        self.algorithm_map = {}
        
        zhang_suen_radio = QRadioButton("Zhang-Suen")
        zhang_suen_id = 0
        self.algorithm_group.addButton(zhang_suen_radio, zhang_suen_id)
        self.algorithm_map[zhang_suen_id] = SkeletonizationAlgorithm.ZHANG_SUEN
        layout.addWidget(zhang_suen_radio)
        
        hildritch_radio = QRadioButton("Hildritch")
        hildritch_id = 1
        self.algorithm_group.addButton(hildritch_radio, hildritch_id)
        self.algorithm_map[hildritch_id] = SkeletonizationAlgorithm.HILDRITCH
        layout.addWidget(hildritch_radio)
        
        # Set current selection
        if current_algorithm == SkeletonizationAlgorithm.ZHANG_SUEN:
            zhang_suen_radio.setChecked(True)
        elif current_algorithm == SkeletonizationAlgorithm.HILDRITCH:
            hildritch_radio.setChecked(True)
        else:
            zhang_suen_radio.setChecked(True)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_selected_algorithm(self) -> SkeletonizationAlgorithm:
        """Get selected algorithm."""
        checked_id = self.algorithm_group.checkedId()
        if checked_id in self.algorithm_map:
            return self.algorithm_map[checked_id]
        return SkeletonizationAlgorithm.ZHANG_SUEN

