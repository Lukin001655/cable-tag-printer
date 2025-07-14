#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import io
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from handwriting_converter import HandwritingConverter

class PDFHandler:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.converter = HandwritingConverter()
        
        self.page_width = 210
        self.page_height = 297
        self.cols = 3
        self.rows = 4
        self.tag_width = self.page_width / self.cols
        self.tag_height = self.page_height / self.rows
        
        self.text_positions = {
            'triangle': [
                (self.tag_width/2, self.tag_height*0.3),
                (self.tag_width/2, self.tag_height*0.7),
            ],
            'square': [
                (self.tag_width/2, self.tag_height*0.3),
                (self.tag_width/2, self.tag_height*0.7),
            ]
        }
        
    def create_pdf(self, data, template_type, font_size=12):
        template_key = 'triangle' if template_type == 'Triangular' else 'square'
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"cable_tags_{template_type.lower()}_{timestamp}.pdf"
        output_path = os.path.join(os.path.dirname(__file__), 'output', output_filename)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        c = canvas.Canvas(output_path, pagesize=A4)
        
        tags_per_page = 12
        page_number = 1
        
        for page_start in range(0, len(data), tags_per_page):
            page_data = data[page_start:page_start + tags_per_page]
            
            self._draw_template_background(c, template_key)
            self._place_text_on_tags(c, page_data, template_key, font_size)
            self._add_page_info(c, page_number, len(data))
            
            if page_start + tags_per_page < len(data):
                c.showPage()
                page_number += 1
        
        c.save()
        return output_path
    
    def _draw_template_background(self, canvas_obj, template_key):
        canvas_obj.setStrokeColorRGB(0.8, 0.8, 0.8)
        canvas_obj.setLineWidth(0.5)
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.tag_width * mm
                y = (self.page_height - (row + 1) * self.tag_height) * mm
                
                if template_key == 'triangle':
                    self._draw_triangle_template(canvas_obj, x, y)
                else:
                    self._draw_square_template(canvas_obj, x, y)
                
    def _draw_triangle_template(self, canvas_obj, x, y):
        width = self.tag_width * mm
        height = self.tag_height * mm
        
        canvas_obj.beginPath()
        canvas_obj.moveTo(x + width/2, y + height)
        canvas_obj.lineTo(x, y)
        canvas_obj.lineTo(x + width, y)
        canvas_obj.closePath()
        canvas_obj.stroke()
        
        field_width = width * 0.4
        field_height = height * 0.15
        
        canvas_obj.ellipse(x + width/2 - field_width/2, y + height*0.7 - field_height/2,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       