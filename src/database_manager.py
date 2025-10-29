import os
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from dotenv import load_dotenv
from bson import ObjectId # ⭐️ Importante para buscar por _id

class DatabaseManager:
    """Maneja la conexión y operaciones con MongoDB"""
    
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("DB_NAME", "lotetracker_db")
        
        if not self.mongo_uri:
            print("Error: MONGO_URI no encontrada. Asegúrate de crear un archivo .env")
            self.client = None
            self.db = None
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
            self.client = None
            self.db = None
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado al conectar a DB: {e}")
            self.client = None
            self.db = None

    def add_product(self, product_name):
        if self.db is None: return
        self.productos.find_one_and_update(
            {"nombre": product_name},
            {"$set": {"nombre": product_name}},
            upsert=True
        )

    def add_supplier(self, supplier_name):
        if self.db is None: return
        self.proveedores.find_one_and_update(
            {"nombre": supplier_name},
            {"$set": {"nombre": supplier_name}},
            upsert=True
        )

    def add_history_record(self, record):
        """Añade un nuevo registro de QR al historial"""
        if self.db is None: return
        
        # ⭐️ NUEVO ESQUEMA: Añadimos los campos de estado y stock
        try:
            cantidad_num = float(record.get("quantity", 0))
        except ValueError:
            cantidad_num = 0.0

        record_con_estado = {
            **record,
            "cantidad_inicial": cantidad_num,
            "cantidad_restante": cantidad_num, # Inicialmente es la misma
            "estado": "Almacenado" # Estado inicial por defecto
        }
        
        # Insertamos el documento y retornamos el resultado
        return self.registros.insert_one(record_con_estado)

    # ⭐️ NUEVO MÉTODO: Para buscar un lote por su ID de MongoDB
    def get_lote_by_id(self, lote_id):
        """Obtiene un registro de lote específico por su _id"""
        if self.db is None: return None
        
        try:
            # Convertimos el string del ID a un objeto ObjectId de Mongo
            oid = ObjectId(lote_id)
            return self.registros.find_one({"_id": oid})
        except Exception as e:
            print(f"Error al buscar lote por ID: {e}")
            return None

    # ⭐️ NUEVO MÉTODO: Para estadísticas generales del dashboard
    def get_dashboard_stats(self):
        """Obtiene estadísticas generales para el dashboard"""
        if self.db is None: return {"total_lotes": 0, "stock_por_producto": []}

        # 1. Total de lotes
        total_lotes = self.registros.count_documents({})
        
        # 2. Stock agrupado por producto (Ej: Cúrcuma, Jengibre)
        pipeline = [
            {
                "$group": {
                    "_id": "$productType", # Agrupar por nombre de producto
                    "cantidad_total": {"$sum": "$cantidad_restante"}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        stock_por_producto = list(self.registros.aggregate(pipeline))
        
        return {
            "total_lotes": total_lotes,
            "stock_por_producto": stock_por_producto # Ej: [{'_id': 'Cúrcuma', 'cantidad_total': 500}]
        }

    def get_history(self):
        """Obtiene los últimos 10 registros del historial"""
        if self.db is None: return []
        
        records_cursor = self.registros.find().sort("_id", -1).limit(10)
        return list(records_cursor)