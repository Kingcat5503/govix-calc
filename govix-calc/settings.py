from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QRadioButton,
    QPushButton, QButtonGroup
)
from PySide6.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_theme='dark'):
        super().__init__(parent)
        self.setWindowTitle('Govix Calc – Settings')
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(300, 220)

        # Apply theme-specific styling
        if current_theme == 'light':
            self.setStyleSheet("""
                QDialog { background: #f0f0f0; }
                QLabel, QRadioButton, QPushButton { color: #000000; }
            """)
        else:
            self.setStyleSheet("""
                QDialog { background: #2b2b2b; }
                QLabel, QRadioButton, QPushButton { color: #ffffff; }
            """)

        # Layout setup
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Theme selection
        layout.addWidget(QLabel('Choose Theme:'))

        self.theme_group = QButtonGroup(self)
        self.dark_radio = QRadioButton('Dark')
        self.light_radio = QRadioButton('Light')

        self.theme_group.addButton(self.dark_radio)
        self.theme_group.addButton(self.light_radio)

        layout.addWidget(self.dark_radio)
        layout.addWidget(self.light_radio)

        self.dark_radio.setChecked(current_theme != 'light')
        self.light_radio.setChecked(current_theme == 'light')

        # About section
        layout.addSpacing(10)
        layout.addWidget(QLabel('About Govix Calc:'))

        about = QLabel(
            'Version 1.0\n'
            'Built with ❤️ using Python & PySide6.\n'
            'A dual-display calculator for power users.'
        )
        about.setWordWrap(True)
        layout.addWidget(about)

        # Close button
        close_btn = QPushButton('Close')
        close_btn.setFixedWidth(80)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def selected_theme(self) -> str:
        return 'light' if self.light_radio.isChecked() else 'dark'
