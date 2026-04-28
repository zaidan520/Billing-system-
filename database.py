"""
Database Handler for Restaurant Billing System
"""

import sqlite3
import bcrypt
from datetime import datetime, timedelta
import os
import shutil

class Database:
    def __init__(self):
        """Initialize database connection and create tables"""
        
        # Ensure database directory exists
        if not os.path.exists('database'):
            os.makedirs('database')
        
        # Connect to database
        self.conn = sqlite3.connect('database/restaurant.db')
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Menu items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                is_available INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table with bill_number
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_number TEXT UNIQUE,
                customer_id INTEGER,
                total_amount REAL NOT NULL,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                menu_item_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
            )
        ''')
        
        # Admin users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                failed_attempts INTEGER DEFAULT 0,
                lock_until DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default admin if not exists
        cursor.execute("SELECT * FROM admin_users WHERE username = 'admin'")
        if not cursor.fetchone():
            password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt())
            cursor.execute("""
                INSERT INTO admin_users (username, password_hash, full_name) 
                VALUES (?, ?, ?)
            """, ('admin', password_hash, 'Administrator'))
        
        # Insert default settings
        default_settings = [
            ('restaurant_name', 'Raza Foods'),
            ('restaurant_address', '123 Main Street, City'),
            ('restaurant_phone', '+92 123 4567890'),
            ('tax_rate', '0'),
            ('printer_enabled', '1'),
            ('last_bill_number', '0')
        ]
        
        for key, value in default_settings:
            cursor.execute("SELECT * FROM settings WHERE key = ?", (key,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO settings (key, value) VALUES (?, ?)", (key, value))
        
        # Insert sample menu items if empty
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        if cursor.fetchone()[0] == 0:
            sample_items = [
                ('Chicken Burger', 'Burgers', 350),
                ('Beef Burger', 'Burgers', 400),
                ('Zinger Burger', 'Burgers', 450),
                ('Double Patty Burger', 'Burgers', 550),
                ('Chicken Shawarma', 'Shawarma', 300),
                ('Beef Shawarma', 'Shawarma', 350),
                ('Special Shawarma Plate', 'Shawarma', 500),
                ('French Fries', 'Sides', 150),
                ('Cheese Fries', 'Sides', 250),
                ('Onion Rings', 'Sides', 180),
                ('Cold Drink', 'Beverages', 80),
                ('Water Bottle', 'Beverages', 50),
                ('Fresh Juice', 'Beverages', 150),
                ('Tea', 'Beverages', 100),
                ('Coffee', 'Beverages', 120),
                ('Chicken Pizza', 'Pizza', 500),
                ('Beef Pizza', 'Pizza', 550),
                ('Veggie Pizza', 'Pizza', 450),
                ('Chicken Biryani', 'Rice', 250),
                ('Beef Biryani', 'Rice', 280),
                ('Garden Salad', 'Salads', 120),
                ('Chicken Salad', 'Salads', 200),
                ('Ice Cream', 'Desserts', 150),
                ('Brownie', 'Desserts', 200)
            ]
            cursor.executemany(
                "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
                sample_items
            )
        
        self.conn.commit()
    
    def get_next_bill_number(self):
        """Generate unique bill number"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'last_bill_number'")
        result = cursor.fetchone()
        last_num = int(result[0]) if result else 0
        new_num = last_num + 1
        cursor.execute("UPDATE settings SET value = ? WHERE key = 'last_bill_number'", (str(new_num),))
        self.conn.commit()
        
        today = datetime.now()
        return f"RAZA{today.strftime('%Y%m%d')}{new_num:04d}"
    
    # ========== CUSTOMER OPERATIONS ==========
    
    def search_customers(self, search_term):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, phone, address FROM customers WHERE name LIKE ? ORDER BY name LIMIT 10", (f'%{search_term}%',))
        return cursor.fetchall()
    
    def add_customer(self, name, phone='', address=''):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_customer(self, customer_id, name, phone, address):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE customers SET name = ?, phone = ?, address = ? WHERE id = ?", (name, phone, address, customer_id))
        self.conn.commit()
    
    def get_customer(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, phone, address FROM customers WHERE id = ?", (customer_id,))
        return cursor.fetchone()
    
    # ========== MENU OPERATIONS ==========
    
    def get_menu_items(self, available_only=True):
        cursor = self.conn.cursor()
        if available_only:
            cursor.execute("SELECT id, name, category, price FROM menu_items WHERE is_available = 1 ORDER BY category, name")
        else:
            cursor.execute("SELECT id, name, category, price, is_available FROM menu_items ORDER BY category, name")
        return cursor.fetchall()
    
    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu_items WHERE is_available = 1 ORDER BY category")
        return [row[0] for row in cursor.fetchall()]
    
    def get_menu_by_category(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu_items WHERE is_available = 1 ORDER BY category")
        categories = cursor.fetchall()
        
        menu_by_cat = {}
        for cat in categories:
            cat_name = cat[0]
            cursor.execute("SELECT id, name, price FROM menu_items WHERE category = ? AND is_available = 1 ORDER BY name", (cat_name,))
            menu_by_cat[cat_name] = cursor.fetchall()
        return menu_by_cat
    
    def add_menu_item(self, name, category, price):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)", (name, category, price))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_menu_item(self, item_id, name=None, category=None, price=None, is_available=None):
        cursor = self.conn.cursor()
        if name:
            cursor.execute("UPDATE menu_items SET name = ? WHERE id = ?", (name, item_id))
        if category:
            cursor.execute("UPDATE menu_items SET category = ? WHERE id = ?", (category, item_id))
        if price is not None:
            cursor.execute("UPDATE menu_items SET price = ? WHERE id = ?", (price, item_id))
        if is_available is not None:
            cursor.execute("UPDATE menu_items SET is_available = ? WHERE id = ?", (is_available, item_id))
        self.conn.commit()
    
    def delete_menu_item(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
        self.conn.commit()
    
    # ========== ORDER OPERATIONS ==========
    
    def save_order(self, customer_id, items, subtotal, tax_rate=0):
        """Save order and return order_id and bill_number"""
        cursor = self.conn.cursor()
        
        bill_number = self.get_next_bill_number()
        total_amount = subtotal
        
        cursor.execute(
            "INSERT INTO orders (bill_number, customer_id, total_amount) VALUES (?, ?, ?)",
            (bill_number, customer_id if customer_id else None, total_amount)
        )
        order_id = cursor.lastrowid
        
        for item in items:
            cursor.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, item['id'], item['quantity'], item['price'])
            )
        
        self.conn.commit()
        return order_id, bill_number
    
    def get_orders_by_date(self, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT o.id, o.bill_number, c.name, o.total_amount, o.order_date 
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE date(o.order_date) BETWEEN ? AND ?
            ORDER BY o.order_date DESC
        ''', (start_date, end_date))
        return cursor.fetchall()
    
    def get_all_orders(self, limit=500):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT o.id, o.bill_number, c.name, o.total_amount, o.order_date 
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def get_sales_summary(self, period='today'):
        cursor = self.conn.cursor()
        
        if period == 'today':
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders WHERE date(order_date) = date("now")')
        elif period == 'week':
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders WHERE date(order_date) >= date("now", "-7 days")')
        elif period == 'month':
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders WHERE strftime("%Y-%m", order_date) = strftime("%Y-%m", "now")')
        elif period == 'year':
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders WHERE strftime("%Y", order_date) = strftime("%Y", "now")')
        else:
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM orders')
        
        result = cursor.fetchone()
        return {'orders': result[0] or 0, 'total': result[1] or 0}
    
    def get_top_items(self, limit=10, days=30):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT mi.name, mi.category, SUM(oi.quantity) as sold, SUM(oi.quantity * oi.unit_price) as revenue
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            JOIN orders o ON oi.order_id = o.id
            WHERE date(o.order_date) >= date("now", ?)
            GROUP BY mi.id
            ORDER BY sold DESC
            LIMIT ?
        ''', (f'-{days} days', limit))
        return cursor.fetchall()
    
    def get_order_details(self, order_id):
        """Get complete order details including items"""
        cursor = self.conn.cursor()
        
        # Get order header
        cursor.execute('''
            SELECT o.id, o.bill_number, c.name, c.phone, c.address, o.total_amount, o.order_date
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        ''', (order_id,))
        order = cursor.fetchone()
        
        if not order:
            return None
        
        # Get order items
        cursor.execute('''
            SELECT mi.name, oi.quantity, oi.unit_price
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = cursor.fetchall()
        
        subtotal = sum(item[1] * item[2] for item in items)
        
        return {
            'id': order[0],
            'bill_number': order[1],
            'customer_name': order[2] if order[2] else 'Walk-in Customer',
            'customer_phone': order[3] if order[3] else '',
            'customer_address': order[4] if order[4] else '',
            'total': order[5],
            'subtotal': subtotal,
            'date': order[6],
            'items': [{'name': i[0], 'quantity': i[1], 'price': i[2]} for i in items]
        }
    
    # ========== ADMIN OPERATIONS ==========
    
    def verify_admin(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, password_hash, failed_attempts, lock_until, full_name FROM admin_users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            return False, "User not found", 0
        
        if user[3]:
            lock_until = datetime.fromisoformat(user[3])
            if datetime.now() < lock_until:
                remaining = (lock_until - datetime.now()).seconds // 60
                return False, f"Account locked. Try again in {remaining} minutes", user[2]
        
        if bcrypt.checkpw(password.encode('utf-8'), user[1]):
            cursor.execute("UPDATE admin_users SET failed_attempts = 0, lock_until = NULL WHERE id = ?", (user[0],))
            self.conn.commit()
            return True, user[4], user[2]
        else:
            new_attempts = user[2] + 1
            if new_attempts >= 3:
                lock_until = datetime.now() + timedelta(minutes=5)
                cursor.execute("UPDATE admin_users SET failed_attempts = ?, lock_until = ? WHERE id = ?",
                             (new_attempts, lock_until.isoformat(), user[0]))
                message = "Too many failed attempts. Account locked for 5 minutes."
            else:
                cursor.execute("UPDATE admin_users SET failed_attempts = ? WHERE id = ?", (new_attempts, user[0]))
                message = f"Invalid password. {3 - new_attempts} attempts remaining."
            self.conn.commit()
            return False, message, new_attempts
    
    def get_setting(self, key, default=None):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else default
    
    def update_setting(self, key, value):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (key, value))
        self.conn.commit()
    
    def backup_database(self):
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{backup_dir}/restaurant_backup_{timestamp}.db"
        
        self.conn.close()
        shutil.copy2('database/restaurant.db', backup_name)
        self.conn = sqlite3.connect('database/restaurant.db')
        self.conn.row_factory = sqlite3.Row
        
        return backup_name
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()