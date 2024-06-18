from PySide6.QtCore import QPoint
from PySide6.QtGui import QImage, QPixmap, QPolygonF
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem


class MaximumProjection(QGraphicsScene):
    def __init__(self, max_projection_path):
        super().__init__()

        self.image_path = max_projection_path

        self.image = None
        self.pixmap = None
        self.pixmap_item = None

        self.cell_contours = None
        self.cell_outline_polygons = []
        self.cell_outline_references = []
        self.cell_labels = []
        self.polygon_dict = {}

        self.scale = 1
        self.direction = 0

        self.load_maxproj_image()

    def load_maxproj_image(self):
        self.image = QImage(self.image_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.addItem(self.pixmap_item)

    def create_outline_polygons(self):
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

        self.cell_outline_polygons = cell_outline_polygons

