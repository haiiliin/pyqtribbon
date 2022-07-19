import enum
import typing

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

from .toolbutton import ToolButton
from .separator import Separator


class ActionStyle(enum.IntEnum):
    """The buttonStyle of an action."""

    Small = 0
    Medium = 1
    Large = 2


class GridLayoutManager(object):
    def __init__(self, rows: int):
        self.rows = rows
        self.cells = np.ones((rows, 1), dtype=bool)

    def request_cells(self, rowSpan: int = 1, colSpan: int = 1):
        """Request a number of available cells from the grid.

        :param rowSpan: The number of rows the cell should span.
        :param colSpan: The number of columns the cell should span.
        :return: row, col, the row and column of the requested cell.
        """
        if rowSpan > self.rows:
            raise ValueError("RowSpan is too large")
        for row in range(self.cells.shape[0] - rowSpan + 1):
            for col in range(self.cells.shape[1] - colSpan + 1):
                if self.cells[row: row + rowSpan, col: col + colSpan].all():
                    self.cells[row: row + rowSpan, col: col + colSpan] = False
                    return row, col
        cols = self.cells.shape[1]
        self.cells = np.append(
            self.cells, np.ones((self.rows, colSpan), dtype=bool), axis=1
        )
        self.cells[:rowSpan, cols: cols + colSpan] = False
        return 0, cols


