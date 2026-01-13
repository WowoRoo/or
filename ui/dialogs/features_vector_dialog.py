"""Features vector display dialog."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
)
from domain.value_objects.features_vector import FeaturesVector


class FeaturesVectorDialog(QDialog):
    """Dialog for displaying features vector."""
    
    def __init__(self, features_vector: FeaturesVector, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Features Vector")
        self.setModal(False)
        self._setup_ui(features_vector)
    
    def _setup_ui(self, features_vector: FeaturesVector):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        # Display feature counts
        from domain.enums.feature_type import FeatureType
        
        endpoints_label = QLabel(f"Endpoints: {features_vector.feature_counts.get(FeatureType.ENDPOINT, 0)}")
        layout.addWidget(endpoints_label)
        
        bifurcations_label = QLabel(f"Bifurcations: {features_vector.feature_counts.get(FeatureType.BIFURCATION, 0)}")
        layout.addWidget(bifurcations_label)
        
        crossings_label = QLabel(f"Crossings: {features_vector.feature_counts.get(FeatureType.CROSSING, 0)}")
        layout.addWidget(crossings_label)
        
        # Density
        density = features_vector.vector[3] if len(features_vector.vector) > 3 else 0.0
        density_label = QLabel(f"Density: {density:.6f} features/tile")
        layout.addWidget(density_label)
        
        # Vector display
        layout.addWidget(QLabel("Vector:"))
        vector_text = QTextEdit()
        vector_text.setReadOnly(True)
        vector_text.setText(str(features_vector.vector.tolist()))
        layout.addWidget(vector_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

