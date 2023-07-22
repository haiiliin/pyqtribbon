from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar


def test_panel(qtbot: QtBot):
    # Central widget
    window = QtWidgets.QMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    # Add a category
    category = ribbonbar.addCategory("Category 1")
    assert category.title() == "Category 1"
    assert category in ribbonbar.categories().values()

    # Add a panel
    panel = category.addPanel("Panel 1")
    assert panel.title() == "Panel 1"
    assert panel in category.panels().values()

    button1 = panel.addButton("Button 1")
    assert button1.text() == "Button 1"
    assert button1 in panel.widgets()
    button2 = panel.addButton("Button 2")
    assert button2.text() == "Button 2"
    assert button2 in panel.widgets()

    # Show the window
    window.resize(1800, 350)
