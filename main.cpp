//
// Created by hailin on 8/21/2024.
//

#include <QApplication>
#include <QFormLayout>
#include <QIcon>
#include <QLabel>
#include <QLineEdit>
#include <QMainWindow>
#include <QMenu>
#include <QVBoxLayout>

#include "qtribbon/RibbonBar.hpp"
#include "qtribbon/RibbonButton.hpp"
#include "qtribbon/RibbonCategory.hpp"
#include "qtribbon/RibbonGallery.hpp"
#include "qtribbon/RibbonMenu.hpp"
#include "qtribbon/RibbonPanel.hpp"
#include "qtribbon/RibbonToggleButton.hpp"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    app.setFont(QFont("Times New Roman", 10));
    app.setStyle("Windows");

    QMainWindow window;
    qtribbon::RibbonBar ribbon(6);
    ribbon.setRibbonStyle(qtribbon::RibbonStyle::Default);
    window.setMenuBar(&ribbon);
    window.setWindowTitle("Ribbon Test");
    window.setWindowIcon(QIcon("pyqtribbon/icons/python.png"));

    QWidget centralWidget;
    window.setCentralWidget(&centralWidget);
    QVBoxLayout layout(&centralWidget);

    QToolButton saveButton;
    saveButton.setAutoRaise(true);
    saveButton.setText("Button");
    saveButton.setIcon(QIcon("pyqtribbon/icons/save.png"));
    ribbon.addQuickAccessButton(&saveButton);

    QToolButton undoButton;
    undoButton.setAutoRaise(true);
    undoButton.setText("Button");
    undoButton.setIcon(QIcon("pyqtribbon/icons/undo.png"));
    ribbon.addQuickAccessButton(&undoButton);

    QToolButton redoButton;
    redoButton.setAutoRaise(true);
    redoButton.setText("Button");
    redoButton.setIcon(QIcon("pyqtribbon/icons/redo.png"));
    ribbon.addQuickAccessButton(&redoButton);

    auto category1 = ribbon.addCategory("Category 1");
    auto panel = category1->addPanel("Panel 1", false);
    panel->addSmallButton("Button 1", QIcon("pyqtribbon/icons/close.png"));
    panel->addSmallButton("Button 2", QIcon("pyqtribbon/icons/close.png"));
    panel->addSmallButton("Button 3", QIcon("pyqtribbon/icons/close.png"));
    auto showCategoryButton2 =
        panel->addMediumToggleButton("Show/Hide Category 2", QIcon("pyqtribbon/icons/close.png"));
    panel->addVerticalSeparator();
    auto showCategoryButton3 =
        panel->addMediumToggleButton("Show/Hide Category 3", QIcon("pyqtribbon/icons/close.png"));
    auto showCategoryButton45 =
        panel->addMediumToggleButton("Show/Hide Category 4/5", QIcon("pyqtribbon/icons/close.png"), 2, Qt::AlignLeft);
    panel->addLargeButton("Button 6", QIcon("pyqtribbon/icons/close.png"));
    panel->addVerticalSeparator();
    panel->addMediumButton("Button 7", QIcon("pyqtribbon/icons/close.png"));
    panel->addMediumButton("Button 8", QIcon("pyqtribbon/icons/close.png"));

    auto saveButton = panel->addLargeButton("Button 8", QIcon("pyqtribbon/icons/close.png"));
    auto menu = new QMenu();
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 1");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 2");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 3");
    saveButton->setMenu(menu);
    saveButton->setPopupMode(QToolButton::InstantPopup);

    saveButton = panel->addLargeButton("Button 9", QIcon("pyqtribbon/icons/close.png"));
    menu = new QMenu();
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 1");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 2");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 3");
    saveButton->setMenu(menu);
    saveButton->setPopupMode(QToolButton::MenuButtonPopup);

    saveButton = panel->addLargeButton("Button 10", QIcon("pyqtribbon/icons/close.png"));
    menu = new QMenu();
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 1");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 2");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 3");
    saveButton->setMenu(menu);
    saveButton->setPopupMode(QToolButton::DelayedPopup);

    saveButton = panel->addLargeButton("Button 11", QIcon("pyqtribbon/icons/close.png"));
    menu = saveButton->addRibbonMenu();
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 1");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 2");
    menu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 3");
    auto submenu = menu->addMenu(QIcon("pyqtribbon/icons/close.png"), "Submenu");
    submenu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 4");
    submenu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 5");
    submenu->addAction(QIcon("pyqtribbon/icons/close.png"), "Action 6");
    menu->addSpacing();
    menu->addLabel("This is a custom widget");
    auto formLayout = menu->addFormLayoutWidget();
    formLayout->addRow(new QLabel("Row 1"), new QLineEdit());
    saveButton->setPopupMode(QToolButton::InstantPopup);
    panel->addWidget(saveButton, Large);

    QLabel label("Ribbon Test Window");
    label.setFont(QFont("Arial", 20));
    label.setAlignment(Qt::AlignCenter);
    layout.addWidget(&label, 1);

    window.resize(1800, 350);
    window.show();
    return app.exec();
}