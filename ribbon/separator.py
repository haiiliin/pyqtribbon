from PyQt5 import QtCore, QtWidgets, QtGui


class RibbonSeparator(QtWidgets.QWidget):
    _topMargins: int = 4
    _bottomMargins: int = 4
    _leftMargins: int = 4
    _rightMargins: int = 4
    _orientation: QtCore.Qt.Orientation

    def __init__(self, orientation=QtCore.Qt.Vertical, width=6, parent=None) -> None:
        super().__init__(parent=parent)
        self._orientation = orientation
        if orientation == QtCore.Qt.Horizontal:
            self.setFixedHeight(width)
            self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        else:
            self.setFixedWidth(width)
            self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

    def sizeHint(self) -> QtCore.QSize:
        return self.size()

    def setTopBottomMargins(self, top: int, bottom: int) -> None:
        self._topMargins = top
        self._bottomMargins = bottom

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(QtCore.Qt.gray))
        painter.setPen(pen)
        if self._orientation == QtCore.Qt.Vertical:
            x1 = self.rect().center().x()
            painter.drawLine(
                QtCore.QPoint(x1, self.rect().top() + self._topMargins),
                QtCore.QPoint(x1, self.rect().bottom() - self._bottomMargins),
            )
        else:
            y1 = self.rect().center().y()
            painter.drawLine(
                QtCore.QPoint(self.rect().left() + self._leftMargins, y1),
                QtCore.QPoint(self.rect().right() - self._rightMargins, y1),
            )


class RibbonHorizontalSeparator(RibbonSeparator):

    def __init__(self, width: int = 6, parent=None) -> None:
        super().__init__(QtCore.Qt.Horizontal, width, parent)


class RibbonVerticalSeparator(RibbonSeparator):

    def __init__(self, width: int = 6, parent=None) -> None:
        super().__init__(QtCore.Qt.Vertical, width, parent)
