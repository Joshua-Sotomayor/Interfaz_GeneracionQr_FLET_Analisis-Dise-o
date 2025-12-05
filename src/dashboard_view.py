import flet as ft
from src.database_manager import DatabaseManager

def create_dashboard_view(page: ft.Page, db: DatabaseManager, lote_id=None):
    """
    Crea la vista del Dashboard corregida y compatible con Flet.
    """

    # Colores (hex para evitar problemas con constantes no disponibles)
    COLOR_PRIMARY = "#22543D"
    COLOR_CARD_BG = "#FFFFFF"
    COLOR_BORDER = "#E6EDF0"
    COLOR_BAR_COLORS = ["#48BB78", "#4299E1", "#F6AD55", "#F56565"]
    COLOR_ERROR = "#D53F3F"

    # --- Controles de texto (referencias) ---
    product_txt = ft.Text("N/A", size=14)
    estado_txt = ft.Text("N/A", size=14)
    cant_inicial_txt = ft.Text("0", size=14)
    medida_txt = ft.Text("Unidades", size=14)
    cant_restante_txt = ft.Text("0", size=14)
    proveedor_txt = ft.Text("N/A", size=14)
    operador_txt = ft.Text("N/A", size=14)
    fecha_txt = ft.Text("N/A", size=14)

    total_lotes_txt = ft.Text("0", size=14)

    # Un contenedor donde pondremos las barras (se actualizará más abajo)
    bars_row = ft.Row(spacing=12, alignment=ft.MainAxisAlignment.CENTER)

    # Error text
    error_text = ft.Text(
        "❌ Error: Lote no encontrado. Es posible que el ID no exista o sea incorrecto.",
        size=14,
        color=COLOR_ERROR,
        weight=ft.FontWeight.BOLD,
        visible=False
    )

    # --- Lote card (usa referencias en vez de keys/index) ---
    lote_card = ft.Card(
        visible=False,
        elevation=4,
        content=ft.Container(
            padding=24,
            border_radius=16,
            width=600,
            bgcolor=COLOR_CARD_BG,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Detalle del Lote", size=20, weight=ft.FontWeight.W_500, color=COLOR_PRIMARY),
                    ft.Divider(),
                    ft.Row([ft.Text("Producto:", weight=ft.FontWeight.BOLD), product_txt]),
                    ft.Row([ft.Text("Estado:", weight=ft.FontWeight.BOLD), estado_txt]),
                    ft.Row([ft.Text("Cantidad Inicial:", weight=ft.FontWeight.BOLD), cant_inicial_txt]),
                    ft.Row([ft.Text("Medida:", weight=ft.FontWeight.BOLD), medida_txt]),
                    ft.Row([ft.Text("Cantidad Restante:", weight=ft.FontWeight.BOLD), cant_restante_txt]),
                    ft.Row([ft.Text("Proveedor:", weight=ft.FontWeight.BOLD), proveedor_txt]),
                    ft.Row([ft.Text("Operador:", weight=ft.FontWeight.BOLD), operador_txt]),
                    ft.Row([ft.Text("Fecha:", weight=ft.FontWeight.BOLD), fecha_txt]),
                ]
            )
        )
    )

    # --- Stats card (total + gráfico simple) ---
    stats_card = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=24,
            border_radius=16,
            width=600,
            bgcolor=COLOR_CARD_BG,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("Estadísticas Generales", size=20, weight=ft.FontWeight.W_500, color=COLOR_PRIMARY),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("Total de Lotes Registrados:", weight=ft.FontWeight.BOLD),
                        total_lotes_txt
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text("Stock Total por Producto:", weight=ft.FontWeight.BOLD),
                    ft.Container(  # contenedor del "chart"
                        padding=12,
                        border_radius=8,
                        bgcolor="#FAFAFA",
                        content=ft.Column(
                            controls=[
                                bars_row
                            ]
                        ),
                    ),
                ]
            )
        )
    )

    # --- Funciones para cargar datos ---
    def load_lote_data(lote_id_param):
        lote_data = db.get_lote_by_id(lote_id_param)
        if lote_data:
            product_txt.value = lote_data.get("productType", "N/A")
            estado_txt.value = lote_data.get("estado", "N/A")
            cant_inicial_txt.value = str(lote_data.get("cantidad_inicial", "0"))
            cant_restante_txt.value = str(lote_data.get("cantidad_restante", "0"))
            proveedor_txt.value = lote_data.get("supplier", "N/A")
            operador_txt.value = lote_data.get("operatorName", "N/A")
            fecha_txt.value = lote_data.get("date", "N/A")
            lote_card.visible = True
            error_text.visible = False
        else:
            lote_card.visible = False
            error_text.visible = True
        # actualizar UI
        page.update()

    def load_stats_data():
        stats = db.get_dashboard_stats()
        total_lotes = stats.get("total_lotes", 0)
        total_lotes_txt.value = str(total_lotes)

        stock_list = stats.get("stock_por_producto", [])
        # calcular máximo para escala
        max_qty = max([item.get("cantidad_total", 0) for item in stock_list], default=1)

        # reconstruir barras
        bars_row.controls.clear()
        for i, item in enumerate(stock_list):
            qty = item.get("cantidad_total", 0)
            # escala de altura entre 30 y 140 px
            height = 30 if max_qty == 0 else int(30 + (qty / max_qty) * 110)
            color = COLOR_BAR_COLORS[i % len(COLOR_BAR_COLORS)]
            label = str(item.get("_id", "producto"))
            bar = ft.Column(
                [
                    ft.Container(width=36, height=height, bgcolor=color, border_radius=6),
                    ft.Text(label, size=12, text_align=ft.TextAlign.CENTER),
                    ft.Text(str(qty), size=11, color="#4A5568", text_align=ft.TextAlign.CENTER)
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            bars_row.controls.append(bar)

        page.update()

    # --- Carga inicial ---
    if lote_id:
        load_lote_data(lote_id)
    load_stats_data()

    # --- Construir content principal ---
    header_text = f"Detalle del Lote: {lote_id}" if lote_id else "Dashboard General"

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
            spacing=24,
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
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    main_content,
                ]
            )
        ]
    )
