import typing
from enum import Enum

from PyQt5.QtCore import (
    QAbstractListModel,
    QItemSelectionModel,
    QModelIndex,
    QRect,
    QSize,
    Qt,
    QVariant,
    pyqtSignal,
    QPoint,
)
from PyQt5.QtGui import QIcon, QPainter, QPaintEvent, QResizeEvent
from PyQt5.QtWidgets import (
    QAction,
    QListView,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QActionGroup,
    QApplication,
    QFrame,
    QScrollBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QToolButton,
)
from .typehints import PyQtSignalType


class GalleryItem:
    _data: dict[int, QVariant]
    _flags: Qt.ItemFlags
    _action: QAction

    def __init__(self, icon_or_action: typing.Union[QIcon, QAction] = None) -> None:
        self._flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        self._action = QAction()
        self._data = {}
        if isinstance(icon_or_action, QIcon):
            self.setIcon(icon_or_action)
        elif isinstance(icon_or_action, QAction):
            self.setAction(icon_or_action)

    # 设置角色
    def setData(self, role: int, data: QVariant) -> None:
        self._data[role] = data

    def data(self, role: int) -> QVariant:
        if self._action:
            if role == Qt.DisplayRole:
                return self._action.text()
            elif role == Qt.ToolTipRole:
                return self._action.toolTip()
            elif role == Qt.DecorationRole:
                return self._action.icon()
        return self._data[role]

    # 设置文字描述
    def setText(self, text: str) -> None:
        self.setData(Qt.DisplayRole, QVariant(text))

    def text(self) -> str:
        if self._action:
            return self._action.text()
        return str(self.data(Qt.DisplayRole))

    # 设置tooltip
    def setToolTip(self, text: str) -> None:
        self.setData(Qt.ToolTipRole, QVariant(text))

    def toolTip(self) -> str:
        if self._action:
            return self._action.text()
        return str(self.data(Qt.ToolTipRole))

    # 设置图标
    def setIcon(self, icon: QIcon) -> None:
        self.setData(Qt.DecorationRole, icon)

    def icon(self) -> QIcon:
        if self._action:
            return self._action.icon()
        return self.data(Qt.DecorationRole)

    # 设置是否可见
    def isSelectable(self) -> bool:
        return self._flags and Qt.ItemIsSelectable

    def setSelectable(self, isSelectable: bool) -> None:
        if isSelectable:
            self._flags |= Qt.ItemIsSelectable
        else:
            self._flags &= not Qt.ItemIsSelectable

    # 设置是否可选
    def isEnable(self) -> bool:
        if self._action:
            return self._action.isEnabled()
        return self._flags and Qt.ItemIsEnabled

    def setEnable(self, isEnable: bool) -> None:
        if self._action:
            self._action.setEnabled(isEnable)

        if isEnable:
            self._flags |= Qt.ItemIsEnabled
        else:
            self._flags &= not Qt.ItemIsEnabled

    # 设置item的flag
    def setFlags(self, flags: Qt.ItemFlags) -> None:
        self._flags = flags
        if self._action:
            self._action.setEnabled(flags and Qt.ItemIsEnabled)

    def flags(self) -> Qt.ItemFlags:
        return self._flags

    # 设置action
    def setAction(self, action: QAction) -> None:
        self._action = action
        if action.isEnabled():
            self._flags |= Qt.ItemIsEnabled
        else:
            self._flags &= not Qt.ItemIsEnabled

    def action(self) -> QAction:
        return self._action


