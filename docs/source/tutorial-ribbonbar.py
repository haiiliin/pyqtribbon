import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from ribbon import RibbonBar
from ribbon.utils import data_file_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Times New Roman", 8))
    
    # Central widget
    window = QMainWindow()
    window.setWindowIcon(QIcon(data_file_path("icons/python.png")))
    centralWidget = QWidget()
    window.setCentralWidget(centralWidget)
    layout = QVBoxLayout(centralWidget)
    
    # Ribbon bar
    ribbonbar = RibbonBar()
    category = ribbonbar.addCategory("Category 1")
    panel = category.addPanel("Panel 1")
    panel.addLargeButton("A Large Button", QIcon(data_file_path("icons/python.png")))
    panel.addMediumButton("A Medium Button", QIcon(data_file_path("icons/python.png")))
    panel.addMediumButton("A Medium Button", QIcon(data_file_path("icons/python.png")))
    panel.addSmallButton("A Small Button", QIcon(data_file_path("icons/python.png")))
    panel.addSmallButton("A Small Button", QIcon(data_file_path("icons/python.png")))
    panel.addSmallButton("A Small Button", QIcon(data_file_path("icons/python.png")))
    
    # Display a label in the main window
    label = QLabel("Ribbon Test Window")
    label.setFont(QFont("Arial", 20))
    label.setAlignment(Qt.AlignCenter)
    
    # Add the ribbon bar and label to the layout
    layout.addWidget(ribbonbar, 0)
    layout.addWidget(label, 1)
    
    # Show the window
    window.resize(1800, 350)
    window.show()
    sys.exit(app.exec_())
    