import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow

import gui
from project_folder import ProjectFolder
import pandas as pd

def launch_gui():

    app = QApplication([])
    qdarktheme.setup_theme('dark')

    project_folder = ProjectFolder(project_dir='C:/Projects/Test_Data/VGLUT-20')
    cell_props = pd.read_csv(project_folder.cell_props_path, header=0, engine='pyarrow')
    cell_names = cell_props['Name']

    window = gui.ManualCurationUI(project_folder, cell_names)
    window.show()

    result = app.exec()
    print(window.value)

    del window
    del app


if __name__ == '__main__':
    launch_gui()
