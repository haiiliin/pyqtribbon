from PyQt5 import QtWidgets, QtCore, QtGui


class RibbonCategoryLayoutButton(QtWidgets.QToolButton):
    pass


class RibbonDisplayOptionsButton(QtWidgets.QToolButton):
    pass


class RibbonCategoryLayoutWidget(QtWidgets.QFrame):
    displayOptionsButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 0, 5, 0)
        self._mainLayout.setSpacing(5)

        self._categoryScrollArea = QtWidgets.QScrollArea()
        self._categoryScrollArea.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self._categoryScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._categoryScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._categoryLayout = QtWidgets.QHBoxLayout(self._categoryScrollArea)
        self._categoryLayout.setContentsMargins(0, 0, 0, 0)
        self._categoryLayout.setSpacing(5)
        self._categoryLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self._previousButton = RibbonCategoryLayoutButton(self)
        self._previousButton.setIcon(QtGui.QIcon("icons/backward.png"))
        self._previousButton.setIconSize(QtCore.QSize(24, 24))
        self._previousButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._previousButton.setAutoRaise(True)
        self._nextButton = RibbonCategoryLayoutButton(self)
        self._nextButton.setIcon(QtGui.QIcon("icons/forward.png"))
        self._nextButton.setIconSize(QtCore.QSize(24, 24))
        self._nextButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._nextButton.setAutoRaise(True)

        self._mainLayout.addWidget(self._previousButton, 0, QtCore.Qt.AlignVCenter)
        self._mainLayout.addWidget(self._categoryScrollArea, 0)
        self._mainLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,
                                                             QtWidgets.QSizePolicy.Minimum))
        self._mainLayout.setStretch(2, 1)
        self._mainLayout.addWidget(self._nextButton, 0, QtCore.Qt.AlignVCenter)

        # self.hideScrollPreviousButton()
        # self.hideScrollNextButton()
        self._nextButton.clicked.connect(self.scrollNext)
        self._previousButton.clicked.connect(self.scrollPrevious)

    def showScrollPreviousButton(self):
        """Show the previous button."""
        self._previousButton.show()

    def hideScrollPreviousButton(self):
        """Hide the previous button."""
        self._previousButton.hide()

    def showScrollNextButton(self):
        """Show the next button."""
        self._nextButton.show()

    def hideScrollNextButton(self):
        """Hide the next button."""
        self._nextButton.hide()

    def scrollPrevious(self):
        """Scroll the category to the previous widget."""
        self._categoryScrollArea.horizontalScrollBar().setValue(
            self._categoryScrollArea.horizontalScrollBar().value() + 50
        )

    def scrollNext(self):
        """Scroll the category to the next widget."""
        self._categoryScrollArea.horizontalScrollBar().setValue(
            self._categoryScrollArea.horizontalScrollBar().value() - 50
        )

    def addWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the category layout.

        :param widget: The widget to add.
        """
        self._categoryLayout.addWidget(widget)

    def removeWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the category layout.

        :param widget: The widget to remove.
        """
        self._categoryLayout.removeWidget(widget)

    def takeWidget(self, widget: QtWidgets.QWidget):
        """Remove and return a widget from the category layout.

        :param widget: The widget to remove.
        :return: The widget that was removed.
        """
        self._categoryLayout.removeWidget(widget)
        return widget
