# main.py
import flet as ft
from src.app import LoteTrackerApp

def main(page: ft.Page):
    """Función principal que se pasa a ft.app()"""
    page.title = "LoteTracker - Sistema de Trazabilidad"
    page.padding = 0
    page.bgcolor = "#ffffff"
    page.scroll = ft.ScrollMode.AUTO

    # Crea una instancia de tu aplicación
    app = LoteTrackerApp(page)
    
    # Construye la interfaz de usuario
    app.build_layout()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)