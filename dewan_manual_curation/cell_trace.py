import numpy as np
import pandas as pd

import matplotlib as mpl
from PySide6.QtWidgets import QSizePolicy
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_qtagg  import FigureCanvasQTAgg

from sklearn.preprocessing import MinMaxScaler


# Let's set the default font to be Arial Bold 14pt
mpl.rcParams['font.family'] = 'arial'
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['font.size'] = 14


class CellTrace(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=30, height=1.1, dpi=100, figure_min_max=(0, 1), reference_line=False,
                 reference_line_color='r'):
        self.parent = parent
        self.dpi = dpi

        self.figure_min_max = figure_min_max
        self.reference_line = reference_line
        self.reference_line_color = reference_line_color
        self.reference_line_color = reference_line_color
        self.trace_name = 'No_Cell_Present'

        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)

    def __str__(self):
        return f'Manual Curation Trace {{Cell: {self.trace_name}}}'

    def plot_trace(self, trace_data: pd.Series, cell_name):

        self.trace_name = cell_name

        ymin_label = round(trace_data.min(), 4)  # We want the original max/min to display alongside the z-scored data
        ymax_label = round(trace_data.max(), 4)

        data_2_plot = self._scale_data(trace_data, self.figure_min_max)
        x_values = np.arange(len(data_2_plot))  # Quicker than list(range(x))
        self.axes.plot(x_values, data_2_plot, color='k', linewidth=0.5)

        # ==CHANGE APPEARANCE== #

        largest_x = x_values[-1]

        xaxis_offset = largest_x * 0.01

        x_minlim = -xaxis_offset
        x_maxlim = largest_x + xaxis_offset
        self.axes.set_xlim([-xaxis_offset, (x_values[-1] + xaxis_offset)])
        self.axes.set_ylim([0, 1])  # y-values will always be [0, 1]
        y_line_val = np.mean(data_2_plot)
        if self.reference_line:
            self.axes.hlines(y=y_line_val, xmin=x_minlim, xmax=x_maxlim,
                             linestyles=(0, (5, 10)), colors=self.reference_line_color)

        self.axes.tick_params(axis='both', which='both', left=False, bottom=False)
        self.axes.set_xticks([], labels=[])
        self.axes.set_yticks([0, 1], labels=[ymin_label, ymax_label])

        self.axes.get_yaxis().set_label_coords(-0.1, 0.5)  # Align all the things
        self.axes.yaxis.tick_right()

        self.axes.set_ylabel(f'Cell: {self.trace_name}', rotation=0, va='center', ha='center')

        self._set_trace_sizing()  # Reset sizing after plotting

    def _set_trace_sizing(self):
        width, height = self.get_width_height()
        self.setMinimumSize(-1, height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

    @staticmethod
    def _scale_data(trace_data: pd.Series, feature_range: tuple):

        _min, _max = feature_range

        # TODO: I will need to rework this for a pandas Series
        scaler = MinMaxScaler(feature_range=(_min, _max))
        scaled_data = scaler.fit_transform(trace_data.reshape(-1, 1)).ravel()

        return scaled_data

