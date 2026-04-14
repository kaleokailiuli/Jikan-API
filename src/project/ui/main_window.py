import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel, QScrollArea
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anime Search App")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search anime...")
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)
        
        # Results
        results_label = QLabel("Search Results:")
        main_layout.addWidget(results_label)
        self.results_list = QListWidget()
        main_layout.addWidget(self.results_list)
        
        # Favorites
        favorites_label = QLabel("Favorites:")
        main_layout.addWidget(favorites_label)
        self.favorites_list = QListWidget()
        main_layout.addWidget(self.favorites_list)
        
        # Status label
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
