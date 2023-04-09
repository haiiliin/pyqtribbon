from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar


def test_category(qtbot: QtBot):
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

    # Show the window
    window.resize(1800, 350)
