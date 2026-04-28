"""
Custom Widgets for consistent UI
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AnimatedButton(QPushButton):
    """Button with hover effect"""
    
    def __init__(self, text, parent=None, color="#129990"):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #096B68;
            }}
        """)


class StyledLineEdit(QLineEdit):
    """Styled input field"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(42)
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #129990;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 13px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #096B68;
            }
            QLineEdit:hover {
                border-color: #096B68;
            }
        """)


class StyledTextEdit(QTextEdit):
    """Styled text area"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMaximumHeight(70)
        self.setMinimumHeight(65)
        self.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #129990;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 13px;
                color: #2c3e50;
            }
            QTextEdit:focus {
                border-color: #096B68;
            }
        """)


class StyledComboBox(QComboBox):
    """Styled dropdown"""
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setMinimumHeight(42)
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #129990;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 13px;
                color: #2c3e50;
            }
            QComboBox:focus {
                border-color: #096B68;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #129990;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #129990;
                border-radius: 8px;
                selection-background-color: #129990;
                selection-color: white;
                padding: 5px;
            }
        """)
        if placeholder:
            self.addItem(placeholder, None)


class StyledSpinBox(QSpinBox):
    """Styled quantity selector"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(1, 99)
        self.setValue(1)
        self.setMinimumHeight(42)
        self.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #129990;
                border-radius: 10px;
                padding: 8px 10px;
                font-size: 13px;
                color: #2c3e50;
            }
            QSpinBox:focus {
                border-color: #096B68;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 25px;
                background-color: #90D1CA;
                border-radius: 5px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #129990;
            }
        """)


class SectionTitle(QLabel):
    """Styled section title"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #129990;
            margin-bottom: 12px;
            margin-top: 5px;
        """)


class InfoCard(QFrame):
    """Information card for shortcuts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #90D1CA;
                border-radius: 12px;
                padding: 12px;
                margin-top: 15px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 11px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title = QLabel("⚡ KEYBOARD SHORTCUTS")
        title.setStyleSheet("font-weight: bold; font-size: 12px; color: #096B68;")
        layout.addWidget(title)
        
        layout.addWidget(QLabel("• ENTER → Print Bill"))
        layout.addWidget(QLabel("• Ctrl+N → New Order"))
        layout.addWidget(QLabel("• TAB → Next Field"))
        layout.addWidget(QLabel("• F1 → Help"))


class CardFrame(QFrame):
    """Statistics card"""
    
    def __init__(self, title, value, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #90D1CA;
                padding: 15px;
                min-width: 140px;
            }
        """)
        layout = QVBoxLayout(self)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 11px; color: #096B68; font-weight: bold;")
        layout.addWidget(title_label)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #129990;")
        layout.addWidget(self.value_label)
    
    def set_value(self, value):
        self.value_label.setText(value)