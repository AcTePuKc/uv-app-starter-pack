# main.py
# ---------------------
# GUI launcher for the UV-App-Starter-Pack.
# ---------------------

from PySide6.QtWidgets import QApplication
import sys
from gui.gui_app import UVAppWindow  # Import the actual GUI class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVAppWindow()
    window.show()
    sys.exit(app.exec())