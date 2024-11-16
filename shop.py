# shop_v3.py
import json
import logging
from datetime import datetime
from pathlib import Path
import shutil

class ShopManager:
    def __init__(self, data_dir="shop_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.inventory_file = self.data_dir / "inventory.json"
        self.suppliers_file = self.data_dir / "suppliers.json"
        self.sales_file = self.data_dir / "sales.json"
        
        logging.basicConfig(
            filename=self.data_dir / "shop.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.inventory = self._load_json(self.inventory_file)
        self.suppliers = self._load_json(self.suppliers_file)
        self.sales = self._load_json(self.sales_file)

    def _load_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_json(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        self._create_backup()

    def _create_backup(self):
        backup_dir = self.data_dir / "backup"
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for file in self.data_dir.glob("*.json"):
            backup_file = backup_dir / f"{file.stem}_{timestamp}.json"
            shutil.copy2(file, backup_file)

    def add_product(self, name, price, quantity, category, supplier_id):
        if not isinstance(price, (int, float)) or price <= 0:
            logging.error(f"Invalid price for product {name}")
            raise ValueError("Price must be a positive number")

        self.inventory[name] = {
            'price': price,
            'quantity': quantity,
            'category': category,
            'supplier_id': supplier_id,
            'last_updated': datetime.now().isoformat()
        }
        self._save_json(self.inventory, self.inventory_file)
        logging.info(f"Added/Updated product: {name}")

    def add_supplier(self, supplier_id, name, contact, address):
        self.suppliers[supplier_id] = {
            'name': name,
            'contact': contact,
            'address': address,
            'last_updated': datetime.now().isoformat()
        }
        self._save_json(self.suppliers, self.suppliers_file)
        logging.info(f"Added/Updated supplier: {name}")

    # The buggy version (shop_v5.py with calculation error)
    def sell_product(self, name, quantity):
        if name not in self.inventory:
            logging.error(f"Product not found: {name}")
            return False

        if self.inventory[name]['quantity'] < quantity:
            logging.warning(f"Insufficient stock for {name}")
            return False

        # BUG: Incorrect price calculation
        self.inventory[name]['quantity'] -= quantity
        sale = {
            'product': name,
            'quantity': quantity,
            'price': self.inventory[name]['price'] * quantity * 1.1,  # Incorrect tax calculation
            'timestamp': datetime.now().isoformat()
        }
        
        if 'sales_history' not in self.sales:
                self.sales['sales_history'] = []
            
        self.sales['sales_history'].append(sale)
        self._save_json(self.inventory, self.inventory_file)
        self._save_json(self.sales, self.sales_file)
        logging.info(f"Sold {quantity} units of {name}")
        return True

    def generate_report(self, report_type="sales", start_date=None, end_date=None):
        if report_type == "sales":
            return self._generate_sales_report(start_date, end_date)
        elif report_type == "inventory":
            return self._generate_inventory_report()
        elif report_type == "suppliers":
            return self._generate_supplier_report()

    def _generate_sales_report(self, start_date=None, end_date=None):
        sales = self.sales.get('sales_history', [])
        if start_date:
            sales = [s for s in sales if s['timestamp'] >= start_date]
        if end_date:
            sales = [s for s in sales if s['timestamp'] <= end_date]
            
        total_sales = sum(s['price'] * s['quantity'] for s in sales)
        return {
            'total_sales': total_sales,
            'num_transactions': len(sales),
            'sales_details': sales
        }

    def _generate_inventory_report(self):
        low_stock = []
        total_value = 0
        
        for name, details in self.inventory.items():
            total_value += details['price'] * details['quantity']
            if details['quantity'] < 10:  # Low stock threshold
                low_stock.append(name)
                
        return {
            'total_value': total_value,
            'low_stock_items': low_stock,
            'inventory_details': self.inventory
        }

    def _generate_supplier_report(self):
        return {
            'total_suppliers': len(self.suppliers),
            'supplier_details': self.suppliers
        }