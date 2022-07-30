import sys

from qtpy.QtWidgets import QApplication, QToolButton

from ribbon import RibbonBar
from ribbon.screenshotwindow import RibbonScreenShotWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RibbonScreenShotWindow('ribbonbar-customize.png')

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    # Title of the ribbon
    ribbonbar.setTitle('This is my custom title')
    
    # Quick Access Bar
    qbutton = QToolButton()
    qbutton.setText('Quick Button')
    ribbonbar.addQuickAccessButton(qbutton)
    
    # Right toolbar
    rbutton = QToolButton()
    rbutton.setText('Right Button')
    ribbonbar.addRightToolButton(rbutton)

    # Show the window
    window.resize(1000, 250)
    window.show()

    sys.exit(app.exec_())