class GalleryGroupItemDelegate(QStyledItemDelegate):
    _group: "GalleryGroup"

    def __init__(self, group: "GalleryGroup", parent=None) -> None:
        super().__init__(parent)
        self._group = group

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        if self._group is None:
            return
        if self._group.enableIconText():
            self.paintIconWithText(painter, option, index)
        else:
            self.paintIconOnly(painter, option, index)

    def paintIconOnly(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        style = self._group.style()
        painter.save()
        painter.setClipRect(option.rect)
        style.drawPrimitive(QStyle.PE_PanelItemViewItem, option, painter, self._group)
        # draw the icon
        iconRect: QRect = option.rect
        iconRect.adjust(3, 3, -3, -3)

        icon = index.data(Qt.DecorationRole)  # type: QIcon
        icon.paint(painter, iconRect, Qt.AlignCenter, QIcon.Normal, QIcon.On)
        painter.restore()

    def paintIconWithText(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        super().paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        # option.rect对应grid size
        return QSize(option.rect.width(), option.rect.height())


class GalleryGroupModel(QAbstractListModel):
    _items: list[GalleryItem]

    def __init__(self, parent=None) -> None:
        super(QAbstractListModel, self).__init__(parent=parent)
        self._items = []

    def rowCount(self, parent: QModelIndex = None) -> int:
        return 0 if parent.isValid() else len(self._items)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid() or index.row() >= len(self._items):
            return Qt.NoItemFlags
        return self._items[index.row()].flags()

    def data(self, index: QModelIndex, role: int = None) -> QVariant:
        if not index.isValid() or index.row() >= len(self._items):
            return QVariant()
        return self._items[index.row()].data(role)

    def index(
        self, row: int, column: int = 0, parent: QModelIndex = None
    ) -> QModelIndex:
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column, self._items[row])
        return QModelIndex()

    def setData(self, index: QModelIndex, value: QVariant, role: int = None) -> bool:
        if not index.isValid() or index.row() >= len(self._items):
            return False
        self._items[index.row()].setData(role, value)
        return True

    def clear(self) -> None:
        self.beginResetModel()
        del self._items
        self.endResetModel()

    def itemAt(self, row: int) -> GalleryItem:
        return self._items[row]

    def insert(self, row: int, item: GalleryItem) -> None:
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.insert(row, item)
        self.endInsertRows()

    def take(self, row: int) -> GalleryItem:
        if row < 0 or row > len(self._items):
            raise ValueError("row = {row} out of range".format(row=row))
        self.beginRemoveRows(QModelIndex(), row, row)
        item = self._items[row]
        del self._items[row]
        self.endRemoveRows()
        return item

    def append(self, item: GalleryItem) -> None:
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items) + 1)
        self._items.append(item)
        self.endInsertRows()


class PreinstallStyle(Enum):
    LargeIconWithText = 0  # 大图标带文字
    LargeIconOnly = 1


