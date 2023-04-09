from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar
from pyqtribbon.panel import RibbonPanel
from pyqtribbon.toolbutton import RibbonToolButton


def test_categories(qtbot: QtBot):
    # Central widget
    window = QtWidgets.QMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    categories = ribbonbar.addContextCategories("name", ["Context 1", "Context 2"])
    assert isinstance(categories, dict)
    assert len(categories) == 2
    assert categories["Context 1"].title() == "Context 1"
    assert categories["Context 2"].title() == "Context 2"

    panel1 = categories["Context 1"].addPanel("Context 1 Panel 1")
    button1 = panel1.addLargeButton("Button 1")
    assert isinstance(panel1, RibbonPanel)
    assert panel1.title() == "Context 1 Panel 1"
    assert isinstance(button1, RibbonToolButton)
    assert button1.text() == "Button 1"

    panel2 = categories["Context 2"].addPanel("Context 2 Panel 1")
    button2 = panel2.addLargeButton("Button 2")
    assert isinstance(panel2, RibbonPanel)
    assert panel2.title() == "Context 2 Panel 1"
    assert isinstance(button2, RibbonToolButton)
    assert button2.text() == "Button 2"

    # Show the window
    window.resize(1800, 350)
