"""
Admin Panel - Reports, Items Management
ADDED: Food Items column to show what was sold
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from utils.constants import COLORS
from utils.helpers import format_currency

class AdminPanel(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.db = database
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        self.setWindowTitle("Admin - Raza Food Billing")
        self.setMinimumSize(1300, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("🔐 ADMIN DASHBOARD")
        title.setStyleSheet(f"font-size: 22pt; font-weight: bold; color: #129990;")
        header.addWidget(title)
        header.addStretch()
        
        self.user_label = QLabel()
        header.addWidget(self.user_label)
        
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 8px; padding: 8px 15px;")
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setVisible(False)
        header.addWidget(self.logout_btn)
        
        layout.addLayout(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setVisible(False)
        layout.addWidget(self.tabs)
        
        self.create_reports_tab()
        self.create_items_tab()
    
    def create_reports_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Date filter
        filter_frame = QGroupBox("📅 FILTER REPORTS")
        filter_layout = QHBoxLayout(filter_frame)
        
        filter_layout.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("To:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        filter_layout.addWidget(self.end_date)
        
        self.load_btn = QPushButton("🔍 Load Reports")
        self.load_btn.setStyleSheet("background-color: #129990; color: white; border-radius: 8px; padding: 8px 20px;")
        self.load_btn.clicked.connect(self.load_reports)
        filter_layout.addWidget(self.load_btn)
        
        self.download_btn = QPushButton("📎 Download Excel")
        self.download_btn.setStyleSheet("background-color: #27ae60; color: white; border-radius: 8px; padding: 8px 20px;")
        self.download_btn.clicked.connect(self.download_report)
        filter_layout.addWidget(self.download_btn)
        
        layout.addWidget(filter_frame)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        self.total_sales_label = QLabel("💰 Total Sales: PKR 0")
        self.total_orders_label = QLabel("📊 Total Orders: 0")
        self.avg_order_label = QLabel("📈 Average Order: PKR 0")
        
        for label in [self.total_sales_label, self.total_orders_label, self.avg_order_label]:
            label.setStyleSheet(f"background-color: #90D1CA; padding: 12px; border-radius: 10px; font-weight: bold; font-size: 12px;")
            stats_layout.addWidget(label)
        
        layout.addLayout(stats_layout)
        
        # Orders table - ADDED Food Items column
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["🧾 Bill #", "👤 Customer", "🍽️ Food Items", "💰 Amount", "📅 Date"])
        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.horizontalHeader().setStretchLastSection(True)
        self.orders_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #90D1CA;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #129990;
                color: white;
                padding: 10px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.orders_table)
        
        self.load_reports()
        self.tabs.addTab(tab, "📊 SALES REPORTS")
    
    def create_items_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Add item form
        form_layout = QHBoxLayout()
        
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText("Item Name")
        self.item_name.setStyleSheet("padding: 10px; border: 2px solid #90D1CA; border-radius: 8px;")
        form_layout.addWidget(self.item_name)
        
        self.item_category = QLineEdit()
        self.item_category.setPlaceholderText("Category")
        self.item_category.setStyleSheet("padding: 10px; border: 2px solid #90D1CA; border-radius: 8px;")
        form_layout.addWidget(self.item_category)
        
        self.item_price = QSpinBox()
        self.item_price.setRange(0, 10000)
        self.item_price.setSuffix(" PKR")
        self.item_price.setStyleSheet("padding: 10px; border: 2px solid #90D1CA; border-radius: 8px;")
        form_layout.addWidget(self.item_price)
        
        add_btn = QPushButton("➕ Add Item")
        add_btn.setStyleSheet("background-color: #129990; color: white; border-radius: 8px; padding: 10px 20px;")
        add_btn.clicked.connect(self.add_item)
        form_layout.addWidget(add_btn)
        
        layout.addLayout(form_layout)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels(["ID", "Item Name", "Category", "Price"])
        self.items_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #90D1CA;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #129990;
                color: white;
                padding: 10px;
            }
        """)
        layout.addWidget(self.items_table)
        
        self.load_items()
        self.tabs.addTab(tab, "📝 MENU ITEMS")
    
    def load_reports(self):
        """Load sales report with food items"""
        try:
            start = self.start_date.date().toString("yyyy-MM-dd")
            end = self.end_date.date().toString("yyyy-MM-dd")
            
            # Get orders with their items
            orders = self.db.get_orders_by_date(start, end)
            
            total_sales = sum(order[3] for order in orders)
            total_orders = len(orders)
            avg_order = total_sales / total_orders if total_orders > 0 else 0
            
            self.total_sales_label.setText(f"💰 Total Sales: {format_currency(total_sales)}")
            self.total_orders_label.setText(f"📊 Total Orders: {total_orders}")
            self.avg_order_label.setText(f"📈 Average Order: {format_currency(avg_order)}")
            
            self.orders_table.setRowCount(len(orders))
            
            for row, order in enumerate(orders):
                order_id = order[0]
                bill_number = order[1]
                customer_name = order[2] if order[2] else "Walk-in"
                amount = order[3]
                date_str = order[4][:10] if order[4] else ""
                
                # Get order details to fetch items
                order_details = self.db.get_order_details(order_id)
                items_list = []
                if order_details and 'items' in order_details:
                    for item in order_details['items']:
                        items_list.append(f"{item['quantity']}x {item['name']}")
                
                food_items = ", ".join(items_list) if items_list else "-"
                
                self.orders_table.setItem(row, 0, QTableWidgetItem(bill_number))
                self.orders_table.setItem(row, 1, QTableWidgetItem(customer_name))
                self.orders_table.setItem(row, 2, QTableWidgetItem(food_items))
                self.orders_table.setItem(row, 3, QTableWidgetItem(format_currency(amount)))
                self.orders_table.setItem(row, 4, QTableWidgetItem(date_str))
            
            self.orders_table.resizeColumnsToContents()
            # Set column widths
            self.orders_table.setColumnWidth(0, 150)  # Bill #
            self.orders_table.setColumnWidth(1, 120)  # Customer
            self.orders_table.setColumnWidth(2, 300)  # Food Items (wider)
            self.orders_table.setColumnWidth(3, 100)  # Amount
            self.orders_table.setColumnWidth(4, 110)  # Date
            
        except Exception as e:
            print(f"Error loading reports: {e}")
            QMessageBox.warning(self, "Error", f"Could not load report: {str(e)}")
    
    def download_report(self):
        """Download report to Excel with food items"""
        try:
            import pandas as pd
            start = self.start_date.date().toString("yyyy-MM-dd")
            end = self.end_date.date().toString("yyyy-MM-dd")
            
            orders = self.db.get_orders_by_date(start, end)
            
            data = []
            for order in orders:
                order_id = order[0]
                order_details = self.db.get_order_details(order_id)
                items_list = []
                if order_details and 'items' in order_details:
                    for item in order_details['items']:
                        items_list.append(f"{item['quantity']}x {item['name']} ({format_currency(item['price'])})")
                
                food_items = ", ".join(items_list) if items_list else "-"
                
                data.append({
                    'Bill Number': order[1],
                    'Customer': order[2] if order[2] else 'Walk-in',
                    'Food Items': food_items,
                    'Amount': order[3],
                    'Date': order[4]
                })
            
            df = pd.DataFrame(data)
            filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            QMessageBox.information(self, "Success", f"Report saved to {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Export failed: {str(e)}")
    
    def load_items(self):
        """Load menu items"""
        items = self.db.get_menu_items(available_only=False)
        self.items_table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.items_table.setItem(row, 0, QTableWidgetItem(str(item[0])))
            self.items_table.setItem(row, 1, QTableWidgetItem(item[1]))
            self.items_table.setItem(row, 2, QTableWidgetItem(item[2]))
            self.items_table.setItem(row, 3, QTableWidgetItem(format_currency(item[3])))
        
        self.items_table.resizeColumnsToContents()
    
    def add_item(self):
        """Add new menu item"""
        name = self.item_name.text().strip()
        category = self.item_category.text().strip() or "Other"
        price = self.item_price.value()
        if name and price > 0:
            self.db.add_menu_item(name, category, price)
            self.item_name.clear()
            self.item_category.clear()
            self.item_price.setValue(0)
            self.load_items()
            QMessageBox.information(self, "Success", f"Added {name}")
    
    def show_login(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Admin Login")
        dialog.setModal(True)
        dialog.setFixedSize(380, 280)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        
        title = QLabel("🔐 ADMIN LOGIN")
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #129990; text-align: center;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        username = QLineEdit()
        username.setPlaceholderText("Username")
        username.setStyleSheet("padding: 12px; border: 2px solid #90D1CA; border-radius: 8px; font-size: 12px;")
        layout.addWidget(username)
        
        password = QLineEdit()
        password.setPlaceholderText("Password")
        password.setEchoMode(QLineEdit.Password)
        password.setStyleSheet("padding: 12px; border: 2px solid #90D1CA; border-radius: 8px; font-size: 12px;")
        layout.addWidget(password)
        
        login_btn = QPushButton("LOGIN")
        login_btn.setStyleSheet("background-color: #129990; color: white; border-radius: 8px; padding: 12px; font-weight: bold; font-size: 12px;")
        login_btn.clicked.connect(lambda: self.do_login(username.text(), password.text(), dialog))
        layout.addWidget(login_btn)
        
        dialog.exec_()
    
    def do_login(self, username, password, dialog):
        success, msg, _ = self.db.verify_admin(username, password)
        if success:
            self.user_label.setText(f"👤 {username}")
            self.user_label.setStyleSheet("color: #129990; font-weight: bold; font-size: 11px;")
            self.logout_btn.setVisible(True)
            self.tabs.setVisible(True)
            dialog.accept()
        else:
            QMessageBox.warning(self, "Error", msg)
    
    def logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()