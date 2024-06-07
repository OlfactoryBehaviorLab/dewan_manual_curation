import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow

from gui import ManualCurationUI


def launch_gui():

    app = QApplication([])
    qdarktheme.setup_theme('dark')

    window = ManualCurationUI()
    window.show()

    result = app.exec()
    print(window.value)

    del window
    del app


if __name__ == '__main__':
    launch_gui()
