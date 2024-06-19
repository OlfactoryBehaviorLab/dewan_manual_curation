"""
Name: DewanLab Manual Curation V2
Author: Austin Pauley (Dewan Lab, FSU)
Date: 06/2024
Desc: User interface to enable simultaneous 1-P calcium fluorescence traces (dF/F) along with the
spatial positioning of different cells. This interface is intended to be launched both from,
or independent of, the DewanLab InscopixAnalysis.ipynb processing pipeline notebook.
"""

import qdarktheme
from PySide6.QtWidgets import QApplication
from shapely import Polygon
import pandas as pd

from . import gui

from .project_folder import ProjectFolder
from ._components.cell_trace import CellTrace
from dewan_calcium.helpers import DewanJSON


def launch_gui(cell_trace_data_override=None, cell_names_override=None,
               cell_contours_override=None):

    cell_traces = []
    cell_props = []
    cell_names = []
    cell_contours = []


    project_folder = ProjectFolder(project_dir='C:/Projects/Test_Data/VGLUT-20')

    if cell_trace_data_override is None:
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

    #cell_traces = generate_cell_traces(cell_trace_data, cell_names)


    app = QApplication.instance()
    if not app:
        app = QApplication([])
    qdarktheme.setup_theme('dark')

    window = gui.ManualCurationUI(cell_names, cell_traces, cell_contours,
                                  project_folder.max_projection_path)
    window.show()

    return_val = app.exec()

    if return_val == 0:  # Success!
        return window.curated_cells


if __name__ == '__main__':
    launch_gui()
