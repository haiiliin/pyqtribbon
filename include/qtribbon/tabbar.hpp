//
// Created by hailin on 8/21/2024.
//

#ifndef PYQTRIBBON_TABBAR_HPP
#define PYQTRIBBON_TABBAR_HPP

#include <QColor>
#include <QMap>
#include <QStringList>
#include <QStyle>
#include <QTabBar>
#include <QTabWidget>

namespace qtribbon {

class RibbonTabBar : public QTabBar {
    Q_OBJECT

   private:
    int _contextCategoryTopMargin;
    int _contextCategoryDarkColorHeight;
    QMap<QString, QColor> _tabColors;
    QMap<QString, QStringList> _associated_tabs;

   public:
    explicit RibbonTabBar(QWidget* parent = nullptr)
        : QTabBar(parent), _contextCategoryTopMargin(0), _contextCategoryDarkColorHeight(5) {
        connect(this, &QTabBar::currentChanged, this, &RibbonTabBar::changeColor);
        setDrawBase(false);
    }
    ~RibbonTabBar() override = default;

    int indexOf(const QString& tabName) {
        for (int i = 0; i < count(); ++i) {
            if (tabText(i) == tabName) {
                return i;
            }
        }
        return -1;
    }

    QStringList tabTitles() {
        QStringList titles;
        for (int i = 0; i < count(); ++i) {
            titles.append(tabText(i));
        }
        return titles;
    }

    int addTab(const QString& text, const QColor& color = QColor()) {
        _tabColors[text] = color;
        return QTabBar::addTab(text);
    }

    QList<int> addAssociatedTabs(const QString& name, const QStringList& texts, const QColor& color) {
        _tabColors[name] = color;
        for (const QString& text : texts) {
            _associated_tabs[text] = texts;
            _associated_tabs[text].removeAll(text);
        }
        QList<int> indices;
        for (const QString& text : texts) {
            indices.append(addTab(text, color));
        }
        return indices;
    }

    void removeAssociatedTabs(const QStringList& titles) {
        QStringList tabTitles = this->tabTitles();
        for (const QString& title : titles) {
            if (tabTitles.contains(title)) {
                removeTab(indexOf(title));
                _tabColors.remove(title);
                _associated_tabs.remove(title);
            }
        }
    }

    QColor currentTabColor() { return _tabColors[tabText(currentIndex())]; }

    void changeColor(int inx) {
        if (count() > 0) {
            QString currentTabText = tabText(inx);
            QColor currentTabColor = _tabColors[currentTabText];
            if (currentTabColor.isValid()) {
                setStyleSheet(QString("QTabBar::tab:selected {color: %1;}").arg(currentTabColor.name()));
            } else {
                setStyleSheet("QTabBar::tab:selected {color: black;}");
            }
        }
    }
};
}  // namespace qtribbon

#endif  // PYQTRIBBON_TABBAR_HPP
