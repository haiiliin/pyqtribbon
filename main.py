import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from ribbon import Ribbon


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    app.setStyle("Windows")

    app.setStyleSheet(open("styles/Default.qss", "r").read())

    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Ribbon Test")
    window.setWindowIcon(QtGui.QIcon("icons/python.png"))
    window.setCentralWidget(QtWidgets.QWidget())
    layout = QtWidgets.QVBoxLayout(window.centralWidget())

    ribbon = Ribbon()

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

    category = ribbon.addCategory("Category 1")
    panel = category.addPanel("Panel 1")
    panel.addSmallButton("Button 1", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 3", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 4", icon=QtGui.QIcon("icons/close.png"))
    panel.addSeparator()
    panel.addMediumButton("Button 5", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 6", icon=QtGui.QIcon("icons/close.png"))
    panel.addSeparator()
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

    panel = category.addPanel("Panel 2")
    panel.addMediumButton("Button 8", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 9", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("This is a very very very very very long button",
                         icon=QtGui.QIcon("icons/close.png"), colSpan=3)
    panel.addSmallToggleButton("Button 10", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallToggleButton("Button 11", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallToggleButton("Button 12", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("This is a very very very very very long button",
                         icon=QtGui.QIcon("icons/close.png"), colSpan=3)

    category = ribbon.addCategory("Category 2")
    panel = category.addPanel("Panel 1")
    panel.addSmallButton("Button 1", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addSmallButton("Button 3", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 4", icon=QtGui.QIcon("icons/close.png"))
    panel.addMediumButton("Button 5", icon=QtGui.QIcon("icons/close.png"))
    panel.addCalendarWidget()

    category = ribbon.addCategory("Category 3")
    panel = category.addPanel("Panel 1")
    panel.addLargeButton("Button 1", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 2", icon=QtGui.QIcon("icons/close.png"))
    panel.addLargeButton("Button 3", icon=QtGui.QIcon("icons/close.png"))

    layout.addWidget(ribbon, 0)

    label = QtWidgets.QLabel("Ribbon Test Window")
    label.setFont(QtGui.QFont("Arial", 20))
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label, 1)

    window.resize(1800, 350)
    window.show()
    sys.exit(app.exec_())
