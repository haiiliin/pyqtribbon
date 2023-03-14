import sys

from qtpy import QtWidgets, QtGui
from qtpy.QtGui import QIcon
from pyqtribbon import RibbonBar

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))

    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Microsoft Word")
    window.setWindowIcon(QIcon("word.png"))
    centralWidget = QtWidgets.QWidget()
    window.setCentralWidget(centralWidget)
    layout = QtWidgets.QVBoxLayout(centralWidget)
    ribbonbar = RibbonBar()
    ribbonbar.setRibbonHeight(160)
    window.setMenuBar(ribbonbar)

    layout.addWidget(QtWidgets.QTextEdit(), 1)
    ribbonbar.setApplicationIcon(QIcon("word.png"))
    ribbonbar.applicationOptionButton().setToolTip("Microsoft Word")

    # Home category
    homeCategory = ribbonbar.addCategory("Home")
    undoPanel = homeCategory.addPanel("Undo")
    undoPanel.addMediumButton("Undo", icon=QIcon("undo.png"))
    undoPanel.addMediumButton("Redo", icon=QIcon("redo.png"))

    clipboardPanel = homeCategory.addPanel("Clipboard")
    pasteButton = clipboardPanel.addLargeButton("Paste", icon=QIcon("paste.png"), tooltip="Paste")
    pasteButton.addAction(QtWidgets.QAction(QIcon('paste-special.png'), "Paste Special"))
    pasteButton.addAction(QtWidgets.QAction(QIcon('paste-as-text.png'), "Paste as Text"))
    clipboardPanel.addSmallButton("Cut", icon=QIcon("cut.png"), showText=False, tooltip="Cut")
    clipboardPanel.addSmallButton("Copy", icon=QIcon("copy.png"), showText=False, tooltip="Copy")
    clipboardPanel.addSmallButton("Painter", icon=QIcon("painter.png"), showText=False, tooltip="Format Painter")

    fontPanel = homeCategory.addPanel("Font")
    fontComboBox = fontPanel.addFontComboBox(rowSpan=3, colSpan=6)
    fontPanel.addSmallToggleButton("Bold", icon=QIcon("bold.png"), showText=False, tooltip="Bold")
    fontPanel.addSmallToggleButton("Italic", icon=QIcon("italic.png"), showText=False, tooltip="Italic")
    fontPanel.addSmallToggleButton("Underline", icon=QIcon("underline.png"), showText=False, tooltip="Underline")
    fontPanel.addSmallToggleButton("Strikethrough", icon=QIcon("strikethrough.png"), showText=False,
                                   tooltip="Strikethrough")
    fontPanel.addSmallToggleButton("Superscript", icon=QIcon("superscript.png"), showText=False, tooltip="Superscript")
    fontPanel.addSmallToggleButton("Subscript", icon=QIcon("subscript.png"), showText=False, tooltip="Subscript")
    fontSizeComboBox = fontPanel.addComboBox(['8', '9', '10'], rowSpan=3, colSpan=2)
    fontPanel.addSmallToggleButton("Increase Font Size", icon=QIcon("increase-font.png"),
                                   showText=False, tooltip="Increase Font Size")
    fontPanel.addSmallToggleButton("Decrease Font Size", icon=QIcon("decrease-font.png"),
                                   showText=False, tooltip="Decrease Font Size")
    fontPanel.addSmallToggleButton("Decrease Font Size", icon=QIcon("decrease-font.png"),
                                   showText=False, tooltip="Decrease Font Size")

    window.resize(1500, 1000)
    window.show()
    sys.exit(app.exec_())
