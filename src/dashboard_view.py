import flet as ft
from src.database_manager import DatabaseManager

def create_dashboard_view(page: ft.Page, db: DatabaseManager, lote_id=None):
    """
    Crea la vista del Dashboard.
    """
    
    # --- 1. Definir Controles de la UI ---
    
    lote_card = ft.Card(
        visible=False, elevation=4,
        content=ft.Container(
            padding=24, border_radius=16, width=600,
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Text("Detalle del Lote", size=20, weight=ft.FontWeight.W_500, color="#22543D"),
                    ft.Divider(),
                    ft.Row([ft.Text("Producto:", weight=ft.FontWeight.BOLD), ft.Text(key="producto")]),
                    ft.Row([ft.Text("Estado:", weight=ft.FontWeight.BOLD), ft.Text(key="estado")]),
                    ft.Row([ft.Text("Cantidad Inicial:", weight=ft.FontWeight.BOLD), ft.Text(key="cant_inicial")]),
                    ft.Row([ft.Text("Cantidad Restante:", weight=ft.FontWeight.BOLD), ft.Text(key="cant_restante")]),
                    ft.Row([ft.Text("Proveedor:", weight=ft.FontWeight.BOLD), ft.Text(key="proveedor")]),
                    ft.Row([ft.Text("Operador:", weight=ft.FontWeight.BOLD), ft.Text(key="operador")]),
                    ft.Row([ft.Text("Fecha:", weight=ft.FontWeight.BOLD), ft.Text(key="fecha")]),
                ]
            )
        )
    )

    stats_card = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=24, border_radius=16, width=600,
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Text("Estadísticas Generales", size=20, weight=ft.FontWeight.W_500, color="#22543D"),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("Total de Lotes Registrados:", weight=ft.FontWeight.BOLD),
                        ft.Text(key="total_lotes")
                    ]),
                    ft.Text("Stock Total por Producto:", weight=ft.FontWeight.BOLD),
                    ft.BarChart(
                        bar_groups=[], key="stock_chart",
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=8, padding=16, expand=True
                    )
                ]
            )
        )
    )
    
    error_text = ft.Text(
        "❌ Error: Lote no encontrado. Es posible que el ID no exista o sea incorrecto.",
        size=16, color=ft.colors.RED_700, weight=ft.FontWeight.BOLD,
        visible=False
    )

    # --- 2. Lógica de Carga de Datos ---
    
    def load_lote_data(lote_id):
        lote_data = db.get_lote_by_id(lote_id)
        if lote_data:
            (lote_card.content.content.controls[2].controls[1]).value = lote_data.get("productType", "N/A")
            (lote_card.content.content.controls[3].controls[1]).value = lote_data.get("estado", "N/A")
            (lote_card.content.content.controls[4].controls[1]).value = str(lote_data.get("cantidad_inicial", "0"))
            (lote_card.content.content.controls[5].controls[1]).value = str(lote_data.get("cantidad_restante", "0"))
            (lote_card.content.content.controls[6].controls[1]).value = lote_data.get("supplier", "N/A")
            (lote_card.content.content.controls[7].controls[1]).value = lote_data.get("operatorName", "N/A")
            (lote_card.content.content.controls[8].controls[1]).value = lote_data.get("date", "N/A")
            lote_card.visible = True
        else:
            error_text.visible = True
            lote_card.visible = False

    def load_stats_data():
        stats = db.get_dashboard_stats()
        (stats_card.content.content.controls[2].controls[1]).value = str(stats.get("total_lotes", 0))
        
        chart: ft.BarChart = stats_card.content.content.controls[4]
        chart.bar_groups.clear()
        
        colores = [ft.colors.GREEN_500, ft.colors.BLUE_500, ft.colors.AMBER_500, ft.colors.RED_500]
        
        for i, item in enumerate(stats.get("stock_por_producto", [])):
            chart.bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=item["cantidad_total"],
                            width=30,
                            color=colores[i % len(colores)],
                            tooltip=f"{item['_id']}: {item['cantidad_total']}"
                        )
                    ]
                )
            )

    # --- 3. Carga Inicial de Datos ---
    if lote_id:
        load_lote_data(lote_id)
    load_stats_data()

    # --- 4. Construir y Retornar la Vista ---
    if lote_id:
        header_text = f"Detalle del Lote: {lote_id}"
    else:
        header_text = "Dashboard General"

    # Contenedor principal de la vista
    main_content = ft.Container(
        padding=ft.padding.symmetric(vertical=32, horizontal=16),
        
        # 👇 ¡AQUÍ ESTÁ TU GRADIENTE!
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1,
            colors=[
                "#E6F4EA",  # Verde muy claro
                "#F9FCFA",  # Casi blanco (zona intermedia)
                "#F3F3F3"   # Blanco total en el borde
            ],
            stops=[0.0, 0.6, 1.0]
        ),
        
        expand=True, # Se expande para llenar el espacio
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER, # Centra tarjetas
            spacing=32,
            controls=[
                ft.Text(header_text, size=16, italic=True),
                error_text,
                lote_card,    
                stats_card    
            ],
        ),
    )

    return ft.View(
        route=f"/lote/{lote_id}" if lote_id else "/dashboard",
        appbar=ft.AppBar(title=ft.Text("Dashboard de Trazabilidad"), bgcolor="#C6F6D5"),
        padding=0,
        scroll=ft.ScrollMode.AUTO, # El scroll va en la Vista
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Esta vista no tiene el header/footer principal,
                    # solo el contenido principal
                    main_content,
                ]
            )
        ]
    )