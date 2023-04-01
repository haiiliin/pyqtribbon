import sys

from qtpy import QtWidgets

from pyqtribbon import RibbonBar, RibbonCategoryStyle


def test_filemenu():
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        # Central widget
        window = QtWidgets.QMainWindow()

        # Ribbon bar
        ribbonbar = RibbonBar()
        window.setMenuBar(ribbonbar)

        # Show the window
        window.resize(1800, 350)
        window.show()
        sys.exit(app.exec_())
