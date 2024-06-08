from PySide6.QtWidgets import (QDialog, QPushButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QFileDialog, QScrollArea, QSizePolicy)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from pathlib import Path


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

        self.bottom_half_container = None
        self.cell_trace_box_layout = None

        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None

        self.value = []

        self.initUI()

    def init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

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


class ProjectFolder:
    def __init__(self, root_dir=None):
        self.root_dir = root_dir

        self.project_folder = None
        self.cell_trace_data = None
        self.max_projection_image = None

        self.setup_folder()

    def setup_folder(self):
        project_folder = self.get_project_folder()[0]
        temp_folder = Path(project_folder)

        if not temp_folder.exists():
            raise FileNotFoundError(f'Project folder {project_folder} does not exist')
        else:
            self.project_folder = temp_folder

        self.get_project_files()

    def get_project_folder(self) -> list[str]:
        file_names = []

        root_directory = Path(self.root_dir)

        if not root_directory.exists():
            print(f"Root path {str(root_directory)} does not exist! Setting root path to default!")
            self.root_dir = ""
        else:
            self.root_dir = str(root_directory)

        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Select Project Directory:")
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setDirectory(self.root_dir)

        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()

        return file_names

    def get_project_files(self):
        self.max_projection_path = None
        self.cell_trace_data_path = None
        self.cell_props_path = None

        self.inscopix_path = self.project_folder.joinpath(*['InscopixProcessing', 'DataAnalysis'])

        if not self.inscopix_path.exists():
            raise FileNotFoundError(f'Data folder {self.inscopix_path} does not exist!')

        max_projection_path = list(self.inscopix_path.glob('*HD*MAX_PROJ*.tiff'))
        cell_trace_data_path = list(self.inscopix_path.glob('*TRACES*.csv'))
        cell_props_path = list(self.inscopix_path.glob('*props*.csv'))

        if len(max_projection_path) == 0:
            raise FileNotFoundError(f'Max Projection image not found!')
        elif len(cell_trace_data_path) == 0:
            raise FileNotFoundError(f'Cell Trace data not found!')
        elif len(cell_props_path) == 0:
            raise FileNotFoundError(f'Cell Props data not found!')
        else:
            self.max_projection_path = max_projection_path[0]
            self.cell_trace_data_path = cell_trace_data_path[0]
            self.cell_props_path = cell_props_path[0]

