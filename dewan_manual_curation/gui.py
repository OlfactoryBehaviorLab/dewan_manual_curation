from PySide6.QtWidgets import (QDialog, QPushButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QFrame, QScrollArea, QSizePolicy)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class ManualCurationUI(QDialog):
    def __init__(self):
        super().__init__()
        self.default_font = QFont("Arial", 12)

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

        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None

        self.value = []

        self.initUI()

    def init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setMinimumSize(500, 600)
        # self.resize(400, 400)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def initUI(self):
        self.init_window_params()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_half_container = QHBoxLayout()  # Holds the cell list and max projection

        self.cell_list_box = QGroupBox("Cells")  # Box for cell scroll area and buttons
        self.cell_list_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.cell_list_box.setMaximumWidth(250)

        self.cell_list_layout = QVBoxLayout()
        self.cell_list_box.setLayout(self.cell_list_layout)

        self.cell_scroll_list = QScrollArea()
        self.cell_list_layout.addWidget(self.cell_scroll_list)  # Add the scroll area to the layout

        self.cell_list_control_layout = QHBoxLayout()
        self.select_all_button = QPushButton(u"Select All")
        self.select_all_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.select_none_button = QPushButton(u"Select None")
        self.select_none_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.cell_list_control_layout.addWidget(self.select_all_button)
        self.cell_list_control_layout.addWidget(self.select_none_button)

        self.cell_list_layout.addLayout(self.cell_list_control_layout)

        self.max_projection_box = QGroupBox("Max Projection")
        self.max_projection_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.max_projection_box.setMinimumHeight(300)

        self.top_half_container.addWidget(self.cell_list_box)
        self.top_half_container.addWidget(self.max_projection_box)
        self.main_layout.addLayout(self.top_half_container)

        self.cell_trace_box = QGroupBox("Traces")
        self.cell_trace_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cell_trace_box.setMinimumHeight(200)
        self.bottom_half_layout = QHBoxLayout()
        self.cell_trace_box.setLayout(self.bottom_half_layout)

        self.main_layout.addWidget(self.cell_trace_box)

    def closeEvent(self, e):
        self.reject()

    def reject(self):
        self.value = -10
        self.close()

    def accept(self):
        self.value = 10
        self.close()
