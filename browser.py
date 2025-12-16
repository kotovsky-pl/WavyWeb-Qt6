import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QToolBar, QVBoxLayout,
    QWidget, QTabWidget, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

DATA_FILE = "browser_data.json"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WavyWeb-Qt6")
        self.resize(1200, 800)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # Historia odwiedzonych stron
        self.history = []
        self.load_data()

        # Toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Przyciski na toolbarze
        back_btn = QPushButton("⬅")
        back_btn.clicked.connect(self.go_back)
        forward_btn = QPushButton("➡")
        forward_btn.clicked.connect(self.go_forward)
        refresh_btn = QPushButton("⟳")
        refresh_btn.clicked.connect(self.reload)
        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(self.add_tab)
        duck_btn = QPushButton("DuckDuckGo")
        duck_btn.clicked.connect(lambda: self.navigate_to_url("https://duckduckgo.com"))
        google_btn = QPushButton("Google")
        google_btn.clicked.connect(lambda: self.navigate_to_url("https://google.com"))
        youtube_btn = QPushButton("YouTube")
        youtube_btn.clicked.connect(lambda: self.navigate_to_url("https://youtube.com"))

        # Pasek adresu
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url_from_bar)

        # Dodaj wszystkie przyciski do toolbaru
        self.toolbar.addWidget(back_btn)
        self.toolbar.addWidget(forward_btn)
        self.toolbar.addWidget(refresh_btn)
        self.toolbar.addWidget(new_tab_btn)
        self.toolbar.addWidget(duck_btn)
        self.toolbar.addWidget(google_btn)
        self.toolbar.addWidget(youtube_btn)
        self.toolbar.addWidget(self.url_bar)

        # Połączenia
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_title)

        # Dodaj pierwszą kartę
        self.add_tab("https://duckduckgo.com")

        self.show()

    # Dodawanie nowej karty
    def add_tab(self, url: str = "https://duckduckgo.com"):
        if not isinstance(url, str) or not url:
            url = "https://duckduckgo.com"

        view = QWebEngineView()
        view.setUrl(QUrl(url))
        view.urlChanged.connect(lambda u: self.update_tab_title(view, u))
        index = self.tabs.addTab(view, "New Tab")
        self.tabs.setCurrentIndex(index)

        # Dodaj do historii
        self.history.append(url)
        self.save_data()

    # Zamknięcie karty
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    # Pobranie aktualnej karty
    def current_view(self):
        return self.tabs.currentWidget()

    # Aktualizacja tytułu karty
    def update_tab_title(self, view, url):
        index = self.tabs.indexOf(view)
        self.tabs.setTabText(index, url.toString())
        self.url_bar.setText(url.toString())
        self.save_data()

    def update_title(self, index):
        view = self.current_view()
        if view:
            self.setWindowTitle(f"WavyWeb-Qt6 - {view.url().toString()}")

    # Nawigacja
    def navigate_to_url(self, url: str):
        if not isinstance(url, str) or not url.startswith("http"):
            url = "https://" + str(url)
        self.current_view().setUrl(QUrl(url))

    def navigate_to_url_from_bar(self):
        url = self.url_bar.text()
        self.navigate_to_url(url)

    def go_back(self):
        self.current_view().back()

    def go_forward(self):
        self.current_view().forward()

    def reload(self):
        self.current_view().reload()

    # Zapis / odczyt historii
    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save data: {e}")

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.history = json.load(f)
        except:
            self.history = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec())
