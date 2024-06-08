import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow

import gui


def launch_gui():

    app = QApplication([])
    qdarktheme.setup_theme('dark')

    project_folder = gui.ProjectFolder('/mnt/dev/')

    window = gui.ManualCurationUI()
    window.show()

    result = app.exec()
    print(window.value)

    del window
    del app


if __name__ == '__main__':
    launch_gui()
