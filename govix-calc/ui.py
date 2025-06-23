from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Slot, QEvent
from govix_calc.logic import safe_eval, toggle_sign, calc_percent
from govix_calc.settings import SettingsDialog

class DualCalcUI(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = 'dark'
        self.focused = 'left'

        self.setWindowTitle("Govix Calc")
        self.setMinimumSize(600, 600)

        self.apply_theme()
        self.build_ui()

        self.left_display.setFocus()

    def apply_theme(self):
        if self.theme == 'light':
            self.setStyleSheet("""
                QWidget {
                    background: #f0f0f0;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLineEdit {
                    background: #ffffff;
                    color: #000000;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 12px;
                    border: 2px solid #cccccc;
                    border-radius: 8px;
                }
                QLineEdit:focus {
                    border: 2px solid #3daee9;
                }
                QPushButton {
                    font-size: 18px;
                    padding: 10px 16px;
                    border: none;
                    border-radius: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #fafafa, stop:1 #e0e0e0);
                    color: #000;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e5e5e5, stop:1 #d0d0d0);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #d5d5d5, stop:1 #c0c0c0);
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background: #2b2b2b;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLineEdit {
                    background: #3c3f41;
                    color: #ffffff;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 12px;
                    border: 2px solid #555555;
                    border-radius: 8px;
                }
                QLineEdit:focus {
                    border: 2px solid #3daee9;
                }
                QPushButton {
                    font-size: 18px;
                    padding: 10px 16px;
                    border: none;
                    border-radius: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #6a6a6a, stop:1 #555555);
                    color: #fff;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #7a7a7a, stop:1 #666666);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5a5a5a, stop:1 #444444);
                }
            """)

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)

        self._create_top_bar(main_layout)
        self._create_dual_display_area(main_layout)
        self._create_keypad(main_layout)

        self.setLayout(main_layout)

    def _create_top_bar(self, layout):
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.settings_btn = QPushButton('⚙')
        self.settings_btn.setFixedSize(42, 42)
        self.settings_btn.setToolTip("Open Settings")
        self.settings_btn.setStyleSheet("""
            font-size: 22px;
            color: #ffffff;
            background-color: #444;
            border: none;
            border-radius: 21px;
        """)
        self.settings_btn.clicked.connect(self.open_settings)

        top_bar.addWidget(self.settings_btn)
        layout.addLayout(top_bar)

    def _create_dual_display_area(self, layout):
        """Two rows: buttons + display in each."""
        dual_layout = QVBoxLayout()
        dual_layout.setSpacing(12)

        # --- Top Row (Left Calculator) ---
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.btn_rl_copy = QPushButton("Copy")
        self.btn_rl_add = QPushButton("Add")
        for btn in [self.btn_rl_copy, self.btn_rl_add]:
            btn.setFixedHeight(35)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            top_row.addWidget(btn)

        self.left_display = QLineEdit()
        self.setup_display(self.left_display, 'left')
        self.left_display.setMaximumWidth(400)
        top_row.addWidget(self.left_display)
        dual_layout.addLayout(top_row)

        # --- Bottom Row (Right Calculator) ---
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        self.btn_lr_copy = QPushButton("Copy")
        self.btn_lr_add = QPushButton("Add")
        for btn in [self.btn_lr_add, self.btn_lr_copy]:
            btn.setFixedHeight(35)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            bottom_row.addWidget(btn)

        self.right_display = QLineEdit()
        self.setup_display(self.right_display, 'right')
        self.right_display.setMaximumWidth(400)
        bottom_row.addWidget(self.right_display)
        dual_layout.addLayout(bottom_row)

        # Connect actions
        self.btn_lr_copy.clicked.connect(self.copy_left_to_right)
        self.btn_lr_add.clicked.connect(self.add_left_to_right)
        self.btn_rl_add.clicked.connect(self.add_right_to_left)
        self.btn_rl_copy.clicked.connect(self.copy_right_to_left)

        layout.addLayout(dual_layout)

    def _create_keypad(self, layout):
        keys = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('←', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('+', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('=', 5, 2, 1, 2)
        ]

        grid = QGridLayout()
        grid.setSpacing(10)

        for key in keys:
            text = key[0]
            row, col = key[1], key[2]
            rowspan = key[3] if len(key) > 3 else 1
            colspan = key[4] if len(key) > 4 else 1

            btn = QPushButton(text)
            btn.setMinimumSize(60, 60)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(self._make_key_handler(text))
            grid.addWidget(btn, row, col, rowspan, colspan)

        layout.addLayout(grid)

    def setup_display(self, display, side):
        display.setReadOnly(True)
        display.setAlignment(Qt.AlignRight)
        display.setMinimumHeight(60)
        display.setPlaceholderText("0")
        display.setFocusPolicy(Qt.ClickFocus)
        display.installEventFilter(self)

    def _make_key_handler(self, key):
        def handler():
            self.on_key(key)
        return handler

    def eventFilter(self, source, event):
        if event.type() == QEvent.FocusIn:
            if source == self.left_display:
                self.focused = 'left'
            elif source == self.right_display:
                self.focused = 'right'
        return super().eventFilter(source, event)

    @Slot()
    def on_key(self, key):
        current_display = self.left_display if self.focused == 'left' else self.right_display
        current_text = current_display.text()

        if key == 'C':
            current_display.clear()
        elif key == '←':
            current_display.setText(current_text[:-1])
        elif key == '±':
            current_display.setText(toggle_sign(current_text))
        elif key == '%':
            current_display.setText(calc_percent(current_text))
        elif key == '=':
            current_display.setText(safe_eval(current_text))
        else:
            current_display.setText(current_text + key)

    @Slot()
    def copy_left_to_right(self):
        self.right_display.setText(self.left_display.text())
        self.right_display.setFocus()

    @Slot()
    def copy_right_to_left(self):
        self.left_display.setText(self.right_display.text())
        self.left_display.setFocus()

    @Slot()
    def add_left_to_right(self):
        self.right_display.setText(self.right_display.text() + self.left_display.text())
        self.right_display.setFocus()

    @Slot()
    def add_right_to_left(self):
        self.left_display.setText(self.left_display.text() + self.right_display.text())
        self.left_display.setFocus()

    @Slot()
    def open_settings(self):
        dialog = SettingsDialog(self, current_theme=self.theme)
        if dialog.exec():
            new_theme = dialog.selected_theme()
            if new_theme != self.theme:
                self.theme = new_theme
                self.apply_theme()
