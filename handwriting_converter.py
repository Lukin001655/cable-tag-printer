#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64

class HandwritingConverter:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'models', 'deepscript_model')
        self.font_variations = ['casual', 'neat', 'messy', 'formal', 'quick']
        
    def convert_text_to_handwriting(self, text, style='casual', font_size=12):
        try:
            width = max(200, len(text) * font_size)
            height = font_size * 2
            
            img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            font = self._get_handwriting_font(font_size)
            
            x_offset = 5
            y_offset = font_size // 2
            
            for i, char in enumerate(text):
                char_x = x_offset + i * (font_size * 0.6) + np.random.uniform(-1, 1)
                char_y = y_offset + np.random.uniform(-2, 2)
                
                draw.text((char_x, char_y), char, fill=(0, 0, 0, 255), font=font)
            
            return img
            
        except Exception as e:
            return self._create_simple_text_image(text, font_size)
    
    def _get_handwriting_font(self, size):
        handwriting_fonts = [
            'C:/Windows/Fonts/segoepr.ttf',
            'C:/Windows/Fonts/comic.ttf',
            'C:/Windows/Fonts/comicbd.ttf',
        ]
        
        for font_path in handwriting_fonts:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        try:
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def _create_simple_text_image(self, text, font_size):
        width = max(200, len(text) * font_size)
        height = font_size * 2
        
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        font = self._get_handwriting_font(font_size)
        draw.text((5, font_size // 2), text, fill=(0, 0, 0, 255), font=font)
        
        return img
    
    def convert_data(self, data, style='casual', font_size=12):
        converted_data = []
        
        for number, text in data:
            handwriting_img = self.convert_text_to_handwriting(text, style, font_size)
            
            img_buffer = io.BytesIO()
            handwriting_img.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            converted_data.append((number, img_base64))
        
        return converted_data
    
    def image_from_base64(self, base64_string):
        img_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(img_data))