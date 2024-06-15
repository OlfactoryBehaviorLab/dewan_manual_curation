from PySide6.QtWidgets import (QDialog, QPushButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QScrollArea, QSizePolicy,
                               QGraphicsPixmapItem, QGraphicsView, QGraphicsScene, QCheckBox, QWidget)
from PySide6.QtGui import QFont, QPixmap, QImage, QWheelEvent, QShowEvent
from PySide6.QtCore import Qt

from matplotlib.backends.backend_qt import FigureCanvasQT
from matplotlib.figure import Figure

from project_folder import ProjectFolder

SCALE_FACTOR = 0.01


class CellTrace(FigureCanvasQT):
    def __init__(self, parent=None, width=30, height=1.1, dpi=100):
        self.parent = parent
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.subplots(111)
        super().__init__(self.figure)




class ManualCurationUI(QDialog):
    def __init__(self, project_folder: ProjectFolder, cell_names):

        super().__init__()
        self.default_font = QFont("Arial", 12)
        self.project_folder = project_folder
        self.cells = cell_names
        #  Cell Selection List Components
        self.cell_scroll_area = None
        self.cell_list = None
        self.select_all_button = None
        self.select_none_button = None
        self.cell_selection_checkbox_list = None
        self.cell_view_checkbox_list = None
        # Cell View List Components
        self.cell_view_list = None
        self.cell_view_scroll_area = None
        # Cell Trace List Components
        self.cell_trace_scroll_area_contents = None
        self.cell_trace_scroll_area = None
        #  Layouts
        self.main_layout = None
        self.top_half_container = None
        self.bottom_half_layout = None
        self.cell_list_layout = None
        self.cell_list_control_layout = None
        self.cell_select_checkbox_layout = None
        self.max_projection_layout = None
        self.max_projection_controls = None
        self.cell_view_checkbox_layout = None
        self.bottom_half_container = None
        self.cell_trace_box_layout = None
        self.cell_trace_layout = None
        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None
        #  Max Projection Controls
        self.zoom_in = None
        self.zoom_out = None
        self.zoom_reset = None
        #  Image View Components
        self.max_projection_view = None
        self.scene = None
        self.image = None
        self.pixmap = None
        self.pixmap_item = None
        self.scale = 1
        self.direction = 0

        self.value = []

        self.initUI()

    #  Function Overloads
    def eventFilter(self, obj, event):
        if type(event) is QWheelEvent:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:

                num_degrees = event.angleDelta() / 8
                steps = int(num_degrees.y() / 15)

                self.zoom_image(steps)
            return True
        elif type(event) is QShowEvent:
            self.max_projection_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            return False  # We don't actually wanna handle this event, just needed to run this with it
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.reset_image_zoom()
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Equal:
                self.zoom_image_in()
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_image_out()

    def resizeEvent(self, event):
        event.accept()
        if self.scale == 1:
            self.max_projection_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.scale = 1

    #  Class Functions
    def zoom_image(self, steps: int):
        if steps != self.direction:
            self.scale = 1
            self.direction = steps

        self.scale += (SCALE_FACTOR * steps)
        self.max_projection_view.scale(self.scale, self.scale)

    def reset_image_zoom(self):
        self.scale = 1
        self.max_projection_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def zoom_image_in(self):
        self.zoom_image(1)

    def zoom_image_out(self):
        self.zoom_image(-1)

    def select_none(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(Qt.CheckState.Unchecked)

    def select_all(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(Qt.CheckState.Checked)

    def populate_selection_list(self):
        self.cell_selection_checkbox_list = []

        for each in self.cells:
            selection_CB = QCheckBox(str(each))
            selection_CB.setCheckState(Qt.CheckState.Checked)
            self.cell_selection_checkbox_list.append(selection_CB)
            self.cell_select_checkbox_layout.addWidget(selection_CB)

    def populate_view_list(self):
        self.cell_view_checkbox_list = []

        for each in self.cells:
            view_CB = QCheckBox(str(each))
            view_CB.setCheckState(Qt.CheckState.Checked)
            self.cell_view_checkbox_list.append(view_CB)
            self.cell_view_checkbox_layout.addWidget(view_CB)

    def init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def initUI(self):
        self.init_window_params()

        # ==MAIN LAYOUT== #
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # ==TOP HALF== #
        self.top_half_container = QHBoxLayout()  # Holds the cell list and max projection

        # ==Cell Selection List== #
        self.cell_list_box = QGroupBox("Cells")
        self.cell_list_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.cell_list_box.setMaximumWidth(250)
        self.cell_list_layout = QVBoxLayout()
        self.cell_list_box.setLayout(self.cell_list_layout)

        self.cell_list = QWidget()
        self.cell_select_checkbox_layout = QVBoxLayout(self.cell_list)
        self.populate_selection_list()

        self.cell_scroll_area = QScrollArea()  # Add the scroll area to the layout
        self.cell_scroll_area.setWidget(self.cell_list)
        self.cell_list_layout.addWidget(self.cell_scroll_area)

        # ==Cell Selection List Controls== #
        self.cell_list_control_layout = QHBoxLayout()  # Add the two buttons to a layout
        self.select_all_button = QPushButton(u"Select All")
        self.select_all_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.select_all_button.clicked.connect(self.select_all)
        self.select_none_button = QPushButton(u"Select None")
        self.select_none_button.clicked.connect(self.select_none)
        self.select_none_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.cell_list_control_layout.addWidget(self.select_all_button)
        self.cell_list_control_layout.addWidget(self.select_none_button)
        self.cell_list_layout.addLayout(self.cell_list_control_layout)

        self.top_half_container.addWidget(self.cell_list_box)  # Cell list to top half

        # ==Maximum Projection View== #
        self.max_projection_box = QGroupBox("Max Projection")  # Create the max projection box
        self.max_projection_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_box.setMinimumSize(300, 300)
        self.max_projection_layout = QHBoxLayout()
        self.max_projection_box.setLayout(self.max_projection_layout)

        self.max_projection_controls = QVBoxLayout()
        self.max_projection_controls.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom_in = QPushButton("+")
        self.zoom_out = QPushButton("-")
        self.zoom_reset = QPushButton("R")
        self.zoom_in.clicked.connect(self.zoom_image_in)
        self.zoom_out.clicked.connect(self.zoom_image_out)
        self.zoom_reset.clicked.connect(self.reset_image_zoom)

        self.max_projection_controls.addWidget(self.zoom_in)
        self.max_projection_controls.addWidget(self.zoom_out)
        self.max_projection_controls.addWidget(self.zoom_reset)
        self.max_projection_layout.addLayout(self.max_projection_controls)

        # ==Max Projection Display== #
        self.scene = QGraphicsScene()
        self.max_projection_view = QGraphicsView()
        self.max_projection_view.setInteractive(True)
        self.max_projection_view.setMouseTracking(True)
        self.max_projection_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.max_projection_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.viewport().installEventFilter(self)

        self.image = QImage(self.project_folder.max_projection_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmap_item)
        self.max_projection_view.setScene(self.scene)

        self.max_projection_layout.addWidget(self.max_projection_view)

        # Add the list and max projection box to the top half layout
        self.top_half_container.addWidget(self.max_projection_box)
        self.main_layout.addLayout(self.top_half_container)

        # ==BOTTOM HALF== #
        self.bottom_half_container = QHBoxLayout()  # Layout for the bottom half of the GUI

        # ==CELL TRACE REGION== #
        self.cell_trace_box = QGroupBox("Traces")  # Create the cell trace box and add it to the layout
        self.cell_trace_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cell_trace_box.setMinimumHeight(200)

        self.cell_trace_box_layout = QHBoxLayout()
        self.cell_trace_box.setLayout(self.cell_trace_box_layout)

        # ==Cell View List== #
        self.cell_view_list = QWidget()
        self.cell_view_checkbox_layout = QVBoxLayout(self.cell_view_list)
        self.populate_view_list()

        self.cell_view_scroll_area = QScrollArea()
        self.cell_view_scroll_area.setMaximumWidth(250)
        self.cell_view_scroll_area.setWidget(self.cell_view_list)
        self.cell_trace_box_layout.addWidget(self.cell_view_scroll_area)

        # ==Cell Trace View== #
        self.cell_trace_scroll_area_contents = QWidget()
        self.cell_trace_layout = QVBoxLayout(self.cell_trace_scroll_area_contents)

        self.cell_trace_scroll_area = QScrollArea()
        self.cell_trace_scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cell_trace_scroll_area.setWidget(self.cell_trace_scroll_area_contents)
        self.cell_trace_box_layout.addWidget(self.cell_trace_scroll_area)

        self.bottom_half_container.addWidget(self.cell_trace_box)
        self.main_layout.addLayout(self.bottom_half_container)

    def closeEvent(self, e):
        self.reject()

    def reject(self):
        self.value = -10
        self.close()

    def accept(self):
        self.value = 10
        self.close()
