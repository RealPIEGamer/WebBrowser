from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class ElectronBrowser(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ElectronBrowser, self).__init__(*args, **kwargs)

        self.setWindowTitle("Electron Browser")
        self.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        # Navigation buttons
        self.back_btn = QPushButton("<")
        self.back_btn.setMaximumWidth(30)
        self.back_btn.setMaximumHeight(30)
        self.back_btn.setStyleSheet("background-color: blue; color: white;")

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMaximumWidth(30)
        self.forward_btn.setMaximumHeight(30)
        self.forward_btn.setStyleSheet("background-color: green; color: white;")

        self.reload_btn = QPushButton("R")
        self.reload_btn.setMaximumWidth(30)
        self.reload_btn.setMaximumHeight(30)
        self.reload_btn.setStyleSheet("background-color: red; color: white;")

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setPlaceholderText("Enter URL here...")
        self.url_bar.returnPressed.connect(self.handle_enter_key)
        self.url_bar.setStyleSheet("background-color: white;")

        # Go button
        self.go_btn = QPushButton("Go")
        self.go_btn.setMaximumHeight(30)
        self.go_btn.setMaximumWidth(50)
        self.go_btn.setStyleSheet("background-color: lightblue;")

        # Add widgets to the horizontal layout
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.reload_btn)
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)

        # Tab widget for managing tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar_from_tab)

        # Create a layout to hold the tabs and the "New Tab" button
        self.tab_layout = QHBoxLayout()
        self.tab_layout.addWidget(self.tabs)

        # Add a "New Tab" button to the far right
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setStyleSheet("background-color: green; color: white;")
        self.new_tab_btn.setMaximumWidth(30)
        self.new_tab_btn.setMaximumHeight(30)
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab(QUrl("http://google.com"), "New Tab"))
        self.tab_layout.addWidget(self.new_tab_btn)

        # Add the first tab
        self.add_new_tab(QUrl("http://google.com"), "New Tab")

        # Connect navigation buttons
        self.back_btn.clicked.connect(self.navigate_back)
        self.forward_btn.clicked.connect(self.navigate_forward)
        self.reload_btn.clicked.connect(self.reload_page)
        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.text()))

        # Main layout
        self.layout.addLayout(self.horizontal)
        self.layout.addLayout(self.tab_layout)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def add_new_tab(self, qurl=None, label="New Tab"):
        """Add a new tab with a QWebEngineView."""
        if qurl is None:
            qurl = QUrl("http://google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url_bar)
        browser.titleChanged.connect(lambda title: self.update_tab_title(self.tabs.indexOf(browser), title))  # Update tab title

        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        """Close the tab at the given index."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate(self, url):
        """Navigate to the given URL in the current tab."""
        if not url.startswith("http"):
            url = "http://" + url
        self.url_bar.setText(url)
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.setUrl(QUrl(url))

    def navigate_back(self):
        """Navigate back in the current tab."""
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.back()

    def navigate_forward(self):
        """Navigate forward in the current tab."""
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.forward()

    def reload_page(self):
        """Reload the current tab."""
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.reload()

    def handle_enter_key(self):
        """Handle Enter key press in the URL bar."""
        self.navigate(self.url_bar.text())

    def update_url_bar(self, qurl):
        """Update the URL bar when the browser navigates to a new page."""
        self.url_bar.setText(qurl.toString())
        self.tabs.setTabText(self.tabs.currentIndex(), qurl.toString())

    def update_url_bar_from_tab(self, index):
        """Update the URL bar when switching tabs."""
        current_browser = self.tabs.widget(index)
        if isinstance(current_browser, QWebEngineView):
            self.url_bar.setText(current_browser.url().toString())

    def update_tab_title(self, index, title):
        """Update the tab title when the page title changes."""
        if index >= 0:
            self.tabs.setTabText(index, title)


# Run the application
app = QApplication([])
window = ElectronBrowser()
window.show()
app.exec_()