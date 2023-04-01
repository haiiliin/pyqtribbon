import sys

from qtpy import QtGui
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QIcon

from pyqtribbon import RibbonBar, RibbonCategoryStyle
from pyqtribbon.screenshotwindow import RibbonScreenShotWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    window = RibbonScreenShotWindow('category.png')

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    # Categories
    category1 = ribbonbar.addCategory('Category 1')
    panel1 = category1.addPanel('Panel 1')
    panel1.addLargeButton('Large Button 1', QIcon('python.png'))

    category2 = ribbonbar.addContextCategory('Category 2')
    panel12 = category2.addPanel('Panel 2')
    panel12.addLargeButton('Large Button 2', QIcon('python.png'))

    # Show the window
    window.resize(1000, 250)
    window.show()

    sys.exit(app.exec_())
