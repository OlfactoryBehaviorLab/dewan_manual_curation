from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QImage, QPixmap, QPolygonF, QPen, QBrush
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem


class MaximumProjection(QGraphicsScene):
    def __init__(self, cell_names, cell_contours, max_projection_path):
        super().__init__()

        self.cells = cell_names
        self.cell_contours = cell_contours
        self.image_path = max_projection_path

        self.image = None
        self.pixmap = None
        self.pixmap_item = None

        self.pen = None
        self.brush = None

        self.cell_contours = None
        self.cell_outline_polygons = []
        self.cell_labels = []

        #  References back to polygons for post-draw color changes
        self.cell_outline_references = []
        self.outline_dict = {}

        self._load_maxproj_image()
        self._create_outline_polygons()
        self._create_cell_labels()
        self._create_reference_dict()
        self._draw_cell_outlines()

    def change_outline_color(self, key, new_state: int):
        color = None
        polygon = self.outline_dict[key]

        if new_state == 1:  # Selected
            color = Qt.GlobalColor.green
        elif new_state == 0:  # Not Selected
            color = Qt.GlobalColor.red

        self.pen.setColor(color)  # This might just work?
        #polygon.setPen(new_pen)

        polygon.update()

    def reset_polygon_colors(self):
        for cell in self.cells:
            self.change_outline_color(cell, 0)

    def _load_maxproj_image(self):
        self.image = QImage(self.image_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.addItem(self.pixmap_item)

    def _create_outline_polygons(self):
        for cell in self.cells:  # Iterate through cells
            polygon_verts = []
            cell_coordinates = self.cell_contours[cell][0]  # Get the vertices for a specific cell

            for pair in cell_coordinates:
                _x, _y = pair
                _point = QPoint(_x, _y) * 4
                polygon_verts.append(_point)  # We need a list of QPoints, so generate a QPoint for each pair

            _cell_polygon = QPolygonF(polygon_verts)
            self.cell_outline_polygons.append(_cell_polygon)

    def _create_reference_dict(self):
        self.outline_dict = dict(list(zip(self.name, self.cell_outline_references)))

    def _create_cell_labels(self):
        for cell in self.cells:
            centroid = self.cell_centroids[cell]
            _x, _y = centroid
            _cell_label = str(int(cell.split('C')[1]))  # Little trickery to drop leading zeros

            _label = QGraphicsTextItem(_cell_label)
            _position = QPoint(_x, _y) * 4
            _label.setPos(_position)

            _label.setFont(self.default_font)
            self.cell_labels.append(_label)

    def _draw_cell_outlines(self):
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.NoBrush)
        self.pen = QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap,
                        Qt.PenJoinStyle.RoundJoin)

        for i, polygon in enumerate(self.outline_polygons):
            _polygon_reference = self.scene.addPolygon(polygon, self.pen, self.brush)
            _label = self.cell_labels[i]
            _label.setParentItem(_polygon_reference)
            self.scene.addItem(_label)
            self.cell_outline_references.append(_polygon_reference)
