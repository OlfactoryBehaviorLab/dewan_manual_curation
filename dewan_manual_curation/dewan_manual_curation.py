"""
Name: DewanLab Manual Curation V2
Author: Austin Pauley (Dewan Lab, FSU)
Date: 06/2024
Desc: User interface to enable simultaneous 1-P calcium fluorescence traces (dF/F) along with the
spatial positioning of different cells. This interface is intended to be launched both from,
or independent of, the DewanLab InscopixAnalysis.ipynb processing pipeline notebook.
Version: 2.0
"""

import qdarktheme
import pandas as pd
from PySide6.QtWidgets import QApplication
# Our Libraries
from .gui import ManualCurationUI
from .project_folder import ProjectFolder
from ._components.cell_trace import CellTrace
from dewan_calcium.helpers import DewanJSON


def launch_gui(project_folder_override=None, cell_trace_data_override=None, cell_names_override=None,
               cell_contours_override=None):

    cell_trace_data = []

    if project_folder_override is None:
        project_folder = ProjectFolder(project_dir='C:/Projects/Test_Data/VGLUT-20')
    else:
        project_folder = project_folder_override

    cell_trace_data, cell_names, cell_contours = get_data(project_folder, cell_trace_data_override,
                                                          cell_names_override, cell_contours_override)

    cell_traces = CellTrace.generate_cell_traces(cell_trace_data, cell_names)

    app = QApplication.instance()

    if not app:
        app = QApplication([])

    qdarktheme.setup_theme('dark')

    window = ManualCurationUI(cell_names, cell_traces, cell_contours,
                              project_folder.max_projection_path)
    window.show()

    return_val = app.exec()

    if return_val == 0:  # 0: Success! | 1: Failure!
        return window.curated_cells


def get_data(project_folder, cell_trace_data_override, cell_names_override, cell_contours_override):

    if cell_trace_data_override is None:
        cell_trace_data = []
        pass  # Load cell trace data from pickle
    else:
        cell_trace_data = cell_trace_data_override

    if cell_names_override is None:
        cell_props = pd.read_csv(project_folder.cell_props_path, header=0, engine='pyarrow')
        cell_names = cell_props['Name']
    else:
        cell_names = cell_names_override

    if cell_contours_override is None:
        _, cell_contours = DewanJSON.get_outline_coordinates(project_folder.cell_contours_path)
    else:
        cell_contours = cell_contours_override

    return cell_trace_data, cell_names, cell_contours


if __name__ == '__main__':
    launch_gui()
