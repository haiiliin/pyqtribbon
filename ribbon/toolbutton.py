import typing
from enum import IntEnum

from qtpy import QtWidgets, QtCore

from .menu import RibbonMenu


class RibbonButtonStyle(IntEnum):
    """Button style, Small, Medium, or Large."""
    Small = 0
    Medium = 1
    Large = 2


class RibbonToolButton(QtWidgets.QToolButton):
    """Tool button that is showed in the ribbon."""
    _buttonStyle: RibbonButtonStyle

    _largeButtonIconSize = 64
    _mediumButtonIconSize = 48
    _smallButtonIconSize = 32

    def __init__(self, parent=None):
        """Create a new ribbon tool button.

        :param parent: The parent widget.
        """
        super().__init__(parent)

        # Styles
        self.setButtonStyle(RibbonButtonStyle.Large)
        self.setAutoRaise(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def setButtonStyle(self, style: RibbonButtonStyle):
        """Set the button style of the button.

        :param style: The button style of the button.
        """
        self._buttonStyle = style
        if style == RibbonButtonStyle.Small:
            height = self._smallButtonIconSize
            self.setIconSize(QtCore.QSize(height, height))
            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        elif style == RibbonButtonStyle.Medium:
            height = self._mediumButtonIconSize
            self.setIconSize(QtCore.QSize(height, height))
            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        elif style == RibbonButtonStyle.Large:
            height = self._largeButtonIconSize
            self.setIconSize(QtCore.QSize(height, height))
            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

    def addRibbonMenu(self) -> RibbonMenu:
        """Add a ribbon menu for the button.

        :return: The added ribbon menu.
        """
        menu = RibbonMenu()
        self.setMenu(menu)
        return menu
