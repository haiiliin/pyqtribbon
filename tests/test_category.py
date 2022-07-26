import sys

from qtpy import QtWidgets

from pyqtribbon import RibbonBar


def test_category():
    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
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
        sys.exit(app.exec_())
