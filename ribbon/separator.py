import typing

from PyQt5.QtCore import QSize, QPoint, Qt
from PyQt5.QtGui import QColor, QPaintEvent, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QSizePolicy


class Separator(QWidget):
    _topMargins: int = 4
    _bottomMargins: int = 4

    @typing.overload
    def __init__(self, parent=None) -> None:
        pass

    @typing.overload
    def __init__(self, width=6, parent=None) -> None:
        pass

    def __init__(self, *args, **kwargs) -> None:
        if (args and isinstance(args[0], int)) or (kwargs and "height" in kwargs):
            width = kwargs.get("height", args[0])
            parent = args[1] if len(args) > 1 else kwargs.get("parent", None)
        else:
            width = 6
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super(Separator, self).__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setFixedWidth(width)

    def sizeHint(self) -> QSize:
        return self.size()

    def setTopBottomMargins(self, top: int, bottom: int) -> None:
        self._topMargins = top
        self._bottomMargins = bottom

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(Qt.gray))
        painter.setPen(pen)
        x1: int = self.rect().center().x()
        painter.drawLine(
            QPoint(x1, self.rect().top() + self._topMargins),
            QPoint(x1, self.rect().bottom() - self._bottomMargins),
        )
