//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_TITLEWIDGET_HPP
#define QTRIBBON_TITLEWIDGET_HPP

#include <QFrame>
#include <QHBoxLayout>
#include <QIcon>
#include <QLabel>
#include <QMouseEvent>
#include <QTabBar>
#include <QToolBar>
#include <QToolButton>

#include "menu.hpp"
#include "tabbar.hpp"

namespace qtribbon {

class RibbonApplicationButton : public QToolButton {
    Q_OBJECT

   public:
    explicit RibbonApplicationButton(QWidget *parent = nullptr) : QToolButton(parent) {}
    ~RibbonApplicationButton() override = default;

    RibbonMenu *addFileMenu() {
        auto *menu = new RibbonMenu(this);
        this->setPopupMode(QToolButton::InstantPopup);
        this->setMenu(menu);
        return menu;
    }
};

class RibbonTitleLabel : public QLabel {
    Q_OBJECT

   public:
    explicit RibbonTitleLabel(QWidget *parent = nullptr) : QLabel(parent) {}
    ~RibbonTitleLabel() override = default;
};

class RibbonTitleWidget : public QFrame {
    Q_OBJECT

   private:
    RibbonApplicationButton *_applicationButton;
    QToolBar *_quickAccessToolBar;
    QWidget *_quickAccessToolBarWidget;
    QHBoxLayout *_quickAccessToolBarLayout;
    QToolBar *_rightToolBar;
    QToolButton *_collapseRibbonButton;
    QToolButton *_helpButton;
    RibbonTabBar *_tabBar;
    RibbonTitleLabel *_titleLabel;
    QHBoxLayout *_tabBarLayout;
    QList<QToolButton *> _quickAccessButtons;
    QList<QToolButton *> _rightToolButtons;

    int _quickAccessButtonHeight = 20;
    int _rightButtonHeight = 20;

    QPoint _start_point;
    QPoint _window_point;

   signals:
    void helpButtonClicked(bool checked);
    void collapseRibbonButtonClicked(bool checked);

   public:
    explicit RibbonTitleWidget(QWidget *parent = nullptr) : RibbonTitleWidget("QtRibbon", parent) {}
    explicit RibbonTitleWidget(const QString &title = "QtRibbon", QWidget *parent = nullptr) : QFrame(parent) {
        // Set up the layout
        this->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
        this->_tabBarLayout = new QHBoxLayout(this);
        this->_tabBarLayout->setContentsMargins(0, 0, 0, 0);
        this->_tabBarLayout->setSpacing(0);

        // Set up the application button
        this->_applicationButton = new RibbonApplicationButton();
        this->_applicationButton->setIcon(QIcon(":/icons/python.png"));
        this->_applicationButton->setIconSize(QSize(this->_quickAccessButtonHeight, this->_quickAccessButtonHeight));
        this->_applicationButton->setText("QtRibbon");
        this->_applicationButton->setToolTip("QtRibbon");

        // Set up the quick access toolbar
        this->_quickAccessToolBar = new QToolBar();
        this->_quickAccessToolBar->setIconSize(QSize(this->_quickAccessButtonHeight, this->_quickAccessButtonHeight));
        this->_quickAccessToolBar->setOrientation(Qt::Horizontal);
        this->_quickAccessToolBar->setMovable(false);
        this->_quickAccessToolBar->addWidget(this->_applicationButton);
        this->_quickAccessToolBarWidget = new QWidget();
        this->_quickAccessToolBarLayout = new QHBoxLayout(this->_quickAccessToolBarWidget);
        this->_quickAccessToolBarLayout->setContentsMargins(0, 0, 0, 0);
        this->_quickAccessToolBarLayout->setSpacing(0);
        this->_quickAccessToolBarLayout->addWidget(this->_quickAccessToolBar, 0, Qt::AlignBottom);

        // Set up the right toolbar
        this->_rightToolBar = new QToolBar();
        this->_rightToolBar->setOrientation(Qt::Horizontal);
        this->_rightToolBar->setIconSize(QSize(this->_rightButtonHeight, this->_rightButtonHeight));
        this->_collapseRibbonButton = new QToolButton();
        this->_collapseRibbonButton->setIconSize(QSize(this->_rightButtonHeight, this->_rightButtonHeight));
        this->_collapseRibbonButton->setIcon(QIcon(":/icons/up.png"));
        this->_collapseRibbonButton->setAutoRaise(true);
        this->_collapseRibbonButton->setToolTip("Collapse Ribbon");
        connect(this->_collapseRibbonButton, &QToolButton::clicked, this,
                &RibbonTitleWidget::collapseRibbonButtonClicked);
        this->_helpButton = new QToolButton();
        this->_helpButton->setIconSize(QSize(this->_rightButtonHeight, this->_rightButtonHeight));
        this->_helpButton->setIcon(QIcon(":/icons/help.png"));
        this->_helpButton->setAutoRaise(true);
        this->_helpButton->setToolTip("Help");
        connect(this->_helpButton, SIGNAL(clicked(bool)), this, SIGNAL(helpButtonClicked(bool)));
        this->addRightToolButton(this->_collapseRibbonButton);
        this->addRightToolButton(this->_helpButton);

        // Set up the category tab bar
        this->_tabBar = new RibbonTabBar(this);
        this->_tabBar->setExpanding(false);
        this->_tabBar->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
        QFont font = this->_tabBar->font();
        font.setPointSize(font.pointSize() + 3);
        this->_tabBar->setFont(font);
        this->_tabBar->setShape(QTabBar::RoundedNorth);
        this->_tabBar->setDocumentMode(true);

        // Set up the title label
        this->_titleLabel = new RibbonTitleLabel(this);
        this->_titleLabel->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
        this->_titleLabel->setAlignment(Qt::AlignCenter | Qt::AlignBottom);
        this->_titleLabel->setText(title);
        font = this->_titleLabel->font();
        font.setPointSize(font.pointSize() + 3);
        this->_titleLabel->setFont(font);

        // Add widgets to the layout
        this->_tabBarLayout->addWidget(this->_quickAccessToolBarWidget, 0, Qt::AlignVCenter);
        this->_tabBarLayout->addWidget(this->_tabBar, 0, Qt::AlignVCenter);
        this->_tabBarLayout->addWidget(this->_titleLabel, 1, Qt::AlignVCenter);
        this->_tabBarLayout->addWidget(this->_rightToolBar, 0, Qt::AlignVCenter);
    }
    ~RibbonTitleWidget() override = default;

