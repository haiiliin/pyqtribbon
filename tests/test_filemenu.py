from qtpy import QtWidgets

from ribbon import RibbonBar, mkQApp

app = mkQApp()


def test_filemenu():
    # Central widget
    window = QtWidgets.QMainWindow()

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
    window.show()
