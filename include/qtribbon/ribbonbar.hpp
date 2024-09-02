//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_RIBBONBAR_HPP
#define QTRIBBON_RIBBONBAR_HPP

#include <QFile>
#include <QGraphicsDropShadowEffect>
#include <QMenuBar>
#include <QStackedWidget>
#include <QString>
#include <QVBoxLayout>

#include "category.hpp"
#include "titlewidget.hpp"

namespace qtribbon {
class RibbonStackedWidget : public QStackedWidget {
    Q_OBJECT
   public:
    explicit RibbonStackedWidget(QWidget* parent = nullptr) : QStackedWidget(parent) {
        auto* effect = new QGraphicsDropShadowEffect(this);
        effect->setOffset(2, 2);
        this->setGraphicsEffect(effect);
    }
    ~RibbonStackedWidget() override = default;
};

class RibbonBar : public QMenuBar {
    Q_OBJECT

   private:
    bool _autoHideRibbon = false;
    QMap<QString, RibbonCategory*> _categories = {};
    int _contextCategoryCount = 0;
    int _maxRows = 6;
    bool _ribbonVisible = true;
    int _ribbonHeight = 150;
    int _currentTabIndex = 0;
    RibbonTitleWidget* _titleWidget;
    RibbonStackedWidget* _stackedWidget;
    QVBoxLayout* _mainLayout;

   signals:
    bool helpButtonClicked();

   public:
    explicit RibbonBar(QWidget* parent = nullptr) : RibbonBar("Ribbon Bar Title", 6, parent) {}

    explicit RibbonBar(const QString& title = "Ribbon Bar Title", int maxRows = 6, QWidget* parent = nullptr)
        : QMenuBar(parent), _maxRows(maxRows) {
        this->setFixedHeight(_ribbonHeight);

        _titleWidget = new RibbonTitleWidget(title, this);
        _stackedWidget = new RibbonStackedWidget(this);

        // Main Layout
        _mainLayout = new QVBoxLayout(this);
        _mainLayout->setContentsMargins(0, 0, 0, 0);
        _mainLayout->setSpacing(0);
        _mainLayout->addWidget(_titleWidget, 0);
        _mainLayout->addWidget(_stackedWidget, 1);
        _mainLayout->setSizeConstraint(QLayout::SetMinAndMaxSize);

        // Connect signals
        connect(_titleWidget, &RibbonTitleWidget::helpButtonClicked, this, &RibbonBar::helpButtonClicked);
        connect(_titleWidget, &RibbonTitleWidget::collapseRibbonButtonClicked, this,
                &RibbonBar::_collapseButtonClicked);
        connect(_titleWidget->tabBar(), &QTabBar::currentChanged, this, &RibbonBar::showCategoryByIndex);

        this->setRibbonStyle(RibbonStyle::Default);
    }

    ~RibbonBar() override = default;

    bool autoHideRibbon() const { return _autoHideRibbon; }

    void setAutoHideRibbon(bool autoHide) { _autoHideRibbon = autoHide; }

    bool eventFilter(QObject* object, QEvent* event) override {
        if (_autoHideRibbon && event->type() == QEvent::HoverMove) setRibbonVisible(underMouse());
        return QMenuBar::eventFilter(object, event);
    }

    void setRibbonStyle(RibbonStyle style) {
        QFile baseFile = QFile(":/styles/base.qss");
        baseFile.open(QFile::ReadOnly);
        QString baseStyle = baseFile.readAll();
        QFile specificFile = QFile(QString(":/styles/%1.qss").arg(style == RibbonStyle::Debug ? "debug" : "default"));
        specificFile.open(QFile::ReadOnly);
        QString specificStyle = specificFile.readAll();
        setStyleSheet(baseStyle + specificStyle);
    }

    RibbonApplicationButton* applicationOptionButton() const { return _titleWidget->applicationButton(); }

    void setApplicationIcon(const QIcon& icon) { _titleWidget->applicationButton()->setIcon(icon); }

    void addTitleWidget(QWidget* widget) { _titleWidget->addTitleWidget(widget); }

    void removeTitleWidget(QWidget* widget) { _titleWidget->removeTitleWidget(widget); }

    void insertTitleWidget(int index, QWidget* widget) { _titleWidget->insertTitleWidget(index, widget); }

