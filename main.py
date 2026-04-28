#!/usr/bin/env python3
"""
Restaurant Billing System - Main Entry Point
Modular Architecture - Clean UI Design
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from modules.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()