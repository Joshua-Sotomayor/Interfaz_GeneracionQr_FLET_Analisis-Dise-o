import qrcode
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def generate_qr_image(url_data):
    """Genera imagen QR estética con badge central mostrando información esencial"""
    
    # ============================
    # COLORES PREMIUM
    # ============================
    COLOR_FONDO = (240, 245, 230)       # Verde pálido premium
    COLOR_MODULO = (22, 100, 32)        # Verde oscuro elegante
    COLOR_TEXTO = (0, 0, 0)             # Negro
    COLOR_ACCENT = (56, 161, 105)       # Verde AgroAmigos
    
    # ============================
    # 1. Extraer datos esenciales del payload
    # ============================
    # Parseamos el texto para extraer la información clave
    lines = url_data.split('\n')
    producto = ""
    cantidad = ""
    proveedor = ""
    operador = ""
    fecha = ""
    
    for line in lines:
        if "Producto:" in line:
            producto = line.split("Producto:")[1].strip()
        elif "Cantidad:" in line:
            cantidad = line.split("Cantidad:")[1].strip()
        elif "Proveedor:" in line:
            proveedor = line.split("Proveedor:")[1].strip()
        elif "Operador:" in line:
            operador = line.split("Operador:")[1].strip()
        elif "Fecha:" in line:
            fecha = line.split("Fecha:")[1].strip()
    
    # ============================
    # 2. Generar QR base con alta corrección de errores
    # ============================
    qr = qrcode.QRCode(
        version=5,                                      # versión equilibrada
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alta corrección para el badge
        box_size=30,                                    # módulos GRANDES
        border=4
    )
    qr.add_data(url_data)
    qr.make(fit=True)
    
    # Render del QR con colores premium
    base = qr.make_image(
        fill_color=COLOR_MODULO,
        back_color=COLOR_FONDO
    ).convert("RGB")
    
    width, height = base.size
    
    # ============================
    # 3. Crear Badge Central OPACO
    # ============================
    badge_ratio = 0.32
    badge_size = int(width * badge_ratio)
    
    badge = Image.new("RGBA", (badge_size, badge_size), (255, 255, 255, 255))   # FONDO SÓLIDO
    draw = ImageDraw.Draw(badge)
    
    # Marco suave redondeado
    draw.rounded_rectangle(
        (0, 0, badge_size, badge_size),
        radius=35,
        outline=COLOR_MODULO,
        width=6,
        fill=(255, 255, 255, 255)  # Totalmente opaco para que el QR no se vea detrás
    )
    
    # ============================
    # 4. Tipografías limpias
    # ============================
    try:
        font_title = ImageFont.truetype("arialbd.ttf", int(badge_size * 0.13))
        font_body  = ImageFont.truetype("arial.ttf", int(badge_size * 0.11))
        font_small = ImageFont.truetype("arial.ttf", int(badge_size * 0.08))
    except:
        # Fallback a fuente por defecto
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # ============================
    # 5. Función para centrar texto
    # ============================
    def centrar(texto, y, font, color):
        # Truncar texto si es muy largo
        max_chars = 18
        if len(texto) > max_chars:
            texto = texto[:max_chars-2] + ".."
        
        bbox = draw.textbbox((0, 0), texto, font=font)
        w = bbox[2] - bbox[0]
        x = (badge_size - w) // 2
        draw.text((x, y), texto, fill=color, font=font)
    
    # ============================
    # 6. Escribir Textos Centrados
    # ============================
    Y = badge_size * 0.06
    SALTO = badge_size * 0.16
    
    centrar("AgroAmigos", Y, font_title, COLOR_ACCENT)
    
    # Información esencial
    if producto:
        centrar(producto, Y + SALTO, font_body, COLOR_TEXTO)
    
    if cantidad:
        centrar(f"Cant: {cantidad}", Y + SALTO * 2, font_small, COLOR_TEXTO)
    
    if proveedor:
        centrar(proveedor, Y + SALTO * 2.8, font_small, COLOR_TEXTO)
    
    if fecha:
        centrar(fecha, Y + SALTO * 3.6, font_small, COLOR_TEXTO)
    
    if operador:
        centrar(operador, Y + SALTO * 4.4, font_small, COLOR_ACCENT)
    
    # ============================
    # 7. Colocar Badge centrado en el QR
    # ============================
    pos_x = (width - badge_size) // 2
    pos_y = (height - badge_size) // 2
    
    base.paste(badge, (pos_x, pos_y), badge)
    
    # ============================
    # 8. Convertir a base64
    # ============================
    buffered = BytesIO()
    base.save(buffered, format="PNG", quality=95)
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64