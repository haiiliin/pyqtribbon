//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_CATEGORY_HPP
#define QTRIBBON_CATEGORY_HPP

#include <QColor>
#include <QFrame>
#include <QHBoxLayout>
#include <QMap>
#include <QMenuBar>
#include <QPaintEvent>
#include <QResizeEvent>
#include <QScrollArea>
#include <QScrollBar>
#include <QToolButton>
#include <QVariant>
#include <utility>

#include "constants.hpp"
#include "panel.hpp"
#include "separator.hpp"

namespace qtribbon {

class RibbonCategoryLayoutButton : public QToolButton {
    Q_OBJECT

   public:
    explicit RibbonCategoryLayoutButton(QWidget *parent = nullptr) : QToolButton(parent) {}
    ~RibbonCategoryLayoutButton() override = default;
};

class RibbonCategoryScrollArea : public QScrollArea {
    Q_OBJECT

   public:
    explicit RibbonCategoryScrollArea(QWidget *parent = nullptr) : QScrollArea(parent) {}
    ~RibbonCategoryScrollArea() override = default;
};

class RibbonCategoryScrollAreaContents : public QFrame {
    Q_OBJECT

   public:
    explicit RibbonCategoryScrollAreaContents(QWidget *parent = nullptr) : QFrame(parent) {}
    ~RibbonCategoryScrollAreaContents() override = default;
};

class RibbonCategoryLayoutWidget : public QFrame {
    Q_OBJECT

   private:
    RibbonCategoryScrollAreaContents *_categoryScrollAreaContents;
    QHBoxLayout *_categoryLayout;
    RibbonCategoryScrollArea *_categoryScrollArea;
    RibbonCategoryLayoutButton *_previousButton;
    RibbonCategoryLayoutButton *_nextButton;

   protected:
    QHBoxLayout *_mainLayout;

   signals:
    void displayOptionsButtonClicked();

   public:
    explicit RibbonCategoryLayoutWidget(QWidget *parent = nullptr) : QFrame(parent) {
        // Set up the contents of the category scroll area
        this->_categoryScrollAreaContents = new RibbonCategoryScrollAreaContents(this);
        this->_categoryScrollAreaContents->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        this->_categoryLayout = new QHBoxLayout(this->_categoryScrollAreaContents);
        this->_categoryLayout->setContentsMargins(0, 0, 0, 0);
        this->_categoryLayout->setSpacing(5);
        this->_categoryLayout->setSizeConstraint(QLayout::SetMinAndMaxSize);

        // Set up the category scroll area
        this->_categoryScrollArea = new RibbonCategoryScrollArea(this);
        this->_categoryScrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->_categoryScrollArea->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->_categoryScrollArea->setWidget(this->_categoryScrollAreaContents);

        // Set up the previous/next buttons
        this->_previousButton = new RibbonCategoryLayoutButton(this);
        this->_previousButton->setIcon(QIcon("icons/backward.png"));
        this->_previousButton->setIconSize(QSize(12, 12));
        this->_previousButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
        this->_previousButton->setAutoRaise(true);
        connect(this->_previousButton, &QToolButton::clicked, this, &RibbonCategoryLayoutWidget::scrollPrevious);
        this->_nextButton = new RibbonCategoryLayoutButton(this);
        this->_nextButton->setIcon(QIcon("icons/forward.png"));
        this->_nextButton->setIconSize(QSize(12, 12));
        this->_nextButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
        this->_nextButton->setAutoRaise(true);
        connect(this->_nextButton, &QToolButton::clicked, this, &RibbonCategoryLayoutWidget::scrollNext);

        // Add the widgets to the main layout
        this->_mainLayout = new QHBoxLayout(this);
        this->_mainLayout->setContentsMargins(0, 0, 0, 0);
        this->_mainLayout->setSpacing(0);
        this->_mainLayout->addWidget(this->_previousButton, 0, Qt::AlignVCenter);
        this->_mainLayout->addWidget(this->_categoryScrollArea, 1);
        this->_mainLayout->addSpacerItem(new QSpacerItem(0, 0, QSizePolicy::Expanding, QSizePolicy::Minimum));
        this->_mainLayout->addWidget(this->_nextButton, 0, Qt::AlignVCenter);

        // Auto set the visibility of the scroll buttons
        this->autoSetScrollButtonsVisible();
    }

    ~RibbonCategoryLayoutWidget() override = default;

    void paintEvent(QPaintEvent *event) override {
        QFrame::paintEvent(event);
        autoSetScrollButtonsVisible();
    }

    void resizeEvent(QResizeEvent *event) override {
        QFrame::resizeEvent(event);
        autoSetScrollButtonsVisible();
    }

