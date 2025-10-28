# src/components/header.py
import flet as ft

def create_header():
    """Crea y retorna el control del Header"""
    return ft.Container(
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