# src/components/footer.py
import flet as ft

def create_footer():
    """Crea y retorna el control del Footer"""
    return ft.Container(
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