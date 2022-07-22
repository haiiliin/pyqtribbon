from PyQt5 import QtWidgets, QtGui, QtCore


class RibbonTabBar(QtWidgets.QTabBar):
    """The TabBar for the title widget."""
    #: context category top margin
    _contextCategoryTopMargin = 0
    #: context category dark color height
    _contextCategoryDarkColorHeight = 5
    _contextColor = QtGui.QColor(255, 0, 0)

    _tabColors = {}

    def __init__(self, parent=None):
        """Create a new tab bar.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setDrawBase(False)
        self.setStyleSheet("QTabBar::tab {margin-top: 10px; margin-bottom: 5px; } "
                           "QTabBar::tab:!selected {margin-top: 10px; margin-bottom: 5px; }")

    def indexOf(self, tabName: str) -> int:
        """Return the index of the tab with the given name.

        :param tabName: The name of the tab.
        :return: The index of the tab.
        """
        for i in range(self.count()):
            if self.tabText(i) == tabName:
                return i
        return -1

    def addTab(self, text: str, color: QtGui.QColor = None) -> int:
        """Add a new tab to the tab bar.

        :param text: The text of the tab.
        :param color: The color of the tab.
        :return: The index of the tab.
        """
        self._tabColors[text] = color
        return super().addTab(text)

    def currentTabColor(self) -> QtGui.QColor:
        """Current tab color

        :return: Current tab color
        """
        return self._tabColors[self.tabText(self.currentIndex())]

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Paint the tab bar."""
        if self.count() == 0:
            super().paintEvent(a0)
        color = self.currentTabColor()
        if color is not None:
            # Tab rectangle
            tabRect = self.tabRect(self.currentIndex())
            if self.currentIndex() > 0:
                tabRect.setLeft(tabRect.left() + 6)

            tabRect.setHeight(self.height() - 1)
            tabRect.setTop(self._contextCategoryTopMargin)

            # Paint top dark color area
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(self.currentTabColor())
            painter.drawRect(tabRect.x(),
                             self._contextCategoryTopMargin,
                             tabRect.width(),
                             self._contextCategoryDarkColorHeight)

            # Paint rest of the category
            lightColor = self._contextColor.lighter(190)
            tabRect -= QtCore.QMargins(0, self._contextCategoryDarkColorHeight, 0, 0)
            painter.fillRect(tabRect, lightColor)
        super().paintEvent(a0)
