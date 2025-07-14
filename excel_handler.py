#!/usr/bin/env python3
# -*- coding: utf-8 -*-
pandas = pd
os = os

class ExcelHandler:
    def __init__(self):
        self.data = None
        
    def read_excel(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            df = pd.read_excel(file_path, header=None)
            
            if df.shape[1] < 2:
                raise ValueError("Excel file must contain at least 2 columns")
                
            data = []
            for index, row in df.iterrows():
                number = row[0] if pd.notna(row[0]) else ""
                text = row[1] if pd.notna(row[1]) else ""
                
                if str(number).strip() == "" and str(text).strip() == "":
                    continue
                    
                data.append((str(number), str(text)))
                
            if not data:
                raise ValueError("No data found in Excel file")
                
            self.data = data
            return data
            
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")
            
    def validate_data(self, data):
        if not data:
            return False
            
        for item in data:
            if len(item) != 2:
                return False
                
        return True
        
    def get_data_info(self):
        if not self.data:
            return {"count": 0, "preview": []}
            
        info = {
            "count": len(self.data),
            "preview": self.data[:5]
        }
        
        return info