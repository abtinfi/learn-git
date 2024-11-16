# shop_v2.py
import json
from datetime import datetime

class ShopManager:
    def __init__(self, inventory_file="inventory.json"):
        self.inventory_file = inventory_file
        self.inventory = self._load_inventory()
        self.sales = []

    def _load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_inventory(self):
        with open(self.inventory_file, 'w') as f:
            json.dump(self.inventory, f, indent=4)

    def add_product(self, name, price, quantity):
        self.inventory[name] = {
            'price': price,
            'quantity': quantity,
            'last_updated': datetime.now().isoformat()
        }
        self.save_inventory()

    def generate_sales_report(self):
        total = sum(self.inventory[sale['product']]['price'] * sale['quantity'] 
                   for sale in self.sales)
        return f"Total Sales: ${total:.2f}"
    