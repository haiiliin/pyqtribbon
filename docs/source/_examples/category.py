import sys

from qtpy import QtGui
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication

from pyqtribbon import RibbonBar, RibbonCategoryStyle
from pyqtribbon.screenshotwindow import RibbonScreenShotWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times New Roman", 8))
    window = RibbonScreenShotWindow("category.png")

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    # Categories
    category1 = ribbonbar.addCategory("Category 1")
    panel1 = category1.addPanel("Panel 1")
    panel1.addLargeButton("Large Button 1", QIcon("python.png"))

    category2 = ribbonbar.addContextCategory("Category 2")
    panel12 = category2.addPanel("Panel 2")
    panel12.addLargeButton("Large Button 2", QIcon("python.png"))

    categories = ribbonbar.addCategoriesBy(
        {
            "Category 6": {
                "style": RibbonCategoryStyle.Normal,
                "panels": {
                    "Panel 1": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "Button 1": {
                                "type": "Button",
                                "arguments": {
                                    "icon": QIcon("python.png"),
                                    "text": "Button",
                                    "tooltip": "This is a tooltip",
                                },
                            },
                        },
                    },
                },
            }
        }
    )
    ribbonbar.setCurrentCategory(categories["Category 6"])

    # Show the window
    window.resize(1000, 250)
    window.show()

    sys.exit(app.exec_())
