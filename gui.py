#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI интерфейс для Cable Tag Printer
"""

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                                 QPushButton, QLabel, QComboBox, QFileDialog, 
                                 QTextEdit, QProgressBar, QGroupBox, QSpinBox,
                                 QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from excel_handler import ExcelHandler
from pdf_handler import PDFHandler
from handwriting_converter import HandwritingConverter

class ProcessingThread(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, excel_file, template_type, font_size, handwriting_enabled):
        super().__init__()
        self.excel_file = excel_file
        self.template_type = template_type
        self.font_size = font_size
        self.handwriting_enabled = handwriting_enabled
        
    def run(self):
        try:
            self.status_update.emit("Checking excel file...")
            self.progress_update.emit(20)
            
            excel_handler = ExcelHandler()
            data = excel_handler.read_excel(self.excel_file)
            
            if self.handwriting_enabled:
                self.status_update.emit("Converting to handwriting...")
                self.progress_update.emit(40)
                
                converter = HandwritingConverter()
                data = converter.convert_data(data)
            
            self.status_update.emit("Creating PDF...")
            self.progress_update.emit(60)
            
            pdf_handler = PDFHandler()
            output_path = pdf_handler.create_pdf(data, self.template_type, self.font_size)
            
            self.progress_update.emit(100)
            self.status_update.emit("Done!")
            self.finished.emit(True, output_path)
            
        except Exception as e:
            self.finished.emit(False, str(e))

class CableTagPrinterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.excel_file = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Cable Tag Printer v1.0")
        self.setGeometry(100, 100, 600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        title_label = QLabel("Cable Tag Printer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)
        
        file_group = QGroupBox("1. Select Excel File")
        file_layout = QVBoxLayout(file_group)
        
        self.file_label = QLabel("No file selected")
        file_layout.addWidget(self.file_label)
        
        self.select_file_btn = QPushButton("Select Excel File")
        self.select_file_btn.clicked.connect(self.select_excel_file)
        file_layout.addWidget(self.select_file_btn)
        
        layout.addWidget(file_group)
        
        settings_group = QGroupBox("2. Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Tag Type:"))
        self.template_combo = QComboBox()
        self.template_combo.addItems(["Triangular", "Square"])
        template_layout.addWidget(self.template_combo)
        settings_layout.addLayout(template_layout)
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        font_layout.addWidget(self.font_size_spin)
        settings_layout.addLayout(font_layout)
        
        self.handwriting_check = QCheckBox("Convert to Handwriting")
        self.handwriting_check.setChecked(True)
        settings_layout.addWidget(self.handwriting_check)
        
        layout.addWidget(settings_group)
        
        buttons_layout = QHBoxLayout()
        
        self.place_btn = QPushButton("Place Text")
        self.place_btn.clicked.connect(self.place_text)
        self.place_btn.setEnabled(False)
        buttons_layout.addWidget(self.place_btn)
        
        self.create_pdf_btn = QPushButton("Create PDF")
        self.create_pdf_btn.clicked.connect(self.create_pdf)
        self.create_pdf_btn.setEnabled(False)
        buttons_layout.addWidget(self.create_pdf_btn)
        
        layout.addLayout(buttons_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(100)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)
        
    def select_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel files (*.tlsx *.hls)")
        
        if file_path:
            self.excel_file = file_path
            self.file_label.setText(f"File: {os.path.basename(file_path)}")
            self.place_btn.setEnabled(True)
            self.log_text.append(f"Selected file: {file_path}")
            
    def place_text(self):
        if not self.excel_file:
            QMessageBox.warning(self, "Error", "Select Excel file")
            return
            
        self.create_pdf_btn.setEnabled(True)
        self.log_text.append("Text placed on tags")
        
    def create_pdf(self):
        if not self.excel_file:
            QMessageBox.warning(self, "Error", "Select Excel file")
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.processing_thread = ProcessingThread(
            self.excel_file,
            self.template_combo.currentText(),
            self.font_size_spin.value(),
            self.handwriting_check.isChecked()
        )
        
        self.processing_thread.progress_update.connect(self.progress_bar.setValue)
        self.processing_thread.status_update.connect(self.status_label.setText)
        self.processing_thread.finished.connect(self.on_processing_finished)
        
        self.processing_thread.start()
        
    def on_processing_finished(self, success, message):
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Success", f"PDF created: {message}")
            self.log_text.append(f"PDF created: {message}")
        else:
            QMessageBox.critical(self, "Error", f"Error creating PDF: {message}")
            self.log_text.append(f"Error: {message}")
            
        self.status_label.setText("Ready")