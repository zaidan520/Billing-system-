"""
Helper functions for the application
"""

from datetime import datetime

def format_currency(amount):
    """Format amount as PKR currency"""
    return f"PKR {amount:,.0f}"

def get_current_datetime():
    """Get current date and time as string"""
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

def get_current_date():
    """Get current date as string"""
    return datetime.now().strftime("%Y-%m-%d")

def generate_bill_number(bill_num):
    """Generate formatted bill number"""
    today = datetime.now()
    return f"RAZA{today.strftime('%Y%m%d')}{bill_num:04d}"