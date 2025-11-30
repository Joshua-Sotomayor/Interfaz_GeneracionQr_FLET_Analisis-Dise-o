import flet as ft
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

# Importamos el DatabaseManager
from src.database_manager import DatabaseManager
from src.utils import generate_qr_image

# Importamos los componentes
from src.components.header import create_header
from src.components.footer import create_footer
from src.components.qr_display import create_qr_display_card
from src.components.history_table import create_history_table_card
from src.components.autocomplete_dropdown import create_autocomplete_dropdown
from src.components.unit_selector import create_unit_selector
from src.components.date_time_picker import create_date_time_picker

class GeneratorPage:

    def __init__(self, page: ft.Page, db: DatabaseManager):
        load_dotenv()
        self.page = page
        self.db = db
        self.base_url = os.getenv("BASE_URL")
        self.current_qr_data = {}
        self.current_qr_base64 = ""

        # --- 1. Definir TODOS los controles ---
        # Obtener datos para los dropdowns
        self.operators_dict = db.get_operators()  # {nombre: código}
        # Crear mapa inverso para buscar nombre por código
        self.operators_code_map = {v: k for k, v in self.operators_dict.items()}
        
        products_list = db.get_products()
        suppliers_list = db.get_suppliers()
        
        # Campo de operador con autocompletado
        self.operator_name_field = create_autocomplete_dropdown(
            label="Nombre del operador *",
            hint_text="Ej: Juan Pérez",
            options=list(self.operators_dict.keys()),
            on_change=self.on_operator_selected
        )
        
        # Campo de código de operador con autocompletado
        self.operator_code_field = create_autocomplete_dropdown(
            label="Código del operador *",
            hint_text="Ej: OP-001",
            options=list(self.operators_dict.values()),
            on_change=self.on_code_selected
        )
        
        # Campo de producto con autocompletado
        self.product_type_field = create_autocomplete_dropdown(
            label="Tipo de producto *",
            hint_text="Ej: Cúrcuma",
            options=products_list
        )
        
        # Campo de cantidad con selector de unidad
        self.quantity_field = ft.TextField(
            label="Cantidad de producto *",
            hint_text="Ej: 100",
            bgcolor="#f3f3f5",
            border_color="#e0e0e0",
            focused_border_color="#38A169",
            border_radius=8,
            text_size=16,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True
        )
        
        self.unit_field = create_unit_selector()
        
        # Campo de proveedor con autocompletado
        self.supplier_field = create_autocomplete_dropdown(
            label="Proveedor *",
            hint_text="Ej: Agro Sur S.A.",
            options=suppliers_list
        )
        
        # Selector de fecha/hora
        self.date_picker = create_date_time_picker()
        
        self.generate_button = ft.ElevatedButton(
            "Generar código QR",
            on_click=self.on_generate_qr,
            style=ft.ButtonStyle(color="#ffffff", bgcolor="#38A169"),
            height=40,
            expand=True
        )
        
        self.new_code_button = ft.ElevatedButton(
            "Nuevo código",
            on_click=self.on_new_code,
            visible=False,
            style=ft.ButtonStyle(color="#22543D", bgcolor="#ffffff", side=ft.BorderSide(1, "#e0e0e0")),
            height=40,
            expand=True
        )
        
        self.qr_image = ft.Image(width=200, height=200, fit=ft.ImageFit.CONTAIN)
        self.operator_name_display = ft.Text()
        self.operator_code_display = ft.Text()
        self.product_display = ft.Text()
        self.quantity_display = ft.Text()
        self.supplier_display = ft.Text()
        self.date_display = ft.Text()
        self.history_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in ["Operador", "Producto", "Cantidad", "Proveedor", "Fecha"]],
            rows=[],
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=8,
            horizontal_lines=ft.BorderSide(1, "#e0e0e0")
        )

        # --- 2. Definir las variables de layout ---
        self.header = create_header()
        self.footer = create_footer()
        
        # Crear form_card con los nuevos componentes
        self.form_card = self.create_custom_form_card()
        
        self.qr_info_container = create_qr_display_card(
            self.qr_image,
            self.operator_name_display,
            self.operator_code_display,
            self.product_display,
            self.quantity_display,
            self.supplier_display,
            self.date_display,
            self.download_qr
        )
        self.history_container = create_history_table_card(self.history_table)

    def create_custom_form_card(self):
        """Crea el form card personalizado con los nuevos componentes"""
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        spacing=20,
                        controls=[
                            ft.Text("Generar Código QR", size=28, weight=ft.FontWeight.BOLD, color="#22543D"),
                            # Operador con sugerencias
                            ft.Column(
                                spacing=4,
                                controls=[
                                    self.operator_name_field,
                                    self.operator_name_field.suggestions_container,
                                ]
                            ),
                            # Código de Operador con sugerencias
                            ft.Column(
                                spacing=4,
                                controls=[
                                    self.operator_code_field,
                                    self.operator_code_field.suggestions_container,
                                ]
                            ),
                            # Producto con sugerencias
                            ft.Column(
                                spacing=4,
                                controls=[
                                    self.product_type_field,
                                    self.product_type_field.suggestions_container,
                                ]
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    self.quantity_field,
                                    self.unit_field,
                                ]
                            ),
                            # Proveedor con sugerencias
                            ft.Column(
                                spacing=4,
                                controls=[
                                    self.supplier_field,
                                    self.supplier_field.suggestions_container,
                                ]
                            ),
                            self.date_picker,
                            ft.Row(
                                spacing=12,
                                controls=[
                                    self.generate_button,
                                    self.new_code_button,
                                ]
                            ),
                        ]
                    ),
                    padding=32,
                ),
                elevation=3,
            ),
            width=700,
        )

    def on_operator_selected(self, e):
        """Auto-rellena el código del operador cuando se selecciona uno existente"""
        selected_operator = self.operator_name_field.value
        if selected_operator and selected_operator in self.operators_dict:
            self.operator_code_field.value = self.operators_dict[selected_operator]
            self.operator_code_field.update()
            
    def on_code_selected(self, e):
        """Auto-rellena el nombre del operador cuando se selecciona un código existente"""
        selected_code = self.operator_code_field.value
        if selected_code and selected_code in self.operators_code_map:
            self.operator_name_field.value = self.operators_code_map[selected_code]
            self.operator_name_field.update()

    # --- 3. Lógica de la Aplicación ---

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
            self.show_snackbar("⚠️ Por favor, ingrese la cantidad", "#d4183d")
            return False
        if not self.supplier_field.value:
            self.show_snackbar("⚠️ Por favor, ingrese el proveedor", "#d4183d")
            return False
        return True

    def show_snackbar(self, message, bgcolor="#38A169"):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message, color="#ffffff"), bgcolor=bgcolor)
        self.page.snack_bar.open = True
        self.page.update()

    def on_generate_qr(self, e):
        """Maneja la generación del código QR"""
        if not self.validate_fields():
            return

        if not self.base_url:
            self.show_snackbar("❌ Error: 'BASE_URL' no está configurada en tu archivo .env", "#d4183d")
            self.show_snackbar("Añade la URL de tu servidor (ej. http://192.168.1.7:8550) a .env", "#d4183d")
            return

        # Obtener fecha del date_picker
        date_value = self.date_picker.get_value()
        
        # Obtener unidad
        unit = self.unit_field.value or "kg"
        quantity_with_unit = f"{self.quantity_field.value} {unit}"

        # 1. Obtenemos los datos del formulario
        qr_data = {
            "operatorName": self.operator_name_field.value,
            "operatorCode": self.operator_code_field.value,
            "productType": self.product_type_field.value,
            "quantity": quantity_with_unit,
            "supplier": self.supplier_field.value,
            "date": date_value,
            "unit": unit,  # Guardar unidad por separado también
        }

        # 2. Guardamos en la base de datos
        self.db.add_product(qr_data["productType"])
        self.db.add_supplier(qr_data["supplier"])
        insert_result = self.db.add_history_record(qr_data)
        nuevo_lote_id = insert_result.inserted_id

        # 3. Creamos la URL en vivo
        qr_url = f"{self.base_url}/lote/{nuevo_lote_id}"

        # 4. Creamos el texto de lectura offline + URL
        qr_payload_string = f"""--- LoteTracker ---
Producto: {qr_data['productType']}
Cantidad: {quantity_with_unit}
Proveedor: {qr_data['supplier']}
Fecha: {qr_data['date']}
Operador: {qr_data['operatorName']}
Código Op: {qr_data['operatorCode']}

-------------------
Ver Dashboard en Vivo:
{qr_url}
"""

        # 5. Generamos el QR usando el nuevo texto
        img_base64 = generate_qr_image(qr_payload_string)

        # 6. El resto de la lógica es la misma
        self.qr_image.src_base64 = img_base64
        self.current_qr_base64 = img_base64
        self.current_qr_data = qr_data

        self.update_qr_display(qr_data)
        self.update_history_table()

        self.qr_info_container.visible = True
        self.history_container.visible = True

        self.generate_button.text = "Generar nuevo código QR"
        self.new_code_button.visible = True

        self.show_snackbar("✅ Código QR Híbrido (Offline/Online) generado")
        self.page.update()

    def update_qr_display(self, data):
        self.operator_name_display.value = data["operatorName"]
        self.operator_code_display.value = data["operatorCode"]
        self.product_display.value = data["productType"]
        self.quantity_display.value = data["quantity"]
        self.supplier_display.value = data["supplier"]
        self.date_display.value = data["date"]

    def update_history_table(self):
        history = self.db.get_history()
        self.history_table.rows.clear()
        for record in history:
            # Manejar cantidad con o sin unidad
            quantity_display = record.get("quantity", "")
            
            self.history_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(record.get("operatorName", ""))),
                    ft.DataCell(ft.Text(record.get("productType", ""))),
                    ft.DataCell(ft.Text(quantity_display)),
                    ft.DataCell(ft.Text(record.get("supplier", ""))),
                    ft.DataCell(ft.Text(record.get("date", ""))),
                ])
            )

    def on_new_code(self, e):
        self.operator_name_field.value = ""
        self.operator_code_field.value = ""
        self.product_type_field.value = ""
        self.quantity_field.value = ""
        self.unit_field.value = "kg"
        self.supplier_field.value = ""
        
        # Resetear date_picker a fecha actual
        self.date_picker.use_current_time_checkbox.value = True
        
        now = datetime.now()
        self.date_picker.day_field.value = str(now.day)
        self.date_picker.month_field.value = str(now.month)
        self.date_picker.year_field.value = str(now.year)
        
        h_12 = now.hour % 12
        if h_12 == 0: h_12 = 12
        self.date_picker.hour_field.value = str(h_12)
        
        self.date_picker.minute_field.value = str(now.minute).zfill(2)
        self.date_picker.am_pm_dropdown.value = "AM" if now.hour < 12 else "PM"
        
        # Deshabilitar campos
        self.date_picker.day_field.disabled = True
        self.date_picker.month_field.disabled = True
        self.date_picker.year_field.disabled = True
        self.date_picker.hour_field.disabled = True
        self.date_picker.minute_field.disabled = True
        self.date_picker.am_pm_dropdown.disabled = True
        
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


