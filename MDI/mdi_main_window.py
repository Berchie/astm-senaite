import sys
from functools import partial

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6.QtGui import QAction
from MDI.UI.MDI_MainWindow import Ui_MDI_MainWindow
from Middleware.astm_senaite_middleware import MiddlewareWindow


class MainWindow(QMainWindow, Ui_MDI_MainWindow):
    sequence_number = 0

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setCentralWidget(self.child_mdi_area)

        self.child_mdi_area.subWindowActivated.connect(self.update_menus)

        self.create_status_bar()
        self.add_subwindows_menuWindow()

        self.new_act.triggered.connect(self.new_middleware)
        self.exit_act.triggered.connect(self.exit_application)
        self.close_window_act.triggered.connect(self.close_subWindow)
        self.close_all_windows_act.triggered.connect(self.close_all_subWindow)
        self.cascade_act.triggered.connect(self.cascade)
        self.tile_act.triggered.connect(self.tile)
        self.about_act.triggered.connect(self.about)

    @Slot()
    def new_middleware(self):
        child = self.create_mdi_child()
        child.show()

    @Slot()
    def exit_application(self):
        self.close()

    @Slot()
    def close_subWindow(self):
        self.child_mdi_area.closeActiveSubWindow()

    @Slot()
    def close_all_subWindow(self):
        self.child_mdi_area.closeAllSubWindows()

    @Slot()
    def cascade(self):
        self.child_mdi_area.cascadeSubWindows()

    @Slot()
    def tile(self):
        self.child_mdi_area.tileSubWindows()

    @Slot()
    def about(self):
        QMessageBox.about(self, "About ASTMtoSENAITE",
                          "The <b>ASTMtoSENAITE</b> is responsible for processing the ASTM message"
                          " from the laboratory and transferring it to the SENAITE LIMS system.")

    def create_mdi_child(self):
        # Analyzer - ASTM Middleware
        MainWindow.sequence_number = MainWindow.sequence_number + 1
        child = MiddlewareWindow()
        child.setWindowTitle(f"Analyzer-ASTM Middleware{str(MainWindow.sequence_number)}")
        self.child_mdi_area.addSubWindow(child)

        return child

    def active_mdi_child(self):
        active_child_window = self.child_mdi_area.activeSubWindow()
        if active_child_window:
            return active_child_window.widget()
        return None

    def set_active_sub_window(self, sub_window):
        if sub_window:
            self.child_mdi_area.setActiveSubWindow(sub_window)

    @Slot()
    def update_menus(self):
        has_mdi_child = (self.active_mdi_child() is not None)
        self.close_window_act.setEnabled(has_mdi_child)
        self.close_all_windows_act.setEnabled(has_mdi_child)
        self.tile_act.setEnabled(has_mdi_child)
        self.cascade_act.setEnabled(has_mdi_child)

        # has_selection = (self.active_mdi_child() is not None
        #                  and self.active_mdi_child().textCursor().hasSelection())
        # self._cut_act.setEnabled(has_selection)
        # self._copy_act.setEnabled(has_selection)

    @Slot()
    def update_window_menu(self):

        self.menuWindow.clear()
        self.menuWindow.addAction(self.close_window_act)
        self.menuWindow.addAction(self.close_all_windows_act)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.cascade_act)
        self.menuWindow.addAction(self.tile_act)
        self.menuWindow.addSeparator()

        windows = self.child_mdi_area.subWindowList()

        for i, subwindow in enumerate(windows):
            child = subwindow.widget()

            f = child.windowTitle()
            text = f'{i + 1} {f}'
            if i < 9:
                text = '&' + text

            action = self.menuWindow.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.active_mdi_child())
            slot_func = partial(self.set_active_sub_window, sub_window=subwindow)
            action.triggered.connect(slot_func)

            # action = self.menuWindow.addAction(text)
            # action.triggered.connect(lambda checked, sw=subwindow: self.set_active_sub_window(sw))
            # self.menuWindow.addAction(action)

    def add_subwindows_menuWindow(self):
        self.update_window_menu()
        self.menuWindow.aboutToShow.connect(self.update_window_menu)

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