class GalleryGroup(QListView):
    groupTitleChanged = pyqtSignal(str)  # type: PyQtSignalType

    _enableIconText: bool = False
    _groupTitle: str = ""
    clicked: PyQtSignalType

    def __init__(self, parent=None) -> None:
        super(GalleryGroup, self).__init__(parent=parent)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionRectVisible(True)
        self.setUniformItemSizes(True)
        self.setPreinstallStyle(PreinstallStyle.LargeIconWithText)
        self.setItemDelegate(GalleryGroupItemDelegate(self, self))
        self.clicked.connect(self.onItemClicked)

        self._enableIconText = False
        self._groupTitle = ""

    def setPreinstallStyle(self, style: PreinstallStyle) -> None:
        if style == PreinstallStyle.LargeIconWithText:
            self.setIconSize(QSize(72, 36))
            self.setGridSize(QSize(72, 56))
            self.setEnableIconText(True)
        elif style == PreinstallStyle.LargeIconOnly:
            self.setIconSize(QSize(72, 56))
            self.setGridSize(QSize(72, 56))
            self.setEnableIconText(False)
        else:
            self.setIconSize(QSize(72, 36))
            self.setGridSize(QSize(72, 56))
            self.setEnableIconText(True)

    def addItem(self, icon_or_item: typing.Union[QIcon, GalleryItem]) -> None:
        galleryItem = (
            GalleryItem(icon_or_item)
            if isinstance(icon_or_item, QIcon)
            else icon_or_item
        )
        # self.model().append(galleryItem)
        if self.groupModel() is not None:
            self.groupModel().append(galleryItem)

    def addActionItem(self, action: QAction) -> None:
        if self.groupModel() is not None:
            self.groupModel().append(GalleryItem(action))

    def addActionItemList(self, actions: list[QAction]) -> None:
        model = self.groupModel()
        if model is not None:
            for action in actions:
                model.append(GalleryItem(action))

    def setupGroupModel(self) -> None:
        self.setModel(GalleryGroupModel(self))

    def groupModel(self) -> GalleryGroupModel:
        # return sip.cast(self.model(), GalleryGroupModel)
        return self.model()

    def setEnableIconText(self, enable: bool) -> None:
        self._enableIconText = enable

    def enableIconText(self) -> bool:
        return self._enableIconText

    def setGroupTitle(self, title: str) -> None:
        self._groupTitle = title
        self.groupTitleChanged.emit(self._groupTitle)

    def groupTitle(self) -> str:
        return self._groupTitle

    def selectByIndex(self, i: int) -> None:
        model = self.groupModel()
        if model is None:
            return
        ind: QModelIndex = model.index(i, 0, QModelIndex())
        selectionModel: QItemSelectionModel = self.selectionModel()
        if selectionModel:
            selectionModel.select(ind, QItemSelectionModel.SelectCurrent)

    def onItemClicked(self, index: QModelIndex) -> None:
        if index.isValid():
            # item: GalleryItem = sip.cast(index.internalPointer(), GalleryItem)
            item = self.groupModel().itemAt(index.row())
            try:
                item.action().activate(QAction.Trigger)
            except ValueError:
                pass


class GalleryPopupWidget(QWidget):
    _layout: QVBoxLayout
    _groups: list[GalleryGroup] = []

    def __init__(self, parent=None) -> None:
        super(GalleryPopupWidget, self).__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(1, 1, 1, 1)

    def addGalleryGroup(self, group: GalleryGroup) -> None:
        self._layout.addWidget(group)
        self._groups.append(group)

    def groupAt(self, index: int) -> GalleryGroup:
        return self._groups[index]


