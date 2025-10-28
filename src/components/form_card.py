# src/components/form_card.py
import flet as ft

def create_form_card(
    operator_name_field,
    operator_code_field,
    product_type_field,
    quantity_field,
    supplier_field,
    date_field,
    date_helper_text,
    generate_button,
    new_code_button
):
    """Crea y retorna la Card del formulario con los controles dados"""
    return ft.Card(
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