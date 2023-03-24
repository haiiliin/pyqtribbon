from __future__ import annotations

from enum import IntEnum
from typing import List, Callable, overload, Any, Union, Dict

import numpy as np
from qtpy import QtWidgets, QtGui, QtCore

from .gallery import RibbonGallery
from .separator import RibbonSeparator
from .toolbutton import RibbonToolButton, RibbonButtonStyle, Large, Small

class RibbonPanelTitle(QtWidgets.QLabel): ...

class RibbonSpaceFindMode(IntEnum):
    ColumnWise = 0
    RowWise = 1

ColumnWise = ColumnWise
RowWise = RibbonSpaceFindMode.RowWise

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
    def addWidgetsBy(self, data: Dict[str, Dict]) -> Dict[str, QtWidgets.QWidget]: ...
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

    def addAnyWidget(self, *args, cls, initializer: Callable = None, **kwargs) -> QtWidgets.QWidget: ...
    def addComboBox(
        self,
        items: List[str],
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QComboBox: ...
    def addFontComboBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QFontComboBox: ...
    def addLineEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QLineEdit: ...
    def addTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTextEdit: ...
    def addPlainTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QPlainTextEdit: ...
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
    def addProgressBar(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QProgressBar: ...
    def addSlider(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QSlider: ...
    def addSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QSpinBox: ...
    def addDoubleSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDoubleSpinBox: ...
    def addDateEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDateEdit: ...
    def addTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTimeEdit: ...
    def addDateTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDateTimeEdit: ...
    def addTableWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTableWidget: ...
    def addTreeWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTreeWidget: ...
    def addListWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QListWidget: ...
    def addCalendarWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode=ColumnWise,
        alignment=QtCore.Qt.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QCalendarWidget: ...
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
    def setTitle(self, title: str): ...
    def title(self) -> str: ...
