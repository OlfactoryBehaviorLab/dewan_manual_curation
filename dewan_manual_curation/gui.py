from PySide6.QtWidgets import QDialog


class ManualCurationUI(QDialog):
    def __init__(self):
        super().__init__()
        self.value = []

    def closeEvent(self, e):
        self.reject()

    def reject(self):
        self.value = -10
        self.close()
        return 999

    def accept(self):
        self.value = 10
        self.close()
