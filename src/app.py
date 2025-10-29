import flet as ft
from datetime import datetime
import base64

from .database_manager import DatabaseManager
from .utils import generate_qr_image
from .components.header import create_header
from .components.footer import create_footer
from .components.form_card import create_form_card
from .components.qr_display import create_qr_display_card
from .components.history_table import create_history_table_card

class LoteTrackerApp:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.storage = DatabaseManager() 
        self.current_qr_data = {}
        self.current_qr_base64 = ""

        # --- 1. Definir TODOS los controles aquí ---
        
        # (El código de los controles no cambia...)
        # Controles del Formulario
        self.operator_name_field = ft.TextField(
            label="Nombre del operador *", hint_text="Ej: Juan Pérez",
            bgcolor="#f3f3f5", border_color="#e0e0e0", focused_border_color="#38A169",
            border_radius=8, text_size=16,
        )
        self.operator_code_field = ft.TextField(
            label="Código del operador *", hint_text="Ej: OP-001",
            bgcolor="#f3f3f5", border_color="#e0e0e0", focused_border_color="#38A169",
            border_radius=8, text_size=16,
        )
        self.product_type_field = ft.TextField(
            label="Tipo de producto *", hint_text="Ej: Cúrcuma",
            bgcolor="#f3f3f5", border_color="#e0e0e0", focused_border_color="#38A169",
            border_radius=8, text_size=16,
        )
        self.quantity_field = ft.TextField(
            label="Cantidad de producto *", hint_text="Ej: 100",
            bgcolor="#f3f3f5", border_color="#e0e0e0", focused_border_color="#38A169",
            border_radius=8, text_size=16, keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.supplier_field = ft.TextField(
            label="Proveedor *", hint_text="Ej: Agro Sur S.A.",
            bgcolor="#f3f3f5", border_color="#e0e0e0", focused_border_color="#38A169",
            border_radius=8, text_size=16,
        )
        self.date_field = ft.TextField(
            label="Fecha de producción", hint_text="Opcional - se usará fecha actual",
            bgcolor="#f3f3f5", border_color="#e0e0e0", focused_border_color="#38A169",
            border_radius=8, text_size=16,
        )
        self.date_helper_text = ft.Text(
            "Si no se ingresa, se usará la fecha y hora actual",
            size=12, color="#717182", italic=True,
        )
        self.generate_button = ft.ElevatedButton(
            "Generar código QR",
            on_click=self.on_generate_qr, 
            style=ft.ButtonStyle(color="#ffffff", bgcolor="#38A169"),
            height=40, expand=True,
        )
        self.new_code_button = ft.ElevatedButton(
            "Nuevo código",
            on_click=self.on_new_code,
            visible=False,
            style=ft.ButtonStyle(
                color="#22543D", bgcolor="#ffffff",
                side=ft.BorderSide(1, "#e0e0e0"),
            ),
            height=40, expand=True,
        )

        # Controles del Display QR
        self.qr_image = ft.Image(width=200, height=200, fit=ft.ImageFit.CONTAIN)
        self.operator_name_display = ft.Text()
        self.operator_code_display = ft.Text()
        self.product_display = ft.Text()
        self.quantity_display = ft.Text()
        self.supplier_display = ft.Text()
        self.date_display = ft.Text()

        # Controles de la Tabla de Historial
        self.history_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Operador")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Proveedor")),
                ft.DataColumn(ft.Text("Fecha")),
            ],
            rows=[],
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=8,
            horizontal_lines=ft.BorderSide(1, "#e0e0e0"),
        )

        # --- 2. Definir las variables de layout ---
        
        self.header = create_header()
        self.footer = create_footer()

        self.form_card = create_form_card(
            self.operator_name_field, self.operator_code_field,
            self.product_type_field, self.quantity_field,
            self.supplier_field, self.date_field,
            self.date_helper_text, self.generate_button, self.new_code_button
        )
        
        self.qr_info_container = create_qr_display_card(
            self.qr_image, self.operator_name_display, self.operator_code_display,
            self.product_display, self.quantity_display, self.supplier_display,
            self.date_display, self.download_qr
        )
        
        self.history_container = create_history_table_card(self.history_table)


    def build_layout(self):
        """Construye y añade el layout principal a la página"""
        
        # 👇 CORRECCIÓN AQUÍ
        if self.storage.db is None:
            self.page.add(ft.Column(
                [
                    ft.Text("❌ Error de Conexión a la Base de Datos", size=20, color="red"),
                    ft.Text("Por favor, revisa tu archivo .env y asegúrate de que MongoDB esté corriendo."),
                    ft.Text(f"URI Intentada: {self.storage.mongo_uri}")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ))
            return

        # Si la conexión es exitosa, construye la UI normal
        self.main_content = ft.Container(
            padding=ft.padding.symmetric(vertical=32, horizontal=16),
            gradient=ft.RadialGradient(
                center=ft.alignment.center,
                radius=0.5,
                colors=["#F2FFF7", "#ffffff"],
                stops=[0.3, 1.0]
            ),
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=32,
                controls=[
                    self.form_card,
                    self.qr_info_container,
                    self.history_container,
                ],
            ),
        )
        
        self.page.add(
            ft.Column(
                spacing=0,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.header,
                    self.main_content,
                    self.footer,
                ],
            )
        )
        
        self.update_history_table()
        if len(self.storage.get_history()) > 0:
            self.history_container.visible = True
            
        self.page.update()

    # --- 3. Lógica de la Aplicación (Callbacks) ---
    # (El resto de la lógica no cambia...)
    
    def validate_fields(self):
        if not self.operator_name_field.value:
            self.show_snackbar("⚠️ Por favor, ingrese el nombre del operador", "#d4183d")
            return False
        if not self.operator_code_field.value:
            self.show_snackbar("⚠️ Por favor, ingrese el código del operador", "#d4183d")
            return False
        if not self.product_type_field.value:
            self.show_snackbar("⚠️ Por favor, ingrese el tipo de producto", "#d4183d")
            return False
        if not self.quantity_field.value:
            self.show_snackbar("⚠️ Por favor, ingrese la cantidad", "#d44183d")
            return False
        if not self.supplier_field.value:
            self.show_snackbar("⚠️ Por favor, ingrese el proveedor", "#d4183d")
            return False
        return True

    def show_snackbar(self, message, bgcolor="#38A169"):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="#ffffff"),
            bgcolor=bgcolor,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def on_generate_qr(self, e):
        if not self.validate_fields():
            return
        
        date_value = self.date_field.value if self.date_field.value else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        qr_data = {
            "operatorName": self.operator_name_field.value,
            "operatorCode": self.operator_code_field.value,
            "productType": self.product_type_field.value,
            "quantity": self.quantity_field.value,
            "supplier": self.supplier_field.value,
            "date": date_value,
        }
        
        self.storage.add_product(qr_data["productType"])
        self.storage.add_supplier(qr_data["supplier"])
        record_to_db = {
            "id": str(int(datetime.now().timestamp())), 
            **qr_data
        }
        self.storage.add_history_record(record_to_db)
        
        img_base64 = generate_qr_image(qr_data)
        self.qr_image.src_base64 = img_base64
        self.current_qr_base64 = img_base64
        self.current_qr_data = qr_data
        
        self.update_qr_display(qr_data)
        self.update_history_table() 
        
        self.qr_info_container.visible = True
        self.history_container.visible = True
        
        self.generate_button.text = "Generar nuevo código QR"
        self.new_code_button.visible = True
        
        self.show_snackbar(f"✅ Código generado exitosamente - Lote de {qr_data['productType']} registrado")
        
        self.page.update()

    def update_qr_display(self, data):
        self.operator_name_display.value = data["operatorName"]
        self.operator_code_display.value = data["operatorCode"]
        self.product_display.value = data["productType"]
        self.quantity_display.value = data["quantity"]
        self.supplier_display.value = data["supplier"]
        self.date_display.value = data["date"]

    def update_history_table(self):
        history = self.storage.get_history()
        self.history_table.rows.clear()
        
        for record in history:
            self.history_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(record["operatorName"])),
                        ft.DataCell(ft.Text(record["productType"])),
                        ft.DataCell(ft.Text(record["quantity"])),
                        ft.DataCell(ft.Text(record["supplier"])),
                        ft.DataCell(ft.Text(record["date"])),
                    ]
                )
            )

    def on_new_code(self, e):
        self.operator_name_field.value = ""
        self.operator_code_field.value = ""
        self.product_type_field.value = ""
        self.quantity_field.value = ""
        self.supplier_field.value = ""
        self.date_field.value = ""
        
        self.qr_info_container.visible = False
        self.generate_button.text = "Generar código QR"
        self.new_code_button.visible = False
        
        self.page.update()

    def download_qr(self, e):
        if self.current_qr_data:
            filename = f"QR-{self.current_qr_data['productType']}-{int(datetime.now().timestamp())}.png"
            
            try:
                img_data = base64.b64decode(self.current_qr_base64)
                with open(filename, 'wb') as f:
                    f.write(img_data)
                self.show_snackbar(f"✅ Código QR guardado como {filename}")
            except Exception as ex:
                self.show_snackbar(f"Error al guardar: {ex}", "#d4183d")