class Gallery(QFrame):
    triggered = pyqtSignal(QAction)
    hovered = pyqtSignal(QAction)

    def __init__(self, parent=None) -> None:
        super(Gallery, self).__init__(parent=parent)
        self.setFrameShape(QFrame.Box)
        self.setFixedHeight(60)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(88)

        # private members
        self._popupWidget = GalleryPopupWidget(self)
        self._viewportGroup = GalleryGroup(self)
        self._buttonUp = QToolButton(self)
        self._buttonDown = QToolButton(self)
        self._buttonMore = QToolButton(self)
        self._actionGroup = QActionGroup(self)

        self._buttonUp.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self._buttonDown.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self._buttonMore.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self._buttonUp.setObjectName("RibbonGalleryButtonUp")
        self._buttonDown.setObjectName("RibbonGalleryButtonDown")
        self._buttonMore.setObjectName("RibbonGalleryButtonMore")
        self._buttonUp.setFixedSize(15, 20)
        self._buttonDown.setFixedSize(15, 20)
        self._buttonMore.setFixedSize(15, 20)
        self._buttonUp.setIcon(QIcon("icons/ArrowUp.png"))
        self._buttonDown.setIcon(QIcon("icons/ArrowDown.png"))
        self._buttonMore.setIcon(QIcon("icons/ArrowMore.png"))

        self._buttonUp.clicked.connect(self.onPageUp)
        self._buttonDown.clicked.connect(self.onPageDown)
        self._buttonMore.clicked.connect(self.onShowMoreDetail)
        self._actionGroup.triggered.connect(self.triggered)
        self._actionGroup.hovered.connect(self.hovered)

    def sizeHint(self) -> QSize:
        return QSize(232, 60)

    def minimumSizeHint(self) -> QSize:
        return QSize(88, 60)

    def addGalleryGroup(self, group: GalleryGroup = None) -> GalleryGroup:
        group = GalleryGroup(self) if group is None else group
        viewport = self.ensureGetPopupViewPort()
        model = GalleryGroupModel(self)
        group.setModel(model)
        viewport.addGalleryGroup(group)
        if self._viewportGroup is None:
            self.setCurrentViewGroup(group)
        group.clicked.connect(self.onItemClicked)
        return group

    def addCategoryActions(self, title: str, actions: list[QAction]) -> "GalleryGroup":
        group = GalleryGroup(self)
        model = GalleryGroupModel(self)
        group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        group.setModel(model)
        if not len(title) == 0:
            group.setGroupTitle(title)
        for action in actions:
            self._actionGroup.addAction(action)
        group.addActionItemList(actions)
        group.clicked.connect(self.onItemClicked)
        viewport = self.ensureGetPopupViewPort()
        viewport.addGalleryGroup(group)
        self.setCurrentViewGroup(group)
        return group

    def setCurrentViewGroup(self, group: "GalleryGroup") -> None:
        if self._viewportGroup is None:
            self._viewportGroup = GalleryGroup(self)
        self._viewportGroup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._viewportGroup.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._viewportGroup.setModel(group.model())
        self._viewportGroup.setEnableIconText(group.enableIconText())
        self._viewportGroup.show()
        QApplication.postEvent(self, QResizeEvent(self.size(), self.size()))

    def currentViewGroup(self) -> "GalleryGroup":
        return self._viewportGroup

    def actionGroup(self) -> QActionGroup:
        return self._actionGroup

    def onPageDown(self) -> None:
        if self._viewportGroup is not None:
            vScrollBar: QScrollBar = self._viewportGroup.verticalScrollBar()
            v: int = vScrollBar.value()
            v += vScrollBar.singleStep()
            vScrollBar.setValue(v)

    def onPageUp(self) -> None:
        if self._viewportGroup is not None:
            vScrollBar = self._viewportGroup.verticalScrollBar()
            v: int = vScrollBar.value()
            v -= vScrollBar.singleStep()
            vScrollBar.setValue(v)

    def onShowMoreDetail(self) -> None:
        if self._popupWidget is None:
            return
        popupMenuSize = self._popupWidget.minimumSizeHint()  # sizeHint()
        start: QPoint = self.mapToGlobal(QPoint(0, 0))
        self._popupWidget.setGeometry(
            start.x(), start.y(), self.width(), popupMenuSize.height()
        )
        self._popupWidget.show()

    def onItemClicked(self, index: QModelIndex) -> None:
        group = self.ensureGetPopupViewPort().groupAt(index.row())

        if group is not None:
            curGroup = self.currentViewGroup()
            if curGroup is None:
                self.setCurrentViewGroup(group)
                curGroup = self.currentViewGroup()
            if not curGroup.model() == group.model():
                curGroup.setModel(group.model())
            curGroup.scrollTo(index)
            curGroup.setCurrentIndex(index)
            curGroup.repaint()

    def ensureGetPopupViewPort(self) -> GalleryPopupWidget:
        if self._popupWidget is None:
            self._popupWidget = GalleryPopupWidget(self)
        return self._popupWidget

    def resizeEvent(self, event: QResizeEvent) -> None:
        size = event.size()
        subW = 0
        self._buttonUp.move(size.width() - self._buttonUp.width(), 0)
        subW = max(subW, self._buttonUp.width())
        self._buttonDown.move(
            size.width() - self._buttonDown.width(), self._buttonUp.height()
        )
        subW = max(subW, self._buttonDown.width())
        self._buttonMore.move(
            size.width() - self._buttonMore.width(),
            self._buttonDown.geometry().bottom(),
        )
        subW = max(subW, self._buttonMore.width())
        if self._viewportGroup is not None:
            self._viewportGroup.setGeometry(0, 0, size.width() - subW, size.height())
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