    RibbonMenu* addFileMenu() { return _titleWidget->applicationButton()->addFileMenu(); }

    int ribbonHeight() const { return _ribbonHeight; }

    void setRibbonHeight(int height) {
        _ribbonHeight = height;
        setFixedHeight(height);
    }

    RibbonTabBar* tabBar() const { return _titleWidget->tabBar(); }

    QToolBar* quickAccessToolBar() const { return _titleWidget->quickAccessToolBar(); }

    void addQuickAccessButton(QToolButton* button) {
        button->setAutoRaise(true);
        _titleWidget->quickAccessToolBar()->addWidget(button);
    }

    void setQuickAccessButtonHeight(int height) { _titleWidget->setQuickAccessButtonHeight(height); }

    QString title() const { return _titleWidget->title(); }

    void setTitle(const QString& title) { _titleWidget->setTitle(title); }

    void setTitleWidgetHeight(int height) { _titleWidget->setTitleWidgetHeight(height); }

    QToolBar* rightToolBar() const { return _titleWidget->rightToolBar(); }

    void addRightToolButton(QToolButton* button) {
        button->setAutoRaise(true);
        _titleWidget->addRightToolButton(button);
    }

    void setRightToolBarHeight(int height) { _titleWidget->setRightToolBarHeight(height); }

    QToolButton* helpRibbonButton() const { return _titleWidget->helpRibbonButton(); }

    void setHelpButtonIcon(const QIcon& icon) { _titleWidget->setHelpButtonIcon(icon); }

    void removeHelpButton() { _titleWidget->removeHelpButton(); }

    QToolButton* collapseRibbonButton() const { return _titleWidget->collapseRibbonButton(); }

    void setCollapseButtonIcon(const QIcon& icon) { _titleWidget->setCollapseButtonIcon(icon); }

    void removeCollapseButton() { _titleWidget->removeCollapseButton(); }

    RibbonCategory* category(const QString& name) const { return _categories[name]; }

    QMap<QString, RibbonCategory*> categories() const { return _categories; }

    RibbonCategory* addCategory(const QString& title, RibbonCategoryStyle style = Normal, QColor color = QColor()) {
        if (_categories.contains(title))
            throw std::invalid_argument(QString("Category with title %1 already exists.").arg(title).toStdString());

        if (style == RibbonCategoryStyle::Context && color == QColor()) {
            color = contextColors[_contextCategoryCount % contextColors.size()];
            _contextCategoryCount++;
        }
        RibbonCategory* category;
        if (style == RibbonCategoryStyle::Context)
            category = new RibbonContextCategory(title, color, this);
        else
            category = new RibbonNormalCategory(title, this);

        category->setMaximumRows(_maxRows);
        category->setFixedHeight(_ribbonHeight - _mainLayout->spacing() * 2 - _mainLayout->contentsMargins().top() -
                                 _mainLayout->contentsMargins().bottom() - _titleWidget->height());
        _categories[title] = category;
        _stackedWidget->addWidget(category);
        if (style == RibbonCategoryStyle::Normal) {
            _titleWidget->tabBar()->addTab(title, color);
        } else if (style == RibbonCategoryStyle::Context) {
            category->hide();
        }
        if (_categories.size() == 1) {
            _titleWidget->tabBar()->setCurrentIndex(1);
            showCategoryByIndex(1);
        }
        return category;
    }

    RibbonNormalCategory* addNormalCategory(const QString& title) {
        return dynamic_cast<RibbonNormalCategory*>(addCategory(title, RibbonCategoryStyle::Normal));
    }

    RibbonContextCategory* addContextCategory(const QString& title, QColor color) {
        return dynamic_cast<RibbonContextCategory*>(addCategory(title, RibbonCategoryStyle::Context, color));
    }

    RibbonContextCategories* addContextCategories(const QString& name, const QStringList& titles, QColor color) {
        if (color == QColor()) {
            color = contextColors[_contextCategoryCount % contextColors.size()];
            _contextCategoryCount++;
        }
        QMap<QString, RibbonContextCategory*> categories;
        for (const QString& title : titles) categories[title] = addContextCategory(title, color);
        return new RibbonContextCategories(name, color, categories);
    }

