from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QFont, QPixmap, QImage, QWheelEvent, QShowEvent, QPolygonF, QBrush, QColor, QPen
from PySide6.QtWidgets import (QDialog, QPushButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QScrollArea, QSizePolicy,
                               QGraphicsPixmapItem, QGraphicsView, QGraphicsScene, QCheckBox, QWidget, QListView,
                               QListWidgetItem, QListWidget, QAbstractItemView, QGraphicsTextItem)
from typing import TYPE_CHECKING
from .cell_trace import CellTrace

if TYPE_CHECKING:
    from .project_folder import ProjectFolder
SCALE_FACTOR = 0.01


class ManualCurationUI(QDialog):
    def __init__(self, project_folder: 'ProjectFolder', cell_names, cell_traces, cell_contours, cell_centroids):

        super().__init__()
        self.default_font = QFont("Arial", 12)
        self.project_folder = project_folder
        self.cells = cell_names
        self.cell_traces = cell_traces
        self.cell_contours = cell_contours
        self.cell_centroids = cell_centroids

        #  Cell Selection List Components
        self.cell_scroll_area = None
        self.cell_list = None
        self.select_all_button = None
        self.select_none_button = None
        self.export_cells_button = None
        self.cell_selection_checkbox_list = None
        self.cell_view_checkbox_list = None
        # Cell View List Components
        self.cell_view_list = None
        self.cell_view_scroll_area = None
        self.view_all_button = None
        self.view_none_button = None
        # Cell Trace List Components
        self.cell_trace_scroll_area_contents = None
        self.cell_trace_scroll_area = None
        #  Layouts
        self.main_layout = None
        self.top_half_container = None
        self.bottom_half_layout = None
        self.cell_list_layout = None
        self.cell_list_control_layout = None
        self.cell_select_checkbox_layout = None
        self.max_projection_layout = None
        self.max_projection_controls = None
        self.cell_view_checkbox_layout = None
        self.bottom_half_container = None
        self.cell_trace_box_layout = None
        self.cell_trace_contents_layout = None
        self.cell_view_layout = None
        self.cell_view_controls_layout = None
        self.cell_list_control_selection_layout = None
        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None
        #  Max Projection Controls
        self.zoom_in = None
        self.zoom_out = None
        self.zoom_reset = None
        #  Image View Components
        self.max_projection_view = None
        self.scene = None
        self.image = None
        self.pixmap = None
        self.pixmap_item = None
        self.outline_polygons = None
        self.cell_labels = None
        self.scale = 1
        self.direction = 0

        self.trace_pointers = []
        self.polygon_references = []
        self.polygon_dict = {}
        self.value = []

        self.curated_cells = []

        self.initUI()

    #  Function Overloads
    def eventFilter(self, obj, event):
        if type(event) is QWheelEvent:
            if type(obj) is CellTrace:
                self.cell_trace_scroll_area.wheelEvent(event)
                return True
            elif obj is self.max_projection_view.viewport():
                if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    num_degrees = event.angleDelta() / 8
                    steps = int(num_degrees.y() / 15)
                    self.zoom_image(steps)
                    return True
        elif type(event) is QShowEvent and obj is self.max_projection_view.viewport():
            self.max_projection_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            # We don't actually wanna handle this event, just needed to run this with it
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.reset_image_zoom()
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Equal:
                self.zoom_image_in()
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_image_out()

    def resizeEvent(self, event):
        event.accept()
        if self.scale == 1:
            self.max_projection_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.scale = 1

    # ===Class Functions=== #
    def zoom_image(self, steps: int):
        if steps != self.direction:
            self.scale = 1
            self.direction = steps

        self.scale += (SCALE_FACTOR * steps)
        self.max_projection_view.scale(self.scale, self.scale)

    def reset_image_zoom(self):
        self.scale = 1
        self.max_projection_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def zoom_image_in(self):
        self.zoom_image(1)

    def zoom_image_out(self):
        self.zoom_image(-1)

    def get_trace_pointers(self):
        self.trace_pointers = []

        for trace in range(self.cell_trace_scroll_area.count()):
            _trace = self.cell_trace_scroll_area.item(trace)
            self.trace_pointers.append(_trace)

    def change_view_checkboxes(self, checked=False):
        check_state = Qt.CheckState.Unchecked
        if checked:
            check_state = Qt.CheckState.Checked

        for checkbox in self.cell_view_checkbox_list:
            checkbox.setCheckState(check_state)

    # ==Callbacks== #

    def select_none(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(Qt.CheckState.Unchecked)

    def select_all(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(Qt.CheckState.Checked)

    def export_cells(self):
        for checkbox in self.cell_selection_checkbox_list:
            if checkbox.checkState() is Qt.CheckState.Checked:
                self.curated_cells.append(checkbox.text())
        self.accept()

    def view_all(self):
        self.change_view_checkboxes(True)
        for trace in self.trace_pointers:
            trace.setHidden(False)

    def view_none(self):
        self.change_view_checkboxes()
        for trace in self.trace_pointers:
            trace.setHidden(True)

    def on_checkbox_release(self, checkbox):
        cell_key = checkbox.text()
        cell_index = int(cell_key.split('C')[1])  # Drop leading zeros by converting to int
        check_state = checkbox.checkState()

        if check_state == Qt.CheckState.Checked:
            self.trace_pointers[cell_index].setHidden(False)
        elif check_state == Qt.CheckState.Unchecked:
            self.trace_pointers[cell_index].setHidden(True)

        self.change_polygon_color(cell_key, check_state)

    def initUI(self):
        self.init_window_params()

        # ==MAIN LAYOUT== #
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # ==TOP HALF== #
        self.top_half_container = QHBoxLayout()  # Holds the cell list and max projection

        # ==Cell Selection List== #
        self.cell_list_box = QGroupBox("Cells")
        self.cell_list_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.cell_list_box.setMaximumWidth(250)
        self.cell_list_layout = QVBoxLayout()
        self.cell_list_box.setLayout(self.cell_list_layout)

        self.cell_list = QWidget()
        self.cell_select_checkbox_layout = QVBoxLayout(self.cell_list)
        self.populate_selection_list()

        self.cell_scroll_area = QScrollArea()  # Add the scroll area to the layout
        self.cell_scroll_area.setWidget(self.cell_list)
        self.cell_list_layout.addWidget(self.cell_scroll_area)

        # ==Cell Selection List Controls== #
        self.cell_list_control_layout = QVBoxLayout()
        self.cell_list_control_selection_layout = QHBoxLayout()  # Add the two buttons to a layout
        self.select_all_button = QPushButton(u"Select All")
        self.select_all_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.select_all_button.clicked.connect(self.select_all)
        self.select_none_button = QPushButton(u"Select None")
        self.select_none_button.clicked.connect(self.select_none)
        self.select_none_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.export_cells_button = QPushButton(u"Export Cells")
        self.export_cells_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.export_cells_button.clicked.connect(self.export_cells)
        self.cell_list_control_selection_layout.addWidget(self.select_all_button)
        self.cell_list_control_selection_layout.addWidget(self.select_none_button)
        self.cell_list_control_layout.addLayout(self.cell_list_control_selection_layout)
        self.cell_list_control_layout.addWidget(self.export_cells_button)
        self.cell_list_layout.addLayout(self.cell_list_control_layout)

        self.top_half_container.addWidget(self.cell_list_box)  # Cell list to top half

        # ==Maximum Projection View== #
        self.max_projection_box = QGroupBox("Max Projection")  # Create the max projection box
        self.max_projection_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_box.setMinimumSize(300, 300)
        self.max_projection_layout = QHBoxLayout()
        self.max_projection_box.setLayout(self.max_projection_layout)

        self.max_projection_controls = QVBoxLayout()
        self.max_projection_controls.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom_in = QPushButton("+")
        self.zoom_out = QPushButton("-")
        self.zoom_reset = QPushButton("R")
        self.zoom_in.clicked.connect(self.zoom_image_in)
        self.zoom_out.clicked.connect(self.zoom_image_out)
        self.zoom_reset.clicked.connect(self.reset_image_zoom)

        self.max_projection_controls.addWidget(self.zoom_in)
        self.max_projection_controls.addWidget(self.zoom_out)
        self.max_projection_controls.addWidget(self.zoom_reset)
        self.max_projection_layout.addLayout(self.max_projection_controls)

        # ==Max Projection Display== #
        self.scene = QGraphicsScene()
        self.max_projection_view = QGraphicsView()
        self.max_projection_view.setInteractive(True)
        self.max_projection_view.setMouseTracking(True)
        self.max_projection_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.max_projection_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.viewport().installEventFilter(self)

        self.image = QImage(self.project_folder.max_projection_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmap_item)

        self.create_cell_polygons()
        self.create_cell_labels()
        self.draw_cell_outlines()
        self.create_polygon_dict()

        self.max_projection_view.setScene(self.scene)

        self.max_projection_layout.addWidget(self.max_projection_view)

        # Add the list and max projection box to the top half layout
        self.top_half_container.addWidget(self.max_projection_box)
        self.main_layout.addLayout(self.top_half_container)

        # ==BOTTOM HALF== #
        self.bottom_half_container = QHBoxLayout()  # Layout for the bottom half of the GUI

        # ==CELL TRACE REGION== #
        self.cell_trace_box = QGroupBox("Traces")  # Create the cell trace box and add it to the layout
        self.cell_trace_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cell_trace_box.setMinimumHeight(300)

        self.cell_trace_box_layout = QHBoxLayout()
        self.cell_trace_box.setLayout(self.cell_trace_box_layout)

        # ==Cell View List== #
        self.cell_view_layout = QVBoxLayout()

        self.cell_view_list = QWidget()
        self.cell_view_checkbox_layout = QVBoxLayout(self.cell_view_list)
        self.populate_view_list()

        self.cell_view_scroll_area = QScrollArea()
        self.cell_view_scroll_area.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.cell_view_scroll_area.setMinimumWidth(100)
        self.cell_view_scroll_area.setWidget(self.cell_view_list)

        self.cell_view_controls_layout = QHBoxLayout()
        self.view_all_button = QPushButton(u'View All')
        self.view_none_button = QPushButton(u'View None')
        self.view_all_button.clicked.connect(self.view_all)
        self.view_none_button.clicked.connect(self.view_none)
        self.cell_view_controls_layout.addWidget(self.view_all_button)
        self.cell_view_controls_layout.addWidget(self.view_none_button)

        self.cell_view_layout.addWidget(self.cell_view_scroll_area)
        self.cell_view_layout.addLayout(self.cell_view_controls_layout)
        self.cell_trace_box_layout.addLayout(self.cell_view_layout)

        # ==Cell Trace View== #
        # TODO: reduce scroll bar step size
        self.cell_trace_scroll_area = QListWidget()
        self.cell_trace_box_layout.addWidget(self.cell_trace_scroll_area)
        self.cell_trace_scroll_area.setSizeAdjustPolicy(QListWidget.SizeAdjustPolicy.AdjustToContents)
        self.cell_trace_scroll_area.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                                  QSizePolicy.Policy.MinimumExpanding)
        self.cell_trace_scroll_area.setSpacing(2)
        self.cell_trace_scroll_area.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.populate_cell_traces()
        self.get_trace_pointers()

        self.main_layout.addLayout(self.bottom_half_container)
        self.bottom_half_container.addWidget(self.cell_trace_box)

    def populate_selection_list(self):
        self.cell_selection_checkbox_list = []

        for each in self.cells:
            selection_CB = QCheckBox(str(each))
            selection_CB.setCheckState(Qt.CheckState.Checked)
            self.cell_selection_checkbox_list.append(selection_CB)
            self.cell_select_checkbox_layout.addWidget(selection_CB)

    def populate_view_list(self):
        from functools import partial
        self.cell_view_checkbox_list = []

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

    def draw_cell_outlines(self):
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.NoBrush)
        pen = QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap,
                   Qt.PenJoinStyle.RoundJoin)

        polygon_references = []

        for i, polygon in enumerate(self.outline_polygons):
            _polygon_reference = self.scene.addPolygon(polygon, pen, brush)
            _label = self.cell_labels[i]
            _label.setParentItem(_polygon_reference)
            self.scene.addItem(_label)
            polygon_references.append(_polygon_reference)

        self.polygon_references = polygon_references

    def create_polygon_dict(self):
        pairs = list(zip(self.cells, self.polygon_references))
        self.polygon_dict = dict(pairs)

    def change_polygon_color(self, key, new_state):

        color = []

        polygon = self.polygon_dict[key]

        if new_state is Qt.CheckState.Checked:
            color = Qt.GlobalColor.green
        elif new_state is Qt.CheckState.Unchecked:
            color = Qt.GlobalColor.red

        new_pen = QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap,
                       Qt.PenJoinStyle.RoundJoin)

        polygon.setPen(new_pen)
        polygon.update()

    def create_cell_polygons(self):
        cell_outline_polygons = []
        for cell in self.cells:  # Iterate through cells
            polygon_verts = []
            cell_coordinates = self.cell_contours[cell][0]  # Get the vertices for a specific cell
            for pair in cell_coordinates:
                _x, _y = pair
                _point = QPoint(_x, _y) * 4
                polygon_verts.append(_point)  # We need a list of QPoints, so generate a QPoint for each pair

            _cell_polygon = QPolygonF(polygon_verts)
            cell_outline_polygons.append(_cell_polygon)

        self.outline_polygons = cell_outline_polygons

    def create_cell_labels(self):
        cell_labels = []

        for cell in self.cells:
            centroid = self.cell_centroids[cell]
            _x, _y = centroid
            _cell_label = str(int(cell.split('C')[1]))  # Little trickery to drop leading zeros

            _label = QGraphicsTextItem(_cell_label)
            _position = QPoint(_x, _y) * 4
            _label.setPos(_position)

            _label.setFont(self.default_font)
            cell_labels.append(_label)

        self.cell_labels = cell_labels

    def init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.activateWindow()

    def closeEvent(self, e):
        self.reject()

    def reject(self):
        self.curated_cells = []
        super().reject()
