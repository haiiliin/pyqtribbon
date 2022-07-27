import typing

from qtpy import QtWidgets, QtGui, QtCore


class RibbonTabBar(QtWidgets.QTabBar):
    """The TabBar for the title widget."""
    #: context category top margin
    _contextCategoryTopMargin = 0
    #: context category dark color height
    _contextCategoryDarkColorHeight = 5

    _tabColors = {}
    _associated_tabs = {}

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

    def tabTitles(self) -> typing.List[str]:
        """Return the titles of all tabs.

        :return: The titles of all tabs.
        """
        return [self.tabText(i) for i in range(self.count())]

    def addTab(
        self,
        text: str,
        color: QtGui.QColor = None,
    ) -> int:
        """Add a new tab to the tab bar.

        :param text: The text of the tab.
        :param color: The color of the tab.
        :return: The index of the tab.
        """
        self._tabColors[text] = color
        return super().addTab(text)

    def addAssociatedTabs(
        self,
        name: str,
        texts: typing.List[str],
        color: QtGui.QColor,
    ) -> typing.List[int]:
        """Add associated multiple tabs which have the same color to the tab bar.

        :param name: The name of the context category.
        :param texts: The texts of the tabs.
        :param color: The color of the tabs.
        :return: The indices of the tabs.
        """
        self._tabColors[name] = color
        for text in texts:
            self._associated_tabs[text] = [t for t in texts if t != text]
        return [self.addTab(text, color) for text in texts]

    def removeAssociatedTabs(self, titles: typing.List[str]) -> None:
        """Remove tabs with the given titles.

        :param titles: The titles of the tabs to remove.
        """
        tabTitles = self.tabTitles()
        for title in titles:
            if title in tabTitles:
                self.removeTab(self.indexOf(title))
                del self._tabColors[title]
                if title in self._associated_tabs:
                    del self._associated_tabs[title]

    def currentTabColor(self) -> QtGui.QColor:
        """Current tab color

        :return: Current tab color
        """
        return self._tabColors[self.tabText(self.currentIndex())]

    def _paintTabRect(self, rect: QtCore.QRect, color: QtGui.QColor) -> None:
        """Paint the tab rectangle.

        :param rect: The tab rectangle.
        :param color: The color of the tab.
        """
        rect.setRight(rect.right() + 5)
        rect.setHeight(self.height() - 1)
        rect.setTop(self._contextCategoryTopMargin)

        # Paint top dark color area
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        color = QtGui.QColor(color)  # in case color is a GlobalColor object
        painter.setBrush(color)
        painter.drawRect(rect.x(),
                         self._contextCategoryTopMargin,
                         rect.width(),
                         self._contextCategoryDarkColorHeight)

        # Paint rest of the category
        lightColor = color.lighter(190)
        rect -= QtCore.QMargins(0, self._contextCategoryDarkColorHeight, 0, 0)
        painter.fillRect(rect, lightColor)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Paint the tab bar."""
        if self.count() > 0:
            currentTabText = self.tabText(self.currentIndex())
            currentTabColor = self._tabColors[currentTabText]
            if currentTabColor is not None:
                self._paintTabRect(self.tabRect(self.currentIndex()), currentTabColor)
                if currentTabText in self._associated_tabs and self._associated_tabs[currentTabText]:
                    for tabText in self._associated_tabs[currentTabText]:
                        self._paintTabRect(self.tabRect(self.indexOf(tabText)),
                                           currentTabColor)
        super().paintEvent(a0)
