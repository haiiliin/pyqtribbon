from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar


def test_filemenu(qtbot: QtBot):
    window = QtWidgets.QMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    fileMenu = ribbonbar.applicationOptionButton().addFileMenu()
    submenu = fileMenu.addMenu("Submenu")
    action1 = submenu.addAction("Action 1")
    assert action1.text() == "Action 1"
    assert action1 in submenu.actions()

    fileMenu.addSeparator()

    action2 = fileMenu.addAction("Action 2")
    assert action2.text() == "Action 2"
    assert action2 in fileMenu.actions()

    # Show the window
    window.resize(1800, 350)
