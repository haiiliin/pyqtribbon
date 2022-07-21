import sys

from PyQt5 import QtWidgets, QtGui
from ribbon import RibbonMainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    app.setStyleSheet(open("styles/default.qss", "r").read())

    window = RibbonMainWindow()
    window.setWindowTitle("Microsoft Word")
    window.setWindowIcon(QtGui.QIcon("examples/word.png"))
    window.mainLayout.addWidget(QtWidgets.QTextEdit())
    window.ribbon.setApplicationIcon(QtGui.QIcon("examples/word.png"))
    window.ribbon.applicationButton().setToolTip("Microsoft Word")

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
    fontComboBox = fontPanel.addFontComboBox(rowSpan=3, colSpan=6)
    fontPanel.addSmallToggleButton("Bold", icon=QtGui.QIcon("examples/bold.png"), showText=False, tooltip="Bold")
    fontPanel.addSmallToggleButton("Italic", icon=QtGui.QIcon("examples/italic.png"), showText=False, tooltip="Italic")
    fontPanel.addSmallToggleButton("Underline", icon=QtGui.QIcon("examples/underline.png"), showText=False,
                                   tooltip="Underline")
    fontPanel.addSmallToggleButton("Strikethrough", icon=QtGui.QIcon("examples/strikethrough.png"), showText=False,
                                   tooltip="Strikethrough")
    fontPanel.addSmallToggleButton("Superscript", icon=QtGui.QIcon("examples/superscript.png"), showText=False,
                                   tooltip="Superscript")
    fontPanel.addSmallToggleButton("Subscript", icon=QtGui.QIcon("examples/subscript.png"), showText=False,
                                   tooltip="Subscript")
    fontSizeComboBox = fontPanel.addComboBox(['8', '9', '10'], rowSpan=3, colSpan=2)
    fontPanel.addSmallToggleButton("Increase Font Size", icon=QtGui.QIcon("examples/increase-font.png"),
                                   showText=False, tooltip="Increase Font Size")
    fontPanel.addSmallToggleButton("Decrease Font Size", icon=QtGui.QIcon("examples/decrease-font.png"),
                                   showText=False, tooltip="Decrease Font Size")
    fontPanel.addSmallToggleButton("Decrease Font Size", icon=QtGui.QIcon("examples/decrease-font.png"),
                                   showText=False, tooltip="Decrease Font Size")

    window.resize(1500, 1000)
    window.show()
    sys.exit(app.exec_())
