import os
import flet as ft
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from dotenv import load_dotenv

class DatabaseManager:
    """Maneja la conexión y operaciones con MongoDB"""
    
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME", "lotetracker_db")
        
        if not self.mongo_uri:
            print("Error: MONGO_URI no encontrada. Asegúrate de crear un archivo .env")
            self.client = None
            self.db = None # Asegurarse de que db sea None
            return

        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            print(f"✅ Conectado exitosamente a MongoDB en {self.db_name}")
            
            self.db = self.client[self.db_name]
            self.registros: Collection = self.db.registros
            self.productos: Collection = self.db.productos
            self.proveedores: Collection = self.db.proveedores
            
        except errors.ServerSelectionTimeoutError as err:
            print(f"❌ Error de conexión a MongoDB: {err}")
            print("Asegúrate de que MongoDB esté corriendo o que tu MONGO_URI sea correcta.")
            self.client = None
            self.db = None
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado al conectar a DB: {e}")
            self.client = None
            self.db = None

    def add_product(self, product_name):
        """Añade un producto a la colección, sin duplicados"""
        # 👇 CORRECCIÓN AQUÍ
        if self.db is None: return
        
        self.productos.find_one_and_update(
            {"nombre": product_name},
            {"$set": {"nombre": product_name}},
            upsert=True
        )

    def add_supplier(self, supplier_name):
        """Añade un proveedor a la colección, sin duplicados"""
        # 👇 CORRECCIÓN AQUÍ
        if self.db is None: return
        
        self.proveedores.find_one_and_update(
            {"nombre": supplier_name},
            {"$set": {"nombre": supplier_name}},
            upsert=True
        )

    def add_history_record(self, record):
        """Añade un nuevo registro de QR al historial"""
        # 👇 CORRECCIÓN AQUÍ
        if self.db is None: return
        
        self.registros.insert_one(record)

    def get_products(self):
        """Obtiene la lista de nombres de productos"""
        # 👇 CORRECCIÓN AQUÍ
        if self.db is None: return []
        
        return [doc["nombre"] for doc in self.productos.find()]

    def get_suppliers(self):
        """Obtiene la lista de nombres de proveedores"""
        # 👇 CORRECCIÓN AQUÍ
        if self.db is None: return []
        
        return [doc["nombre"] for doc in self.proveedores.find()]

    def get_history(self):
        """Obtiene los últimos 10 registros del historial"""
        # 👇 CORRECCIÓN AQUÍ
        if self.db is None: return []
        
        records_cursor = self.registros.find().sort("_id", -1).limit(10)
        return list(records_cursor)