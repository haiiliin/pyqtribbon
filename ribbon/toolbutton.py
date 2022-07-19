import typing
from enum import IntEnum

from PyQt5 import QtWidgets, QtCore


class ButtonStyle(IntEnum):
    Small = 0
    Medium = 1
    Large = 2


class MenuRole(IntEnum):
    """The role of a menu item.

    The role of a menu item is used to determine the action to be performed
    when the menu item is selected.

    The separator role is used to indicate that the menu will only be showed when user click on the arrow.
    """
    Normal = 0
    Separate = 1


class ToolButton(QtWidgets.QToolButton):
    _buttonStyle: ButtonStyle
    _actions: typing.List[QtWidgets.QAction]
    _maxHeight: int

    def __init__(self, parent=None):
        super().__init__(parent)
        self._actions = []
        self._maxHeight = 64

        # Make way for the popup button
        self.setStyleSheet("""ToolButton[popupMode="1"] { padding-right: 20px; }""")

        # Styles
        self.setButtonStyle(ButtonStyle.Large)
        self.setAutoRaise(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Connect signals
        self.triggered.connect(self.setDefaultAction)

    def setMaximumHeight(self, maxh: int) -> None:
        """Set the maximum height of the button.

        :param maxh: The maximum height of the button.
        """
        super().setMaximumHeight(maxh)
        self.setButtonMaximumHeight(int(maxh * 0.7))

    def setButtonMaximumHeight(self, height: int):
        """Set the maximum height of the button.

        :param height: The maximum height of the button.
        """
        self._maxHeight = height
        self.setButtonStyle(self._buttonStyle)

    def setButtonStyle(self, style: ButtonStyle):
        """Set the buttonStyle of the button.

        :param style: The buttonStyle of the button.
        """
        self._buttonStyle = style
        largeHeight = self._maxHeight
        smallHeight, mediumHeight = int(.5 * largeHeight), int(.75 * largeHeight)
        if style == ButtonStyle.Small:
            self.setIconSize(QtCore.QSize(smallHeight, smallHeight))
            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        elif style == ButtonStyle.Medium:
            self.setIconSize(QtCore.QSize(mediumHeight, mediumHeight))
            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        elif style == ButtonStyle.Large:
            self.setIconSize(QtCore.QSize(largeHeight, largeHeight))
            self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

    def setMenu(self, menu: QtWidgets.QMenu):
        """Set the menu of the button.

        :param menu: The menu of the button.
        """
        super().setMenu(menu)
        self.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        if self.menu().actions():
            self.setDefaultAction(self.menu().actions()[0])
