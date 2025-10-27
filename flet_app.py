"""
LoteTracker - Sistema de Trazabilidad por Código QR
Aplicación Flet (Python) equivalente al diseño React/Tailwind

Colores del diseño:
- Primary: #22543D (verde oscuro)
- Accent: #C6F6D5 (verde claro) 
- Button: #38A169 (verde medio)
- Button hover: #2F855A
- Background: #ffffff
- Input background: #f3f3f5
- Border: #38A169
"""

import flet as ft
import qrcode
from io import BytesIO
import base64
import json
from datetime import datetime
import os

# ============================================
# STORAGE MANAGER (simulates localStorage)
# ============================================
class StorageManager:
    """Maneja el almacenamiento persistente de datos"""
    
    def __init__(self):
        self.storage_file = "qr_tracker_data.json"
        self.data = self.load_data()
    
    def load_data(self):
        """Carga datos desde archivo JSON"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
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


# ============================================
# QR CODE GENERATOR
# ============================================
def generate_qr_image(data):
    """Genera imagen QR en formato base64"""
    qr_data = json.dumps({
        "producto": data["productType"],
        "cantidad": data["quantity"],
        "proveedor": data["supplier"],
        "fecha": data["date"]
    }, ensure_ascii=False)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64


# ============================================
# MAIN APPLICATION
# ============================================
def main(page: ft.Page):
    # ============================================
    # PAGE CONFIGURATION
    # ============================================
    page.title = "LoteTracker - Sistema de Trazabilidad"
    page.padding = 0
    page.bgcolor = "#ffffff"
    page.scroll = ft.ScrollMode.AUTO
    
    # Initialize storage
    storage = StorageManager()
    
    # ============================================
    # STATE VARIABLES
    # ============================================
    current_qr_data = {}
    CARD_MAX_WIDTH = 700
    CARD_MIN_WIDTH = 360
    CARD_PADDING = 24
    CARD_RADIUS = 16
    CARD_ELEVATION = 4
    CARD_BG = "#FFFFFF"
    # ============================================
    # FORM FIELDS (with refs for access)
    # ============================================
    operator_name_field = ft.TextField(
        label="Nombre del operador *",
        hint_text="Ej: Juan Pérez",
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
    )
    
    operator_code_field = ft.TextField(
        label="Código del operador *",
        hint_text="Ej: OP-001",
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
    )
    
    product_type_field = ft.TextField(
        label="Tipo de producto *",
        hint_text="Ej: Cúrcuma",
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
    )
    
    quantity_field = ft.TextField(
        label="Cantidad de producto *",
        hint_text="Ej: 100",
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    
    supplier_field = ft.TextField(
        label="Proveedor *",
        hint_text="Ej: Agro Sur S.A.",
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
    )
    
    date_field = ft.TextField(
        label="Fecha de producción",
        hint_text="Opcional - se usará fecha actual",
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
    )
    
    date_helper_text = ft.Text(
        "Si no se ingresa, se usará la fecha y hora actual",
        size=12,
        color="#717182",
        italic=True,
    )
    
    # ============================================
    # QR DISPLAY SECTION (Initially hidden)
    # ============================================
    qr_image = ft.Image(
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )
    
    qr_info_container = ft.Container(
        ###################  INLCUSION DE LO RESPONSIVE   #########################
        
        ###########################################
        visible=False, alignment=ft.alignment.center,
        width=CARD_MAX_WIDTH,
        bgcolor="transparent",
        content=ft.Card(
            elevation=CARD_ELEVATION,
            content=ft.Container(
                padding=24,
                border_radius=16,
                bgcolor="#ffffff",
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                    controls=[
                    ft.Text(
                        "Información del Lote",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color="#22543D",
                        text_align=ft.TextAlign.CENTER,
                    ),
                        # Info container
                        ft.Container(
                            padding=16,
                            border_radius=8,
                            bgcolor="#E6F7ED",  # accent/50
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Operador:", color="#717182"),
                                            ft.Text("", key="operator_name_display"),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Código operador:", color="#717182"),
                                            ft.Text("", key="operator_code_display"),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Producto:", color="#717182"),
                                            ft.Text("", key="product_display"),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Cantidad:", color="#717182"),
                                            ft.Text("", key="quantity_display"),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Proveedor:", color="#717182"),
                                            ft.Text("", key="supplier_display"),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Fecha:", color="#717182"),
                                            ft.Text("", key="date_display"),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        # QR Code
                        ft.Container(
                            padding=16,
                            border_radius=8,
                            bgcolor="#ffffff",
                            border=ft.border.all(2, "#38A169"),
                            content=qr_image,
                        ),
                        # Download button
                        ft.ElevatedButton(
                            "Descargar código QR",
                            icon=ft.Icons.DOWNLOAD,
                            on_click=lambda e: download_qr(),
                            style=ft.ButtonStyle(
                                color="#22543D",
                                bgcolor="#ffffff",
                                side=ft.BorderSide(1, "#e0e0e0"),
                            ),
                            width=300,
                        ),
                        # Helper text
                        ft.Text(
                            "El código QR contiene: Producto, Cantidad, Proveedor y Fecha",
                            size=12,
                            color="#717182",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),
            ),
        ),
    )
    
    # ============================================
    # HISTORY TABLE (Initially hidden)
    # ============================================
    history_table = ft.DataTable(
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
    
    history_container = ft.Container(
        visible=False,
        alignment=ft.alignment.center,
        width=CARD_MAX_WIDTH,
        bgcolor="transparent",
        content=ft.Card(
            elevation=CARD_ELEVATION,
            content=ft.Container(
            padding=CARD_PADDING,
            border_radius=CARD_RADIUS,
            bgcolor=CARD_BG,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Text(
                        "Historial de Registros",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color="#22543D",
                    ),
                    ft.Container(
                        height=300,
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            controls=[history_table],
                            ),
                        ),
                    ],
                ),
            ),
        ),
    )    
    # ============================================
    # EVENT HANDLERS
    # ============================================
    def validate_fields():
        """Valida que los campos requeridos estén completos"""
        if not operator_name_field.value:
            show_snackbar("⚠️ Por favor, ingrese el nombre del operador", "#d4183d")
            return False
        if not operator_code_field.value:
            show_snackbar("⚠️ Por favor, ingrese el código del operador", "#d4183d")
            return False
        if not product_type_field.value:
            show_snackbar("⚠️ Por favor, ingrese el tipo de producto", "#d4183d")
            return False
        if not quantity_field.value:
            show_snackbar("⚠️ Por favor, ingrese la cantidad", "#d4183d")
            return False
        if not supplier_field.value:
            show_snackbar("⚠️ Por favor, ingrese el proveedor", "#d4183d")
            return False
        return True
    
    def show_snackbar(message, bgcolor="#38A169"):
        """Muestra mensaje de notificación"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="#ffffff"),
            bgcolor=bgcolor,
        )
        page.snack_bar.open = True
        page.update()
    
    def on_generate_qr(e):
        """Maneja la generación del código QR"""
        if not validate_fields():
            return
        
        # Get date or use current
        date_value = date_field.value if date_field.value else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare data
        qr_data = {
            "operatorName": operator_name_field.value,
            "operatorCode": operator_code_field.value,
            "productType": product_type_field.value,
            "quantity": quantity_field.value,
            "supplier": supplier_field.value,
            "date": date_value,
        }
        
        # Save to storage
        storage.add_product(qr_data["productType"])
        storage.add_supplier(qr_data["supplier"])
        storage.add_history_record({
            "id": str(int(datetime.now().timestamp())),
            **qr_data
        })
        
        # Generate QR image
        img_base64 = generate_qr_image(qr_data)
        qr_image.src_base64 = img_base64
        
        # Update display info
        update_qr_display(qr_data)
        
        # Update history table
        update_history_table()
        
        # Show QR section
        qr_info_container.visible = True
        history_container.visible = True
        
        # Update button text
        generate_button.text = "Generar nuevo código QR"
        new_code_button.visible = True
        
        # Show success message
        show_snackbar(f"✅ Código generado exitosamente - Lote de {qr_data['productType']} registrado")
        
        # Store current data for download
        nonlocal current_qr_data
        current_qr_data = qr_data
        
        page.update()
    
    def update_qr_display(data):
        """Actualiza la información mostrada del QR"""
        # Find and update display texts
        info_container = qr_info_container.content.content.content.controls[1].content
        info_container.controls[0].controls[1].value = data["operatorName"]
        info_container.controls[1].controls[1].value = data["operatorCode"]
        info_container.controls[2].controls[1].value = data["productType"]
        info_container.controls[3].controls[1].value = data["quantity"]
        info_container.controls[4].controls[1].value = data["supplier"]
        info_container.controls[5].controls[1].value = data["date"]
    
    def update_history_table():
        """Actualiza la tabla de historial"""
        history = storage.get_history()
        history_table.rows.clear()
        
        for record in history:
            history_table.rows.append(
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
    
    def on_new_code(e):
        """Limpia el formulario para un nuevo código"""
        operator_name_field.value = ""
        operator_code_field.value = ""
        product_type_field.value = ""
        quantity_field.value = ""
        supplier_field.value = ""
        date_field.value = ""
        
        qr_info_container.visible = False
        generate_button.text = "Generar código QR"
        new_code_button.visible = False
        
        page.update()
    
    def download_qr():
        """Descarga el código QR como PNG"""
        if current_qr_data:
            # Create filename
            filename = f"QR-{current_qr_data['productType']}-{int(datetime.now().timestamp())}.png"
            
            # Decode base64 and save
            img_data = base64.b64decode(qr_image.src_base64)
            with open(filename, 'wb') as f:
                f.write(img_data)
            
            show_snackbar(f"✅ Código QR guardado como {filename}")
    
    # ============================================
    # BUTTONS
    # ============================================
    generate_button = ft.ElevatedButton(
        "Generar código QR",
        on_click=on_generate_qr,
        style=ft.ButtonStyle(
            color="#ffffff",
            bgcolor="#38A169",
        ),
        height=40,
        expand=True,
    )
    
    new_code_button = ft.ElevatedButton(
        "Nuevo código",
        on_click=on_new_code,
        visible=False,
        style=ft.ButtonStyle(
            color="#22543D",
            bgcolor="#ffffff",
            side=ft.BorderSide(1, "#e0e0e0"),
        ),
        height=40,
        expand=True,
    )
    
    # ============================================
    # FORM CARD
    # ============================================
    form_card = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=24,
            border_radius=16,
            bgcolor="#ffffff",
            width=500,
            content=ft.Column(
                spacing=16,
                controls=[
                    operator_name_field,
                    operator_code_field,
                    product_type_field,
                    quantity_field,
                    supplier_field,
                    date_field,
                    date_helper_text,
                    ft.Container(height=8),  # Spacing
                    ft.Row(
                        spacing=12,
                        controls=[
                            generate_button,
                            new_code_button,
                        ],
                    ),
                ],
            ),
        ),
    )
    
    # ============================================
    # HEADER
    # ============================================
    header = ft.Container(
        bgcolor="#ffffff",
        border=ft.border.only(bottom=ft.BorderSide(2, "#38A169")),
        padding=ft.padding.symmetric(vertical=24, horizontal=16),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.INVENTORY_2, size=32, color="#22543D"),
                ft.Column(
                    spacing=4,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "LoteTracker",
                            size=28,
                            weight=ft.FontWeight.W_500,
                            color="#22543D",
                        ),
                        ft.Text(
                            "Sistema de trazabilidad por código QR",
                            size=14,
                            color="#717182",
                        ),
                    ],
                ),
            ],
        ),
    )
    
    # ============================================
    # FOOTER
    # ============================================
    footer = ft.Container(
    bgcolor="#C6F6D5",
    border=ft.border.only(top=ft.BorderSide(1, "#38A169")),
    padding=ft.padding.symmetric(vertical=20, horizontal=10),
    margin=ft.margin.only(top=40),
    content=ft.ResponsiveRow(
        [
            ft.Column(
                [
                    ft.Text(
                        "Prototipo de sistema de trazabilidad para PYMEs",
                        size=12,
                        color="#22543D",
                        text_align=ft.TextAlign.CENTER,
                        expand=True,
                    ),
                    ft.Text(
                        "Desarrollado con ❤️ en Flet (Python)",
                        size=11,
                        italic=True,
                        color="#276749",
                        text_align=ft.TextAlign.CENTER,
                        expand=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5,
                col={"xs": 12, "sm": 12, "md": 12, "lg": 12},
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    alignment=ft.alignment.center,
    )

    layout = ft.Column(
    [
        form_card,
        qr_info_container,
        history_container,
        footer,  # 👈 si lo estás usando
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    alignment=ft.MainAxisAlignment.CENTER,
    expand=True,
    spacing=40,
    )
    
    # ============================================
    # MAIN CONTENT
    # ============================================
    main_content = ft.Container(
        padding=ft.padding.symmetric(vertical=32, horizontal=16),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#ffffff", "#E6F7ED"],
        ),
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=32,
            controls=[
                form_card,
                qr_info_container,
                history_container,
            ],
        ),
    )
    
    # ============================================
    # BUILD PAGE
    # ============================================
    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                header,
                main_content,
                footer,
            ],
        )
    )
    
    # Load initial history
    update_history_table()
    if len(storage.get_history()) > 0:
        history_container.visible = True
        page.update()


# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
