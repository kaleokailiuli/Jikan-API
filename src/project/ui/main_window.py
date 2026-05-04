import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Qt
from utils.controller import AnimeController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jikan API")
        self.setGeometry(100, 100, 900, 700)
        
        # Initialize controller
        self.controller = AnimeController()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search anime...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_clicked)
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
    
    def on_search_clicked(self):
        # Get search input
        search_query = self.search_input.text()
        
        if not search_query:
            self.status_label.setText("Please enter an anime name")
            return
        
        # Update status
        self.status_label.setText("Searching...")
        
        # Call controller to search
        results = self.controller.search_anime(search_query)
        
        if results:
            self.display_results(results)
            self.status_label.setText(f"Found {len(results)} results")
        else:
            self.status_label.setText("No results found")
    
    def display_results(self, anime_list):
        # Clears results
        self.results_list.clear()
        
        # Add each animes to results list
        for anime in anime_list:
            title = anime.get("title", "Unknown")
            rating = anime.get("rating", "N/A")
            episodes = anime.get("episodes", "N/A")
            
            item_text = f"{title} | Rating: {rating} | Episodes: {episodes}"
            item = QListWidgetItem(item_text)
            self.results_list.addItem(item)
