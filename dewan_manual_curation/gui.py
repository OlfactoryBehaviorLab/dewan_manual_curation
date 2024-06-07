from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class ManualCurationUI(QDialog):
    def __init__(self):
        super().__init__()
        self.default_font = QFont("Arial", 12)

        #  Layouts
        self.main_layout = None
        self.top_half_layout = None
        self.bottom_half_layout = None

        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None

        self.value = []

        self.initUI()

    def init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setMinimumSize(400, 400)
        self.resize(400, 400)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def initUI(self):
        self.init_window_params()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_half_layout = QHBoxLayout()
        self.cell_list_box = QGroupBox("Cells")
        self.max_projection_box = QGroupBox("Max Projection")
        self.top_half_layout.addWidget(self.cell_list_box)
        self.top_half_layout.addWidget(self.max_projection_box)
        self.main_layout.addLayout(self.top_half_layout)

        self.cell_trace_box = QGroupBox("Traces")
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
