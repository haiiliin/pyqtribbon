from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar
from pyqtribbon.gallery import RibbonGallery


def test_ribbonbar(qtbot: QtBot):
    # Central widget
    window = QtWidgets.QMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    category = ribbonbar.addCategory("name")
    panel = category.addPanel("Panel 1")

    gallery = panel.addGallery(popupHideOnClick=True)
    for i in range(100):
        gallery.addToggleButton(f"item {i + 1}")
    popupMenu = gallery.popupMenu()
    submenu = popupMenu.addMenu("Submenu")
    submenu.addAction("Action 1")
    popupMenu.addAction("Action 2")
    popupMenu.addSeparator()
    popupMenu.addWidget(QtWidgets.QLabel("This is a custom widget"))
    formLayout = popupMenu.addFormLayoutWidget()
    formLayout.addRow(QtWidgets.QLabel("Row 1"), QtWidgets.QLineEdit("Line Edit"))

    assert isinstance(gallery, RibbonGallery)
    assert gallery.popupMenu() is not None
    assert gallery.popupMenu().actions()[0].text() == "Submenu"
    assert submenu.actions()[0].text() == "Action 1"
    assert gallery.popupMenu().actions()[1].text() == "Action 2"
    assert gallery.popupMenu().actions()[2].isSeparator()
    assert gallery.popupMenu().actions()[3].defaultWidget().text() == "This is a custom widget"
    assert isinstance(formLayout, QtWidgets.QFormLayout)
    assert formLayout.itemAt(0, QtWidgets.QFormLayout.LabelRole).widget().text() == "Row 1"
    assert formLayout.itemAt(0, QtWidgets.QFormLayout.FieldRole).widget().text() == "Line Edit"

    # Show the window
    window.resize(1800, 350)