# --- Esta función NO CAMBIA ---
def create_generator_view(page: ft.Page, db: DatabaseManager):
    """Crea y retorna la ft.View para la página principal del generador"""

    generator_logic = GeneratorPage(page, db)
    generator_logic.update_history_table()
    if len(db.get_history()) > 0:
        generator_logic.history_container.visible = True

    if not generator_logic.base_url:
        warning_text = ft.Container(
            content=ft.Text(
                "⚠️ ADVERTENCIA: 'BASE_URL' no está configurada en tu archivo .env. Los QR generados no funcionarán en otros dispositivos.",
                color=ft.colors.ORANGE_800,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
                size=14
            ),
            bgcolor=ft.colors.ORANGE_100,
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.colors.ORANGE_300)
        )
        generator_logic.form_card.content.content.controls.insert(0, warning_text)

    # El contenedor usa tu gradiente radial
    main_content = ft.Container(
        padding=ft.padding.symmetric(vertical=32, horizontal=16),
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1,
            colors=[
                "#E6F4EA",
                "#F9FCFA",
                "#F3F3F3"
            ],
            stops=[0.0, 0.6, 1.0]
        ),
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=32,
            controls=[
                generator_logic.form_card,
                generator_logic.qr_info_container,
                generator_logic.history_container,
            ],
        ),
    )

    return ft.View(
        route="/",
        padding=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    generator_logic.header,
                    main_content,
                    generator_logic.footer,
                ]
            )
        ]
    )