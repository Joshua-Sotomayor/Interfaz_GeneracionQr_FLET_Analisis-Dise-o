import flet as ft

def create_autocomplete_dropdown(label, hint_text, options, on_change=None):
    """
    Crea un TextField con autocompletado tipo combo box que:
    - Muestra todas las opciones al hacer clic
    - Filtra mientras escribes
    - Permite agregar nuevos valores
    
    Args:
        label: Etiqueta del campo
        hint_text: Texto de ayuda
        options: Lista de opciones para sugerir
        on_change: Función callback cuando cambia el valor
    
    Returns:
        TextField con funcionalidad de combo box
    """
    
    # TextField principal que permite entrada libre
    text_field = ft.TextField(
        label=label,
        hint_text=hint_text,
        bgcolor="#f3f3f5",
        border_color="#e0e0e0",
        focused_border_color="#38A169",
        border_radius=8,
        text_size=16,
    )
    
    # Contenedor de sugerencias (inicialmente oculto)
    suggestions_column = ft.Column(
        spacing=0,
        controls=[],
        scroll=ft.ScrollMode.AUTO,
    )
    
    suggestions_container = ft.Container(
        visible=False,
        bgcolor="#ffffff",
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=8,
        padding=0,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color="#00000026",
            offset=ft.Offset(0, 2),
        ),
        content=suggestions_column,
        height=0,
    )
    
    def show_all_options():
        """Muestra todas las opciones disponibles"""
        if not options or len(options) == 0:
            return
        
        suggestions_column.controls.clear()
        
        # Mostrar todas las opciones (máximo 8 para no hacer el dropdown muy largo)
        for option in options[:8]:
            def make_click_handler(text):
                def handler(e):
                    text_field.value = text
                    suggestions_container.visible = False
                    suggestions_container.height = 0
                    if on_change:
                        class FakeEvent:
                            pass
                        fake_e = FakeEvent()
                        on_change(fake_e)
                    text_field.update()
                    suggestions_container.update()
                return handler
            
            suggestion_item = ft.Container(
                content=ft.Text(
                    option, 
                    size=14, 
                    color="#2D3748",
                    weight=ft.FontWeight.W_400
                ),
                bgcolor="#ffffff",
                padding=12,
                border=ft.border.only(bottom=ft.BorderSide(1, "#f0f0f0")),
                on_click=make_click_handler(option),
                ink=True,
                on_hover=lambda e, item=option: (
                    setattr(e.control, 'bgcolor', '#f7fafc' if e.data == "true" else '#ffffff'),
                    e.control.update()
                )
            )
            
            suggestions_column.controls.append(suggestion_item)
        
        # Calcular altura basada en número de opciones
        num_options = min(len(options), 8)
        suggestions_container.height = num_options * 45
        suggestions_container.visible = True
        
        try:
            suggestions_container.update()
        except:
            pass
    
    def filter_and_show_suggestions(e):
        """Filtra y muestra sugerencias basadas en el texto ingresado"""
        query = text_field.value.lower() if text_field.value else ""
        
        # Llamar al callback original si existe
        if on_change:
            on_change(e)
        
        if not query or len(query) < 1:
            # Si está vacío, mostrar todas las opciones
            show_all_options()
        else:
            # Filtrar opciones que coincidan
            filtered = [opt for opt in options if query in opt.lower()]
            
            if filtered and len(filtered) > 0:
                suggestions_column.controls.clear()
                
                # Limitar a 8 sugerencias
                for suggestion in filtered[:8]:
                    def make_click_handler(text):
                        def handler(e):
                            text_field.value = text
                            suggestions_container.visible = False
                            suggestions_container.height = 0
                            if on_change:
                                class FakeEvent:
                                    pass
                                fake_e = FakeEvent()
                                on_change(fake_e)
                            text_field.update()
                            suggestions_container.update()
                        return handler
                    
                    suggestion_item = ft.Container(
                        content=ft.Text(
                            suggestion, 
                            size=14, 
                            color="#2D3748",
                            weight=ft.FontWeight.W_400
                        ),
                        bgcolor="#ffffff",
                        padding=12,
                        border=ft.border.only(bottom=ft.BorderSide(1, "#f0f0f0")),
                        on_click=make_click_handler(suggestion),
                        ink=True,
                        on_hover=lambda e, item=suggestion: (
                            setattr(e.control, 'bgcolor', '#f7fafc' if e.data == "true" else '#ffffff'),
                            e.control.update()
                        )
                    )
                    
                    suggestions_column.controls.append(suggestion_item)
                
                # Calcular altura basada en número de sugerencias
                num_suggestions = min(len(filtered), 8)
                suggestions_container.height = num_suggestions * 45
                suggestions_container.visible = True
            else:
                # No hay coincidencias, ocultar dropdown
                suggestions_container.visible = False
                suggestions_container.height = 0
        
        try:
            suggestions_container.update()
        except:
            pass
    
    def on_focus(e):
        """Cuando el campo recibe foco, mostrar todas las opciones"""
        show_all_options()
    
    def on_blur(e):
        """Cuando el campo pierde foco, ocultar dropdown después de un delay"""
        # Usar un delay para permitir que el clic en la sugerencia se registre antes de ocultar
        import time
        import threading
        
        def hide_delayed():
            time.sleep(0.2)
            suggestions_container.visible = False
            suggestions_container.height = 0
            try:
                suggestions_container.update()
            except:
                pass
        
        threading.Thread(target=hide_delayed).start()
    
    text_field.on_change = filter_and_show_suggestions
    text_field.on_focus = on_focus
    text_field.on_blur = on_blur
    
    # Agregar atributos personalizados al TextField para compatibilidad
    text_field.suggestions_container = suggestions_container
    text_field.suggestions_column = suggestions_column
    
    return text_field
