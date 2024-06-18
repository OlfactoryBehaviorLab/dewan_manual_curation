from PySide6.QtCore import QPoint
from PySide6.QtGui import QImage, QPixmap, QPolygonF
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem


class MaximumProjection(QGraphicsScene):
    def __init__(self, max_projection_path):
        super().__init__()

        self.image_path = max_projection_path

        self.image = None
        self.pixmap = None
        self.pixmap_item = None

        self.cell_contours = None
        self.cell_outline_polygons = []
        self.cell_labels = []

        #  References back to polygons for post-draw color changes
        self.cell_outline_references = []
        self.polygon_dict = {}

        self.scale = 1
        self.direction = 0

        self.load_maxproj_image()
        self.create_outline_polygons()
        self.create_cell_labels()

    def load_maxproj_image(self):
        self.image = QImage(self.image_path)
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.addItem(self.pixmap_item)

    def create_outline_polygons(self):
        for cell in self.cells:  # Iterate through cells
            polygon_verts = []
            cell_coordinates = self.cell_contours[cell][0]  # Get the vertices for a specific cell

            for pair in cell_coordinates:
                _x, _y = pair
                _point = QPoint(_x, _y) * 4
                polygon_verts.append(_point)  # We need a list of QPoints, so generate a QPoint for each pair

            _cell_polygon = QPolygonF(polygon_verts)
            self.cell_outline_polygons.append(_cell_polygon)

    def create_reference_dict(self):
        self.polygon_dict = dict(list(zip(self.name, self.cell_outline_references)))

    def create_cell_labels(self):
        for cell in self.cells:
            centroid = self.cell_centroids[cell]
            _x, _y = centroid
            _cell_label = str(int(cell.split('C')[1]))  # Little trickery to drop leading zeros

            _label = QGraphicsTextItem(_cell_label)
            _position = QPoint(_x, _y) * 4
            _label.setPos(_position)

            _label.setFont(self.default_font)
            self.cell_labels.append(_label)


