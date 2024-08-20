"""
Name: DewanLab Manual Curation V2
Author: Austin Pauley (Dewan Lab, FSU)
Date: 06/2024
Desc: User interface to enable simultaneous 1-P calcium fluorescence traces (dF/F) along with the
spatial positioning of different cells. This interface is intended to be launched both from,
or independent of, the DewanLab InscopixAnalysis.ipynb processing pipeline notebook.
Version: 2.1
"""

import qdarktheme
import pandas as pd
from PySide6.QtWidgets import QApplication
# Our Libraries
from .gui import ManualCurationUI
from dewan_calcium.helpers.project_folder import ProjectFolder
from ._components.cell_trace import CellTrace
from dewan_calcium.helpers import parse_json


def launch_gui(project_folder_override=None, cell_trace_data_override=None, cell_names_override=None,
               cell_contours_override=None):

    if project_folder_override is None:
        project_folder = ProjectFolder(select_dir=True)
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
                              project_folder.inscopix_dir.max_projection_path)
    window.show()

    return_val = app.exec()

    if return_val == 0:  # 0: Success! | 1: Failure!
        return window.curated_cells
    else:
        return None


def get_data(project_folder, cell_trace_data_override, cell_names_override, cell_contours_override):

    if cell_trace_data_override is None:
        cell_trace_data = []
        pass  # Load cell trace data from pickle
    else:
        cell_trace_data = cell_trace_data_override

    if cell_names_override is None:
        cell_props = pd.read_csv(project_folder.inscopix_dir.props_path, header=0, engine='pyarrow')
        cell_names = cell_props['Name']
    else:
        cell_names = cell_names_override

    if cell_contours_override is None:
        _, cell_contours = DewanJSON.get_outline_coordinates(project_folder.inscopix_dir.contours_path)
    else:
        cell_contours = cell_contours_override

    return cell_trace_data, cell_names, cell_contours


def _preprocess_data(cell_trace_data, cell_props):
    # Drop the first row which contains all 'undecided' labels which is the Inscopix default label.
    cell_trace_data = cell_trace_data.drop([0])
    # Force all dF/F values to be numbers and round times to 2 decimal places
    cell_trace_data = cell_trace_data.apply(pd.to_numeric, errors='coerce')
    # Set the times as the index so the listed data is all dF/F values
    cell_trace_data[cell_trace_data.columns[0]] = cell_trace_data[cell_trace_data.columns[0]].round(2)
    cell_trace_data = cell_trace_data.set_index(cell_trace_data.columns[0])
    # Remove spaces from column names and contents
    cell_trace_data.columns = cell_trace_data.columns.str.replace(" ", "")

    cell_props = cell_props[cell_props['NumComponents'] == 1]  # We only want cells that have one component
    cell_props = cell_props.drop(columns='Status').reset_index(drop=True)
    cell_names = cell_props['Name'].values

    return cell_trace_data, cell_props, cell_names


if __name__ == '__main__':
    launch_gui()
