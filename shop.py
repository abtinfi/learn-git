# Programmer B's changes (discount_feature.py)
from datetime import datetime

class ShopManager:
    def __init__(self, data_dir="shop_data"):
        # Existing initialization code...
        self.customers_file = self.data_dir / "customers.json"
        self.customers = self._load_json(self.customers_file)

    def add_customer(self, customer_id, name, email):
        self.customers[customer_id] = {
            'name': name,
            'email': email,
            'points': 0,
            'tier': 'Bronze'
        }
        self._save_json(self.discounts, self.discounts_file)

    def sell_product(self, name, quantity):
        if name in self.discounts:
            current_date = datetime.now().isoformat()
            if self.discounts[name]['start_date'] <= current_date <= self.discounts[name]['end_date']:
                self.inventory[name]['price'] *= (1 - self.discounts[name]['percentage']/100)
        return super().sell_product(name, quantity)
    