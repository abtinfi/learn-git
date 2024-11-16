# Programmer B's changes (discount_feature.py)
from datetime import datetime

class ShopManager:
    def __init__(self, data_dir="shop_data"):
        # Existing initialization code...
        self.discounts_file = self.data_dir / "discounts.json"
        self.discounts = self._load_json(self.discounts_file)

    def add_discount(self, product_name, percentage, start_date, end_date):
        self.discounts[product_name] = {
            'percentage': percentage,
            'start_date': start_date,
            'end_date': end_date
        }
        self._save_json(self.discounts, self.discounts_file)

    def sell_product(self, name, quantity):
        if name in self.discounts:
            current_date = datetime.now().isoformat()
            if self.discounts[name]['start_date'] <= current_date <= self.discounts[name]['end_date']:
                self.inventory[name]['price'] *= (1 - self.discounts[name]['percentage']/100)
        return super().sell_product(name, quantity)
    