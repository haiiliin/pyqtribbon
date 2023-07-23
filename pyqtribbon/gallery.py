import typing

from qtpy import QtCore, QtGui, QtWidgets

from .menu import RibbonPermanentMenu
from .separator import RibbonHorizontalSeparator
from .toolbutton import RibbonToolButton
from .utils import DataFile


class RibbonPopupWidget(QtWidgets.QFrame):
    """The popup widget for the gallery widget."""

    pass


class RibbonGalleryListWidget(QtWidgets.QListWidget):
    """Gallery list widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setVerticalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setIconSize(QtCore.QSize(64, 64))

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        """Resize the list widget."""
        super().resizeEvent(e)

    def scrollToNextRow(self) -> None:
        """Scroll to the next row."""
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() + self.verticalScrollBar().singleStep())

    def scrollToPreviousRow(self) -> None:
        """Scroll to the previous row."""
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - self.verticalScrollBar().singleStep())


class RibbonGalleryButton(QtWidgets.QToolButton):
    """Gallery button."""

    pass


class RibbonGalleryPopupListWidget(RibbonGalleryListWidget):
    """Gallery popup list widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


class RibbonGallery(QtWidgets.QFrame):
    """A widget that displays a gallery of buttons."""

    _popupWindowSize = QtCore.QSize(500, 500)
    _buttons: typing.List[RibbonToolButton] = []
    _popupButtons: typing.List[RibbonToolButton] = []
    _popupHideOnClick = False

    @typing.overload
    def __init__(self, minimumWidth=800, popupHideOnClick=False, parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a gallery.

        :param minimumWidth: minimum width of the gallery
        :param popupHideOnClick: hide on click flag
        :param parent: parent widget
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or (
            "minimumWidth" in kwargs or "popupHideOnClick" in kwargs
        ):
            minimumWidth = args[0] if len(args) > 0 else kwargs.get("minimumWidth", 800)
            popupHideOnClick = args[1] if len(args) > 1 else kwargs.get("popupHideOnClick", False)
            parent = args[2] if len(args) > 2 else kwargs.get("parent", None)
        else:
            minimumWidth = 800
            popupHideOnClick = False
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent)
        self.setMinimumWidth(minimumWidth)
        self._popupHideOnClick = popupHideOnClick

        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 5, 5, 5)
        self._mainLayout.setSpacing(5)

        self._upButton = RibbonGalleryButton(self)
        self._upButton.setIcon(QtGui.QIcon(DataFile("icons/up.png")))
        self._upButton.setIconSize(QtCore.QSize(24, 24))
        self._upButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._upButton.setAutoRaise(True)
        self._downButton = RibbonGalleryButton(self)
        self._downButton.setIcon(QtGui.QIcon(DataFile("icons/down.png")))
        self._downButton.setIconSize(QtCore.QSize(24, 24))
        self._downButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._downButton.setAutoRaise(True)
        self._moreButton = RibbonGalleryButton(self)
        self._moreButton.setIcon(QtGui.QIcon(DataFile("icons/more.png")))
        self._moreButton.setIconSize(QtCore.QSize(24, 24))
        self._moreButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._moreButton.setAutoRaise(True)
        self._scrollButtonLayout = QtWidgets.QVBoxLayout()
        self._scrollButtonLayout.setContentsMargins(0, 0, 0, 0)
        self._scrollButtonLayout.setSpacing(2)
        self._scrollButtonLayout.addWidget(self._upButton)
        self._scrollButtonLayout.addWidget(self._downButton)
        self._scrollButtonLayout.addWidget(self._moreButton)

        self._listWidget = RibbonGalleryListWidget()
        self._mainLayout.addWidget(self._listWidget)
        self._mainLayout.addLayout(self._scrollButtonLayout)

        self._upButton.clicked.connect(self._listWidget.scrollToPreviousRow)  # type: ignore
        self._downButton.clicked.connect(self._listWidget.scrollToNextRow)  # type: ignore

        self._popupWidget = RibbonPopupWidget()  # type: ignore
        self._popupWidget.setFont(QtWidgets.QApplication.instance().font())  # type: ignore
        self._popupWidget.setWindowFlags(QtCore.Qt.Popup)
        self._popupLayout = QtWidgets.QVBoxLayout(self._popupWidget)
        self._popupLayout.setContentsMargins(5, 5, 5, 5)
        self._popupLayout.setSpacing(2)

        self._popupListWidget = RibbonGalleryPopupListWidget()
        self._popupLayout.addWidget(self._popupListWidget)
        self._popupLayout.addWidget(RibbonHorizontalSeparator())

        self._popupMenu = RibbonPermanentMenu()
        self._popupMenu.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)  # type: ignore
        self._popupMenu.actionAdded.connect(self._handlePopupAction)
        self._popupLayout.addWidget(self._popupMenu)

        self._moreButton.clicked.connect(self.showPopup)  # type: ignore

    def _handlePopupAction(self, action: QtWidgets.QAction) -> None:
        """Handle a popup action."""
        if isinstance(action, QtWidgets.QAction):
            action.triggered.connect(self.hidePopupWidget)  # type: ignore

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Resize the gallery."""
        height = self.height() - self._mainLayout.contentsMargins().top() - self._mainLayout.contentsMargins().bottom()
        self._upButton.setFixedSize(height // 4, height // 3)  # type: ignore
        self._downButton.setFixedSize(height // 4, height // 3)  # type: ignore
        self._moreButton.setFixedSize(height // 4, height // 3)  # type: ignore
        super().resizeEvent(a0)

    def popupMenu(self) -> RibbonPermanentMenu:
        """Return the popup menu."""
        return self._popupMenu

    def showPopup(self):
        """Show the popup window"""
        self._popupWidget.move(self.mapToGlobal(self.geometry().topLeft()))
        self._popupWidget.resize(
            QtCore.QSize(
                max(self.popupWindowSize().width(), self.width()), max(self.popupWindowSize().height(), self.height())
            )
        )
        self._popupMenu.setFixedWidth(
            self._popupWidget.width()
            - self._popupLayout.contentsMargins().left()
            - self._popupLayout.contentsMargins().right()
        )
        self._popupWidget.show()

    def hidePopupWidget(self):
        """Hide the popup window"""
        self._popupWidget.hide()

    def popupWindowSize(self):
        """Return the size of the popup window

        :return: size of the popup window
        """
        return self._popupWindowSize

    def setPopupWindowSize(self, size: QtCore.QSize):
        """Set the size of the popup window

        :param size: size of the popup window
        """
        self._popupWindowSize = size

    def setSelectedButton(self):
        """Set the selected button"""
        button = self.sender()
        if isinstance(button, RibbonToolButton):
            row = self._popupButtons.index(button)
            self._listWidget.scrollTo(self._listWidget.model().index(row, 0), QtWidgets.QAbstractItemView.EnsureVisible)
            if self._buttons[row].isCheckable():
                self._buttons[row].setChecked(not self._buttons[row].isChecked())

    def _addWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the gallery

        :param widget: widget to add
        """
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self._listWidget.setSpacing((self.height() - item.sizeHint().height()) // 2)
        self._listWidget.addItem(item)
        self._listWidget.setItemWidget(item, widget)

    def _addPopupWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the popup gallery

        :param widget: widget to add
        """
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self._popupListWidget.setSpacing((self.height() - item.sizeHint().height()) // 2)
        self._popupListWidget.addItem(item)
        self._popupListWidget.setItemWidget(item, widget)

    def setPopupHideOnClick(self, popupHideOnClick: bool):
        """Set the hide on click flag

        :param popupHideOnClick: hide on click flag
        """
        self._popupHideOnClick = popupHideOnClick

    def addButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
        checkable=False,
    ) -> RibbonToolButton:
        """Add a button to the gallery

        :param text: text of the button
        :param icon: icon of the button
        :param slot: slot to call when the button is clicked
        :param shortcut: shortcut of the button
        :param tooltip: tooltip of the button
        :param statusTip: status tip of the button
        :param checkable: checkable flag of the button.
        :return: the button added
        """
        button = RibbonToolButton(self)
        popupButton = RibbonToolButton(self._popupWidget)
        if text is not None:
            button.setText(text)
            popupButton.setText(text)
        if icon is not None:
            button.setIcon(icon)
            popupButton.setIcon(icon)
        if slot is not None:
            button.clicked.connect(slot)  # type: ignore
            popupButton.clicked.connect(slot)  # type: ignore
        if shortcut is not None:
            button.setShortcut(shortcut)
            popupButton.setShortcut(shortcut)
        if tooltip is not None:
            button.setToolTip(tooltip)
            popupButton.setToolTip(tooltip)
        if statusTip is not None:
            button.setStatusTip(statusTip)
            popupButton.setStatusTip(statusTip)
        if checkable:
            button.setCheckable(True)
            popupButton.setCheckable(True)
        self._buttons.append(button)
        self._popupButtons.append(popupButton)
        button.clicked.connect(lambda checked: popupButton.setChecked(checked))  # type: ignore
        if self._popupHideOnClick:
            popupButton.clicked.connect(self.hidePopupWidget)  # type: ignore
        popupButton.clicked.connect(self.setSelectedButton)  # type: ignore

        if text is None:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            popupButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        else:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            popupButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self._addWidget(button)
        self._addPopupWidget(popupButton)
        return button

    def addToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
    ) -> RibbonToolButton:
        """Add a toggle button to the gallery

        :param text: text of the button
        :param icon: icon of the button
        :param slot: slot to call when the button is clicked
        :param shortcut: shortcut of the button
        :param tooltip: tooltip of the button
        :param statusTip: status tip of the button.
        :return: the button added
        """
        button = self.addButton(text, icon, slot, shortcut, tooltip, statusTip, True)
        return button
