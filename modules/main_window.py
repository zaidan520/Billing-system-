"""
Main Billing Window - Clean UI, Keyboard Focused
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from database import Database
from modules.printer import PrinterEngine
from modules.widgets import (
    AnimatedButton, StyledLineEdit, StyledTextEdit, 
    StyledComboBox, StyledSpinBox, SectionTitle, InfoCard
)
from utils.constants import COLORS, get_item_emoji, get_category_emoji
from utils.helpers import format_currency, get_current_datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.printer = PrinterEngine(self.db)
        
        self.current_order = {'customer_id': None, 'items': [], 'subtotal': 0}
        self.load_stylesheet()
        self.init_ui()
        self.load_menu()
        self.load_dropdown()
        
        # Timer for clock
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # Refresh summary timer
        self.summary_timer = QTimer()
        self.summary_timer.timeout.connect(self.update_summary)
        self.summary_timer.start(5000)
        
        self.update_summary()
        self.name_input.setFocus()
    
    def load_stylesheet(self):
        try:
            with open('style.css', 'r') as f:
                self.setStyleSheet(f.read())
        except:
            pass
    
    def init_ui(self):
        self.setWindowTitle("Raza Food Billing")
        self.setMinimumSize(1300, 800)
        self.setStyleSheet(f"QMainWindow {{ background-color: {COLORS['background']}; }}")
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== HEADER =====
        header = QWidget()
        header.setStyleSheet(f"background-color: white; border-radius: 15px; padding: 10px;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("🍽️ RAZA FOOD BILLING")
        title.setStyleSheet(f"font-size: 22pt; font-weight: bold; color: #129990;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(f"background-color: #90D1CA; padding: 8px 18px; border-radius: 25px; font-weight: bold;")
        header_layout.addWidget(self.summary_label)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"font-size: 12pt; font-weight: bold; color: #096B68; padding: 8px;")
        header_layout.addWidget(self.time_label)
        
        self.admin_btn = AnimatedButton("🔐 Admin", color="#129990")
        self.admin_btn.setFixedSize(90, 40)
        self.admin_btn.clicked.connect(self.open_admin)
        header_layout.addWidget(self.admin_btn)
        
        main_layout.addWidget(header)
        
        # ===== MAIN CONTENT =====
        content = QHBoxLayout()
        content.setSpacing(15)
        
        # LEFT PANEL
        left_panel = self.create_left_panel()
        content.addWidget(left_panel, 28)
        
        # MIDDLE PANEL - MENU
        middle_panel = self.create_menu_panel()
        content.addWidget(middle_panel, 47)
        
        # RIGHT PANEL
        right_panel = self.create_order_panel()
        content.addWidget(right_panel, 25)
        
        main_layout.addLayout(content)
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ Ready | ENTER = Print Bill | Ctrl+N = New Order", 5000)
        
        # Keyboard Shortcuts
        QShortcut(QKeySequence("Return"), self, self.print_bill)
        QShortcut(QKeySequence("Ctrl+N"), self, self.clear_order)
        QShortcut(QKeySequence("F1"), self, self.show_help)
        QShortcut(QKeySequence("Tab"), self, self.focus_next)
    
    def focus_next(self):
        if self.name_input.hasFocus():
            self.phone_input.setFocus()
        elif self.phone_input.hasFocus():
            self.address_input.setFocus()
        elif self.address_input.hasFocus():
            self.item_dropdown.setFocus()
        elif self.item_dropdown.hasFocus():
            self.dropdown_qty.setFocus()
        else:
            self.name_input.setFocus()
    
    def create_left_panel(self):
        panel = QWidget()
        panel.setStyleSheet(f"background-color: white; border-radius: 15px; padding: 15px;")
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Customer section
        title = SectionTitle("👤 CUSTOMER DETAILS")
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Name"))
        self.name_input = StyledLineEdit("Customer name (optional)")
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("Phone"))
        self.phone_input = StyledLineEdit("Optional")
        layout.addWidget(self.phone_input)
        
        layout.addWidget(QLabel("Address"))
        self.address_input = StyledTextEdit("Optional")
        layout.addWidget(self.address_input)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e0e0e0; height: 1px; margin: 10px 0;")
        layout.addWidget(line)
        
        # Dropdown section
        dropdown_title = SectionTitle("🍔 OR SELECT FROM DROPDOWN")
        layout.addWidget(dropdown_title)
        
        self.item_dropdown = StyledComboBox("-- Select Item --")
        layout.addWidget(self.item_dropdown)
        
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Quantity"))
        self.dropdown_qty = StyledSpinBox()
        qty_layout.addWidget(self.dropdown_qty)
        qty_layout.addStretch()
        layout.addLayout(qty_layout)
        
        self.add_btn = AnimatedButton("➕ Add Item", color="#129990")
        self.add_btn.clicked.connect(self.add_from_dropdown)
        layout.addWidget(self.add_btn)
        
        layout.addStretch()
        
        # Shortcuts
        info_card = InfoCard()
        layout.addWidget(info_card)
        
        return panel
    
    def create_menu_panel(self):
        panel = QWidget()
        panel.setStyleSheet(f"background-color: white; border-radius: 15px; padding: 15px;")
        layout = QVBoxLayout(panel)
        
        title = SectionTitle("🍕 MENU (Click to Add)")
        layout.addWidget(title)
        
        self.menu_scroll = QScrollArea()
        self.menu_scroll.setWidgetResizable(True)
        self.menu_scroll.setStyleSheet("border: none; background-color: transparent;")
        
        self.menu_container = QWidget()
        self.menu_grid = QGridLayout(self.menu_container)
        self.menu_grid.setSpacing(10)
        self.menu_grid.setContentsMargins(10, 10, 10, 10)
        
        self.menu_scroll.setWidget(self.menu_container)
        layout.addWidget(self.menu_scroll)
        
        return panel
    
    def create_order_panel(self):
        panel = QWidget()
        panel.setStyleSheet(f"background-color: white; border-radius: 15px; padding: 15px;")
        layout = QVBoxLayout(panel)
        
        title = SectionTitle("🛒 CURRENT ORDER")
        layout.addWidget(title)
        
        self.order_list = QListWidget()
        self.order_list.setMinimumHeight(350)
        layout.addWidget(self.order_list)
        
        # Bill Summary
        summary = QFrame()
        summary.setStyleSheet(f"background-color: #90D1CA; border-radius: 12px; padding: 15px;")
        summary_layout = QVBoxLayout(summary)
        
        self.subtotal_label = QLabel("Subtotal: PKR 0")
        self.subtotal_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        summary_layout.addWidget(self.subtotal_label)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #129990; height: 2px;")
        summary_layout.addWidget(line)
        
        self.total_label = QLabel("TOTAL: PKR 0")
        self.total_label.setStyleSheet("font-size: 22pt; font-weight: bold; color: #129990;")
        summary_layout.addWidget(self.total_label)
        
        layout.addWidget(summary)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.print_btn = AnimatedButton("🖨️ PRINT", color="#27ae60")
        self.print_btn.clicked.connect(self.print_bill)
        btn_layout.addWidget(self.print_btn)
        
        self.clear_btn = AnimatedButton("🗑️ CLEAR", color="#e74c3c")
        self.clear_btn.clicked.connect(self.clear_order)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        return panel
    
    def load_menu(self):
        """Load menu items into grid - FIXED display"""
        for i in reversed(range(self.menu_grid.count())):
            w = self.menu_grid.itemAt(i).widget()
            if w:
                w.deleteLater()
        
        menu_by_cat = self.db.get_menu_by_category()
        row = 0
        
        for category, items in menu_by_cat.items():
            # Category header
            emoji = get_category_emoji(category)
            cat_label = QLabel(f"{emoji}  {category}")
            cat_label.setStyleSheet(f"""
                font-size: 14pt; 
                font-weight: bold; 
                color: #129990; 
                padding: 8px;
                margin-top: 5px;
                background-color: #FFFBDE;
                border-radius: 8px;
            """)
            self.menu_grid.addWidget(cat_label, row, 0, 1, 4)
            row += 1
            
            # Items in this category
            col = 0
            for item in items:
                item_id, name, price = item
                
                # Create button with clear text
                btn = QPushButton()
                btn.setText(f"{name}\n{format_currency(price)}")
                btn.setMinimumHeight(70)
                btn.setMinimumWidth(150)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #90D1CA;
                        color: #2c3e50;
                        border: none;
                        border-radius: 10px;
                        font-size: 11px;
                        font-weight: bold;
                        text-align: center;
                        padding: 8px;
                    }
                    QPushButton:hover {
                        background-color: #129990;
                        color: white;
                    }
                """)
                btn.clicked.connect(lambda checked, iid=item_id, p=price, n=name: self.add_to_order(iid, n, p))
                self.menu_grid.addWidget(btn, row, col)
                
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
            
            if col > 0:
                row += 1
            row += 1
    
    def load_dropdown(self):
        items = self.db.get_menu_items(available_only=True)
        for item in items:
            item_id, name, category, price = item
            self.item_dropdown.addItem(f"{name} - {format_currency(price)}", 
                                       {'id': item_id, 'name': name, 'price': price})
    
    def add_from_dropdown(self):
        data = self.item_dropdown.currentData()
        if not data:
            return
        qty = self.dropdown_qty.value()
        for _ in range(qty):
            self.add_to_order(data['id'], data['name'], data['price'])
        self.show_message(f"Added {qty}x {data['name']}")
    
    def add_to_order(self, item_id, name, price):
        for item in self.current_order['items']:
            if item['id'] == item_id:
                item['quantity'] += 1
                self.update_order()
                return
        self.current_order['items'].append({'id': item_id, 'name': name, 'price': price, 'quantity': 1})
        self.update_order()
    
    def update_order(self):
        self.order_list.clear()
        subtotal = 0
        for item in self.current_order['items']:
            total = item['price'] * item['quantity']
            subtotal += total
            self.order_list.addItem(f"{item['quantity']}x  {item['name']:<20}  {format_currency(total)}")
        
        self.current_order['subtotal'] = subtotal
        self.subtotal_label.setText(f"Subtotal: {format_currency(subtotal)}")
        self.total_label.setText(f"TOTAL: {format_currency(subtotal)}")
    
    def remove_item(self, item):
        row = self.order_list.row(item)
        if row >= 0:
            removed = self.current_order['items'].pop(row)
            self.update_order()
            self.show_message(f"Removed {removed['name']}")
    
    def clear_order(self):
        self.current_order = {'customer_id': None, 'items': [], 'subtotal': 0}
        self.update_order()
        self.show_message("Order cleared")
    
    def update_summary(self):
        summary = self.db.get_sales_summary('today')
        self.summary_label.setText(f"📊 Today: {summary['orders']} orders | {format_currency(summary['total'])}")
    
    def update_time(self):
        self.time_label.setText(get_current_datetime())
    
    def show_message(self, msg):
        self.status_bar.showMessage(f"✅ {msg}", 2000)
    
    def print_bill(self):
        if not self.current_order['items']:
            self.show_message("No items in order!")
            return
        
        name = self.name_input.text().strip() or "Walk-in Customer"
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()
        
        customer_id = self.current_order['customer_id']
        if not customer_id and name != "Walk-in Customer":
            customer_id = self.db.add_customer(name, phone, address)
        
        subtotal = self.current_order['subtotal']
        order_id, bill_number = self.db.save_order(customer_id, self.current_order['items'], subtotal, 0)
        
        order_data = {
            'bill_number': bill_number,
            'customer_name': name,
            'customer_phone': phone,
            'customer_address': address,
            'items': self.current_order['items'],
            'subtotal': subtotal,
            'total': subtotal
        }
        
        success, msg = self.printer.print_receipt(order_data)
        
        msg_box = QMessageBox(self)
        if success:
            msg_box.setWindowTitle("Success")
            msg_box.setText(f"✅ Bill Printed!\n\n🧾 Bill #: {bill_number}\n💰 Total: {format_currency(subtotal)}")
            msg_box.setIcon(QMessageBox.Information)
        else:
            msg_box.setWindowTitle("Error")
            msg_box.setText(f"⚠️ Printer Error!\n\n{msg}\nPDF saved.")
            msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()
        
        # Clear for next order
        self.clear_order()
        self.name_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.name_input.setFocus()
        self.update_summary()
    
    def show_help(self):
        help_text = """
        <h2 style='color:#129990'>Quick Help Guide</h2>
        <b>Keyboard Shortcuts:</b><br>
        • <b>ENTER</b> - Print Bill<br>
        • <b>Ctrl+N</b> - New Order<br>
        • <b>TAB</b> - Next Field<br>
        • <b>F1</b> - Help<br><br>
        
        How to Add Items:<br>
        • Click menu buttons OR<br>
        • Use dropdown on left panel<br><br>
        
        Customer:<br>
        • Name is optional<br>
        • Leave blank for "Walk-in Customer"<br><br>
        
        After Printing:<br>
        • Screen clears automatically
        """
        QMessageBox.information(self, "Help", help_text)
    
    def open_admin(self):
        from modules.admin_panel import AdminPanel
        self.admin_window = AdminPanel(self.db)
        self.admin_window.show()