//
// Created by hailin on 8/21/2024.
//

#ifndef QTRIBBON_MENU_HPP
#define QTRIBBON_MENU_HPP

#include <QApplication>
#include <QFormLayout>
#include <QGridLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QMenu>
#include <QVBoxLayout>
#include <QWidgetAction>

namespace qtribbon {

class RibbonMenu : public QMenu {
    Q_OBJECT

   public:
    explicit RibbonMenu(QWidget *parent = nullptr) : RibbonMenu("", parent) {}
    explicit RibbonMenu(const QString &title, QWidget *parent = nullptr) : QMenu(title, parent) {
        this->setFont(QApplication::font());
    }
    ~RibbonMenu() {}

    void addWidget(QWidget *widget) {
        QWidgetAction *widgetAction = new QWidgetAction(this);
        widgetAction->setDefaultWidget(widget);
        this->addAction(widgetAction);
    }

    QHBoxLayout *addHorizontalLayoutWidget() {
        QWidget *widget = new QWidget();
        QHBoxLayout *layout = new QHBoxLayout(widget);
        layout->setContentsMargins(0, 0, 0, 0);
        this->addWidget(widget);
        return layout;
    }

    QVBoxLayout *addVerticalLayoutWidget() {
        QWidget *widget = new QWidget();
        QVBoxLayout *layout = new QVBoxLayout(widget);
        layout->setContentsMargins(0, 0, 0, 0);
        this->addWidget(widget);
        return layout;
    }

    QGridLayout *addGridLayoutWidget() {
        QWidget *widget = new QWidget();
        QGridLayout *layout = new QGridLayout(widget);
        layout->setContentsMargins(0, 0, 0, 0);
        this->addWidget(widget);
        return layout;
    }

    QFormLayout *addFormLayoutWidget() {
        QWidget *widget = new QWidget();
        QFormLayout *layout = new QFormLayout(widget);
        layout->setContentsMargins(0, 0, 0, 0);
        this->addWidget(widget);
        return layout;
    }

    void addSpacing(int spacing = 5) {
        QLabel *spacer = new QLabel();
        spacer->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
        spacer->setFixedHeight(spacing);
        this->addWidget(spacer);
    }

    void addLabel(const QString &text = "", Qt::Alignment alignment = Qt::AlignLeft) {
        QLabel *label = new QLabel(text);
        label->setAlignment(alignment);
        this->addWidget(label);
    }
};

class RibbonPermanentMenu : public RibbonMenu {
    Q_OBJECT

   signals:
    void actionAdded(QAction *action);

   public:
    explicit RibbonPermanentMenu(QWidget *parent = nullptr) : RibbonMenu(parent) {}
    explicit RibbonPermanentMenu(const QString &title, QWidget *parent = nullptr) : RibbonMenu(title, parent) {}
    ~RibbonPermanentMenu() {}

    void hideEvent(QHideEvent *event) override { this->show(); }

    QAction *addAction(const QString &text) {
        QAction *action = RibbonMenu::addAction(text);
        emit actionAdded(action);
        return action;
    }
};
}  // namespace qtribbon

#endif  // QTRIBBON_MENU_HPP
