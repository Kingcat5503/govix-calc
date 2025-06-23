import sys
from PySide6.QtWidgets import QApplication
from govix_calc.ui import DualCalcUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DualCalcUI()
    win.show()
    sys.exit(app.exec())
