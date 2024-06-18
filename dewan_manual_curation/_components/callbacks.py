""" Parent Class for ManualCurationUI to provide callback methods """

from PySide6.QtCore import Qt

CHECKED = Qt.CheckState.Checked
UNCHECKED = Qt.CheckState.Unchecked


class GuiCallbacks:

    def select_none(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(UNCHECKED)

    def select_all(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(CHECKED)

    def export_cells(self):
        for checkbox in self.cell_selection_checkbox_list:
            if checkbox.checkState() is CHECKED:
                self.curated_cells.append(checkbox.text())
        self.accept()

    def view_all(self):
        self.change_view_checkboxes(True)
        for trace in self.trace_pointers:
            trace.setHidden(False)

        self.reset_polygon_colors()

    def view_none(self):
        self.change_view_checkboxes(False)
        for trace in self.trace_pointers:
            trace.setHidden(True)

        self.reset_polygon_colors()

    def on_checkbox_release(self, checkbox):
        cell_key = checkbox.text()
        cell_index = int(cell_key.split('C')[1])  # Drop leading zeros by converting to int
        check_state = checkbox.checkState()

        outline_state = []

        if check_state == CHECKED:
            self.trace_pointers[cell_index].setHidden(False)
            outline_state = 1
        elif check_state == UNCHECKED:
            self.trace_pointers[cell_index].setHidden(True)
            outline_state = 0

        self.change_polygon_color(cell_key, outline_state)