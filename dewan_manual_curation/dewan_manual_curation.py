import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow

import gui
from project_folder import ProjectFolder


def launch_gui():

    app = QApplication([])
    qdarktheme.setup_theme('dark')

    project_folder = ProjectFolder('/mnt/dev/Test_Data', '/mnt/dev/Test_Data/Odor/VGLUT-20')

    window = gui.ManualCurationUI()
    window.show()

    result = app.exec()
    print(window.value)

    del window
    del app


if __name__ == '__main__':
    launch_gui()
