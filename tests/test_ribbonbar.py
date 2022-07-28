from qtpy import QtWidgets

from ribbon import RibbonBar, mkQApp


def test_ribbonbar():
    if __name__ == '__main__':
        app = mkQApp()
        # Central widget
        window = QtWidgets.QMainWindow()

        # Ribbon bar
        ribbonbar = RibbonBar()
        window.setMenuBar(ribbonbar)

        assert isinstance(window.menuBar(), RibbonBar)

        # Show the window
        window.resize(1800, 350)
        window.show()
