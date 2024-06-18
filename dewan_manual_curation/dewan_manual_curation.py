import qdarktheme
from PySide6.QtWidgets import QApplication
from shapely import Polygon
import pandas as pd

from . import gui

from .project_folder import ProjectFolder
from ._comps.cell_trace import CellTrace
from dewan_calcium.helpers import DewanJSON


def launch_gui(cell_trace_data_override=None, cell_names_override=None,
               cell_contours_override=None):

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

    cell_traces = generate_cell_traces(cell_trace_data, cell_names)

    cell_centroids = generate_new_centroids(cell_names, cell_contours)

    app = QApplication.instance()
    if not app:
        app = QApplication([])
    qdarktheme.setup_theme('dark')

    window = gui.ManualCurationUI(project_folder, cell_names, cell_traces, cell_contours,
                                  cell_centroids)
    window.show()

    return_val = app.exec()

    if return_val == 0:  # Success!
        return window.curated_cells


def generate_cell_traces(cell_trace_data, cell_names):
    cell_traces = []
    for cell in cell_names:
        data = cell_trace_data[cell].values
        _cell_trace = CellTrace(reference_line=True)
        _cell_trace.plot_trace(data, cell)
        cell_traces.append(_cell_trace)

    return cell_traces


def generate_new_centroids(cell_names, cell_contours):
    cell_keys = cell_contours.keys()

    centroids = []
    for cell in cell_keys:
        polygon_verts = cell_contours[cell][0]
        polygon = Polygon(polygon_verts)
        new_centroid = (polygon.centroid.x, polygon.centroid.y)
        centroids.append(new_centroid)

    centroids_dict = dict(list(zip(cell_names, centroids)))

    return centroids_dict


if __name__ == '__main__':
    launch_gui()
