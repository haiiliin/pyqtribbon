from pytestqt.qtbot import QtBot
from qtpy import QtWidgets

from pyqtribbon import RibbonBar, RibbonCategoryStyle


def test_filemenu(qtbot: QtBot):
    # Central widget
    window = QtWidgets.QMainWindow()
    window.show()
    qtbot.addWidget(window)

    # Ribbon bar
    ribbonbar = RibbonBar()
    window.setMenuBar(ribbonbar)

    categories1 = ribbonbar.addCategoriesBy(
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
                                    "text": "Button",
                                    "tooltip": "This is a tooltip",
                                },
                            },
                            "Button 2": {
                                "type": "Button",
                                "arguments": {
                                    "text": "Button 2",
                                    "tooltip": "This is a tooltip",
                                },
                            },
                        },
                    },
                    "Panel 2": {
                        "showPanelOptionButton": False,
                        "widgets": {
                            "Button 3": {
                                "type": "Button",
                                "arguments": {
                                    "text": "Button 3",
                                    "tooltip": "This is a tooltip",
                                },
                            },
                            "Button 4": {
                                "type": "Button",
                                "arguments": {
                                    "text": "Button 4",
                                    "tooltip": "This is a tooltip",
                                },
                            },
                        },
                    },
                },
            }
        }
    )

    assert categories1["Category 6"].title() == "Category 6"
    assert categories1["Category 6"].categoryStyle() == RibbonCategoryStyle.Normal
    assert categories1["Category 6"].panels()["Panel 1"].title() == "Panel 1"
    assert categories1["Category 6"].panels()["Panel 1"]._showPanelOptionButton
    assert categories1["Category 6"].panels()["Panel 1"].widgets()[0].text() == "Button"
    assert categories1["Category 6"].panels()["Panel 1"].widgets()[0].toolTip() == "This is a tooltip"
    assert categories1["Category 6"].panels()["Panel 1"].widgets()[1].text() == "Button 2"
    assert categories1["Category 6"].panels()["Panel 1"].widgets()[1].toolTip() == "This is a tooltip"
    assert categories1["Category 6"].panels()["Panel 2"].title() == "Panel 2"
    assert not categories1["Category 6"].panels()["Panel 2"]._showPanelOptionButton
    assert categories1["Category 6"].panels()["Panel 2"].widgets()[0].text() == "Button 3"
    assert categories1["Category 6"].panels()["Panel 2"].widgets()[0].toolTip() == "This is a tooltip"
    assert categories1["Category 6"].panels()["Panel 2"].widgets()[1].text() == "Button 4"
    assert categories1["Category 6"].panels()["Panel 2"].widgets()[1].toolTip() == "This is a tooltip"

    # Show the window
    window.resize(1800, 350)
