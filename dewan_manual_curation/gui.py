from PySide6.QtWidgets import (QDialog, QPushButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QScrollArea, QSizePolicy, QGraphicsPixmapItem, QGraphicsView, QGraphicsScene)
from PySide6.QtGui import QFont, QPixmap, QImage, QBrush
from PySide6.QtCore import Qt

from project_folder import ProjectFolder

class ManualCurationUI(QDialog):
    def __init__(self, project_folder: ProjectFolder):
        super().__init__()
        self.default_font = QFont("Arial", 12)
        self.project_folder = project_folder


        #  Cell List Components
        self.cell_scroll_list = None
        self.select_all_button = None
        self.select_none_button = None

        #  Layouts
        self.main_layout = None
        self.top_half_container = None
        self.bottom_half_layout = None
        self.cell_list_layout = None
        self.cell_list_control_layout = None

        self.bottom_half_container = None
        self.cell_trace_box_layout = None

        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None

        self.max_projection_view = None

        self.value = []

        self.initUI()

    def init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.max_projection_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def initUI(self):
        self.init_window_params()

        # Main Layout for GUI
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_half_container = QHBoxLayout()  # Holds the cell list and max projection

        self.cell_list_box = QGroupBox("Cells")  # Box for cell scroll area and buttons
        self.cell_list_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.cell_list_box.setMaximumWidth(250)
        self.cell_list_layout = QVBoxLayout()
        self.cell_list_box.setLayout(self.cell_list_layout)

        self.cell_scroll_list = QScrollArea()  # Add the scroll area to the layout
        self.cell_list_layout.addWidget(self.cell_scroll_list)

        self.cell_list_control_layout = QHBoxLayout()  # Add the two buttons to a layout
        self.select_all_button = QPushButton(u"Select All")
        self.select_all_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.select_none_button = QPushButton(u"Select None")
        self.select_none_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cell_list_control_layout.addWidget(self.select_all_button)
        self.cell_list_control_layout.addWidget(self.select_none_button)

        self.cell_list_layout.addLayout(self.cell_list_control_layout)  # Add the control area to the list layout

        self.max_projection_box = QGroupBox("Max Projection")  # Create the max projection box
        self.max_projection_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.max_projection_box.setMinimumSize(300, 300)
        self.max_projection_layout = QHBoxLayout()
        self.max_projection_box.setLayout(self.max_projection_layout)

        self.scene = QGraphicsScene()
        self.max_projection_view = QGraphicsView()
        self.max_projection_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        image = QImage(self.project_folder.max_projection_path)
        pixmap = QPixmap.fromImage(image)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addText("Hello World!")
        self.scene.addItem(self.pixmap_item)
        self.max_projection_view.setScene(self.scene)
        self.max_projection_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.max_projection_view.setMinimumSize(pixmap.size())
        # self.max_projection_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

        self.max_projection_layout.addWidget(self.max_projection_view)

        self.top_half_container.addWidget(self.cell_list_box)
        # Add the list and max projection box to the top half layout
        self.top_half_container.addWidget(self.max_projection_box)
        self.main_layout.addLayout(self.top_half_container)

        self.bottom_half_container = QHBoxLayout()  # Layout for the bottom half of the GUI

        self.cell_trace_box = QGroupBox("Traces")  # Create the cell trace box and add it to the layout
        self.cell_trace_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cell_trace_box.setMinimumHeight(200)

        self.cell_trace_box_layout = QHBoxLayout()
        self.cell_trace_box.setLayout(self.cell_trace_box_layout)

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

