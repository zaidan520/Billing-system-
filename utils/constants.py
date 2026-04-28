"""
Constants and Emojis for the application
"""

# Color Scheme
COLORS = {
    'primary': '#129990',
    'secondary': '#90D1CA',
    'background': '#FFFBDE',
    'dark': '#096B68',
    'success': '#27ae60',
    'error': '#e74c3c',
    'warning': '#f39c12',
    'white': '#FFFFFF',
    'text': '#2c3e50',
}

# Category Emojis
CATEGORY_EMOJIS = {
    'Burgers': '🍔',
    'Shawarma': '🥙',
    'Sides': '🍟',
    'Beverages': '🥤',
    'Pizza': '🍕',
    'Rice': '🍚',
    'Salads': '🥗',
    'Desserts': '🍦',
    'Default': '🍽️'
}

def get_item_emoji(name):
    """Get emoji for an item based on its name"""
    return '🍽️'

def get_category_emoji(category):
    """Get emoji for a category"""
    return CATEGORY_EMOJIS.get(category, CATEGORY_EMOJIS['Default'])