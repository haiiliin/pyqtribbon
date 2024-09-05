//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_GALLERY_HPP
#define QTRIBBON_GALLERY_HPP

#include <QAction>
#include <QApplication>
#include <QFrame>
#include <QHBoxLayout>
#include <QIcon>
#include <QListWidget>
#include <QListWidgetItem>
#include <QResizeEvent>
#include <QScrollBar>
#include <QSize>
#include <QToolButton>
#include <QVBoxLayout>
#include <tuple>

#include "menu.hpp"
#include "separator.hpp"
#include "toolbutton.hpp"

namespace qtribbon {

class RibbonPopupWidget : public QFrame {
    Q_OBJECT

   public:
    explicit RibbonPopupWidget(QWidget *parent = nullptr) : QFrame(parent) {}
    ~RibbonPopupWidget() override = default;
};

class RibbonGalleryListWidget : public QListWidget {
    Q_OBJECT

   public:
    explicit RibbonGalleryListWidget(QWidget *parent = nullptr) : QListWidget(parent) {
        setViewMode(QListWidget::IconMode);
        setResizeMode(QListWidget::Adjust);
        setVerticalScrollMode(QListWidget::ScrollPerPixel);
        setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        setIconSize(QSize(64, 64));
    }
    ~RibbonGalleryListWidget() override = default;

    void resizeEvent(QResizeEvent *e) override {
        // Resize the list widget.
        QListWidget::resizeEvent(e);
    }

    void scrollToNextRow() {
        // Scroll to the next row.
        verticalScrollBar()->setValue(verticalScrollBar()->value() + verticalScrollBar()->singleStep());
    }

    void scrollToPreviousRow() {
        // Scroll to the previous row.
        verticalScrollBar()->setValue(verticalScrollBar()->value() - verticalScrollBar()->singleStep());
    }
};

class RibbonGalleryButton : public QToolButton {
    Q_OBJECT

   public:
    explicit RibbonGalleryButton(QWidget *parent = nullptr) : QToolButton(parent) {}
    ~RibbonGalleryButton() override = default;
};

class RibbonGalleryPopupListWidget : public RibbonGalleryListWidget {
    Q_OBJECT

   public:
    explicit RibbonGalleryPopupListWidget(QWidget *parent = nullptr) : RibbonGalleryListWidget(parent) {
        setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
    }
    ~RibbonGalleryPopupListWidget() override = default;
};

class RibbonGallery : public QFrame {
    Q_OBJECT

   private:
    QSize _popupWindowSize;
    QList<RibbonToolButton *> _buttons;
    QList<RibbonToolButton *> _popupButtons;
    bool _popupHideOnClick;
    QHBoxLayout *_mainLayout;
    QVBoxLayout *_scrollButtonLayout;
    RibbonGalleryButton *_upButton;
    RibbonGalleryButton *_downButton;
    RibbonGalleryButton *_moreButton;
    RibbonGalleryListWidget *_listWidget;
    RibbonPopupWidget *_popupWidget;
    QVBoxLayout *_popupLayout;
    RibbonGalleryPopupListWidget *_popupListWidget;
    RibbonPermanentMenu *_popupMenu;

   public:
    explicit RibbonGallery(QWidget *parent = nullptr) : RibbonGallery(800, false, parent) {}

    explicit RibbonGallery(int minimumWidth = 800, bool popupHideOnClick = false, QWidget *parent = nullptr)
        : QFrame(parent) {
        setMinimumWidth(minimumWidth);
        _popupHideOnClick = popupHideOnClick;

        _mainLayout = new QHBoxLayout(this);
        _mainLayout->setContentsMargins(5, 5, 5, 5);
        _mainLayout->setSpacing(5);

        _upButton = new RibbonGalleryButton(this);
        _upButton->setIcon(QIcon(":/icons/up.png"));
        _upButton->setIconSize(QSize(24, 24));
        _upButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
        _upButton->setAutoRaise(true);

        _downButton = new RibbonGalleryButton(this);
        _downButton->setIcon(QIcon(":/icons/down.png"));
        _downButton->setIconSize(QSize(24, 24));
        _downButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
        _downButton->setAutoRaise(true);

        _moreButton = new RibbonGalleryButton(this);
        _moreButton->setIcon(QIcon(":/icons/more.png"));
        _moreButton->setIconSize(QSize(24, 24));
        _moreButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
        _moreButton->setAutoRaise(true);

        _scrollButtonLayout = new QVBoxLayout();
        _scrollButtonLayout->setContentsMargins(0, 0, 0, 0);
        _scrollButtonLayout->setSpacing(2);
        _scrollButtonLayout->addWidget(_upButton);
        _scrollButtonLayout->addWidget(_downButton);
        _scrollButtonLayout->addWidget(_moreButton);

        _listWidget = new RibbonGalleryListWidget();
        _mainLayout->addWidget(_listWidget);
        _mainLayout->addLayout(_scrollButtonLayout);

        connect(_upButton, &RibbonGalleryButton::clicked, _listWidget, &RibbonGalleryListWidget::scrollToPreviousRow);
        connect(_downButton, &RibbonGalleryButton::clicked, _listWidget, &RibbonGalleryListWidget::scrollToNextRow);

        _popupWidget = new RibbonPopupWidget();
        _popupWidget->setFont(qApp->font());
        _popupWidget->setWindowFlags(Qt::Popup);

        _popupLayout = new QVBoxLayout(_popupWidget);
        _popupLayout->setContentsMargins(5, 5, 5, 5);
        _popupLayout->setSpacing(2);

        _popupListWidget = new RibbonGalleryPopupListWidget();
        _popupLayout->addWidget(_popupListWidget);
        _popupLayout->addWidget(new RibbonHorizontalSeparator());

        _popupMenu = new RibbonPermanentMenu();
        _popupMenu->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Minimum);
        connect(_popupMenu, SIGNAL(actionAdded), this, SLOT(_handlePopupAction));
        _popupLayout->addWidget(_popupMenu);

