from PySide6.QtWidgets import QApplication
from ui import DualCalcUI
import sys

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = DualCalcUI()
    window.left_display.setFocus()
    window.show()
    sys.exit(app.exec())
