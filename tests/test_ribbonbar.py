import sys

from qtpy import QtWidgets

from pyqtribbon import RibbonBar


def test_ribbonbar():
    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        # Central widget
        window = QtWidgets.QMainWindow()

        # Ribbon bar
        ribbonbar = RibbonBar()
        window.setMenuBar(ribbonbar)

        assert isinstance(window.menuBar(), RibbonBar)

        # Show the window
        window.resize(1800, 350)
        window.show()
        sys.exit(app.exec_())
