import flet as ft
from src.database_manager import DatabaseManager
from src.app import create_generator_view
from src.dashboard_view import create_dashboard_view

def main(page: ft.Page):
    """Función principal que ahora actúa como ENRUTADOR"""
    page.title = "LoteTracker - Sistema de Trazabilidad"
    page.padding = 0
    page.bgcolor = "#ffffff"

    # 1. Crear una única instancia del gestor de base de datos
    db = DatabaseManager()

    # 2. Comprobar la conexión a la DB
    if db.db is None:
        page.add(ft.Column(
            [
                ft.Text("❌ Error de Conexión a la Base de Datos", size=20, color="red"),
                ft.Text("Por favor, revisa tu archivo .env y asegúrate de que MongoDB esté corriendo."),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        ))
        return

    # 3. Definir el manejador de rutas
    def route_change(route):
        page.views.clear() # Limpia las vistas anteriores
        
        # Ruta principal (Generador QR)
        if page.route == "/":
            view = create_generator_view(page, db)
            page.views.append(view)
        
        # Ruta del Dashboard General
        elif page.route == "/dashboard":
            view = create_dashboard_view(page, db) # Sin lote_id
            page.views.append(view)
        
        # Ruta del Lote Específico (ej. /lote/60f...)
        elif page.route.startswith("/lote/"):
            # Extraemos el ID de la URL
            lote_id = page.route.split("/")[-1] 
            view = create_dashboard_view(page, db, lote_id=lote_id)
            page.views.append(view)
            
        page.update()

    # 4. Definir cómo manejar el botón "Atrás" del navegador
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route) # Navega a la vista anterior

    # 5. Configurar la página
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # 6. Ir a la ruta inicial (puede ser la raíz o una específica)
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)