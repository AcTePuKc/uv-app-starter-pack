# gui_app.py
# ---------------------
# UV-App GUI Core
# You've reached the guts of the GUI. This file actually does stuff.
# Customize it to build your app — or stare at it and pretend you're busy.
# ---------------------

from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

class UVAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UV App Starter")
        self.setMinimumSize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        # Fake loading label
        self.status_label = QLabel("Booting up core modules...", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Fake loading lines
        self.loading_messages = [
            "Initializing Entropy Matrix...",
            "Calibrating Quantum Pipelines...",
            "Bootstrapping AI Consciousness...",
            "Linking Neural Uplink...",
            "Compiling Sentient Widgets...",
            "Hacking the Mainframe (just kidding)...",
            "Downloading more RAM...",
            "Engaging Anti-Bug Protocols...",
            "Synthesizing Pure Vibes...",
        ]
        self.current_index = 0

        # Rotate messages every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading_message)
        self.timer.start(2000)

    def update_loading_message(self):
        self.status_label.setText(self.loading_messages[self.current_index])
        self.current_index = (self.current_index + 1) % len(self.loading_messages)

