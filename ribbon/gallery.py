from PyQt5 import QtWidgets, QtGui, QtCore

from .toolbutton import RibbonToolButton
from .utils import package_source_dir


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
    _buttons: list[RibbonToolButton] = []
    _popupButtons: list[RibbonToolButton] = []
    _popupHideOnClick = False

    def __init__(self, minimumWidth=800, popupHideOnClick=False, parent=None):
        """Create a gallery.

        :param minimumWidth: minimum width of the gallery
        :param popupHideOnClick: hide on click flag
        :param parent: parent widget
        """
        super().__init__(parent)
        self.setMinimumWidth(minimumWidth)
        self._popupHideOnClick = popupHideOnClick

        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 0, 0, 0)
        self._mainLayout.setSpacing(5)

        self._upButton = RibbonGalleryButton(self)
        self._upButton.setIcon(QtGui.QIcon(package_source_dir() + "/icons/up.png"))
        self._upButton.setIconSize(QtCore.QSize(24, 24))
        self._upButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._upButton.setAutoRaise(True)
        self._downButton = RibbonGalleryButton(self)
        self._downButton.setIcon(QtGui.QIcon(package_source_dir() + "/icons/down.png"))
        self._downButton.setIconSize(QtCore.QSize(24, 24))
        self._downButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._downButton.setAutoRaise(True)
        self._moreButton = RibbonGalleryButton(self)
        self._moreButton.setIcon(QtGui.QIcon(package_source_dir() + "/icons/more.png"))
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
        self._listWidget.setStyleSheet("QListWidget { background-color: transparent; }")
        self._mainLayout.addWidget(self._listWidget)
        self._mainLayout.addLayout(self._scrollButtonLayout)

        self._upButton.clicked.connect(self._listWidget.scrollToPreviousRow)
        self._downButton.clicked.connect(self._listWidget.scrollToNextRow)

        self._popupWidget = QtWidgets.QWidget()
        self._popupWidget.setWindowFlags(QtCore.Qt.Popup)
        self._popupLayout = QtWidgets.QVBoxLayout(self._popupWidget)
        self._popupLayout.setContentsMargins(0, 0, 0, 0)
        self._popupListWidget = RibbonGalleryPopupListWidget()
        self._popupLayout.addWidget(self._popupListWidget)

        self._moreButton.clicked.connect(self.showPopup)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Resize the gallery."""
        self._upButton.setFixedSize(self.height() // 4, self.height() // 3)
        self._downButton.setFixedSize(self.height() // 4, self.height() // 3)
        self._moreButton.setFixedSize(self.height() // 4, self.height() // 3)
        super().resizeEvent(a0)

    def showPopup(self):
        """Show the popup window"""
        self._popupWidget.move(self.mapToGlobal(self._listWidget.geometry().topLeft()))
        self._popupWidget.resize(QtCore.QSize(
            max(self.popupWindowSize().width(), self.width()),
            max(self.popupWindowSize().height(), self.height())
        ))
        self._popupWidget.show()

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
        :param checkable: checkable flag of the button
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
            button.clicked.connect(slot)
            popupButton.clicked.connect(slot)
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
        button.clicked.connect(lambda checked: popupButton.setChecked(checked))
        if self._popupHideOnClick:
            popupButton.clicked.connect(self._popupWidget.hide)
        popupButton.clicked.connect(self.setSelectedButton)

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
        :param statusTip: status tip of the button
        :return: the button added
        """
        button = self.addButton(text, icon, slot, shortcut, tooltip, statusTip, True)
        return button