    void autoSetScrollButtonsVisible() {
        QScrollBar *horizontalScrollBar = _categoryScrollArea->horizontalScrollBar();
        _previousButton->setVisible(horizontalScrollBar->value() > horizontalScrollBar->minimum());
        _nextButton->setVisible(horizontalScrollBar->value() < horizontalScrollBar->maximum());
        _previousButton->setIconSize(QSize(12, this->size().height() - 15));
        _nextButton->setIconSize(QSize(12, this->size().height() - 15));
    }

    void scrollPrevious() {
        QScrollBar *horizontalScrollBar = _categoryScrollArea->horizontalScrollBar();
        horizontalScrollBar->setValue(horizontalScrollBar->value() - 50);
        autoSetScrollButtonsVisible();
    }

    void scrollNext() {
        QScrollBar *horizontalScrollBar = _categoryScrollArea->horizontalScrollBar();
        horizontalScrollBar->setValue(horizontalScrollBar->value() + 50);
        autoSetScrollButtonsVisible();
    }

    void addWidget(QWidget *widget) { _categoryLayout->addWidget(widget); }

    void removeWidget(QWidget *widget) { _categoryLayout->removeWidget(widget); }

    QWidget *takeWidget(QWidget *widget) {
        _categoryLayout->removeWidget(widget);
        return widget;
    }
};

class RibbonCategory : public RibbonCategoryLayoutWidget {
    Q_OBJECT

   private:
    QString _title;
    RibbonCategoryStyle _style;
    QMap<QString, RibbonPanel *> _panels = QMap<QString, RibbonPanel *>();
    int _maxRows = 6;

   protected:
    QColor _color;

   public:
    explicit RibbonCategory(QWidget *parent = nullptr) : RibbonCategory("", Normal, QColor(), parent) {}
    explicit RibbonCategory(QString title = "", RibbonCategoryStyle style = Normal, QColor color = QColor(),
                            QWidget *parent = nullptr)
        : RibbonCategoryLayoutWidget(parent), _title(std::move(title)), _style(style), _color(color) {}
    ~RibbonCategory() override = default;

    void setMaximumRows(int rows) { _maxRows = rows; }
    QString title() const { return _title; }
    virtual void setCategoryStyle(RibbonCategoryStyle style) { _style = style; }
    RibbonCategoryStyle categoryStyle() const { return _style; }

    RibbonPanel *addPanel(const QString &title, bool showPanelOptionButton) {
        auto *panel = new RibbonPanel(title, _maxRows, showPanelOptionButton, this);
        panel->setFixedHeight(this->height() - _mainLayout->spacing() - _mainLayout->contentsMargins().top() -
                              _mainLayout->contentsMargins().bottom());
        _panels[title] = panel;
        this->addWidget(panel);
        this->addWidget(new RibbonSeparator(Qt::Vertical, 10));
        return panel;
    }

    void removePanel(const QString &title) {
        this->removeWidget(_panels[title]);
        _panels.remove(title);
    }

    RibbonPanel *takePanel(const QString &title) {
        RibbonPanel *panel = _panels[title];
        this->removePanel(title);
        return panel;
    }

    RibbonPanel *panel(const QString &title) { return _panels[title]; }

    QMap<QString, RibbonPanel *> panels() { return _panels; }
};

class RibbonNormalCategory : public RibbonCategory {
    Q_OBJECT

   public:
    explicit RibbonNormalCategory(QString title = "", QWidget *parent = nullptr)
        : RibbonCategory(std::move(title), Normal, QColor(), parent) {}
    ~RibbonNormalCategory() override = default;

    void setCategoryStyle(RibbonCategoryStyle style) override {
        throw std::runtime_error("You can not set the category style of a normal category.");
    }
};

class RibbonContextCategory : public RibbonCategory {
    Q_OBJECT

   public:
    explicit RibbonContextCategory(QString title = "", QColor color = QColor(), QWidget *parent = nullptr)
        : RibbonCategory(std::move(title), Context, color, parent) {}
    ~RibbonContextCategory() override = default;

    void setCategoryStyle(RibbonCategoryStyle style) override {
        throw std::runtime_error("You can not set the category style of a context category.");
    }

    QColor color() const { return _color; }
    void setColor(QColor color) { _color = color; }
};

class RibbonContextCategories : public QMap<QString, RibbonContextCategory *> {
   private:
    QString _name;
    QColor _color;

   public:
    RibbonContextCategories(QString name, QColor color, QMap<QString, RibbonContextCategory *> categories)
        : QMap<QString, RibbonContextCategory *>(std::move(categories)), _name(std::move(name)), _color(color) {}
    ~RibbonContextCategories() = default;

    QString name() const { return _name; }
    void setName(QString name) { _name = std::move(name); }
    QColor color() const { return _color; }
    void setColor(QColor color) { _color = color; }
};
}  // namespace qtribbon

#endif  // QTRIBBON_CATEGORY_HPP
