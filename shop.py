# shop_v1.py
class ShopManager:
    def __init__(self):
        self.inventory = {}
        self.sales = []

    def add_product(self, name, price, quantity):
        self.inventory[name] = {'price': price, 'quantity': quantity}

    def sell_product(self, name, quantity):
        if name not in self.inventory or self.inventory[name]['quantity'] < quantity:
            return False
        self.inventory[name]['quantity'] -= quantity
        self.sales.append({'product': name, 'quantity': quantity})
        return True

    def display_inventory(self):
        print("\nCurrent Inventory:")
        for name, details in self.inventory.items():
            print(f"{name}: {details['quantity']} units at ${details['price']}")
            