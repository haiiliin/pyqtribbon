import sys

from qtpy import QtGui, QtWidgets
from qtpy.QtGui import QIcon

from pyqtribbon import RibbonBar, RowWise

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
    window.setMenuBar(ribbonbar)

    layout.addWidget(QtWidgets.QTextEdit(), 1)
    ribbonbar.setApplicationIcon(QIcon("word.png"))
    ribbonbar.applicationOptionButton().setToolTip("Microsoft Word")

    undoButton = QtWidgets.QToolButton()
    undoButton.setAutoRaise(True)
    undoButton.setText("Button")
    undoButton.setIcon(QIcon("undo.png"))
    undoButton.setToolTip("Undo")
    ribbonbar.addQuickAccessButton(undoButton)

    redoButton = QtWidgets.QToolButton()
    redoButton.setAutoRaise(True)
    redoButton.setText("Button")
    redoButton.setIcon(QIcon("redo.png"))
    redoButton.setToolTip("Redo")
    ribbonbar.addQuickAccessButton(redoButton)

    # Home category
    homeCategory = ribbonbar.addCategory("Home")

    clipboardPanel = homeCategory.addPanel("Clipboard")
    pasteButton = clipboardPanel.addLargeButton("Paste", icon=QIcon("paste.png"), tooltip="Paste")
    pasteButton.addAction(QtWidgets.QAction(QIcon("paste-special.png"), "Paste Special"))
    pasteButton.addAction(QtWidgets.QAction(QIcon("paste-as-text.png"), "Paste as Text"))
    clipboardPanel.addSmallButton("Cut", icon=QIcon("cut.png"), showText=False, tooltip="Cut")
    clipboardPanel.addSmallButton("Copy", icon=QIcon("copy.png"), showText=False, tooltip="Copy")
    clipboardPanel.addSmallButton("Painter", icon=QIcon("painter.png"), showText=False, tooltip="Format Painter")

    fontPanel = homeCategory.addPanel("Font")
    fontComboBox = fontPanel.addSmallFontComboBox(colSpan=5, fixedHeight=True)
    fontPanel.addSmallToggleButton("Bold", icon=QIcon("bold.png"), showText=False, tooltip="Bold")
    fontPanel.addSmallToggleButton("Italic", icon=QIcon("italic.png"), showText=False, tooltip="Italic")
    fontPanel.addSmallToggleButton("Underline", icon=QIcon("underline.png"), showText=False, tooltip="Underline")
    fontPanel.addSmallToggleButton(
        "Strikethrough", icon=QIcon("strikethrough.png"), showText=False, tooltip="Strikethrough"
    )
    fontPanel.addSmallToggleButton("Superscript", icon=QIcon("superscript.png"), showText=False, tooltip="Superscript")
    fontPanel.addSmallToggleButton("Subscript", icon=QIcon("subscript.png"), showText=False, tooltip="Subscript")
    fontPanel.addSmallToggleButton(
        "Increase Font Size", icon=QIcon("increase-font.png"), showText=False, tooltip="Increase Font Size"
    )
    fontPanel.addSmallToggleButton(
        "Decrease Font Size", icon=QIcon("decrease-font.png"), showText=False, tooltip="Decrease Font Size"
    )
    fontPanel.addSmallToggleButton(
        "Decrease Font Size", icon=QIcon("decrease-font.png"), showText=False, tooltip="Decrease Font Size"
    )
    fontSizeComboBox = fontPanel.addSmallComboBox(["8", "9", "10"], fixedHeight=True, mode=RowWise)

    window.resize(1500, 1000)
    window.show()
    sys.exit(app.exec_())
