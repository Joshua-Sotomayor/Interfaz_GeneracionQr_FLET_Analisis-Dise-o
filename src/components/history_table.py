# src/components/history_table.py
import flet as ft

def create_history_table_card(history_table):
    """Crea y retorna la Card del historial con la tabla dada"""
    return ft.Container(
        # La visibilidad se controlará desde app.py
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