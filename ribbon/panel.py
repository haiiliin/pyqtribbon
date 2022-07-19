import typing

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

from .toolbutton import ToolButton, ButtonStyle
from .separator import Separator


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

    def __init__(self, title: str, maxRows=6, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QWidget { background-color: white; }")
        self._maxRows = maxRows
        self._gridLayoutManager = GridLayoutManager(self._maxRows)
        self._widgets = []

        # Main layout
        self._mainLayout = QtWidgets.QVBoxLayout(self)
        self._mainLayout.setContentsMargins(10, 10, 5, 5)
        self._mainLayout.setSpacing(0)

        # Actions layout
        self._horizontalLayout = QtWidgets.QHBoxLayout()
        self._actionsLayout = QtWidgets.QGridLayout()
        self._actionsLayout.setContentsMargins(0, 0, 0, 0)
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
        self, widget: QtWidgets.QWidget, rowSpan: int = 2, colSpan: int = 1
    ):
        """Add a widget to the panel.

        :param widget: The widget to add.
        :param rowSpan: The number of rows the widget should span, 2: small, 3: medium, 6: large.
        :param colSpan: The number of columns the widget should span.
        """
        self._widgets.append(widget)
        row, col = self._gridLayoutManager.request_cells(rowSpan, colSpan)
        self._actionsLayout.addWidget(
            widget, row, col, rowSpan, colSpan, QtCore.Qt.AlignCenter
        )

    def addSmallWidget(self, widget: QtWidgets.QWidget):
        """Add a small widget to the panel.

        :param widget: The widget to add.
        :return: The widget that was added.
        """
        return self.addWidget(widget, 2, 1)

    def addMediumWidget(self, widget: QtWidgets.QWidget):
        """Add a medium widget to the panel.

        :param widget: The widget to add.
        """
        return self.addWidget(widget, 3, 1)

    def addLargeWidget(self, widget: QtWidgets.QWidget):
        """Add a large widget to the panel.

        :param widget: The widget to add.
        """
        return self.addWidget(widget, 6, 1)

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
            text: str = None,
            icon: QtGui.QIcon = None,
            style: ButtonStyle = ButtonStyle.Large,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        button = ToolButton(self)
        button.setButtonStyle(style)
        if text:
            button.setText(text)
        if icon:
            button.setIcon(icon)
        if slot:
            button.clicked.connect(slot)
        if shortcut:
            button.setShortcut(shortcut)
        if statusTip:
            button.setStatusTip(statusTip)
        button.setMaximumHeight(self.height() - self._titleLabel.sizeHint().height() -
                                self._mainLayout.spacing() -
                                self._mainLayout.contentsMargins().top() -
                                self._mainLayout.contentsMargins().bottom())
        self.addWidget(
            button,
            rowSpan=2 if style == ButtonStyle.Small else 3 if style == ButtonStyle.Medium else 6,
            colSpan=1,
        )
        return button

    def addSmallButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        return self.addButton(text, icon, ButtonStyle.Small, slot, shortcut, statusTip)

    def addMediumButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        return self.addButton(text, icon, ButtonStyle.Medium, slot, shortcut, statusTip)

    def addLargeButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        return self.addButton(text, icon, ButtonStyle.Large, slot, shortcut, statusTip)

    def addToggleButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            style: ButtonStyle = ButtonStyle.Large,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        button = ToolButton(self)
        button.setButtonStyle(style)
        if text:
            button.setText(text)
        if icon:
            button.setIcon(icon)
        button.setCheckable(True)
        if slot:
            button.clicked.connect(slot)
        if shortcut:
            button.setShortcut(shortcut)
        if statusTip:
            button.setStatusTip(statusTip)
        self.addWidget(
            button,
            rowSpan=2 if style == ButtonStyle.Small else 3 if style == ButtonStyle.Medium else 6,
            colSpan=1,
        )
        return button

    def addSmallToggleButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        return self.addToggleButton(
            text, icon, ButtonStyle.Small, slot, shortcut, statusTip
        )

    def addMediumToggleButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        return self.addToggleButton(
            text, icon, ButtonStyle.Medium, slot, shortcut, statusTip
        )

    def addLargeToggleButton(
            self,
            text: str = None,
            icon: QtGui.QIcon = None,
            slot=None,
            shortcut=None,
            statusTip=None,
    ) -> ToolButton:
        return self.addToggleButton(
            text, icon, ButtonStyle.Large, slot, shortcut, statusTip
        )

    def addComboBox(
            self, items: typing.List[str], rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QComboBox:
        comboBox = QtWidgets.QComboBox(self)
        comboBox.addItems(items)
        self.addWidget(comboBox, rowSpan, colSpan)
        return comboBox

    def addFontComboBox(
            self, rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QFontComboBox:
        comboBox = QtWidgets.QFontComboBox(self)
        self.addWidget(comboBox, rowSpan, colSpan)
        return comboBox

    def addLineEdit(self, rowSpan: int = 2, colSpan: int = 1) -> QtWidgets.QLineEdit:
        lineEdit = QtWidgets.QLineEdit(self)
        self.addWidget(lineEdit, rowSpan, colSpan)
        return lineEdit

    def addTextEdit(self, rowSpan: int = 2, colSpan: int = 1) -> QtWidgets.QTextEdit:
        textEdit = QtWidgets.QTextEdit(self)
        self.addWidget(textEdit, rowSpan, colSpan)
        return textEdit

    def addPlainTextEdit(
            self, rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QPlainTextEdit:
        textEdit = QtWidgets.QPlainTextEdit(self)
        self.addWidget(textEdit, rowSpan, colSpan)
        return textEdit

    def addLabel(
            self, text: str, rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(self)
        label.setText(text)
        self.addWidget(label, rowSpan, colSpan)
        return label

    def addProgressBar(
            self, rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QProgressBar:
        progressBar = QtWidgets.QProgressBar(self)
        self.addWidget(progressBar, rowSpan, colSpan)
        return progressBar

    def addSlider(self, rowSpan: int = 2, colSpan: int = 1) -> QtWidgets.QSlider:
        slider = QtWidgets.QSlider(self)
        slider.setOrientation(QtCore.Qt.Horizontal)
        self.addWidget(slider, rowSpan, colSpan)
        return slider

    def addSpinBox(self, rowSpan: int = 2, colSpan: int = 1) -> QtWidgets.QSpinBox:
        spinBox = QtWidgets.QSpinBox(self)
        self.addWidget(spinBox, rowSpan, colSpan)
        return spinBox

    def addDoubleSpinBox(
            self, rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QDoubleSpinBox:
        doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.addWidget(doubleSpinBox, rowSpan, colSpan)
        return doubleSpinBox

    def addDateEdit(self, rowSpan: int = 2, colSpan: int = 1) -> QtWidgets.QDateEdit:
        dateEdit = QtWidgets.QDateEdit(self)
        self.addWidget(dateEdit, rowSpan, colSpan)
        return dateEdit

    def addTimeEdit(self, rowSpan: int = 2, colSpan: int = 1) -> QtWidgets.QTimeEdit:
        timeEdit = QtWidgets.QTimeEdit(self)
        self.addWidget(timeEdit, rowSpan, colSpan)
        return timeEdit

    def addDateTimeEdit(
            self, rowSpan: int = 2, colSpan: int = 1
    ) -> QtWidgets.QDateTimeEdit:
        dateTimeEdit = QtWidgets.QDateTimeEdit(self)
        self.addWidget(dateTimeEdit, rowSpan, colSpan)
        return dateTimeEdit

    def addTableWidget(
            self, rowSpan: int = 6, colSpan: int = 1
    ) -> QtWidgets.QTableWidget:
        tableWidget = QtWidgets.QTableWidget(self)
        self.addWidget(tableWidget, rowSpan, colSpan)
        return tableWidget

    def addTreeWidget(
            self, rowSpan: int = 6, colSpan: int = 1
    ) -> QtWidgets.QTreeWidget:
        treeWidget = QtWidgets.QTreeWidget(self)
        self.addWidget(treeWidget, rowSpan, colSpan)
        return treeWidget

    def addListWidget(
            self, rowSpan: int = 6, colSpan: int = 1
    ) -> QtWidgets.QListWidget:
        listWidget = QtWidgets.QListWidget(self)
        self.addWidget(listWidget, rowSpan, colSpan)
        return listWidget

    def addCalendarWidget(
            self, rowSpan: int = 6, colSpan: int = 1
    ) -> QtWidgets.QCalendarWidget:
        calendarWidget = QtWidgets.QCalendarWidget(self)
        self.addWidget(calendarWidget, rowSpan, colSpan)
        return calendarWidget

    def addSeparator(self, width=10) -> Separator:
        """Add a separator to the panel.

        :param width: The width of the separator.
        """
        separator = Separator(width=width)
        self.addWidget(separator, rowSpan=6, colSpan=1)
        return separator

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
