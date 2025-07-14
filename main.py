#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cable Tag Printer - Главный файл приложения
Автор: Lukin001655
Описание: Приложение для печати кабельных бирок с преобразованием текста в рукописный
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import CableTagPrinterGUI

def main():
    """Главная функция запуска приложения"""
    app = QApplication(sys.argv)
    
    # Установка иконки приложения
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Создание главного окна
    window = CableTagPrinterGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()