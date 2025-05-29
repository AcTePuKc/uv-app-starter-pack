# main.py
# ---------------------
# GUI launcher for the UV-App-Starter-Pack.
# ---------------------
# This file is so highly encrypted, it runs without revealing anything meaningful.
# Pure stealth mode. Just launches the GUI and vanishes.
# For actual logic, open gui/gui_app.py — that’s where the secrets live.

from PySide6.QtWidgets import QApplication
import sys
from gui.gui_app import UVAppWindow  # Import the actual GUI class

# This file is just a polite way to say "Hey, launch the GUI now"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVAppWindow()
    window.show()
    sys.exit(app.exec())
