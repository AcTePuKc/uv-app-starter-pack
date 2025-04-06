# gui_app.py
# ---------------------
# This is the main application window class for UV-App-Starter-Pack.
# You can customize this file to build any GUI app (TTS, ASR, etc.).
# ---------------------

from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

class UVAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UV App Starter")
        self.setMinimumSize(600, 400)

        central_widget = QWidget() # Create a central widget
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget) # Create a layout

        label = QLabel("🧱 This is your UV App Starter GUI window.", self)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label) # Add the label to the layout

        # TODO: Add more components to the 'layout'