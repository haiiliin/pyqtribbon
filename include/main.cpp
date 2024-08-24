//
// Created by hailin on 8/21/2024.
//

#include <QApplication>
#include <QIcon>
#include <QLabel>
#include <QLineEdit>
#include <QMainWindow>
#include <QMenu>
#include <QVBoxLayout>

#include "qtribbon/ribbonbar.hpp"
#include "qtribbon/toolbutton.hpp"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    QApplication::setFont(QFont("Times New Roman", 10));

    QMainWindow window;
    qtribbon::RibbonBar ribbon("Ribbon Bar Title", 6);
    ribbon.setRibbonStyle(qtribbon::RibbonStyle::Default);
    window.setMenuBar(&ribbon);
    window.setWindowTitle("Ribbon Test");
    window.setWindowIcon(QIcon(":/icons/python.png"));

    QWidget centralWidget;
    window.setCentralWidget(&centralWidget);
    QVBoxLayout layout(&centralWidget);

    QToolButton saveButton;
    saveButton.setAutoRaise(true);
    saveButton.setText("Button");
    saveButton.setIcon(QIcon(":/icons/save.png"));
    ribbon.addQuickAccessButton(&saveButton);

    QToolButton undoButton;
    undoButton.setAutoRaise(true);
    undoButton.setText("Button");
    undoButton.setIcon(QIcon(":/icons/undo.png"));
    ribbon.addQuickAccessButton(&undoButton);

    QToolButton redoButton;
    redoButton.setAutoRaise(true);
    redoButton.setText("Button");
    redoButton.setIcon(QIcon(":/icons/redo.png"));
    ribbon.addQuickAccessButton(&redoButton);

    auto category1 = ribbon.addCategory("Category 1");
    auto panel = category1->addPanel("Panel 1", false);
    panel->addSmallButton("Button 1", QIcon(":/icons/close.png"));
    panel->addSmallButton("Button 2", QIcon(":/icons/close.png"));
    panel->addSmallButton("Button 3", QIcon(":/icons/close.png"));
    auto showCategoryButton2 = panel->addMediumToggleButton("Show/Hide Category 2", QIcon(":/icons/close.png"));
    panel->addVerticalSeparator();
    auto showCategoryButton3 = panel->addMediumToggleButton("Show/Hide Category 3", QIcon(":/icons/close.png"));
    auto showCategoryButton45 =
        panel->addMediumToggleButton("Show/Hide Category 4/5", QIcon(":/icons/close.png"), 2, Qt::AlignLeft);
    panel->addLargeButton("Button 6", QIcon(":/icons/close.png"));
    panel->addVerticalSeparator();
    panel->addMediumButton("Button 7", QIcon(":/icons/close.png"));
    panel->addMediumButton("Button 8", QIcon(":/icons/close.png"));

    auto *saveButton1 = panel->addLargeButton("Button 8", QIcon(":/icons/close.png"));
    auto menu1 = new QMenu();
    menu1->addAction(QIcon(":/icons/close.png"), "Action 1");
    menu1->addAction(QIcon(":/icons/close.png"), "Action 2");
    menu1->addAction(QIcon(":/icons/close.png"), "Action 3");
    saveButton1->setMenu(menu1);
    saveButton1->setPopupMode(QToolButton::InstantPopup);

    auto *saveButton2 = panel->addLargeButton("Button 9", QIcon(":/icons/close.png"));
    auto *menu2 = new QMenu();
    menu2->addAction(QIcon(":/icons/close.png"), "Action 1");
    menu2->addAction(QIcon(":/icons/close.png"), "Action 2");
    menu2->addAction(QIcon(":/icons/close.png"), "Action 3");
    saveButton2->setMenu(menu2);
    saveButton2->setPopupMode(QToolButton::MenuButtonPopup);

    auto *saveButton3 = panel->addLargeButton("Button 10", QIcon(":/icons/close.png"));
    auto *menu3 = new QMenu();
    menu3->addAction(QIcon(":/icons/close.png"), "Action 1");
    menu3->addAction(QIcon(":/icons/close.png"), "Action 2");
    menu3->addAction(QIcon(":/icons/close.png"), "Action 3");
    saveButton3->setMenu(menu3);
    saveButton3->setPopupMode(QToolButton::DelayedPopup);

    auto *saveButton4 = panel->addLargeButton("Button 11", QIcon(":/icons/close.png"));
    auto *menu4 = saveButton4->addRibbonMenu();
    menu4->addAction(QIcon(":/icons/close.png"), "Action 1");
    menu4->addAction(QIcon(":/icons/close.png"), "Action 2");
    menu4->addAction(QIcon(":/icons/close.png"), "Action 3");
    auto *submenu = menu4->addMenu(QIcon(":/icons/close.png"), "Submenu");
    submenu->addAction(QIcon(":/icons/close.png"), "Action 4");
    submenu->addAction(QIcon(":/icons/close.png"), "Action 5");
    submenu->addAction(QIcon(":/icons/close.png"), "Action 6");
    menu4->addSpacing();
    menu4->addLabel("This is a custom widget");
    auto formLayout = menu4->addFormLayoutWidget();
    formLayout->addRow(new QLabel("Row 1"), new QLineEdit());
    saveButton4->setPopupMode(QToolButton::InstantPopup);
    panel->addLargeWidget(saveButton4);

    QLabel label("Ribbon Test Window");
    label.setFont(QFont("Arial", 20));
    label.setAlignment(Qt::AlignCenter);
    layout.addWidget(&label, 1);

    window.resize(1200, 350);
    window.show();
    return QApplication::exec();
}