        connect(_moreButton, &RibbonGalleryButton::clicked, this, &RibbonGallery::showPopup);
    }

    ~RibbonGallery() override = default;

    void _handlePopupAction(QAction *action) const {
        if (action != nullptr) {
            connect(action, &QAction::triggered, this, &RibbonGallery::hidePopupWidget);
        }
    }

    void resizeEvent(QResizeEvent *event) override {
        int height = this->height() - _mainLayout->contentsMargins().top() - _mainLayout->contentsMargins().bottom();
        _upButton->setFixedSize(height / 4, height / 3);
        _downButton->setFixedSize(height / 4, height / 3);
        _moreButton->setFixedSize(height / 4, height / 3);
        QFrame::resizeEvent(event);
    }

    RibbonPermanentMenu *popupMenu() { return _popupMenu; }

    void showPopup() {
        _popupWidget->move(mapToGlobal(geometry().topLeft()));
        _popupWidget->resize(
            QSize(std::max(popupWindowSize().width(), width()), std::max(popupWindowSize().height(), height())));
        _popupMenu->setFixedWidth(_popupWidget->width() - _popupLayout->contentsMargins().left() -
                                  _popupLayout->contentsMargins().right());
        _popupWidget->show();
    }

    void hidePopupWidget() { _popupWidget->hide(); }

    QSize popupWindowSize() { return _popupWindowSize; }

    void setPopupWindowSize(QSize size) { _popupWindowSize = size; }

    void setSelectedButton() {
        auto *button = qobject_cast<RibbonToolButton *>(sender());
        if (button != nullptr) {
            int row = _popupButtons.indexOf(button);
            _listWidget->scrollTo(_listWidget->model()->index(row, 0), QAbstractItemView::EnsureVisible);
            if (_buttons[row]->isCheckable()) {
                _buttons[row]->setChecked(!_buttons[row]->isChecked());
            }
        }
    }

    void _addWidget(QWidget *widget) {
        auto *item = new QListWidgetItem();
        item->setSizeHint(widget->sizeHint());
        _listWidget->setSpacing((height() - item->sizeHint().height()) / 2);
        _listWidget->addItem(item);
        _listWidget->setItemWidget(item, widget);
    }

    void _addPopupWidget(QWidget *widget) {
        auto *item = new QListWidgetItem();
        item->setSizeHint(widget->sizeHint());
        _popupListWidget->setSpacing((height() - item->sizeHint().height()) / 2);
        _popupListWidget->addItem(item);
        _popupListWidget->setItemWidget(item, widget);
    }

    void setPopupHideOnClick(bool popupHideOnClick) { _popupHideOnClick = popupHideOnClick; }

    std::tuple<RibbonToolButton *, RibbonToolButton *> addButton(const QString &text = "", const QIcon &icon = QIcon(),
                                                                 const QKeySequence &shortcut = QKeySequence(),
                                                                 const QString &tooltip = "",
                                                                 const QString &statusTip = "",
                                                                 bool checkable = false) {
        auto *button = new RibbonToolButton(this);
        auto *popupButton = new RibbonToolButton(_popupWidget);
        if (!text.isEmpty()) {
            button->setText(text);
            popupButton->setText(text);
        }
        if (!icon.isNull()) {
            button->setIcon(icon);
            popupButton->setIcon(icon);
        }
        if (!shortcut.isEmpty()) {
            button->setShortcut(shortcut);
            popupButton->setShortcut(shortcut);
        }
        if (!tooltip.isEmpty()) {
            button->setToolTip(tooltip);
            popupButton->setToolTip(tooltip);
        }
        if (!statusTip.isEmpty()) {
            button->setStatusTip(statusTip);
            popupButton->setStatusTip(statusTip);
        }
        if (checkable) {
            button->setCheckable(true);
            popupButton->setCheckable(true);
        }
        _buttons.append(button);
        _popupButtons.append(popupButton);
        connect(button, &RibbonToolButton::clicked, [popupButton](bool checked) { popupButton->setChecked(checked); });
        if (_popupHideOnClick) connect(popupButton, &RibbonToolButton::clicked, this, &RibbonGallery::hidePopupWidget);

        connect(popupButton, &RibbonToolButton::clicked, this, &RibbonGallery::setSelectedButton);

        if (text.isEmpty()) {
            button->setToolButtonStyle(Qt::ToolButtonIconOnly);
            popupButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
        } else {
            button->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
            popupButton->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
        }
        _addWidget(button);
        _addPopupWidget(popupButton);
        return std::make_tuple(button, popupButton);
    }

    std::tuple<RibbonToolButton *, RibbonToolButton *> addToggleButton(const QString &text = "",
                                                                       const QIcon &icon = QIcon(),
                                                                       const QKeySequence &shortcut = QKeySequence(),
                                                                       const QString &tooltip = "",
                                                                       const QString &statusTip = "") {
        return addButton(text, icon, shortcut, tooltip, statusTip, true);
    }
};

}  // namespace qtribbon

#endif  // QTRIBBON_GALLERY_HPP
