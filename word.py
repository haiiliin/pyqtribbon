import sys

from PyQt5 import QtWidgets, QtGui
from ribbon import RibbonMainWindow, SpaceFindMode

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    app.setStyleSheet(open("styles/default.qss", "r").read())

    window = RibbonMainWindow()
    window.setWindowTitle("Microsoft Word")
    window.setWindowIcon(QtGui.QIcon("examples/word.png"))
    window.mainLayout.addWidget(QtWidgets.QTextEdit())
    window.ribbon.setApplicationIcon(QtGui.QIcon("examples/word.png"))
    window.ribbon.applicationOptionButton().setToolTip("Microsoft Word")

    # Home category
    homeCategory = window.ribbon.addCategory("Home")
    undoPanel = homeCategory.addPanel("Undo")
    undoPanel.addMediumButton("Undo", icon=QtGui.QIcon("examples/undo.png"))
    undoPanel.addMediumButton("Redo", icon=QtGui.QIcon("examples/redo.png"))

    clipboardPanel = homeCategory.addPanel("Clipboard")
    pasteButton = clipboardPanel.addLargeButton("Paste", icon=QtGui.QIcon("examples/paste.png"), tooltip="Paste")
    pasteButton.addAction(QtWidgets.QAction(QtGui.QIcon('examples/paste-special.png'), "Paste Special"))
    pasteButton.addAction(QtWidgets.QAction(QtGui.QIcon('examples/paste-as-text.png'), "Paste as Text"))
    clipboardPanel.addSmallButton("Cut", icon=QtGui.QIcon("examples/cut.png"), showText=False, tooltip="Cut")
    clipboardPanel.addSmallButton("Copy", icon=QtGui.QIcon("examples/copy.png"), showText=False, tooltip="Copy")
    clipboardPanel.addSmallButton("Painter", icon=QtGui.QIcon("examples/painter.png"), showText=False,
                                  tooltip="Format Painter")

    fontPanel = homeCategory.addPanel("Font")
    fontComboBox = fontPanel.addFontComboBox(rowSpan=3, colSpan=4)
    fontComboBox.setMinimumHeight(60)
    fontPanel.addMediumToggleButton("Bold", icon=QtGui.QIcon("examples/bold.png"), showText=False, tooltip="Bold")
    fontPanel.addMediumToggleButton("Italic", icon=QtGui.QIcon("examples/italic.png"), showText=False, tooltip="Italic")
    fontPanel.addMediumToggleButton("Underline", icon=QtGui.QIcon("examples/underline.png"), showText=False,
                                    tooltip="Underline")
    fontPanel.addMediumToggleButton("Strikethrough", icon=QtGui.QIcon("examples/strikethrough.png"), showText=False,
                                    tooltip="Strikethrough")
    fontSizeComboBox = fontPanel.addComboBox(['8', '9', '10'], rowSpan=3, colSpan=2)
    fontSizeComboBox.setMinimumHeight(60)
    fontSizeComboBox.setMinimumWidth(100)
    fontPanel.addMediumToggleButton("Superscript", icon=QtGui.QIcon("examples/superscript.png"), showText=False,
                                    tooltip="Superscript")
    fontPanel.addMediumToggleButton("Subscript", icon=QtGui.QIcon("examples/subscript.png"), showText=False,
                                    tooltip="Subscript")
    fontPanel.addMediumToggleButton("Increase Font Size", icon=QtGui.QIcon("examples/increase-font.png"),
                              showText=False, tooltip="Increase Font Size")
    fontPanel.addMediumButton("Decrease Font Size", icon=QtGui.QIcon("examples/decrease-font.png"),
                              showText=False, tooltip="Decrease Font Size", mode=SpaceFindMode.RowWise)
    fontPanel.addMediumButton("Decrease Font Size", icon=QtGui.QIcon("examples/decrease-font.png"),
                              showText=False, tooltip="Decrease Font Size", mode=SpaceFindMode.ColumnWise)

    window.resize(1500, 1000)
    window.show()
    sys.exit(app.exec_())
