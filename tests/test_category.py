from qtpy import QtWidgets

from ribbon import RibbonBar, mkQApp

app = mkQApp()


def test_category():
    # Central widget
    window = QtWidgets.QMainWindow()

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    # Add a category
    category = ribbonbar.addCategory("Category 1")
    assert category.title() == "Category 1"
    assert category in ribbonbar.categories().values()

    # Show the window
    window.resize(1800, 350)
    window.show()
