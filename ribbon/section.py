from PyQt5 import QtCore, QtWidgets, QtGui


class RibbonDisplayOptionsButton(QtWidgets.QToolButton):
    pass


class RibbonSection(QtWidgets.QFrame):
    #: The signal that is emitted when the display options button is clicked.
    displayOptionsButtonClicked = QtCore.pyqtSignal(bool)
    _displayOptionsButtonHeight = 24

    def __init__(self, parent=None):
        super().__init__(parent)
        # stacked widget
        self._stackedWidget = QtWidgets.QStackedWidget(self)

        # Display options button
        self._displayOptionsLayout = QtWidgets.QVBoxLayout()
        self._displayOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self._displayOptionsLayout.setSpacing(5)
        self._displayOptionsLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
            )
        )
        self._displayOptionsButton = RibbonDisplayOptionsButton()
        self._displayOptionsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self._displayOptionsButton.setIcon(QtGui.QIcon("icons/down.png"))
        self._displayOptionsButton.setIconSize(QtCore.QSize(self._displayOptionsButtonHeight,
                                                            self._displayOptionsButtonHeight))
        self._displayOptionsButton.setText("Ribbon Display Options")
        self._displayOptionsButton.setToolTip("Ribbon Display Options")
        self._displayOptionsButton.setEnabled(True)
        self._displayOptionsButton.setAutoRaise(True)
        self._displayOptionsButton.clicked.connect(self.displayOptionsButtonClicked)
        self._displayOptionsLayout.addWidget(self._displayOptionsButton, 0, QtCore.Qt.AlignBottom)
        self._displayOptionsMenu = QtWidgets.QMenu()

        # layout for the display options button and stacked widget
        self._horizontalLayout = QtWidgets.QHBoxLayout(self)
        self._horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self._horizontalLayout.setSpacing(5)
        self._horizontalLayout.addWidget(self._stackedWidget, 1)
        self._horizontalLayout.addLayout(self._displayOptionsLayout, 0)

    def stackedWidget(self):
        return self._stackedWidget

    def displayOptionsButton(self) -> RibbonDisplayOptionsButton:
        """Return the display options button.

        :return: The display options button.
        """
        return self._displayOptionsButton

    def addDisplayOptionAction(self, action: QtWidgets.QAction):
        """Add a display option to the category.

        :param action: The action of the display option.
        """
        self._displayOptionsMenu.addAction(action)
        self._displayOptionsButton.setMenu(self._displayOptionsMenu if self._displayOptionsMenu.actions() else None)

    def setDisplayOptionsButtonHeight(self, height: int = 24):
        """Set the height of the display options button.

        :param height: The height to set.
        """
        self._displayOptionsButtonHeight = height
        self._displayOptionsButton.setIconSize(QtCore.QSize(height, height))

    def displayOptionsMenu(self) -> QtWidgets.QMenu:
        """Return the display options menu.

        :return: The display options menu."""
        return self._displayOptionsMenu
