import flet as ft
from datetime import datetime

def create_date_time_picker(on_change=None):
    """
    Crea un selector de fecha y hora intuitivo con campos separados
    y opción para usar fecha/hora actual automáticamente.
    
    Args:
        on_change: Función callback cuando cambia la fecha/hora
    
    Returns:
        Container con todos los campos de fecha/hora
    """
    
    # Obtener fecha/hora actual
    now = datetime.now()
    
    # Campos individuales
    day_field = ft.TextField(
        label="Día",
        value=str(now.day),
        width=70,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        disabled=True  # Inicialmente deshabilitado
    )
    
    month_field = ft.TextField(
        label="Mes",
        value=str(now.month),
        width=70,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        disabled=True
    )
    
    year_field = ft.TextField(
        label="Año",
        value=str(now.year),
        width=90,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=4,
        disabled=True
    )
    
    # Convertir hora de 24h a 12h
    hour_12 = now.hour % 12
    if hour_12 == 0:
        hour_12 = 12
    
    hour_field = ft.TextField(
        label="Hora",
        value=str(hour_12),
        width=70,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        disabled=True
    )
    
    minute_field = ft.TextField(
        label="Min",
        value=str(now.minute).zfill(2),
        width=70,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=2,
        disabled=True
    )
    
    am_pm_dropdown = ft.Dropdown(
        label="AM/PM",
        value="AM" if now.hour < 12 else "PM",
        options=[
            ft.dropdown.Option("AM"),
            ft.dropdown.Option("PM"),
        ],
        width=100,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        disabled=True
    )

    def on_checkbox_change(e):
        """Habilita o deshabilita los campos según el checkbox"""
        is_checked = e.control.value
        
        # Si se marca, actualizar a la hora actual
        if is_checked:
            current_now = datetime.now()
            day_field.value = str(current_now.day)
            month_field.value = str(current_now.month)
            year_field.value = str(current_now.year)
            
            h_12 = current_now.hour % 12
            if h_12 == 0: h_12 = 12
            hour_field.value = str(h_12)
            
            minute_field.value = str(current_now.minute).zfill(2)
            am_pm_dropdown.value = "AM" if current_now.hour < 12 else "PM"
        
        # Actualizar estado de los campos
        day_field.disabled = is_checked
        month_field.disabled = is_checked
        year_field.disabled = is_checked
        hour_field.disabled = is_checked
        minute_field.disabled = is_checked
        am_pm_dropdown.disabled = is_checked
        
        # Actualizar UI
        day_field.update()
        month_field.update()
        year_field.update()
        hour_field.update()
        minute_field.update()
        am_pm_dropdown.update()
        
        if on_change:
            on_change(e)

    use_current_time_checkbox = ft.Checkbox(
        label="Usar fecha y hora actual",
        value=True,
        on_change=on_checkbox_change,
        fill_color="#38A169"
    )
    
    def get_datetime_string():
        """Convierte los valores de los campos a string de fecha/hora"""
        # Si está marcado "Usar actual", devolver datetime.now() fresco
        if use_current_time_checkbox.value:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        try:
            day = int(day_field.value or 1)
            month = int(month_field.value or 1)
            year = int(year_field.value or now.year)
            hour_12_val = int(hour_field.value or 12)
            minute = int(minute_field.value or 0)
            am_pm = am_pm_dropdown.value
            
            # Convertir a formato 24 horas
            hour_24 = hour_12_val
            if am_pm == "PM" and hour_12_val != 12:
                hour_24 = hour_12_val + 12
            elif am_pm == "AM" and hour_12_val == 12:
                hour_24 = 0
            
            # Validar y crear fecha
            dt = datetime(year, month, day, hour_24, minute, 0)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Si hay error, retornar fecha/hora actual
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Container principal
    container = ft.Container(
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Fecha de producción", size=14, weight=ft.FontWeight.BOLD, color="#22543D"),
                        use_current_time_checkbox
                    ]
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        day_field,
                        ft.Text("/", size=20, color="#717182"),
                        month_field,
                        ft.Text("/", size=20, color="#717182"),
                        year_field,
                    ]
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        hour_field,
                        ft.Text(":", size=20, color="#717182"),
                        minute_field,
                        am_pm_dropdown,
                    ]
                ),
            ]
        ),
        padding=10,
        bgcolor="#ffffff",
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=8,
    )
    
    # Exponer método para obtener el valor y campos
    container.get_value = get_datetime_string
    container.day_field = day_field
    container.month_field = month_field
    container.year_field = year_field
    container.hour_field = hour_field
    container.minute_field = minute_field
    container.am_pm_dropdown = am_pm_dropdown
    container.use_current_time_checkbox = use_current_time_checkbox
    
    return container