    void showCategoryByIndex(int index) {
        _currentTabIndex = index;
        QString title = _titleWidget->tabBar()->tabText(index);
        if (_categories.contains(title)) {
            _stackedWidget->setCurrentWidget(_categories[title]);
        }
    }

    void showContextCategory(RibbonCategory* category) {
        auto* contextCategory = dynamic_cast<RibbonContextCategory*>(category);
        if (contextCategory) {
            _titleWidget->tabBar()->addTab(contextCategory->title(), contextCategory->color());
            _titleWidget->tabBar()->setCurrentIndex(_titleWidget->tabBar()->count() - 1);
            _stackedWidget->setCurrentWidget(contextCategory);
        }
        auto* contextCategories = dynamic_cast<RibbonContextCategories*>(category);
        if (contextCategories) {
            QStringList titles = contextCategories->keys();
            _titleWidget->tabBar()->addAssociatedTabs(contextCategories->name(), titles, contextCategories->color());
            _titleWidget->tabBar()->setCurrentIndex(_titleWidget->tabBar()->count() - titles.size());
            _stackedWidget->setCurrentWidget((*contextCategories)[titles[0]]);
        }
    }

    void hideContextCategory(RibbonCategory* category) {
        auto* contextCategory = dynamic_cast<RibbonContextCategory*>(category);
        if (contextCategory) {
            tabBar()->removeTab(tabBar()->indexOf(contextCategory->title()));
        }
        auto* contextCategories = dynamic_cast<RibbonContextCategories*>(category);
        if (contextCategories) {
            for (RibbonContextCategory* c : *contextCategories) {
                tabBar()->removeTab(tabBar()->indexOf(c->title()));
            }
        }
    }

    bool categoryVisible(RibbonCategory* category) {
        return _titleWidget->tabBar()->tabTitles().contains(category->title());
    }

    void removeCategory(RibbonCategory* category) {
        tabBar()->removeTab(_titleWidget->tabBar()->indexOf(category->title()));
        _stackedWidget->removeWidget(category);
    }

    void removeCategories(RibbonContextCategories* categories) {
        for (RibbonContextCategory* category : *categories) {
            removeCategory(category);
        }
    }

    void setCurrentCategory(RibbonCategory* category) {
        _stackedWidget->setCurrentWidget(category);
        if (_titleWidget->tabBar()->tabTitles().contains(category->title())) {
            _titleWidget->tabBar()->setCurrentIndex(_titleWidget->tabBar()->indexOf(category->title()));
        } else {
            throw std::invalid_argument(
                QString("Category %1 is not in the ribbon, please show the context category/categories first.")
                    .arg(category->title())
                    .toStdString());
        }
    }

    RibbonCategory* currentCategory() {
        return _categories[_titleWidget->tabBar()->tabText(_titleWidget->tabBar()->currentIndex())];
    }

    QSize minimumSizeHint() { return {QMenuBar::minimumSizeHint().width(), _ribbonHeight}; }

    void _collapseButtonClicked() {
        connect(tabBar(), &QTabBar::currentChanged, this, &RibbonBar::showRibbon);
        if (_stackedWidget->isVisible()) {
            hideRibbon();
        } else {
            showRibbon();
        }
    }

    void showRibbon() {
        if (!_ribbonVisible) {
            _ribbonVisible = true;
            collapseRibbonButton()->setToolTip("Collapse Ribbon");
            collapseRibbonButton()->setIcon(QIcon(":/icons/up.png"));
            _stackedWidget->setVisible(true);
            setFixedSize(sizeHint());
        }
    }

    void hideRibbon() {
        if (_ribbonVisible) {
            _ribbonVisible = false;
            collapseRibbonButton()->setToolTip("Expand Ribbon");
            collapseRibbonButton()->setIcon(QIcon(":/icons/down.png"));
            _stackedWidget->setVisible(false);
            setFixedSize(sizeHint().width(), _titleWidget->size().height() + 5);
        }
    }

    bool ribbonVisible() const { return _ribbonVisible; }

    void setRibbonVisible(bool visible) {
        if (visible)
            showRibbon();
        else
            hideRibbon();
    }
};
}  // namespace qtribbon

#endif  // QTRIBBON_RIBBONBAR_HPP
