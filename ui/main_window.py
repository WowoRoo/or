"""Main application window."""

from PyQt6.QtWidgets import (
    QMainWindow, QMenuBar, QToolBar, QStatusBar,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QKeySequence, QAction
from domain.entities.workspace import Workspace
from domain.value_objects.references import TileListReference, FunctionalTileListReference
from domain.enums.tile_type import TileType
from domain.enums.functional_tile_type import FunctionalTileType
from editing.workspace.workspace_service import WorkspaceService
from editing.tools.tool_manager import ToolManager
from editing.commands.command_history import CommandHistory
from editing.persistence.workspace_serializer import WorkspaceSerializer
from editing.persistence.workspace_loader import WorkspaceLoader
from editing.tile_transformation.transformation_service import TransformationService
from core.events.event_bus import EventBus
from biometric.segmentation.segmentation_service import SegmentationService
from biometric.preprocessing.preprocessing_service import PreprocessingService
from biometric.skeletonization.skeletonization_service import SkeletonizationService
from biometric.crossinizer.crossinizer_service import CrossinizerService
from biometric.features.feature_detector import FeatureDetector
from biometric.vectorization.vector_generator import VectorGenerator
from biometric.conversion.bitmap_converter import BitmapConverter
from biometric.processor.biometric_processor import BiometricProcessor
from prefab.importer.image_importer import ImageImporter
from prefab.converter.template_converter import TemplateConverter
from visualization.canvas.workspace_canvas import WorkspaceCanvas
from domain.enums.tool_type import ToolType
from domain.enums.skeletonization_algorithm import SkeletonizationAlgorithm
from domain.value_objects.preprocessing_parameters import PreprocessingParameters
from ui.panels.layers_panel import LayersPanel
from ui.panels.properties_panel import PropertiesPanel
from ui.dialogs.new_workspace_dialog import NewWorkspaceDialog
from ui.dialogs.import_image_dialog import ImportImageDialog
from ui.dialogs.algorithm_selection_dialog import AlgorithmSelectionDialog
from ui.dialogs.features_vector_dialog import FeaturesVectorDialog
from ui.dialogs.transformation_dialog import TransformationDialog


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Biometric Level Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize services
        self.event_bus = EventBus()
        self.tile_list_ref = TileListReference(list(TileType))
        self.functional_tile_list_ref = FunctionalTileListReference(list(FunctionalTileType))
        self.workspace_service = WorkspaceService(self.event_bus)
        self.segmentation_service = SegmentationService()
        self.preprocessing_service = PreprocessingService()
        self.skeletonization_service = SkeletonizationService()
        self.crossinizer_service = CrossinizerService()
        self.feature_detector = FeatureDetector()
        self.vector_generator = VectorGenerator()
        self.bitmap_converter = BitmapConverter()
        self.biometric_processor = BiometricProcessor()
        self.image_importer = ImageImporter()
        self.template_converter = TemplateConverter(self.segmentation_service)
        self.command_history = CommandHistory()
        self.serializer = WorkspaceSerializer()
        self.loader = WorkspaceLoader()
        self.transformation_service = TransformationService(self.segmentation_service)
        self.current_algorithm = SkeletonizationAlgorithm.ZHANG_SUEN
        
        # Create default workspace
        self.workspace = self.workspace_service.create_workspace(
            "New Workspace", "User", 50, 50,
            self.tile_list_ref, self.functional_tile_list_ref
        )
        
        # Setup UI first (creates canvas)
        self._setup_ui()
        
        # Initialize tool manager (after workspace and canvas are created)
        self.tool_manager = None
        self._update_tool_manager()
        
        # Load default workspace if exists
        self._load_default_workspace()
    
    def _setup_ui(self):
        """Setup user interface."""
        # Create splitter for panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)
        
        # Left panel (Layers)
        self.layers_panel = LayersPanel(self.workspace)
        splitter.addWidget(self.layers_panel)
        
        # Center (Canvas)
        self.canvas = WorkspaceCanvas(self.workspace)
        splitter.addWidget(self.canvas)
        
        # Right panel (Properties)
        self.properties_panel = PropertiesPanel(self.workspace)
        splitter.addWidget(self.properties_panel)
        
        # Set splitter sizes (20% - 60% - 20%)
        splitter.setSizes([200, 600, 200])
        
        # Override canvas mouse move to update status bar
        original_mouse_move = self.canvas.mouseMoveEvent
        def mouse_move_handler(event):
            original_mouse_move(event)
            self._canvas_mouse_move(event)
        self.canvas.mouseMoveEvent = mouse_move_handler
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Workspace", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self._new_workspace)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Workspace", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self._open_workspace)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Workspace", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._save_workspace)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save Workspace As", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self._save_workspace_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        import_action = QAction("Import Image", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(self._import_image)
        file_menu.addAction(import_action)
        
        export_action = QAction("Export Image", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._export_image)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        clear_action = QAction("Clear Workspace", self)
        clear_action.setShortcut(QKeySequence("Ctrl+Delete"))
        clear_action.triggered.connect(self._clear_workspace)
        edit_menu.addAction(clear_action)
        
        edit_menu.addSeparator()
        
        transform_action = QAction("Apply Tile Transformations", self)
        transform_action.setShortcut(QKeySequence("Ctrl+T"))
        transform_action.triggered.connect(self._apply_transformations)
        transform_action.setToolTip("Apply automatic tile transformations using biometric algorithms (Zaborization)")
        edit_menu.addAction(transform_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        brush_action = QAction("Brush Tool", self)
        brush_action.setShortcut(QKeySequence("B"))
        brush_action.triggered.connect(lambda: self._set_tool(ToolType.BRUSH))
        tools_menu.addAction(brush_action)
        
        eraser_action = QAction("Eraser Tool", self)
        eraser_action.setShortcut(QKeySequence("E"))
        eraser_action.triggered.connect(lambda: self._set_tool(ToolType.ERASER))
        tools_menu.addAction(eraser_action)
        
        flood_action = QAction("Flood Tool", self)
        flood_action.setShortcut(QKeySequence("F"))
        flood_action.triggered.connect(lambda: self._set_tool(ToolType.FLOOD))
        tools_menu.addAction(flood_action)
        
        trash_action = QAction("Trash Tool", self)
        trash_action.setShortcut(QKeySequence("T"))
        trash_action.triggered.connect(lambda: self._set_tool(ToolType.TRASH))
        tools_menu.addAction(trash_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self._zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self._zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self._reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        view_menu.addSeparator()
        
        self.show_grid_action = QAction("Show Grid", self)
        self.show_grid_action.setCheckable(True)
        self.show_grid_action.setChecked(True)
        self.show_grid_action.triggered.connect(self._toggle_grid)
        view_menu.addAction(self.show_grid_action)
        
        self.show_features_action = QAction("Show Features Overlay", self)
        self.show_features_action.setCheckable(True)
        self.show_features_action.triggered.connect(self._toggle_features)
        view_menu.addAction(self.show_features_action)
        
        self.show_skeleton_action = QAction("Show Skeleton Overlay", self)
        self.show_skeleton_action.setCheckable(True)
        self.show_skeleton_action.triggered.connect(self._toggle_skeleton)
        view_menu.addAction(self.show_skeleton_action)
        
        # Biometric menu
        biometric_menu = menubar.addMenu("Biometric")
        
        preprocessing_action = QAction("Run Preprocessing", self)
        preprocessing_action.triggered.connect(self._run_preprocessing)
        biometric_menu.addAction(preprocessing_action)
        
        zaborization_action = QAction("Run Zaborization", self)
        zaborization_action.triggered.connect(self._run_zaborization)
        biometric_menu.addAction(zaborization_action)
        
        skeletonization_action = QAction("Run Skeletonization", self)
        skeletonization_action.triggered.connect(self._run_skeletonization)
        biometric_menu.addAction(skeletonization_action)
        
        crossinizer_action = QAction("Run Crossinizer", self)
        crossinizer_action.triggered.connect(self._run_crossinizer)
        biometric_menu.addAction(crossinizer_action)
        
        features_vector_action = QAction("Generate Features Vector", self)
        features_vector_action.triggered.connect(self._generate_features_vector)
        biometric_menu.addAction(features_vector_action)
        
        biometric_menu.addSeparator()
        
        select_algorithm_action = QAction("Select Skeletonization Algorithm...", self)
        select_algorithm_action.triggered.connect(self._select_algorithm)
        biometric_menu.addAction(select_algorithm_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create toolbar."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # File operations
        new_action = QAction("New", self)
        new_action.triggered.connect(self._new_workspace)
        toolbar.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self._open_workspace)
        toolbar.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self._save_workspace)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Undo/Redo
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self._undo)
        toolbar.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self._redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        # Tools
        brush_action = QAction("Brush", self)
        brush_action.triggered.connect(lambda: self._set_tool(ToolType.BRUSH))
        toolbar.addAction(brush_action)
        
        eraser_action = QAction("Eraser", self)
        eraser_action.triggered.connect(lambda: self._set_tool(ToolType.ERASER))
        toolbar.addAction(eraser_action)
        
        flood_action = QAction("Flood", self)
        flood_action.triggered.connect(lambda: self._set_tool(ToolType.FLOOD))
        toolbar.addAction(flood_action)
        
        trash_action = QAction("Trash", self)
        trash_action.triggered.connect(lambda: self._set_tool(ToolType.TRASH))
        toolbar.addAction(trash_action)
        
        toolbar.addSeparator()
        
        # Transformations button
        transform_toolbar_action = QAction("Transform", self)
        transform_toolbar_action.setToolTip("Apply Tile Transformations (Ctrl+T)\nUses Zaborization to detect regions")
        transform_toolbar_action.triggered.connect(self._apply_transformations)
        toolbar.addAction(transform_toolbar_action)
    
    def _create_status_bar(self):
        """Create status bar."""
        self.statusBar().showMessage("Ready")
        # Status bar will be updated dynamically
    
    def _set_tool(self, tool_type: ToolType):
        """Set active tool."""
        if self.tool_manager:
            self.tool_manager.set_active_tool(tool_type)
            self.canvas.set_active_tool(self.tool_manager.get_active_tool())
            self.statusBar().showMessage(f"Tool: {tool_type.value}")
    
    def _update_tool_manager(self):
        """Update tool manager with current workspace."""
        self.tool_manager = ToolManager(
            self.workspace, self.event_bus, self.segmentation_service, self.command_history
        )
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.set_active_tool(self.tool_manager.get_active_tool())
    
    def _new_workspace(self):
        """Create new workspace."""
        dialog = NewWorkspaceDialog(self)
        if dialog.exec():
            values = dialog.get_values()
            self.workspace = self.workspace_service.create_workspace(
                values["name"], values["author"], values["width"], values["height"],
                self.tile_list_ref, self.functional_tile_list_ref
            )
            self.canvas.tile_size = values["tile_size"]
            self.canvas.workspace = self.workspace
            self.layers_panel.set_workspace(self.workspace)
            self.properties_panel.set_workspace(self.workspace)
            self._update_tool_manager()
            self.canvas.update()
            self._update_status_bar()
    
    def _open_workspace(self):
        """Open workspace."""
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Workspace", "", "Workspace Files (*.workspace)"
        )
        if filepath:
            try:
                self.workspace = self.loader.load_from_file(
                    filepath, self.tile_list_ref, self.functional_tile_list_ref
                )
                self.workspace_service.set_current_workspace(self.workspace)
                self.canvas.workspace = self.workspace
                self.layers_panel.set_workspace(self.workspace)
                self.properties_panel.set_workspace(self.workspace)
                self._update_tool_manager()
                self.canvas.update()
                self._update_status_bar()
                self.statusBar().showMessage(f"Opened: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open workspace: {e}")
    
    def _save_workspace(self):
        """Save workspace."""
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Workspace", "", "Workspace Files (*.workspace)"
        )
        if filepath:
            try:
                self.serializer.save_to_file(self.workspace, filepath)
                self.statusBar().showMessage(f"Saved: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save workspace: {e}")
    
    def _undo(self):
        """Undo last action."""
        if self.command_history.undo():
            self.canvas.update()
            self._update_status_bar()
    
    def _redo(self):
        """Redo last undone action."""
        if self.command_history.redo():
            self.canvas.update()
            self._update_status_bar()
    
    def _load_default_workspace(self):
        """Load default workspace if exists."""
        import os
        default_path = "default.workspace"
        if os.path.exists(default_path):
            try:
                self.workspace = self.loader.load_from_file(
                    default_path, self.tile_list_ref, self.functional_tile_list_ref
                )
                self.workspace_service.set_current_workspace(self.workspace)
                self.canvas.workspace = self.workspace
                self.layers_panel.set_workspace(self.workspace)
                self.properties_panel.set_workspace(self.workspace)
                self._update_tool_manager()
                self.canvas.update()
                self._update_status_bar()
            except Exception:
                pass  # Ignore errors loading default
    
    def _save_workspace_as(self):
        """Save workspace with new name."""
        self._save_workspace()
    
    def _import_image(self):
        """Import image and convert to template."""
        dialog = ImportImageDialog(self)
        if dialog.exec():
            values = dialog.get_values()
            if values["filepath"]:
                try:
                    bitmap = self.image_importer.import_image(values["filepath"])
                    template = self.template_converter.convert_bitmap_to_template(
                        bitmap, "Imported Template"
                    )
                    # Add template to workspace
                    self.workspace.add_template(template)
                    # Update properties panel to show new template
                    self.properties_panel.set_workspace(self.workspace)
                    QMessageBox.information(
                        self, "Success", 
                        f"Image imported successfully as template '{template.name}'.\n"
                        f"Template contains {len(template.layout.tiles)} tiles."
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to import image: {e}")
    
    def _export_image(self):
        """Export workspace as image."""
        from PyQt6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Image", "", "Image Files (*.png *.jpg)"
        )
        if filepath:
            try:
                # Convert workspace to image and save
                bitmap = self.workspace.tilemap.to_bitmap()
                img = bitmap.to_image()
                img.save(filepath)
                QMessageBox.information(self, "Success", f"Image exported to {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export image: {e}")
    
    def _clear_workspace(self):
        """Clear workspace."""
        reply = QMessageBox.question(
            self, "Clear Workspace", "Are you sure you want to clear the workspace?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # Remove all objects from all layers
            for layer in self.workspace.layers:
                layer.map_objects.clear()
            # Clear tilemap
            for cell in self.workspace.tilemap.cells.values():
                cell.clear()
            self.canvas.update()
            self._update_status_bar()
    
    def _apply_transformations(self):
        """Apply automatic tile transformations using biometric algorithms."""
        if not self.workspace:
            QMessageBox.warning(self, "Warning", "No workspace available")
            return
        
        # Show options dialog
        dialog = TransformationDialog(self)
        if not dialog.exec():
            return
        
        max_iterations = dialog.get_max_iterations()
        
        # Show progress dialog
        from PyQt6.QtWidgets import QProgressDialog
        progress = QProgressDialog("Applying transformations...\nUsing Zaborization to detect regions", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setCancelButton(None)
        progress.show()
        
        try:
            # Update UI
            self.statusBar().showMessage("Applying transformations using biometric algorithms (Zaborization)...")
            
            # Apply transformations (uses zaborization internally)
            count = self.transformation_service.apply_transformations_iterative(
                self.workspace, max_iterations=max_iterations
            )
            
            progress.close()
            self.canvas.update()
            self._update_status_bar()
            
            QMessageBox.information(
                self, "Transformations Applied",
                f"Applied {count} tile transformation(s) using biometric algorithms (Zaborization).\n\n"
                f"Rules applied:\n"
                f"• Dirt → Grass (if free space above or adjacent to grass)\n"
                f"• Lava + Water → Stone\n"
                f"• Water + Lava → Stone\n\n"
                f"Iterations: {max_iterations}"
            )
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Error", f"Transformation failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _zoom_in(self):
        """Zoom in."""
        self.canvas.zoom_level *= 1.2
        self.canvas.update()
    
    def _zoom_out(self):
        """Zoom out."""
        self.canvas.zoom_level /= 1.2
        self.canvas.update()
    
    def _reset_zoom(self):
        """Reset zoom."""
        self.canvas.zoom_level = 1.0
        self.canvas.pan_offset = QPoint(0, 0)
        self.canvas.update()
    
    def _toggle_grid(self):
        """Toggle grid display."""
        self.canvas.show_grid = self.show_grid_action.isChecked()
        self.canvas.update()
    
    def _toggle_features(self):
        """Toggle features overlay."""
        self.canvas.show_features = self.show_features_action.isChecked()
        self.canvas.update()
    
    def _toggle_skeleton(self):
        """Toggle skeleton overlay."""
        self.canvas.show_skeleton = self.show_skeleton_action.isChecked()
        self.canvas.update()
    
    def _run_preprocessing(self):
        """Run preprocessing."""
        if not self.workspace:
            return
        try:
            bitmap = self.workspace.tilemap.to_bitmap()
            params = PreprocessingParameters()
            processed = self.preprocessing_service.preprocess(bitmap, params)
            self.workspace.workspace_bitmap = processed
            QMessageBox.information(self, "Success", "Preprocessing completed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Preprocessing failed: {e}")
    
    def _run_zaborization(self):
        """Run zaborization."""
        if not self.workspace:
            return
        try:
            bitmap = self.workspace.workspace_bitmap or self.workspace.tilemap.to_bitmap()
            result = self.segmentation_service.segment(bitmap)
            # Store result somewhere or display
            QMessageBox.information(self, "Success", f"Zaborization completed: {len(result.foreground_regions)} foreground regions")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Zaborization failed: {e}")
    
    def _run_skeletonization(self):
        """Run skeletonization."""
        if not self.workspace:
            return
        try:
            bitmap = self.workspace.workspace_bitmap or self.workspace.tilemap.to_bitmap()
            result = self.skeletonization_service.skeletonize(bitmap, self.current_algorithm)
            # Store result for overlay
            self.canvas.skeleton_result = result
            QMessageBox.information(self, "Success", f"Skeletonization completed using {result.algorithm_used}")
            self.canvas.update()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Skeletonization failed: {e}")
    
    def _run_crossinizer(self):
        """Run crossinizer."""
        if not hasattr(self.canvas, 'skeleton_result') or not self.canvas.skeleton_result:
            QMessageBox.warning(self, "Warning", "Please run skeletonization first")
            return
        try:
            result = self.crossinizer_service.analyze(self.canvas.skeleton_result)
            # Store for features overlay
            self.canvas.crossinizer_result = result
            QMessageBox.information(
                self, "Success",
                f"Crossinizer completed: {len(result.endpoints)} endpoints, "
                f"{len(result.bifurcations)} bifurcations, {len(result.crossings)} crossings"
            )
            self.canvas.update()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Crossinizer failed: {e}")
    
    def _generate_features_vector(self):
        """Generate features vector."""
        if not hasattr(self.canvas, 'crossinizer_result') or not self.canvas.crossinizer_result:
            QMessageBox.warning(self, "Warning", "Please run crossinizer first")
            return
        try:
            features = self.feature_detector.detect_features(
                self.canvas.crossinizer_result,
                self.canvas.skeleton_result
            )
            features_vector = self.vector_generator.generate(features, self.workspace)
            self.workspace.features_vector = features_vector
            self.properties_panel.set_workspace(self.workspace)
            
            # Show dialog
            dialog = FeaturesVectorDialog(features_vector, self)
            dialog.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Features vector generation failed: {e}")
    
    def _select_algorithm(self):
        """Select skeletonization algorithm."""
        dialog = AlgorithmSelectionDialog(self.current_algorithm, self)
        if dialog.exec():
            self.current_algorithm = dialog.get_selected_algorithm()
            self.statusBar().showMessage(f"Algorithm: {self.current_algorithm.value}")
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About",
            "Biometric Level Editor\n\n"
            "Edytor poziomów platformowych z algorytmami biometrycznymi.\n\n"
            "Version 1.0"
        )
    
    def _canvas_mouse_move(self, event):
        """Handle canvas mouse move to update status bar."""
        point = self.canvas._screen_to_world(event.pos())
        if point:
            self._update_status_bar_cursor(point.x, point.y)
        else:
            self._update_status_bar()
    
    def _update_status_bar(self):
        """Update status bar with current information."""
        if not self.workspace:
            return
        
        active_layer = self.workspace.get_active_layer()
        layer_name = active_layer.name if active_layer else "None"
        
        tool_name = "None"
        if self.tool_manager and self.tool_manager.get_active_tool():
            tool_name = self.tool_manager.get_active_tool().tool_type.value
        
        msg = f"Tool: {tool_name} | Layer: {layer_name} | Size: {self.workspace.metadata.width}x{self.workspace.metadata.height}"
        self.statusBar().showMessage(msg)
    
    def _update_status_bar_cursor(self, x: int, y: int):
        """Update status bar with cursor position."""
        if not self.workspace:
            return
        
        active_layer = self.workspace.get_active_layer()
        layer_name = active_layer.name if active_layer else "None"
        
        tool_name = "None"
        if self.tool_manager and self.tool_manager.get_active_tool():
            tool_name = self.tool_manager.get_active_tool().tool_type.value
        
        msg = f"Tool: {tool_name} | Layer: {layer_name} | Pos: ({x}, {y}) | Size: {self.workspace.metadata.width}x{self.workspace.metadata.height}"
        self.statusBar().showMessage(msg)

