from PyQt5 import QtWidgets, QtGui, QtCore


class TabBar(QtWidgets.QTabBar):
    #: context category top margin
    _contextCategoryTopMargin = 0
    #: context category dark color height
    _contextCategoryDarkColorHeight = 5
    _contextualColor = QtGui.QColor(255, 0, 0)

    _tabColors = {}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QTabBar::tab {margin-top: 20px; } "
                           "QTabBar::tab:!selected {margin-top: 20px; }")

    def addTab(self, text: str, color: QtGui.QColor = None) -> int:
        self._tabColors[text] = color
        return super().addTab(text)

    def currentTabColor(self) -> QtGui.QColor:
        return self._tabColors[self.tabText(self.currentIndex())]

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
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
            lightColor = self._contextualColor.lighter(190)
            tabRect -= QtCore.QMargins(0, self._contextCategoryDarkColorHeight, 0, 0)
            painter.fillRect(tabRect, lightColor)
        super().paintEvent(a0)
