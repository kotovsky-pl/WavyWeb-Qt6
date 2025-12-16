import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QToolBar, QVBoxLayout,
    QWidget, QTabWidget, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QFile, QTextStream

DATA_FILE = "browser_data.json"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Browser z Kartami")
        self.resize(1200, 800)

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Historia adresów
        self.history = []
        self.load_data()

        # Toolbar z przyciskami szybkiego dostępu
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        back_btn = QPushButton("⬅")
        back_btn.clicked.connect(self.go_back)
        forward_btn = QPushButton("➡")
        forward_btn.clicked.connect(self.go_forward)
        refresh_btn = QPushButton("⟳")
        refresh_btn.clicked.connect(self.reload)
        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(self.add_tab)
        duck_btn = QPushButton("DuckDuckGo")
        duck_btn.clicked.connect(lambda: self.current_view().setUrl(QUrl("https://duckduckgo.com")))
        google_btn = QPushButton("Google")
        google_btn.clicked.connect(lambda: self.current_view().setUrl(QUrl("https://google.com")))
        youtube_btn = QPushButton("YouTube")
        youtube_btn.clicked.connect(lambda: self.current_view().setUrl(QUrl("https://youtube.com")))

        self.toolbar.addWidget(back_btn)
        self.toolbar.addWidget(forward_btn)
        self.toolbar.addWidget(refresh_btn)
        self.toolbar.addWidget(new_tab_btn)
        self.toolbar.addWidget(duck_btn)
        self.toolbar.addWidget(google_btn)
        self.toolbar.addWidget(youtube_btn)

        # Dodaj pierwszą kartę
        self.add_tab("https://duckduckgo.com")

        # Zapis przy zamykaniu
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_title)
        self.show()

    # Funkcje do obsługi kart
    def add_tab(self, url="https://duckduckgo.com"):
        view = QWebEngineView()
        view.setUrl(QUrl(url))
        view.urlChanged.connect(lambda u: self.update_tab_title(view, u))
        tab_index = self.tabs.addTab(view, "Nowa karta")
        self.tabs.setCurrentIndex(tab_index)

        # Dodaj do historii
        self.history.append(url)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_view(self):
        return self.tabs.currentWidget()

    def update_tab_title(self, view, url):
        index = self.tabs.indexOf(view)
        self.tabs.setTabText(index, url.toString())
        self.save_data()

    def update_title(self, index):
        view = self.current_view()
        if view:
            self.setWindowTitle(f"Mini Browser - {view.url().toString()}")

    # Przyciski
    def go_back(self):
        self.current_view().back()

    def go_forward(self):
        self.current_view().forward()

    def reload(self):
        self.current_view().reload()

    # Zapis i odczyt danych
    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie udało się zapisać danych: {e}")

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
