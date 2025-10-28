# src/components/qr_display.py
import flet as ft

def create_qr_display_card(
    qr_image,
    operator_name_display,
    operator_code_display,
    product_display,
    quantity_display,
    supplier_display,
    date_display,
    download_button_click_handler
):
    """Crea y retorna la Card de display del QR con los controles dados"""
    
    def _build_info_row(label, text_control):
        """Helper anidado para crear filas de información"""
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, color="#717182"),
                text_control,
            ],
        )

    return ft.Container(
        # La visibilidad se controlará desde app.py cambiando la propiedad 'visible'
        visible=False, 
        alignment=ft.alignment.center,
        width=700,
        bgcolor="transparent",
        content=ft.Card(
            elevation=4,
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
                            bgcolor="#E6F7ED",
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    _build_info_row("Operador:", operator_name_display),
                                    _build_info_row("Código operador:", operator_code_display),
                                    _build_info_row("Producto:", product_display),
                                    _build_info_row("Cantidad:", quantity_display),
                                    _build_info_row("Proveedor:", supplier_display),
                                    _build_info_row("Fecha:", date_display),
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
                            on_click=download_button_click_handler,
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