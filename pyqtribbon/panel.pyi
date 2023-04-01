from __future__ import annotations

from typing import List, Callable, overload, Any, Union, Iterable

import numpy as np
from qtpy import QtWidgets, QtGui, QtCore

from .constants import ColumnWise, RibbonButtonStyle, Large, Small
from .gallery import RibbonGallery
from .separator import RibbonSeparator
from .toolbutton import RibbonToolButton


class RibbonPanelTitle(QtWidgets.QLabel): ...

class RibbonGridLayoutManager(object):
    rows: int
    cells: np.ndarray

    def __init__(self, rows: int): ...
    def request_cells(self, rowSpan: int = 1, colSpan: int = 1, mode=ColumnWise): ...

class RibbonPanelItemWidget(QtWidgets.QFrame):
    def __init__(self, parent=None): ...
    def addWidget(self, widget): ...

class RibbonPanelOptionButton(QtWidgets.QToolButton): ...

class RibbonPanel(QtWidgets.QFrame):
    _maxRows: int = 6
    _largeRows: int = 6
    _mediumRows: int = 3
    _smallRows: int = 2
    _gridLayoutManager: RibbonGridLayoutManager
    _showPanelOptionButton: bool

    _widgets: List[QtWidgets.QWidget] = []

    _titleHeight: int = 20

    panelOptionClicked = QtCore.Signal(bool)

    _mainLayout: QtWidgets.QVBoxLayout
    _actionsLayout: QtWidgets.QGridLayout
    _titleWidget: QtWidgets.QWidget
    _titleLayout: QtWidgets.QHBoxLayout
    _titleLabel: RibbonPanelTitle
    _panelOption: RibbonPanelOptionButton

    @overload
    def __init__(self, title: str = "", maxRows: int = 6, showPanelOptionButton=True, parent=None): ...
    @overload
    def __init__(self, parent=None): ...
    def __init__(self, *args, **kwargs): ...
    def maximumRows(self) -> int: ...
    def largeRows(self) -> int: ...
    def mediumRows(self) -> int: ...
    def smallRows(self) -> int: ...
    def setMaximumRows(self, maxRows: int): ...
    def setLargeRows(self, rows: int): ...
    def setMediumRows(self, rows: int): ...
    def setSmallRows(self, rows: int): ...
    def defaultRowSpan(self, rowSpan: Union[int, RibbonButtonStyle]) -> int: ...
    def panelOptionButton(self) -> RibbonPanelOptionButton: ...
    def setPanelOptionToolTip(self, text: str): ...
    def rowHeight(self) -> int: ...
    def addWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def addSmallWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def addMediumWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def addLargeWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def removeWidget(self, widget: QtWidgets.QWidget): ...
    def widget(self, index: int) -> QtWidgets.QWidget: ...
    def widgets(self) -> List[QtWidgets.QWidget]: ...
    def addButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        rowSpan: RibbonButtonStyle = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addSmallButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addMediumButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addLargeButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        rowSpan: RibbonButtonStyle = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addSmallToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addMediumToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addLargeToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: QtGui.QKeySequence = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...

    ribbonArguments = ["rowSpan", "colSpan", "mode", "alignment", "fixedHeight"]

    def _addAnyWidget(
        self,
        *args,
        cls,
        initializer: Callable = None,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
        **kwargs,
    ) -> QtWidgets.QWidget: ...
    def __getattr__(self, method: str) -> Callable: ...
    def addComboBox(
        self,
        items: Iterable[str],
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QComboBox: ...
    addSmallComboBox = addComboBox
    addMediumComboBox = addComboBox
    addLargeComboBox = addComboBox
    def addFontComboBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QFontComboBox: ...
    addSmallFontComboBox = addFontComboBox
    addMediumFontComboBox = addFontComboBox
    addLargeFontComboBox = addFontComboBox
    def addLineEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QLineEdit: ...
    addSmallLineEdit = addLineEdit
    addMediumLineEdit = addLineEdit
    addLargeLineEdit = addLineEdit
    def addTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTextEdit: ...
    addSmallTextEdit = addTextEdit
    addMediumTextEdit = addTextEdit
    addLargeTextEdit = addTextEdit
    def addPlainTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QPlainTextEdit: ...
    addSmallPlainTextEdit = addPlainTextEdit
    addMediumPlainTextEdit = addPlainTextEdit
    addLargePlainTextEdit = addPlainTextEdit
    def addLabel(
        self,
        text: str,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QLabel: ...
    addSmallLabel = addLabel
    addMediumLabel = addLabel
    addLargeLabel = addLabel
    def addProgressBar(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QProgressBar: ...
    addSmallProgressBar = addProgressBar
    addMediumProgressBar = addProgressBar
    addLargeProgressBar = addProgressBar
    def addSlider(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QSlider: ...
    addSmallSlider = addSlider
    addMediumSlider = addSlider
    addLargeSlider = addSlider
    def addSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QSpinBox: ...
    addSmallSpinBox = addSpinBox
    addMediumSpinBox = addSpinBox
    addLargeSpinBox = addSpinBox
    def addDoubleSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDoubleSpinBox: ...
    addSmallDoubleSpinBox = addDoubleSpinBox
    addMediumDoubleSpinBox = addDoubleSpinBox
    addLargeDoubleSpinBox = addDoubleSpinBox
    def addDateEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDateEdit: ...
    addSmallDateEdit = addDateEdit
    addMediumDateEdit = addDateEdit
    addLargeDateEdit = addDateEdit
    def addTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTimeEdit: ...
    addSmallTimeEdit = addTimeEdit
    addMediumTimeEdit = addTimeEdit
    addLargeTimeEdit = addTimeEdit
    def addDateTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDateTimeEdit: ...
    addSmallDateTimeEdit = addDateTimeEdit
    addMediumDateTimeEdit = addDateTimeEdit
    addLargeDateTimeEdit = addDateTimeEdit
    def addTableWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTableWidget: ...
    addSmallTableWidget = addTableWidget
    addMediumTableWidget = addTableWidget
    addLargeTableWidget = addTableWidget
    def addTreeWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTreeWidget: ...
    addSmallTreeWidget = addTreeWidget
    addMediumTreeWidget = addTreeWidget
    addLargeTreeWidget = addTreeWidget
    def addListWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QListWidget: ...
    addSmallListWidget = addListWidget
    addMediumListWidget = addListWidget
    addLargeListWidget = addListWidget
    def addCalendarWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QCalendarWidget: ...
    addSmallCalendarWidget = addCalendarWidget
    addMediumCalendarWidget = addCalendarWidget
    addLargeCalendarWidget = addCalendarWidget
    def addSeparator(
        self,
        orientation=QtCore.Qt.Vertical,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonSeparator: ...
    addSmallSeparator = addSeparator
    addMediumSeparator = addSeparator
    addLargeSeparator = addSeparator
    def addHorizontalSeparator(
        self,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 2,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonSeparator: ...
    addSmallHorizontalSeparator = addHorizontalSeparator
    addMediumHorizontalSeparator = addHorizontalSeparator
    addLargeHorizontalSeparator = addHorizontalSeparator
    def addVerticalSeparator(
        self,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonSeparator: ...
    addSmallVerticalSeparator = addVerticalSeparator
    addMediumVerticalSeparator = addVerticalSeparator
    addLargeVerticalSeparator = addVerticalSeparator
    def addGallery(
        self,
        minimumWidth=800,
        popupHideOnClick=False,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonGallery: ...
    addSmallGallery = addGallery
    addMediumGallery = addGallery
    addLargeGallery = addGallery
    def setTitle(self, title: str): ...
    def title(self) -> str: ...
