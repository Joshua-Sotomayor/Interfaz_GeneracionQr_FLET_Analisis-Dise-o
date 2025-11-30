import flet as ft

def create_unit_selector(on_change=None):
    """
    Crea un dropdown para seleccionar unidades de medida
    
    Args:
        on_change: Función callback cuando cambia la unidad
    
    Returns:
        ft.Dropdown con unidades de medida
    """
    
    units = ["kg", "libras", "litros", "unidades", "toneladas", "cajas", "sacos"]
    
    dropdown = ft.Dropdown(
        label="Unidad",
        value="kg",  # Valor por defecto
        options=[ft.dropdown.Option(unit) for unit in units],
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
        width=150,
        on_change=on_change,
    )
    
    return dropdown
