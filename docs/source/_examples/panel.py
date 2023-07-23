import sys

from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication, QLabel, QLineEdit, QMenu, QToolButton

from pyqtribbon import RibbonBar
from pyqtribbon.screenshotwindow import RibbonScreenShotWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    window = RibbonScreenShotWindow("panel.png")

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    category1 = ribbonbar.addCategory("Category 1")
    panel = category1.addPanel("Panel 1", showPanelOptionButton=False)
    panel.addSmallButton("Button 1", icon=QIcon("python.png"))
    panel.addSmallButton("Button 2", icon=QIcon("python.png"))
    panel.addSmallButton("Button 3", icon=QIcon("python.png"))
    panel.addMediumToggleButton("Show/Hide Category 2", icon=QIcon("python.png"))
    panel.addVerticalSeparator()
    panel.addMediumToggleButton("Show/Hide Category 3", icon=QIcon("python.png"))
    panel.addMediumToggleButton("Show/Hide Category 4/5", icon=QIcon("python.png"), colSpan=2, alignment=Qt.AlignLeft)
    panel.addLargeButton("Button 4", icon=QIcon("python.png"))
    panel.addVerticalSeparator()
    panel.addMediumButton("Button 5", icon=QIcon("python.png"))
    panel.addMediumButton("Button 6", icon=QIcon("python.png"))

    button = panel.addLargeButton("Button 7", icon=QIcon("python.png"))
    menu = QMenu()
    menu.addAction(QIcon("python.png"), "Action 1")
    menu.addAction(QIcon("python.png"), "Action 2")
    menu.addAction(QIcon("python.png"), "Action 3")
    button.setMenu(menu)
    button.setPopupMode(QToolButton.InstantPopup)
    panel.addWidget(button, rowSpan=6)

    gallery = panel.addGallery(minimumWidth=500, popupHideOnClick=True)
    for i in range(100):
        gallery.addToggleButton(f"item {i+1}", QIcon("python.png"))
    popupMenu = gallery.popupMenu()
    submenu = popupMenu.addMenu(QIcon("python.png"), "Submenu")
    submenu.addAction(QIcon("python.png"), "Action 4")
    popupMenu.addAction(QIcon("python.png"), "Action 1")
    popupMenu.addAction(QIcon("python.png"), "Action 2")
    popupMenu.addSeparator()
    popupMenu.addWidget(QLabel("This is a custom widget"))
    formLayout = popupMenu.addFormLayoutWidget()
    formLayout.addRow(QLabel("Row 1"), QLineEdit())

    # Show the window
    window.resize(1300, 250)
    window.show()

    sys.exit(app.exec_())
