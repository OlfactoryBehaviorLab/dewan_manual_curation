""" Parent Class for ManualCurationUI to provide general GUI function """


from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QCheckBox, QListWidgetItem
from functools import partial


class GuiFuncs:
    def populate_selection_list(self):
        for each in self.cells:
            selection_CB = QCheckBox(str(each))
            selection_CB.setCheckState(Qt.CheckState.Checked)
            self.cell_selection_checkbox_list.append(selection_CB)
            self.cell_select_checkbox_layout.addWidget(selection_CB)

    def populate_view_list(self):
        for each in self.cells:
            view_CB = QCheckBox(str(each))
            view_CB.setCheckState(Qt.CheckState.Checked)
            view_CB.released.connect(partial(self.on_checkbox_release, view_CB))
            # Pass a reference of each checkbox to the click callback
            self.cell_view_checkbox_list.append(view_CB)
            self.cell_view_checkbox_layout.addWidget(view_CB)

    def populate_cell_traces(self):
        for each in self.cell_traces:
            each.installEventFilter(self)
            _list_widget = QListWidgetItem()
            _list_widget.setSizeHint(QSize(each.width() / 3, each.height()))
            self.cell_trace_scroll_area.addItem(_list_widget)
            self.cell_trace_scroll_area.setItemWidget(_list_widget, each)

    def configure_maxproj_view(self):
        self.max_projection_view.setInteractive(True)
        self.max_projection_view.setMouseTracking(True)
        self.max_projection_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.max_projection_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.viewport().installEventFilter(self)
