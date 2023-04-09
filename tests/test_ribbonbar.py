from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar


def test_ribbonbar(qtbot: QtBot):
    # Central widget
    window = QtWidgets.QMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    assert isinstance(window.menuBar(), RibbonBar)

    # Show the window
    window.resize(1800, 350)
