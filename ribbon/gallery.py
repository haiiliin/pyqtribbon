from PyQt5 import QtWidgets, QtGui, QtCore

from .toolbutton import RibbonToolButton


class RibbonGalleryListWidget(QtWidgets.QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setVerticalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setIconSize(QtCore.QSize(64, 64))

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super().resizeEvent(e)

    def scrollToNextRow(self) -> None:
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() + self.verticalScrollBar().singleStep())

    def scrollToPreviousRow(self) -> None:
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - self.verticalScrollBar().singleStep())


class RibbonGalleryPopupListWidget(RibbonGalleryListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


class RibbonGallery(QtWidgets.QFrame):
    _popupWindowSize = QtCore.QSize(500, 500)

    def __init__(self, minimumWidth=800, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(minimumWidth)

        self._mainLayout = QtWidgets.QHBoxLayout(self)
        self._mainLayout.setContentsMargins(5, 0, 5, 0)
        self._mainLayout.setSpacing(5)

        self._upButton = QtWidgets.QToolButton(self)
        self._upButton.setIcon(QtGui.QIcon("icons/up.png"))
        self._upButton.setIconSize(QtCore.QSize(24, 24))
        self._upButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._downButton = QtWidgets.QToolButton(self)
        self._downButton.setIcon(QtGui.QIcon("icons/down.png"))
        self._downButton.setIconSize(QtCore.QSize(24, 24))
        self._downButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._moreButton = QtWidgets.QToolButton(self)
        self._moreButton.setIcon(QtGui.QIcon("icons/more.png"))
        self._moreButton.setIconSize(QtCore.QSize(24, 24))
        self._moreButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._scrollButtonLayout = QtWidgets.QVBoxLayout()
        self._scrollButtonLayout.setContentsMargins(0, 0, 0, 0)
        self._scrollButtonLayout.setSpacing(0)
        self._scrollButtonLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
            )
        )
        self._scrollButtonLayout.addWidget(self._upButton)
        self._scrollButtonLayout.addWidget(self._downButton)
        self._scrollButtonLayout.addWidget(self._moreButton)
        self._scrollButtonLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                10, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
            )
        )

        self._listWidget = RibbonGalleryListWidget()
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

    def addWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the gallery

        :param widget: widget to add
        """
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self._listWidget.setSpacing((self.height() - item.sizeHint().height()) / 2)
        self._listWidget.addItem(item)
        self._listWidget.setItemWidget(item, widget)

    def addPopupWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the popup gallery

        :param widget: widget to add
        """
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self._popupListWidget.setSpacing((self.height() - item.sizeHint().height()) / 2)
        self._popupListWidget.addItem(item)
        self._popupListWidget.setItemWidget(item, widget)

    def addButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        tooltip=None,
        statusTip=None,
    ) -> RibbonToolButton:
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
        popupButton.clicked.connect(self._popupWidget.hide)

        if text is None:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            popupButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        else:
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            popupButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addWidget(button)
        self.addPopupWidget(popupButton)
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
        button = self.addButton(text, icon, slot, shortcut, tooltip, statusTip)
        button.setCheckable(True)
        return button
