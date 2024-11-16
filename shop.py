# Programmer A's changes (loyalty_feature.py)
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
        self._save_json(self.customers, self.customers_file)

    def sell_product(self, name, quantity, customer_id=None):
        success = super().sell_product(name, quantity)
        if success and customer_id:
            points = int(self.inventory[name]['price'] * quantity)
            self.customers[customer_id]['points'] += points
            self._update_customer_tier(customer_id)
        return success
    