class Panel(QtWidgets.QWidget):
    #: maximal number of rows
    _maxRows: int
    #: GridLayout manager to request available cells.
    _gridLayoutManager: GridLayoutManager

    #: widgets that are added to the panel
    _widgets: typing.List[QtWidgets.QWidget] = []

    # Panel options signal
    panelOptionsClicked = QtCore.pyqtSignal(bool)

    def __init__(self, title: str, maxRows=3, parent=None):
        super().__init__(parent)
        self._maxRows = maxRows
        self._gridLayoutManager = GridLayoutManager(self._maxRows)
        self._widgets = []

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)
        self.setLayout(self._mainLayout)

        # Actions layout
        self._horizontalLayout = QtWidgets.QHBoxLayout()
        self._actionsLayout = QtWidgets.QGridLayout()
        self._actionsLayout.setContentsMargins(5, 5, 5, 5)
        self._actionsLayout.setSpacing(5)
        self._horizontalLayout.addLayout(self._actionsLayout, 0)
        self._horizontalLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
            )
        )
        self._mainLayout.addLayout(self._horizontalLayout, 1)

        # Title layout
        self._titleLayout = QtWidgets.QHBoxLayout()
        self._titleLayout.setContentsMargins(0, 0, 0, 0)
        self._titleLayout.setSpacing(5)
        self._titleLabel = QtWidgets.QLabel(self)
        self._titleLabel.setText(title)
        self._titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._titleLayout.addWidget(self._titleLabel, 1)
        self._panelOptions = QtWidgets.QToolButton(self)
        self._panelOptions.setAutoRaise(True)
        self._panelOptions.setIcon(QtGui.QIcon("icons/ribbonPanelOptionButton.png"))
        self._panelOptions.clicked.connect(self.panelOptionsClicked)
        self._titleLayout.addWidget(self._panelOptions, 0)
        self._mainLayout.addLayout(self._titleLayout, 0)

    def addWidget(
        self, widget: QtWidgets.QWidget, rowSpan: int = 1, colSpan: int = 1
    ) -> typing.Union[QtWidgets.QWidget, typing.Any]:
        """Add a widget to the panel."""
        self._widgets.append(widget)
        row, col = self._gridLayoutManager.request_cells(rowSpan, colSpan)
        self._actionsLayout.addWidget(
            widget, row, col, rowSpan, colSpan, QtCore.Qt.AlignCenter
        )
        return widget

    def removeWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the panel."""
        self._actionsLayout.removeWidget(widget)

    def widget(self, index: int) -> QtWidgets.QWidget:
        """Get the widget at the given index.

        :param index: The index of the widget, starting from 0.
        :return: The widget at the given index.
        """
        return self._widgets[index]

    def addButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        style: ActionStyle = ActionStyle.Large,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        if icon is None:
            icon = QtGui.QIcon()
        button = ToolButton(icon, text, style, self)
        if slot:
            button.clicked.connect(slot)
        if shortcut:
            button.setShortcut(shortcut)
        if statusTip:
            button.setStatusTip(statusTip)
        return self.addWidget(
            button,
            rowSpan=1
            if style == ActionStyle.Small
            else 2
            if style == ActionStyle.Medium
            else 3,
            colSpan=1,
        )

    def addSmallButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        return self.addButton(text, icon, ActionStyle.Small, slot, shortcut, statusTip)

    def addMediumButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        return self.addButton(text, icon, ActionStyle.Medium, slot, shortcut, statusTip)

    def addLargeButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        return self.addButton(text, icon, ActionStyle.Large, slot, shortcut, statusTip)

    def addToggleButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        style: ActionStyle = ActionStyle.Large,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        if icon is None:
            icon = QtGui.QIcon()
        button = ToolButton(icon, text, style, self)
        button.setCheckable(True)
        if slot:
            button.clicked.connect(slot)
        if shortcut:
            button.setShortcut(shortcut)
        if statusTip:
            button.setStatusTip(statusTip)
        return self.addWidget(
            button,
            rowSpan=1
            if style == ActionStyle.Small
            else 2
            if style == ActionStyle.Medium
            else 3,
            colSpan=1,
        )

    def addSmallToggleButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        return self.addToggleButton(
            text, icon, ActionStyle.Small, slot, shortcut, statusTip
        )

    def addMediumToggleButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        return self.addToggleButton(
            text, icon, ActionStyle.Medium, slot, shortcut, statusTip
        )

    def addLargeToggleButton(
        self,
        text: str,
        icon: QtGui.QIcon = None,
        slot=None,
        shortcut=None,
        statusTip=None,
    ) -> ToolButton:
        return self.addToggleButton(
            text, icon, ActionStyle.Large, slot, shortcut, statusTip
        )

    def addComboBox(
        self, items: typing.List[str], rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QComboBox:
        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItems(items)
        return self.addWidget(comboBox, rowSpan, colSpan)

    def addFontComboBox(
        self, rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QFontComboBox:
        comboBox = QtWidgets.QFontComboBox(self)
        return self.addWidget(comboBox, rowSpan, colSpan)

    def addLineEdit(self, rowSpan: int = 1, colSpan: int = 1) -> QtWidgets.QLineEdit:
        lineEdit = QtWidgets.QLineEdit(self)
        return self.addWidget(lineEdit, rowSpan, colSpan)

    def addTextEdit(self, rowSpan: int = 1, colSpan: int = 1) -> QtWidgets.QTextEdit:
        textEdit = QtWidgets.QTextEdit(self)
        return self.addWidget(textEdit, rowSpan, colSpan)

    def addPlainTextEdit(
        self, rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QPlainTextEdit:
        textEdit = QtWidgets.QPlainTextEdit(self)
        return self.addWidget(textEdit, rowSpan, colSpan)

    def addLabel(
        self, text: str, rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(self)
        label.setText(text)
        return self.addWidget(label, rowSpan, colSpan)

    def addProgressBar(
        self, rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QProgressBar:
        progressBar = QtWidgets.QProgressBar(self)
        return self.addWidget(progressBar, rowSpan, colSpan)

    def addSlider(self, rowSpan: int = 1, colSpan: int = 1) -> QtWidgets.QSlider:
        slider = QtWidgets.QSlider(self)
        slider.setOrientation(QtCore.Qt.Horizontal)
        return self.addWidget(slider, rowSpan, colSpan)

    def addSpinBox(self, rowSpan: int = 1, colSpan: int = 1) -> QtWidgets.QSpinBox:
        spinBox = QtWidgets.QSpinBox(self)
        return self.addWidget(spinBox, rowSpan, colSpan)

    def addDoubleSpinBox(
            self, rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QDoubleSpinBox:
        doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        return self.addWidget(doubleSpinBox, rowSpan, colSpan)

    def addDateEdit(self, rowSpan: int = 1, colSpan: int = 1) -> QtWidgets.QDateEdit:
        dateEdit = QtWidgets.QDateEdit(self)
        return self.addWidget(dateEdit, rowSpan, colSpan)

    def addTimeEdit(self, rowSpan: int = 1, colSpan: int = 1) -> QtWidgets.QTimeEdit:
        timeEdit = QtWidgets.QTimeEdit(self)
        return self.addWidget(timeEdit, rowSpan, colSpan)

    def addDateTimeEdit(
        self, rowSpan: int = 1, colSpan: int = 1
    ) -> QtWidgets.QDateTimeEdit:
        dateTimeEdit = QtWidgets.QDateTimeEdit(self)
        return self.addWidget(dateTimeEdit, rowSpan, colSpan)

    def addTableWidget(
        self, rowSpan: int = 3, colSpan: int = 1
    ) -> QtWidgets.QTableWidget:
        tableWidget = QtWidgets.QTableWidget(self)
        return self.addWidget(tableWidget, rowSpan, colSpan)

    def addTreeWidget(
        self, rowSpan: int = 3, colSpan: int = 1
    ) -> QtWidgets.QTreeWidget:
        treeWidget = QtWidgets.QTreeWidget(self)
        return self.addWidget(treeWidget, rowSpan, colSpan)

    def addListWidget(
        self, rowSpan: int = 3, colSpan: int = 1
    ) -> QtWidgets.QListWidget:
        listWidget = QtWidgets.QListWidget(self)
        return self.addWidget(listWidget, rowSpan, colSpan)

    def addCalendarWidget(
        self, rowSpan: int = 3, colSpan: int = 1
    ) -> QtWidgets.QCalendarWidget:
        calendarWidget = QtWidgets.QCalendarWidget(self)
        return self.addWidget(calendarWidget, rowSpan, colSpan)

    def addSeparator(self, width=10) -> Separator:
        """Add a separator to the panel.

        :param width: The width of the separator.
        """
        separator = Separator(width=width)
        return self.addWidget(separator, rowSpan=3, colSpan=1)

    def setTitleText(self, text: str):
        """Set the title text of the panel.

        :param text: The text to set.
        """
        self._titleLabel.setText(text)

    def titleText(self):
        """Get the title text of the panel.

        :return: The title text.
        """
        return self._titleLabel.text()
