import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from ribbon import RibbonMainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    app.setStyle("Windows")

    app.setStyleSheet(open("styles/default.qss", "r").read())

    window = RibbonMainWindow()
    window.setWindowTitle("Ribbon Test")
    window.setWindowIcon(QtGui.QIcon("icons/python.png"))

    ribbon = window.ribbon

    saveButton = QtWidgets.QToolButton()
    saveButton.setAutoRaise(True)
    saveButton.setText("Button")
    saveButton.setIcon(QtGui.QIcon("icons/save.png"))
    ribbon.addQuickAccessButton(saveButton)

    undoButton = QtWidgets.QToolButton()
    undoButton.setAutoRaise(True)
    undoButton.setText("Button")
    undoButton.setIcon(QtGui.QIcon("icons/undo.png"))
    ribbon.addQuickAccessButton(undoButton)

    redoButton = QtWidgets.QToolButton()
    redoButton.setAutoRaise(True)
    redoButton.setText("Button")
    redoButton.setIcon(QtGui.QIcon("icons/redo.png"))
    ribbon.addQuickAccessButton(redoButton)

    ribbon.addDisplayOptionAction(QtWidgets.QAction("Display Options", window))

    category1 = ribbon.addCategory("Category 1")
    panel = category1.addPanel("Panel 1")
    panel.addSmallButton("Button 1", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 3", icon=QtGui.QIcon("icons/close.png"))
    showCategoryButton2 = panel.addMediumToggleButton("Show/Hide Category 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addVerticalSeparator()
    showCategoryButton3 = panel.addMediumToggleButton("Show/Hide Category 3", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 6", icon=QtGui.QIcon("icons/close.png"))
    panel.addVerticalSeparator()
    panel.addMediumButton("Button 7", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 8", icon=QtGui.QIcon("icons/close.png"))

    saveButton = panel.addLargeButton("Button 8", icon=QtGui.QIcon("icons/close.png"))
    menu = QtWidgets.QMenu()
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 1")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 2")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 3")
    saveButton.setMenu(menu)
    saveButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
    panel.addWidget(saveButton, rowSpan=6)

    saveButton = panel.addLargeButton("Button 9", icon=QtGui.QIcon("icons/close.png"))
    menu = QtWidgets.QMenu()
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 1")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 2")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 3")
    saveButton.setMenu(menu)
    saveButton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
    panel.addWidget(saveButton, rowSpan=6)

    saveButton = panel.addLargeButton("Button 10", icon=QtGui.QIcon("icons/close.png"))
    menu = QtWidgets.QMenu()
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 1")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 2")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 3")
    saveButton.setMenu(menu)
    saveButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
    panel.addWidget(saveButton, rowSpan=6)

    panel = category1.addPanel("Panel 2")
    panel.addMediumButton("Button 8", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 9", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("This is a very very very very very long button",
                         icon=QtGui.QIcon("icons/close.png"), colSpan=3)
    panel.addSmallToggleButton("Button 10", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallToggleButton("Button 11", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallToggleButton("Button 12", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("This is a very very very very very long button",
                         icon=QtGui.QIcon("icons/close.png"), colSpan=3)

    category2 = ribbon.addContextCategory("Category 2")
    panel = category2.addPanel("Panel 1")
    panel.addSmallButton("Button 1", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 3", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 4", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 5", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 6", icon=QtGui.QIcon("icons/close.png"))
    panel.addVerticalSeparator()
    panel.addMediumButton("Button 7", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 8", icon=QtGui.QIcon("icons/close.png"))

    saveButton = panel.addLargeButton("Button 8", icon=QtGui.QIcon("icons/close.png"))
    menu = QtWidgets.QMenu()
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 1")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 2")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 3")
    saveButton.setMenu(menu)
    saveButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
    panel.addWidget(saveButton, rowSpan=6)

    saveButton = panel.addLargeButton("Button 9", icon=QtGui.QIcon("icons/close.png"))
    menu = QtWidgets.QMenu()
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 1")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 2")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 3")
    saveButton.setMenu(menu)
    saveButton.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
    panel.addWidget(saveButton, rowSpan=6)

    saveButton = panel.addLargeButton("Button 10", icon=QtGui.QIcon("icons/close.png"))
    menu = QtWidgets.QMenu()
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 1")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 2")
    menu.addAction(QtGui.QIcon("icons/close.png"), "Action 3")
    saveButton.setMenu(menu)
    saveButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
    panel.addWidget(saveButton, rowSpan=6)

    panel.addCalendarWidget()

    category3 = ribbon.addContextCategory("Category 3")
    panel = category3.addPanel("Panel 1")
    panel.addLargeButton("Button 1", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 3", icon=QtGui.QIcon("icons/close.png"))

    showCategoryButton2.clicked.connect(lambda checked: category2.setCategoryVisible(checked))
    showCategoryButton3.clicked.connect(lambda checked: category3.setCategoryVisible(not category3.categoryVisible()))

    gallery = panel.addGallery()
    for i in range(100):
        gallery.addToggleButton(f'item {i+1}', QtGui.QIcon("icons/close.png"))

    label = QtWidgets.QLabel("Ribbon Test Window")
    label.setFont(QtGui.QFont("Arial", 20))
    label.setAlignment(QtCore.Qt.AlignCenter)
    window.mainLayout.addWidget(label, 1)

    window.resize(1800, 350)
    window.show()
    sys.exit(app.exec_())