    RibbonApplicationButton *applicationButton() { return _applicationButton; }

    void setApplicationIcon(const QIcon &icon) { _applicationButton->setIcon(icon); }

    void addTitleWidget(QWidget *widget) { _tabBarLayout->addWidget(widget); }

    void insertTitleWidget(int index, QWidget *widget) { _tabBarLayout->insertWidget(index, widget); }

    void removeTitleWidget(QWidget *widget) { _tabBarLayout->removeWidget(widget); }

    RibbonTabBar *tabBar() { return _tabBar; }

    QToolBar *quickAccessToolBar() { return _quickAccessToolBar; }

    QList<QToolButton *> quickAccessButtons() { return _quickAccessButtons; }

    void addQuickAccessButton(QToolButton *button) {
        button->setIconSize(QSize(_quickAccessButtonHeight, _quickAccessButtonHeight));
        _quickAccessButtons.append(button);
        _quickAccessToolBar->addWidget(button);
    }

    void setQuickAccessButtonHeight(int height) {
        _quickAccessButtonHeight = height;
        _applicationButton->setIcon(_applicationButton->icon().pixmap(height, height));
        _quickAccessToolBar->setIconSize(QSize(height, height));
    }

    QString title() { return _titleLabel->text(); }

    void setTitle(const QString &title) { _titleLabel->setText(title); }

    QToolBar *rightToolBar() { return _rightToolBar; }

    void addRightToolButton(QToolButton *button) {
        button->setIconSize(QSize(_rightButtonHeight, _rightButtonHeight));
        _rightToolButtons.append(button);
        _rightToolBar->addWidget(button);
    }

    void setRightToolBarHeight(int height) {
        _rightButtonHeight = height;
        _rightToolBar->setIconSize(QSize(height, height));
    }

    QToolButton *helpRibbonButton() { return _helpButton; }

    void setHelpButtonIcon(const QIcon &icon) { _helpButton->setIcon(icon); }

    void removeHelpButton() { _helpButton->setVisible(false); }

    void setCollapseButtonIcon(const QIcon &icon) { _collapseRibbonButton->setIcon(icon); }

    void removeCollapseButton() { _collapseRibbonButton->setVisible(false); }

    QToolButton *collapseRibbonButton() { return _collapseRibbonButton; }

    void setTitleWidgetHeight(int height) {
        setQuickAccessButtonHeight(height);
        setRightToolBarHeight(height);
    }

    QWidget *topLevelWidget() {
        QWidget *widget = this;
        while (widget->parentWidget()) {
            widget = widget->parentWidget();
        }
        return widget;
    }

    void mousePressEvent(QMouseEvent *event) override {
        _start_point = event->pos();
        _window_point = topLevelWidget()->frameGeometry().topLeft();
    }

    void mouseMoveEvent(QMouseEvent *event) override {
        QPoint relpos = event->pos() - _start_point;
        if (!_start_point.isNull() && !_window_point.isNull()) topLevelWidget()->move(_window_point + relpos);
        // TODO topLevelWidget()->windowHandle()->startSystemMove();
    }

    void mouseDoubleClickEvent(QMouseEvent *event) override {
        if (topLevelWidget()->isMaximized())
            topLevelWidget()->showNormal();
        else
            topLevelWidget()->showMaximized();
    }
};
}  // namespace qtribbon

#endif  // QTRIBBON_TITLEWIDGET_HPP
