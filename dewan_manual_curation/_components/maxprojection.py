from PySide6.QtWidgets import QGraphicsScene


class MaximumProjection(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.image = None
        self.pixmap = None
        self.pixmap_item = None
        self.cell_outline_polygons = None
        self.cell_outline_references = None
        self.cell_labels = None

