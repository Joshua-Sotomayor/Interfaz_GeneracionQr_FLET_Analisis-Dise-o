# src/storage_manager.py
import json
import os
from datetime import datetime

class StorageManager:
    """Maneja el almacenamiento persistente de datos"""
    
    def __init__(self, storage_file="qr_tracker_data.json"):
        self.storage_file = storage_file
        self.data = self.load_data()
    
    def load_data(self):
        """Carga datos desde archivo JSON"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass # Archivo corrupto, se sobrescribirá
        return {
            "products": [],
            "suppliers": [],
            "history": []
        }
    
    def save_data(self):
        """Guarda datos en archivo JSON"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_product(self, product):
        """Añade producto a la lista de sugerencias"""
        if product not in self.data["products"]:
            self.data["products"].append(product)
            self.save_data()
    
    def add_supplier(self, supplier):
        """Añade proveedor a la lista de sugerencias"""
        if supplier not in self.data["suppliers"]:
            self.data["suppliers"].append(supplier)
            self.save_data()
    
    def add_history_record(self, record):
        """Añade registro al historial (máximo 10)"""
        self.data["history"].insert(0, record)
        self.data["history"] = self.data["history"][:10]
        self.save_data()
    
    def get_products(self):
        return self.data["products"]
    
    def get_suppliers(self):
        return self.data["suppliers"]
    
    def get_history(self):
        return self.data["history"]