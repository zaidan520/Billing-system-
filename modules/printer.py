"""
Printing Module - Thermal Printer Support
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PrinterEngine:
    def __init__(self, database):
        self.db = database
        self.restaurant_name = self.db.get_setting('restaurant_name', 'Raza Foods')
        self.restaurant_address = self.db.get_setting('restaurant_address', '123 Main Street')
        self.restaurant_phone = self.db.get_setting('restaurant_phone', '+92 123 4567890')
    
    def print_receipt(self, order_data):
        """Print receipt and save PDF"""
        pdf_path = self.save_receipt(order_data)
        
        printer_enabled = self.db.get_setting('printer_enabled', '1') == '1'
        
        if printer_enabled:
            try:
                # Placeholder for actual thermal printer connection
                print(f"Printing: {order_data['bill_number']}")
                return True, f"Bill printed! Bill #: {order_data['bill_number']}"
            except Exception as e:
                return False, f"Printer error: {str(e)}. PDF saved."
        else:
            return True, f"PDF saved: {pdf_path}"
    
    def save_receipt(self, order_data):
        """Save receipt as PDF for thermal printer"""
        
        receipts_dir = 'receipts'
        if not os.path.exists(receipts_dir):
            os.makedirs(receipts_dir)
        
        filename = f"{receipts_dir}/bill_{order_data['bill_number']}.pdf"
        
        # 80mm thermal paper
        doc = SimpleDocTemplate(filename, pagesize=(80*mm, 220*mm),
                                topMargin=5*mm, bottomMargin=5*mm,
                                leftMargin=5*mm, rightMargin=5*mm)
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'],
                                      fontSize=12, alignment=1, spaceAfter=3, fontName='Helvetica-Bold')
        header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'],
                                       fontSize=9, alignment=1, spaceAfter=2)
        normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'],
                                       fontSize=9, alignment=0, spaceAfter=1)
        bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'],
                                     fontSize=10, alignment=0, fontName='Helvetica-Bold')
        center_bold = ParagraphStyle('CenterBold', parent=styles['Normal'],
                                      fontSize=10, alignment=1, fontName='Helvetica-Bold')
        
        story = []
        
        # Header
        story.append(Paragraph(self.restaurant_name, title_style))
        story.append(Paragraph(self.restaurant_address, header_style))
        story.append(Paragraph(f"Tel: {self.restaurant_phone}", header_style))
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph("-" * 32, normal_style))
        
        # Bill Info
        story.append(Paragraph(f"Bill #: {order_data['bill_number']}", normal_style))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        story.append(Spacer(1, 2*mm))
        
        # Customer
        story.append(Paragraph(f"Customer: {order_data['customer_name']}", normal_style))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph("-" * 32, normal_style))
        
        # Items - Clean format
        story.append(Paragraph("Item                Qty    Total", bold_style))
        story.append(Paragraph("-" * 32, normal_style))
        
        for item in order_data['items']:
            name = item['name'][:18]
            qty = item['quantity']
            total = item['price'] * qty
            line = f"{name:<18}  {qty:>2}    PKR {total:>6,.0f}"
            story.append(Paragraph(line, normal_style))
        
        story.append(Paragraph("-" * 32, normal_style))
        story.append(Paragraph(f"TOTAL:                       PKR {order_data['total']:>7,.0f}", bold_style))
        story.append(Paragraph("=" * 32, normal_style))
        story.append(Spacer(1, 5*mm))
        
        # Footer
        story.append(Paragraph("Thank you for visiting!", center_bold))
        
        doc.build(story)
        return filename